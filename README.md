# ISDF Benchmarking

Set up with:

```python
python -m venv .venv
source .venv/bin/activate 
pip install -e ".[dev]"
```

## TODOS

* Set up a parser that will run on the remote, then copy the data back to this machine
* Visualise the data in Jupyter
* COllate my other python parsing/plotting scripts and move here
* Move inputs here too, into `molecule_set`

For each system, plot the average SCF time comparison (minus first), and first SCF step comparison

Add kmeans profiling to the code and re-run
  Should be able to easily see how much this is adding

Roll back my ISDF options to take an SCF iteration, and inject via the KS obj. See how much of an effect this has

### Issues with Results

* Note, exchange energy per iteration is not output anyway, so I need to add this and re-run everything

* Code is looking slower wit ISDF... wasn't a problem with the serial code
  * Need to roll the code back/modify it, so I can control how often kmeans is called
  * Look at profiling breakdown, and add kmeans profiling
  * Speed drop MUST either be the MPI overhead... which doesn't make a lot of sense when on the same node, or the kmeans 
  needs improving for larger systems, and is killing the speed when run on every SCF cycle
  * See what the serial code does. Repeat with single MPI process
  * Also possible that I ran with too many interpolation points?