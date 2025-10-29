'''
    Name:   parakyt.py
    Author: Keenan Stone
    Date:   7/7/23
    Desc:
        Embarassingly parallel for looping using dask.
        Replaces cumbersome syntax in individual scripts
        with a simple par_for call. No pre-requisites needed.
        Creates temporary dask client if none detected.
        Uses all available resources by default.
    Usage:
        results = parakyt.par_for(
            <function applied to each obj in itterable>,
            <itterable>,
            <execution mode>,
            <number of cores to use>
        )
'''
import multiprocessing as mp
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

import dask
import dask.config
import dask.distributed as ddist
from dask.delayed import Delayed
from dask.distributed import Client

T_Delayed = Union[Delayed, Any]
T_PktComputable = Union[T_Delayed, List[T_Delayed], Tuple[T_Delayed]]
T_Callable = Callable[..., Any]

#------ Classes -------------#
class ClientContextManager:
    """
    A context manager to automatically connect to an existing Dask Client 
    or create a new temporary local cluster. 
    
    If a new client is created, it is automatically closed upon exiting 
    the 'with' block.
    
    This wrapper class is intended to mimic smart pointers functionality by 
    eliminating need to explicitly close clients before they lose scope.
    """
    def __init__(self, num_cores: Optional[int] = None, exec_mode: str = "processes"):
        """
        Args:
            num_cores (Optional[int]): Number of cores for workers if creating a new process-based client.
            exec_mode (str): 'processes' (default) for multiprocessing or 'threads' for multithreading.
        """
        self.client: Optional[Client] = None
        self._must_close: bool = False
        self.num_cores: Optional[int] = num_cores
        self.exec_mode: str = exec_mode.lower()

    def __enter__(self) -> Client:
        """
        Executes on entering the 'with' block. Attempts to get an existing 
        client, or creates a new one.
        """
        try:
            # 1. Attempt to get an existing client
            existing_client = ddist.get_client()
            if existing_client is not None:
                self.client = existing_client
                self._must_close = False
                print("Connected to an existing Dask client.")
            else:
                raise Exception("No existing client detected.")
        except Exception:
            # 2. No existing client found, create a temporary local cluster.
            self._must_close = True
            
            if self.exec_mode == "threads":
                # Local cluster using threads (good for low-latency tasks)
                print("Creating temporary Dask thread-based local cluster...")
                self.client = Client(processes=False) 
            else: 
                # Local cluster using processes (good for CPU-bound tasks)
                if self.num_cores is None:
                    self.num_cores = mp.cpu_count()
                print(f"Creating temporary Dask process-based local cluster with {self.num_cores} workers...")
                self.client = Client(n_workers=self.num_cores)
        
        # Ensure the client is valid before returning
        if self.client is None:
             raise RuntimeError("Failed to connect to or create a Dask client.")

        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Executes on exiting the 'with' block, ensuring cleanup if necessary.
        """
        if self._must_close and self.client is not None:
            # Only close the client if this context manager created it.
            try:
                print("Closing temporary Dask client.")
                self.client.close()
                self.client = None 
            except Exception as e:
                # Print warning if closing fails, but proceed gracefully
                print(f"Warning: Error closing temporary Dask client: {e}")
                
        # Return False to propagate exceptions that occurred within the 'with' block
        return False 


#------ Implementation ------#
@dask.delayed
def delayed_process_iteration(func: T_Callable, args: List[T_Delayed]) -> T_Delayed:
    """
    Wraps the function call in dask.delayed to make it an entry in the graph.
    """
    return func(*args)


def par_for(
    func: T_Callable,
    iterable: Iterable[Any],
    exec_mode: str = "processes",
    num_cores: Optional[int] = None
) -> T_PktComputable:
    """
    Executes a parallelized for loop over an iterable using Dask.

    The Dask client is managed automatically by the ClientContextManager.

    Args:
        func (T_Callable): The callable function to execute for each item.
        iterable (Iterable[Any]): The list of elements to iterate over.
        exec_mode (str): 'processes' or 'threads' for cluster creation.
        num_cores (Optional[int]): Max number of cores to use if creating a process-based cluster.
        
    Returns:
        T_PktComputable: A tuple containing the results of the computation.
    """
    results = None
    with ClientContextManager(num_cores=num_cores, exec_mode=exec_mode) as client:
        # Client is now active, Dask will use it automatically.
        # 1. Build the Dask graph of delayed tasks
        tasks = [delayed_process_iteration(func, [item]) for item in iterable]
        # 2. Compute the results -> dask.compute will send the graph to the active 'client' for parallel execution
        print(f"Submitting {len(tasks)} tasks to Dask for computation...")
        try:
            results = dask.compute(*tasks)
            print("Computation finished successfully.")
        except Exception as e:
            print(f"Error during Dask computation: {e}")
    return results
    

# =====================================================================================================================    
# --- Demonstration Functions ---
# =====================================================================================================================    

def example_task(n: int) -> int:
    """A sample CPU-bound task for demonstration."""
    print(f"Processing number: {n}")
    # Simulate a time-consuming operation
    time.sleep(0.1) 
    return n * n

def demo():
    """Demonstrates usage of the refactored par_for function."""
    print("--- Dask Parallel For Loop Demonstration ---")
    
    # 1. Define the iterable list
    data_list = list(range(1, 11))
    print(f"Input data: {data_list}")
    
    # 2. Run the parallel loop using the default 'processes' mode
    print("\n--- Running in 'processes' mode (Multiprocessing) ---")
    
    # ClientContextManager will automatically create a process-based cluster and close it.
    computed_results = par_for(
        func=example_task, 
        iterable=data_list, 
        exec_mode="processes"
    )

    if computed_results:
        print(f"\nFinal Results (processes): {computed_results}")

    # 3. Run the parallel loop using the 'threads' mode
    print("\n--- Running in 'threads' mode (Multithreading) ---")

    # ClientContextManager will automatically create a thread-based cluster and close it.
    computed_results_threads = par_for(
        func=example_task, 
        iterable=data_list, 
        exec_mode="threads"
    )
    
    if computed_results_threads:
        print(f"\nFinal Results (threads): {computed_results_threads}")
    
    print("\n--- Demonstration Complete ---")

if __name__ == "__main__":
    # Ensure multiprocessing is compatible if run interactively (like in a notebook)
    mp.freeze_support()
    demo()