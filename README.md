# Welcome

## Requirements

 * You require Python 3.
 * You require Docker.

You have to ensure that the logs are generated on same machine,
so you might want to delete my logs first before running on your machine.

## Visualization of results

Running `python -m http.server` you can check
the url `http://localhost:800/report.html` for the details.
The table and graphs (tooltips) are using the date from this file: `results\results.json`.

## Usage

Run in any order as often you like:

 * running `python scripts\run_python_3_10.py`
 * running `python scripts\run_python_3_10_multiprocessing.py`
 * running `python scripts\run_pypy_3_8.py`
 * running `python scripts\run_nodejs_16.py`

With `python analyse.py` the logs will be parsed and
the file `results\results.json` will be upated.
