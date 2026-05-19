# measure.py - Code Quality Measurement

This script automatically analyzes Python files across four coding scenarios (S1–S4) and spits out a CSV report packed with quality metrics. Think of it as a health check for generated or student code. It measures everything from how fast a function runs to whether it crashes on weird inputs.

# How to Run

```bash
python measure.py
```

By default it scans the `data/` folder and writes all results to `results.csv`. Our folder structure is looking something like this:

data/
  S1/solution.py
  S2/solution.py
  ...

# What Each Function Does

`count_tokens(text)`
Counts how many tokens a piece of text contains. If the `tiktoken` library is installed it uses OpenAI's `cl100k_base` tokenizer (the same one used by GPT-4) for an accurate count. If not, it falls back to a simple word count as an approximation.

`compute_pbs(prompt_text, scenario)`
Calculates the Prompt Bloat Score (PBS) - a ratio that tells us how verbose a prompt is relative to the reference solution length for that scenario. A high PBS means a lot of words were used to describe a simple problem.
Returns the raw token count and the PBS ratio (tokens ÷ reference LLOC).

`load_prompt(path)`
Looks for a `prompt.txt` file sitting next to the Python file being analyzed and reads it. If there's no prompt file, it just returns `None`.


`get_scenario(path)`
Figures out which scenario (S1, S2, S3, or S4) a file belongs to by looking at the folder path. For example, a file at `data/S2/solution.py` returns `"S2"`.

`load_func(path, expected_name)`
Loads a Python file and finds the function to test inside it. It first looks for a function with the expected name (like `final_score` for S1). If that's not found, it falls back to the first callable it can find. It also silences any `print()` calls and mocked `input()` prompts so loading the module doesn't flood the terminal.

`build_call(func, args)`
Wraps a function into a zero-argument callable so it can be timed cleanly. It handles two styles:

-Functions with parameters that passes the args directly.
-Functions that use `input()` that automatically feeds the test values through a mock so they don't sit there waiting for keyboard input.

`safe_cv(values)`
Calculates the Coefficient of Variation (standard deviation ÷ mean), which measures how consistent a set of numbers is. Used internally to check stability. Returns `0` if there's only one value or if the mean is effectively zero (to avoid division-by-zero).

`get_lloc(path)`
Runs the `radon` tool on a file to count its Logical Lines of Code (LLOC) - basically the number of meaningful statements, ignoring blank lines and comments. A good measure of actual code size.

`get_cc(path)`
Uses `radon` to calculate Cyclomatic Complexity (CC) - a number that tells you how many independent paths exist through the code. A score of 1 is dead simple, scores above 10 start getting hard to test and maintain. This returns the highest complexity score found across all functions in the file.

`get_vulture(path)`
Runs `vulture` to detect dead code - variables, functions, or imports that are defined but never used. Returns a count of suspected dead code items. It's smart enough to ignore the main expected function name (e.g., `final_score`) so it doesn't falsely flag the entry point.

`measure_memory(func, args, n=5)`
Measures how much memory the function uses when it runs. It runs the function 5 times and tracks the peak memory usage each time (using Python's `tracemalloc`), then returns the average peak in bytes. Running it multiple times smooths out any one-off spikes.

`measure_time(func, args)`
Benchmarks how fast the function runs. It calls the function 1,000 times per repeat, across 5 repeats (so 5,000 calls total) and returns the average execution time in microseconds (µs). This gives a stable, reliable timing even for very fast functions.

`run_edges(func, cases)`
Stress-tests the function with edge case inputs - things like zeros, empty strings, or negative numbers to see how gracefully it handles the unexpected. 
Returns:
-Crash rate - the fraction of edge cases that caused an exception (0.0 = no crashes, 1.0 = crashed on everything).
-Error types - a pipe-separated list of the exception names that were raised (e.g., `ValueError|TypeError`).

`process_file(path)`
The main workhorse. Takes a single `.py` file, figures out its scenario, loads the right function, and runs all the measurements above. Returns a dictionary with all collected metrics, ready to be written to CSV.

`run_all(folder, outcsv)`
Walks an entire folder tree, finds every `.py` file, runs `process_file` on each one, and collects all the results into a single CSV file. Files that error out are logged and skipped so one bad file doesn't stop the whole run.

# Output CSV Columns
| Column | What it means |
| `file` | Path to the analyzed file |
| `scenario` | Which scenario the file belongs to (S1–S4) |
| `lloc` | Logical lines of code |
| `cc` | Maximum cyclomatic complexity |
| `dead_code` | Number of dead code issues detected |
| `memory` | Average peak memory usage (bytes) |
| `time_us` | Average execution time (microseconds) |
| `edge_crash_rate` | Fraction of edge cases that caused a crash |
| `edge_error_types` | Types of errors raised during edge case testing |
| `prompt_tokens` | Token count of the associated prompt (if available) |
| `pbs_ratio` | Prompt Bloat Score - tokens per reference line of code |

# Dependencies

```bash
pip install tiktoken radon vulture
```
- `tiktoken` - accurate token counting (optional but recommended)
- `radon` - LLOC and cyclomatic complexity analysis
- `vulture` - dead code detection
