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

def par_for(
    func: T_Callable,
    iterable: Iterable[T_Delayed],
    exec_mode: str = "distributed",
    num_cores: Optional[int] = None
) -> Optional[T_PktComputable]:
    if num_cores is None:
        num_cores = mp.cpu_count()

    # Attempt to get an existing client
    # Create temporary if none available
    f_close_client = True
    try:
        existing_client = ddist.get_client()
        if existing_client is not None:
            client = existing_client
            f_close_client = False
        else:
            raise Exception("No client existing detected.")
    except:
        if exec_mode == "distributed":
            client = ddist.Client(processes=False)
        elif exec_mode == "threads":
            client = ddist.Client(scheduler='threads')
        else:
            client = ddist.Client(scheduler='processes', num_workers=num_cores)

    results = None
    with dask.config.set(scheduler=client):
        tasks = [delayed_process_iteration(func, [item]) for item in iterable]
        results = dask.compute(*tasks)

    # Close temporary client.
    if f_close_client:
        client.close()
    
    return results
