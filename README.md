# **parakyt**

**A utility for easily embarrassingly parallelizing for loops using Dask.**

`parakyt` simplifies high-performance computing tasks by providing a single function,
`par_for`, that parallelizes iterations over an iterable list. 
It automatically handles the creation and cleanup of a Dask distributed client for 
seamless execution, or detects and connects to an existing client if available.

| parakyt           | 7/23/23   |
|-------------------|-----------|
| Document Version  |  `1.0.0`  |
| Software Version  |  `1.0.0`  |


# 🚀 Installation

You can install parakyt via pip. This package relies on dask and distributed.
```
git clone ... 
pip install parakyt
```

# 🎯 Motivation

For student researchers, or others, who don't have the time to dive into the complexities
of how to best utilize `dask` for efficient parallelization, this should serve as a quick
and easy to use alternative. Some existing tool-boxes, such as `job-lib`, already provide
similar mechanisms for "embarassing parallelization" that users ought to consider as well,
in order to determine what is best for their use case.  

While this can be used in HPC environments, it is perhaps best used for conducting relatively
smaller scale jobs. In situations where one finds themselves needing to make repeated calls 
to `par_for`, they ought also consider establishing a `client` object with configurations 
specific to their computing environment - given that repeated client creation/destruction
and calls to `dask.compute` will greatly reduce performance. Further, more complex tasks,
such as vector|vector operations, will be better suited by other utilizations of `dask`
and `xarray`.

# 💡 Quick Usage Example

The primary function is par_for, which takes a callable function and an iterable of arguments.
```python
from parakyt import par_for
import time
import os

# 1. Define a task (this simulates heavy, independent computation)
def heavy_task(data_point: int) -> dict:
    """A function that simulates work and returns a result."""
    # Simulate a time-consuming process
    time.sleep(0.1) 
    
    # Return some useful data and the worker PID for verification
    return {
        "input": data_point,
        "result": data_point * data_point,
        "worker_pid": os.getpid()
    }

# 2. Define the input data
data_list = list(range(10))

# 3. Execute the parallel loop
# A temporary Dask cluster (using processes by default) is automatically
# created and closed when the function completes.
print("Starting parallel computation...")
results = par_for(
    func=heavy_task,
    iterable=data_list
)

# 4. Print results (the order of execution is not guaranteed, 
# but the order of the results matches the input iterable)
print("\n--- Results ---")
for res in results:
    print(f"Input: {res['input']}, Result: {res['result']}, Process ID: {res['worker_pid']}")
# The 'worker_pid' will likely show multiple process IDs, confirming parallel execution.
```

# 🔗 Project Metadata

Repository: https://github.com/Keenan-M-Stone/parakyt
