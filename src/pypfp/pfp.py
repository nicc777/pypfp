'''
Refer to https://docs.python.org/3.8/library/multiprocessing.html
'''
import multiprocessing


class MultiProcessor:

    def __init__(self, context: dict=None):
        self.functions = list()
        self.context = context
        self.results = list()
        self.function_args = dict()

    def register_function(self, f, f_args: dict=dict()):
        '''
        The function 
        '''
        self.functions.append(f)
        self.function_args[f.__name__] = f_args

    def execute_parallel(self):
        multiprocessing.set_start_method('spawn')
        q = multiprocessing.Queue()
        for function in self.functions:
            f_args = self.function_args[function.__name__]
            p = multiprocessing.Process(target=function, args=(q, self.context, f_args, ))
            p.start()
            self.results.append(q.get())





# EOF
