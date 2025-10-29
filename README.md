# **parakyt**

**A utility for easily embarrassingly parallelizing for loops using Dask.**

[parakyt](https://github.com/Keenan-M-Stone/parakyt.git) 
simplifies high-performance computing tasks by providing a single function,
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
git clone https://github.com/Keenan-M-Stone/parakyt.git 
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

# 💡 Quick Usage Examples

The primary function is par_for, which takes a callable function and an iterable of arguments.
Refer to `parakyt/demo.py` and the internal `parakyt` demo function for demonstrations.

# 🔗 Project Metadata

Repository: https://github.com/Keenan-M-Stone/parakyt

# 📓 Release Notes
This version implements and exposes both the `par_for` function 
for generic usage as well as `ClientContextManager` class, such 
that developers may experiment with it and recommend revisions 
ahead of next release (development expected to continue on `beta` 
branch).

# 🏆 Recognition of Contributers
A similar script was originally developed for uses by the NOAA 
verification group. Special thanks to Samantha Walley, Gavin Harrison,
and Dana Strom for their helpful comments.

