# py_single_file_storage
Store some information within the current .py file for the distribution of a single-source-file Python application.

# Application Scenarios
**py_single_file_storage** is a lightweight utility designed for storing persistent data directly within a single Python source file. It is specially optimized for distributing standalone, single-file Python applications where no external configuration files, databases, or auxiliary resources are desired.

By embedding state and runtime data inside the `.py` file itself, this library enables scripts to retain information across executions — such as execution counters, user preferences, cached parameters, or one-time setup flags — without creating additional files on the filesystem. It works reliably in scripted environments while avoiding conflicts in interactive Python shells, making it ideal for portable tools, utility scripts, self-contained CLI programs, and lightweight deployment scenarios where clean distribution and minimal footprint are priorities.

## Installation

```bash
pip install py_single_file_storage
```

## Usage

> [!IMPORTANT]
> You are recommanded to only use this function in .py source file, not interactive command line of python.

```python
from py_single_file_storage import PSFS_Object
import sys
import os
in_script = not hasattr(sys, 'ps1')

if in_script:
    filepath = __file__
else:
    filepath = os.path.join(os.getcwd(), "a.py")
    open(filepath, "a").close()

# a simple program to count the number of launch for script
with PSFS_Object(filepath) as mem:
    data = mem.get()
    if data.get("run_time") is None:
        data["run_time"] = 0
    data["run_time"] += 1
    mem.put(data)
    print(f"run time now: {data["run_time"]}")
```
