'''
    Additional usage examples for parakyt.par_for function.
'''

from parakyt import par_for
from pprint import pprint
import time
import os

if __name__ == "__main__":
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
        #exec_mode='threads'
    )

    # 4. Print results (the order of execution is not guaranteed, 
    # but the order of the results matches the input iterable)
    print("\n--- Results ---")
    pprint(results)
    # The 'worker_pid' will likely show multiple process IDs, confirming parallel execution.

