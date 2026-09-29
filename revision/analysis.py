"""Revised measurement and analysis pipeline (camera-ready revision, ICTer 2026 paper 175).

Changes relative to the original measure.py, each tied to a reviewer comment or audit finding:
  * Minimal guard-free references are the primary baseline; the original guarded
    references are kept as a sensitivity analysis (R4.4).
  * Functional correctness is checked against a fixed set of valid inputs (R4.3).
  * Arguments are bound by parameter role (e.g. "days" vs "amount"), not only by position.
  * Interactive zero-argument programs are flagged and excluded from runtime,
    correctness-by-value and edge-case statistics instead of being fed mocked input.
  * Edge-case totals are counted per scenario (4 cases for S1, 3 for S2-S4) (R4.2).
  * Timing uses the median of repeats; reference and generated code are timed in the same run.
  * Prompt length is compared to code length in the same unit (tokens) (R4.5).
  * Prompt/output association is reported within scenario (Spearman) to avoid the
    shared-denominator artefact of pooling PBS against LLOC ratio (R4.5).
  * GPT vs Claude comparison uses the paired design (same prompt to both models) (R4.5).

Usage (from the Research/ folder):  python revision/analysis.py
Requires: radon, vulture, tiktoken, scipy
"""
import csv, importlib.util, inspect, io, json, os, re, statistics as st, subprocess, sys, timeit, tracemalloc
from contextlib import redirect_stdout
from unittest.mock import patch

import tiktoken
from radon.complexity import cc_visit
from radon.raw import analyze
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
DATA = os.path.join(RESEARCH, "data")
SCENARIOS = ["S1", "S2", "S3", "S4"]
REF_NAME = {"S1": "final_score", "S2": "is_valid_manifest", "S3": "calculate_credit", "S4": "pr_priority"}
REF_DIRS = {"minimal": os.path.join(HERE, "reference_minimal"),
            "guarded": os.path.join(DATA, "reference")}

CL100K = tiktoken.get_encoding("cl100k_base")
O200K = tiktoken.get_encoding("o200k_base")

# Fixed input used for memory and time measurement (unchanged from the original study).
TIMING_ARGS = {"S1": (3, 5), "S2": ("ALPHAX:500:Mars",), "S3": (100.0, 10), "S4": (3, 4, False)}

# Valid inputs for functional correctness; expected values come from the minimal reference.
CORRECTNESS_ARGS = {
    "S1": [(3, 5), (5, 3), (4, 4), (0, 5), (5, 0), (2, 10), (0, 0), (10, 11)],
    "S2": [("ALPHAX:500:Mars",), ("ABCDEF:7:Earth",), ("ALPHAx:500:Mars",), ("ALPHAX:0:Mars",),
           ("ALPHAX:-5:Mars",), ("ALPHAX:500:New York",), ("ALPHAX:500",), ("ALPHAX:500:Mars:X",),
           ("ABCDEFG:5:Mars",), ("ALPHAX:12.5:Mars",), ("ALPHAX:500:",)],
    "S3": [(100.0, 0), (100.0, 7), (100.0, 8), (100.0, 10), (50.5, 30), (0.0, 20), (80.0, 9)],
    "S4": [(3, 4, False), (3, 4, True), (0, 0, True), (10, 1, False), (0, 5, True)],
}

# Edge-case inputs (unchanged from the original study): 4 for S1, 3 for S2-S4.
EDGE_ARGS = {
    "S1": [(0, 0), (3, 5), (1000, 0), (-1, 5)],
    "S2": [("ALPHAX:500:Mars",), ("",), ("ABC:500 Mars",)],
    "S3": [(0, 10), (100, 0), (100, 1000)],
    "S4": [(0, 0, False), (100, 0, True), (3, 4, True)],
}

# Parameter-role patterns used to bind arguments by meaning rather than position.
ROLES = {
    "S1": [r"zap", r"blitz"],
    "S2": [r".*"],
    "S3": [r"amount|money|balance|start|initial|credit|^m$", r"day|^d$"],
    "S4": [r"day|wait", r"comment", r"urgent"],
}

# Manual root-cause labels for incorrect or non-function outputs (from reading prompt + code).
FAILURE_CAUSE = {
    "s1/p01_claude": ("prompt", "prompt asked for an interactive multi-round game"),
    "s1/p01_gpt": ("prompt", "prompt asked for an interactive multi-round game"),
    "s1/p06_claude": ("prompt", "prompt said blitz points (not zap points) are doubled"),
    "s1/p06_gpt": ("prompt", "prompt said blitz points (not zap points) are doubled"),
    "s2/p07_claude": ("prompt", "prompt specified '/' instead of ':' as separator"),
    "s2/p07_gpt": ("prompt", "prompt specified '/' instead of ':' as separator"),
    "s3/p02_claude": ("prompt", "prompt specified linear decay of 10% of the initial amount"),
    "s3/p02_gpt": ("prompt", "prompt specified linear decay of 10% of the initial amount"),
    "s2/p05_gpt": ("model", "pattern \\S+ accepts extra colon-separated parts"),
}

# Annotation categories that the prompt explicitly requested (so they are not unprompted bloat).
REQUESTED = {"s1/p01_claude": {"feature_bloat", "ui_print_bloat", "example_call"},
             "s1/p01_gpt": {"feature_bloat", "ui_print_bloat", "example_call"}}
ANNOT_COLS = ["comment_bloat", "example_call", "docstring_bloat", "logic_bloat", "feature_bloat", "ui_print_bloat"]
CC_INVISIBLE = {"comment_bloat", "example_call", "docstring_bloat", "ui_print_bloat"}


def load_module(path):
    spec = importlib.util.spec_from_file_location("m" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    with patch("builtins.input", return_value="0"), redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def entry_function(mod, expected):
    if callable(getattr(mod, expected, None)):
        return getattr(mod, expected)
    funcs = [o for n, o in vars(mod).items()
             if inspect.isfunction(o) and o.__module__ == mod.__name__ and not n.startswith("_")]
    if not funcs:
        raise LookupError("no top-level function")
    return funcs[0]


def bind(func, scenario, args):
    """Reorder positional args so each lands on the parameter whose name matches its role."""
    params = list(inspect.signature(func).parameters)
    if len(params) != len(args) or scenario == "S2":
        return args
    order = []
    for p in params:
        hits = [i for i, pat in enumerate(ROLES[scenario]) if re.search(pat, p.lower())]
        order.append(hits[0] if len(hits) == 1 else None)
    if None in order or sorted(order) != list(range(len(args))):
        return args
    return tuple(args[i] for i in order)


def call(func, scenario, args):
    a = bind(func, scenario, args)
    with redirect_stdout(io.StringIO()):
        return func(*a)


def peak_memory(func, scenario, args, n=5):
    vals = []
    for _ in range(n):
        tracemalloc.start()
        try:
            call(func, scenario, args)
        except Exception:
            pass
        vals.append(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    return st.median(vals)


def exec_time_us(func, scenario, args, number=1000, repeat=7):
    a = bind(func, scenario, args)
    sink = io.StringIO()

    def run():
        try:
            with redirect_stdout(sink):
                func(*a)
        except Exception:
            pass
        sink.seek(0); sink.truncate()
    return st.median(timeit.repeat(run, number=number, repeat=repeat)) / number * 1e6


def static_metrics(path, code):
    lloc = analyze(code).lloc
    blocks = cc_visit(code)
    cc = max((b.complexity for b in blocks), default=1)
    return lloc, cc


def dead_code(path, entry_name):
    out = subprocess.run([sys.executable, "-m", "vulture", path], capture_output=True, text=True).stdout
    return len([l for l in out.splitlines() if ":" in l and f"'{entry_name}'" not in l])


def same(got, exp):
    if isinstance(exp, bool):
        return got is exp or (isinstance(got, bool) and got == exp)
    try:
        return abs(float(got) - float(exp)) < 0.006
    except (TypeError, ValueError):
        return False


def main():
    refs = {}
    for kind, root in REF_DIRS.items():
        for s in SCENARIOS:
            path = os.path.join(root, s.lower(), "reference.py")
            code = open(path, encoding="utf-8").read()
            func = entry_function(load_module(path), REF_NAME[s])
            lloc, cc = static_metrics(path, code)
            refs[(kind, s)] = {"func": func, "lloc": lloc, "cc": cc, "code_tokens": len(CL100K.encode(code))}

    annot = {r["file"]: r for r in csv.DictReader(open(os.path.join(RESEARCH, "annotation.csv"), encoding="utf-8"))}

    rows = []
    for s in SCENARIOS:
        sdir = os.path.join(DATA, s.lower())
        for sample in sorted(os.listdir(sdir)):
            path = os.path.join(sdir, sample, "generated.py")
            if not os.path.exists(path):
                continue
            key = f"{s.lower()}/{sample}"
            code = open(path, encoding="utf-8").read()
            prompt = open(os.path.join(sdir, sample, "prompt.txt"), encoding="utf-8").read()
            row = {"sample": key, "scenario": s, "participant": sample.split("_")[0], "model": sample.split("_")[1]}
            try:
                func = entry_function(load_module(path), REF_NAME[s])
            except LookupError:
                row["status"] = "excluded: no top-level function"
                rows.append(row)
                continue
            interactive = len(inspect.signature(func).parameters) == 0
            row["status"] = "interactive" if interactive else "function"
            row["lloc"], row["cc"] = static_metrics(path, code)
            row["dead_code"] = dead_code(path, func.__name__)
            row["code_tokens"] = len(CL100K.encode(code))
            row["prompt_tokens"] = len(CL100K.encode(prompt))
            row["prompt_tokens_o200k"] = len(O200K.encode(prompt))
            for kind in REF_DIRS:
                r = refs[(kind, s)]
                row[f"lloc_ratio_{kind}"] = row["lloc"] / r["lloc"]
                row[f"cc_ratio_{kind}"] = row["cc"] / r["cc"]
            ref = refs[("minimal", s)]
            row["pbs"] = row["prompt_tokens"] / ref["lloc"]
            row["pbs_guarded"] = row["prompt_tokens"] / refs[("guarded", s)]["lloc"]
            row["prompt_to_refcode_tokens"] = row["prompt_tokens"] / ref["code_tokens"]
            a = annot.get(key, {})
            requested = REQUESTED.get(key, set())
            for c in ANNOT_COLS:
                row[c] = int(a.get(c, 0)) if c not in requested else 0
            row["u_total_lines"] = int(a.get("u_total_lines", 0))
            if not interactive:
                results = [(args, call_safe(func, s, args), ref["func"](*args)) for args in CORRECTNESS_ARGS[s]]
                row["tests_passed"] = sum(same(g, e) for _, g, e in results)
                row["tests_total"] = len(results)
                row["correct"] = int(row["tests_passed"] == row["tests_total"])
                crashes = [type(e).__name__ for e in (edge_error(func, s, args) for args in EDGE_ARGS[s]) if e]
                row["edge_calls"] = len(EDGE_ARGS[s])
                row["edge_crashes"] = len(crashes)
                row["edge_error_types"] = "|".join(crashes)
                row["memory"] = peak_memory(func, s, TIMING_ARGS[s])
                row["time_us"] = exec_time_us(func, s, TIMING_ARGS[s])
            cause = FAILURE_CAUSE.get(key)
            row["failure_cause"] = cause[0] if cause and (interactive or not row.get("correct", 1)) else ""
            row["failure_note"] = cause[1] if row["failure_cause"] else ""
            rows.append(row)

    # Reference runtime measured in the same run as the generated code.
    for (kind, s), r in refs.items():
        r["memory"] = peak_memory(r["func"], s, TIMING_ARGS[s])
        r["time_us"] = exec_time_us(r["func"], s, TIMING_ARGS[s])
    for row in rows:
        if "time_us" in row:
            r = refs[("minimal", row["scenario"])]
            row["mem_ratio"] = row["memory"] / r["memory"]
            row["time_ratio"] = row["time_us"] / r["time_us"]

    write_csv(rows, os.path.join(HERE, "results_revised.csv"))
    summary = summarise(rows, refs)
    with open(os.path.join(HERE, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=float)
    print_summary(summary)


def call_safe(func, s, args):
    try:
        return call(func, s, args)
    except Exception as e:
        return f"EXC:{type(e).__name__}"


def edge_error(func, s, args):
    try:
        call(func, s, args)
        return None
    except Exception as e:
        return e


def write_csv(rows, path):
    cols = []
    for r in rows:
        cols += [k for k in r if k not in cols]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def describe(v):
    v = list(v)
    if not v:
        return None
    return {"n": len(v), "mean": st.mean(v), "median": st.median(v), "min": min(v), "max": max(v)}


def summarise(rows, refs):
    analysed = [r for r in rows if r["status"] != "excluded: no top-level function"]
    funcs = [r for r in analysed if r["status"] == "function"]
    out = {"counts": {
        "collected": len(rows),
        "excluded_no_function": [r["sample"] for r in rows if r["status"].startswith("excluded")],
        "analysed_static": len(analysed),
        "interactive": [r["sample"] for r in analysed if r["status"] == "interactive"],
        "analysed_runtime": len(funcs),
    }}
    out["references"] = {f"{k}_{s}": {m: v for m, v in r.items() if m != "func"} for (k, s), r in refs.items()}

    per = {}
    for s in SCENARIOS + ["ALL"]:
        a = [r for r in analysed if s == "ALL" or r["scenario"] == s]
        f = [r for r in funcs if s == "ALL" or r["scenario"] == s]
        per[s] = {
            "n_static": len(a), "n_runtime": len(f),
            "lloc_ratio": describe(r["lloc_ratio_minimal"] for r in a),
            "cc_ratio": describe(r["cc_ratio_minimal"] for r in a),
            "lloc_ratio_guarded": describe(r["lloc_ratio_guarded"] for r in a),
            "cc_ratio_guarded": describe(r["cc_ratio_guarded"] for r in a),
            "mem_ratio": describe(r["mem_ratio"] for r in f),
            "time_ratio": describe(r["time_ratio"] for r in f),
            "prompt_tokens": describe(r["prompt_tokens"] for r in a),
            "pbs": describe(r["pbs"] for r in a),
            "prompt_to_refcode_tokens": describe(r["prompt_to_refcode_tokens"] for r in a),
            "prompts_longer_than_refcode": sum(r["prompt_to_refcode_tokens"] > 1 for r in a),
            "dead_code": describe(r["dead_code"] for r in a),
        }
        if s != "ALL":
            x = [r["prompt_tokens"] for r in a]; y = [r["lloc"] for r in a]
            rho, p = stats.spearmanr(x, y)
            per[s]["spearman_tokens_vs_lloc"] = {"rho": rho, "p": p}
    out["per_scenario"] = per

    x = [r["pbs"] for r in analysed]; y = [r["lloc_ratio_minimal"] for r in analysed]
    out["pooled_pearson_pbs_vs_lloc_ratio"] = dict(zip(("r", "p"), stats.pearsonr(x, y)))
    out["pooled_spearman_raw_tokens_vs_lloc"] = dict(zip(("rho", "p"), stats.spearmanr(
        [r["prompt_tokens"] for r in analysed], [r["lloc"] for r in analysed])))

    # CC sensitivity: how much of the LLOC growth is visible to CC.
    out["cc_vs_lloc"] = {
        "files_lloc_ratio_ge_2": sum(r["lloc_ratio_minimal"] >= 2 for r in analysed),
        "of_which_cc_ratio_le_1": sum(r["lloc_ratio_minimal"] >= 2 and r["cc_ratio_minimal"] <= 1 for r in analysed),
        "files_cc_ratio_gt_lloc_ratio": sum(r["cc_ratio_minimal"] > r["lloc_ratio_minimal"] for r in analysed),
        "extra_lloc_total": sum(r["lloc"] - refs[("minimal", r["scenario"])]["lloc"] for r in analysed),
        "extra_cc_total": sum(r["cc"] - refs[("minimal", r["scenario"])]["cc"] for r in analysed),
        "files_with_only_cc_invisible_bloat": sum(
            any(r[c] for c in CC_INVISIBLE) and not any(r[c] for c in set(ANNOT_COLS) - CC_INVISIBLE) for r in analysed),
        "files_with_any_bloat": sum(any(r[c] for c in ANNOT_COLS) for r in analysed),
    }

    corr = [r for r in funcs]
    out["correctness"] = {
        "evaluated": len(corr),
        "correct": sum(r["correct"] for r in corr),
        "incorrect": [(r["sample"], r["tests_passed"], r["tests_total"], r["failure_cause"], r["failure_note"])
                      for r in corr if not r["correct"]],
        "interactive_not_evaluable": out["counts"]["interactive"],
        "per_model": {m: f"{sum(r['correct'] for r in corr if r['model'] == m)}/{sum(r['model'] == m for r in corr)}"
                      for m in ("claude", "gpt")},
    }

    out["edge_cases"] = {
        "files": len(funcs),
        "calls": sum(r["edge_calls"] for r in funcs),
        "crashes": sum(r["edge_crashes"] for r in funcs),
        "files_with_crash": [(r["sample"], r["edge_error_types"]) for r in funcs if r["edge_crashes"]],
        "original_paper_calls_claimed": 252,
    }

    ann = [r for r in analysed]
    out["annotation"] = {c: sum(r[c] for r in ann) for c in ANNOT_COLS}
    out["annotation"]["n_files"] = len(ann)

    # Paired GPT vs Claude comparison (same participant, same scenario, same prompt).
    pairs = {}
    for r in analysed:
        pairs.setdefault((r["scenario"], r["participant"]), {})[r["model"]] = r
    paired = [(p["gpt"], p["claude"]) for p in pairs.values() if "gpt" in p and "claude" in p]
    g = [a["lloc_ratio_minimal"] for a, _ in paired]; c = [b["lloc_ratio_minimal"] for _, b in paired]
    w = stats.wilcoxon(g, c)
    out["model_comparison"] = {
        "pairs": len(paired),
        "gpt_lloc_ratio": describe(g), "claude_lloc_ratio": describe(c),
        "gpt_longer": sum(a > b for a, b in zip(g, c)), "claude_longer": sum(b > a for a, b in zip(g, c)),
        "ties": sum(a == b for a, b in zip(g, c)),
        "wilcoxon_lloc_ratio": {"statistic": w.statistic, "p": w.pvalue},
        "per_scenario": {s: {"gpt": describe(a["lloc_ratio_minimal"] for a, b in paired if a["scenario"] == s),
                             "claude": describe(b["lloc_ratio_minimal"] for a, b in paired if b["scenario"] == s)}
                         for s in SCENARIOS},
        "annotation": {m: {col: sum(r[col] for r in ann if r["model"] == m) for col in ANNOT_COLS} for m in ("gpt", "claude")},
        "n_files": {m: sum(r["model"] == m for r in ann) for m in ("gpt", "claude")},
    }
    return out


def print_summary(s):
    def f(d):
        return "-" if d is None else f"mean {d['mean']:.2f} | median {d['median']:.2f} | range {d['min']:.2f}-{d['max']:.2f} (n={d['n']})"
    print("COUNTS", json.dumps(s["counts"]))
    print("\nREFERENCES")
    for k, v in s["references"].items():
        print(f"  {k}: LLOC {v['lloc']} CC {v['cc']} code_tokens {v['code_tokens']} mem {v['memory']:.0f}B time {v['time_us']:.3f}us")
    for sc, d in s["per_scenario"].items():
        print(f"\n== {sc} (static n={d['n_static']}, runtime n={d['n_runtime']})")
        for k in ("lloc_ratio", "cc_ratio", "lloc_ratio_guarded", "cc_ratio_guarded", "mem_ratio", "time_ratio",
                  "prompt_tokens", "pbs", "prompt_to_refcode_tokens", "dead_code"):
            print(f"  {k:26s} {f(d[k])}")
        print(f"  prompts longer than ref code: {d['prompts_longer_than_refcode']}/{d['n_static']}")
        if "spearman_tokens_vs_lloc" in d:
            print(f"  Spearman tokens vs LLOC: rho={d['spearman_tokens_vs_lloc']['rho']:.3f} p={d['spearman_tokens_vs_lloc']['p']:.3f}")
    print("\nPOOLED Pearson PBS vs LLOC ratio", s["pooled_pearson_pbs_vs_lloc_ratio"])
    print("POOLED Spearman raw tokens vs LLOC", s["pooled_spearman_raw_tokens_vs_lloc"])
    print("\nCC vs LLOC", json.dumps(s["cc_vs_lloc"]))
    print("\nCORRECTNESS", json.dumps(s["correctness"], indent=1))
    print("\nEDGE CASES", json.dumps(s["edge_cases"]))
    print("\nANNOTATION", json.dumps(s["annotation"]))
    m = s["model_comparison"]
    print(f"\nMODELS pairs={m['pairs']} gpt: {f(m['gpt_lloc_ratio'])}\n       claude: {f(m['claude_lloc_ratio'])}")
    print(f"  gpt longer {m['gpt_longer']}, claude longer {m['claude_longer']}, ties {m['ties']}, Wilcoxon p={m['wilcoxon_lloc_ratio']['p']:.3f}")
    for sc, d in m["per_scenario"].items():
        print(f"  {sc}: gpt {f(d['gpt'])}\n      claude {f(d['claude'])}")
    print("  annotation", json.dumps(m["annotation"]), m["n_files"])


if __name__ == "__main__":
    os.chdir(RESEARCH)
    main()
