'''
    Name:   parakyt.py
    Author: Keenan Stone
    Date:   7/7/23
    Desc:
        Embarassingly parallel for looping using dask.
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

#------ Implementation ------#
@dask.delayed
def delayed_process_iteration(func: T_Callable, args: List[T_Delayed]) -> T_Delayed:
    # Call the function with arguments
    return func(*args)


def connect_create_client(
        client: Any = None,
        num_cores: Optional[int] = None,
        exec_mode: str = "distributed"
    ) -> Boolean:
    # Attempt to get an existing client if none provided.
    # Create temporary if none detected.
    if client is not None:
        return False
    f_close_client = True
    try:
        existing_client = ddist.get_client()
        if existing_client is not None:
            client = existing_client
            f_close_client = False
        else:
            raise Exception("No client existing detected.")
    except Exception as e:
        print(e)
        if exec_mode == "distributed":
            client = ddist.Client(processes=False)
        elif exec_mode == "threads":
            client = ddist.Client(scheduler='threads')
        else:
            # Determine cpu count if none provided.
            if num_cores is None:
                num_cores = mp.cpu_count()
            client = ddist.Client(scheduler='processes', num_workers=num_cores)
    return f_close_client


def par_for(
        func: T_Callable,
        iterable: Iterable[T_Delayed],
        exec_mode: str = "distributed",
        num_cores: Optional[int] = None,
        client: Any = None
    ) -> Optional[T_PktComputable]:
    # Execute parallelized for loop over `func` and .
    f_close_client = connect_create_client(client, num_cores)
    results = None
    with dask.config.set(scheduler=client):
        tasks = [delayed_process_iteration(func, [item]) for item in iterable]
        results = dask.compute(*tasks)

    # Close temporary client.
    if f_close_client:
        client.close()
    
    return results
