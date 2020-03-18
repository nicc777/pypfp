# pypfp

A Python parallel function processor - a demonstration of the Python `multiprocessing` library

Inspired by [this multi-threading and multi-processing tutorial](https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/)

The idea is to implement a class that will be able to take any number of functions and then call them all in parallel, using Python's `multiprocessing` library.

Each function must, however, take a very specific set of parameters, which will be discussed further down.

Each function must also use the `Result` class to store results, which relies on the `multiprocessing`.[Queue](https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Queue) class.

## Whats in the box?

In the `src` folder is the main library code, which has the following files:

* `__init__.py` - contains the `Result` class (will be discussed further down)
* `pfp.py` - The "parallel function processor" main class, called `MultiProcessor`
* A small number of unit tests under the `tests` directory to demonstrate the functionality

## Basic Workflow:

### Implementing Functions

Construct a function or functions that needs to be processed in parallel. An example skeleton function below can be used as reference:

```python
import inspect

def my_function(q, context: dict, args: dict):
    r = Result(function_name=inspect.currentframe().f_code.co_name)
    # processing stuff....
    q.put(r) 
```

__Input Parameters__

| Parameter   | Type                    | Description                                 |
|:-----------:|:-----------------------:|---------------------------------------------|
| q           | `multiprocessing.Queue` | Passed in and used to store our `Result`    |
| context     | `dict`                  | Global context that every function will get |
| args        | `dict`                  | Function specific arguments in a `dict`     |

Any results from processing can be stored in the `Result`:

```python
def my_function(q, context: dict, args: dict):
    r = Result(function_name=inspect.currentframe().f_code.co_name)
    # processing....
    r.result['Greeting'] = 'Hello World'
    q.put(r) 
```

Note that the line `q.put(r)` should be the final line of your function.

### Register Functions

Assuming you have a number of functions, `func1`, `func2` and `func3`, you can start preparing for their execution.

First, decide if there is some global context you need every function to get - typically these would be things like DB credentials or stuff like that. Define it in a `dict`, for example:

```python
GLOBAL_CONTEXT = {
    'Database': {
        'username': '...',
        'password': '...',
    }
}
```

Now, initialize the `MultiProcessor` class and add each function with their own specific arguments:

```python
m = MultiProcessor(context=GLOBAL_CONTEXT)
m.register_function(f=func1, f_args={....})
m.register_function(f=func2, f_args={....})
m.register_function(f=func3, f_args={....})
```

### Process

Finally, process and retrieve all your results:

```python
m.execute_parallel()
```

All results will be in `m.results` which is a list of `Result` objects.


