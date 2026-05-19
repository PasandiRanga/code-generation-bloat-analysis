import os, csv, subprocess, tracemalloc, timeit, statistics
import importlib.util, re, inspect, io
from unittest.mock import patch
from contextlib import redirect_stdout

# TOKEN COUNT
try:
    import tiktoken
    _TOKENIZER = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text):
        return len(_TOKENIZER.encode(text))

except ImportError:
    print("WARNING: tiktoken not found — using word-count approximation")

    def count_tokens(text):
        return len(text.split())


# CONFIG

# reference function names
FUNC_MAP = {
    "S1": "final_score",
    "S2": "is_valid_manifest",
    "S3": "calculate_credit",
    "S4": "pr_priority"
}

# main test input per scenario (used for memory/time measurement)
TEST_ARGS = {
    "S1": (3, 5),
    "S2": ("ALPHAX:500:Mars",),
    "S3": (100.0, 10),
    "S4": (3, 4, False)
}

# edge case inputs per scenario (used for crash-rate measurement)
EDGE_CASES = {
    "S1": [(0, 0), (3, 5), (1000, 0), (-1, 5)],
    "S2": [("ALPHAX:500:Mars",), ("",), ("ABC:500 Mars",)],
    "S3": [(0, 10), (100, 0), (100, 1000)],
    "S4": [(0, 0, False), (100, 0, True), (3, 4, True)]
}

REFERENCE_LLOC = {
    "S1": 4,
    "S2": 3,
    "S3": 2,
    "S4": 4
}

def compute_pbs(prompt_text, scenario):
    if prompt_text is None:
        return None, None
    tokens = count_tokens(prompt_text)
    ref = REFERENCE_LLOC[scenario]
    return tokens, round(tokens / ref, 4)

def load_prompt(path):
    p = os.path.join(os.path.dirname(path), "prompt.txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read()
    return None

def get_scenario(path):
    p = path.lower().replace("\\", "/")
    if "/s1" in p: return "S1"
    if "/s2" in p: return "S2"
    if "/s3" in p: return "S3"
    if "/s4" in p: return "S4"
    return None


def load_func(path, expected_name):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)

    with patch("builtins.input", return_value="0"):
        with redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)

    if hasattr(mod, expected_name):
        f = getattr(mod, expected_name)
        if callable(f):
            return f

    # fallback: first callable
    for name in dir(mod):
        if name.startswith("_"):
            continue

        obj = getattr(mod, name)

        if callable(obj) and not isinstance(obj, type):
            print(f"   fallback -> using {name}")
            return obj

    raise AttributeError(expected_name)


def build_call(func, args):
    n = len(inspect.signature(func).parameters)

    if n == 0:
        def call():
            it = iter(str(x) for x in args)
            with patch(
                "builtins.input",
                side_effect=lambda prompt="": next(it)
            ):
                with redirect_stdout(io.StringIO()):
                    return func()
    else:
        def call():
            with redirect_stdout(io.StringIO()):
                return func(*args)

    return call

def safe_cv(v):
    if len(v) < 2:
        return 0
    m = statistics.mean(v)
    if abs(m) < 1e-12:
        return 0
    return statistics.stdev(v) / m


def get_lloc(path):
    out = subprocess.run(
        ["radon", "raw", path],
        capture_output=True,
        text=True
    ).stdout

    m = re.search(r"LLOC:\s*(\d+)", out)
    return int(m.group(1)) if m else 0


def get_cc(path):
    out = subprocess.run(
        ["radon", "cc", "-s", path],
        capture_output=True,
        text=True
    ).stdout

    vals = re.findall(r"\((\d+)\)", out)
    return max(map(int, vals)) if vals else 1


def get_vulture(path):
    sc = get_scenario(path)
    expected_func = FUNC_MAP.get(sc) if sc else None
    
    out = subprocess.run(
        ["vulture", path],
        capture_output=True,
        text=True
    ).stdout

    issues = [x for x in out.splitlines() if ":" in x]
    if expected_func:
        issues = [x for x in issues if expected_func not in x]
    
    return len(issues)

def measure_memory(func, args, n=5):
    vals = []

    for _ in range(n):
        tracemalloc.start()

        try:
            build_call(func, args)()
        except:
            pass

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        vals.append(peak)

    return statistics.mean(vals)

def measure_time(func, args):
    call = build_call(func, args)

    def t():
        try:
            call()
        except:
            pass

    vals = timeit.repeat(t, number=1000, repeat=5)
    vals = [(x / 1000) * 1e6 for x in vals]

    return statistics.mean(vals)


# EDGE CASES
def run_edges(func, cases):
    """
    Run each edge case through the function using the correct call type.
    Returns crash rate and a pipe-separated list of exception type names.
    """
    if not cases:
        return 0, ""

    crashes = 0
    error_types = []

    for c in cases:
        args = c if isinstance(c, tuple) else (c,)
        try:
            build_call(func, args)()
        except Exception as e:
            crashes += 1
            error_types.append(type(e).__name__)

    crash_rate = round(crashes / len(cases), 4)
    return crash_rate, "|".join(error_types)

def process_file(path):
    sc = get_scenario(path)
    if sc is None:
        return None

    expected = FUNC_MAP[sc]
    args = TEST_ARGS[sc]
    edges = EDGE_CASES[sc]

    func = load_func(path, expected)

    prompt = load_prompt(path)
    tokens, pbs = compute_pbs(prompt, sc)

    edge_crash_rate, edge_error_types = run_edges(func, edges)

    return {
        "file": path,
        "scenario": sc,
        "lloc": get_lloc(path),
        "cc": get_cc(path),
        "dead_code": get_vulture(path),
        "memory": measure_memory(func, args),
        "time_us": measure_time(func, args),
        "edge_crash_rate": edge_crash_rate,
        "edge_error_types": edge_error_types,
        "prompt_tokens": tokens,
        "pbs_ratio": pbs
    }

def run_all(folder, outcsv):
    rows = []

    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                print("Processing:", path)

                try:
                    r = process_file(path)
                    if r:
                        rows.append(r)
                except Exception as e:
                    print("ERROR:", path, type(e).__name__, e)

    if not rows:
        print("WARNING: No files processed.")
        return

    with open(outcsv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print("\nDone:", outcsv)
    print("Files processed:", len(rows))

if __name__ == "__main__":
    run_all("data", "results.csv")