"""
coreit
-------

Helper function to throw code on cores that can be run in parallel.

If you have code like

>>> for i in xrange(start, stop):
...     slow_function(i)

You can speed it up on a 4-core machine by running it like so:

>>> functions = [slow_function for i in xrange(start, stop)]
>>> args = [(i,) for i in xrange(start, stop)]
>>> coreit(functions, args, 4)

Licensed under PSF license
Copyright (c) 2010 Matt Harrison
"""

__license__ = 'psf'
__author__ = 'matthewharrison@gmail.com'
__version__ = '0.0.1'




def coreit(functions, args, num_procs):
    """
    Given a list of functions (and a corresponding list of thier
    arguments (in tuples or empty tuples)), run them concurrently
    using num_procs.
    """
    from multiprocessing import Process, Queue
    from Queue import Empty
    def runit(queue):
        while True:
            try:
                f, args = queue.get(block=False)
                f(*args)
            except Empty:
                break
    work_q = Queue()
    for i, f in enumerate(functions):
        work_q.put((f, args[i]))
    processes = [Process(target=runit, args=(work_q,)) for i in range(num_procs)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

def slow_function():
    import math
    total = 0
    for i in xrange(10000000):
        total = total + math.sqrt(i)
    print total

def test():    
    import timeit
    num_runs = 1
    print '2 core'
    t = timeit.Timer("coreit([slow_function, slow_function], [tuple(), tuple()], 2)", 'from coreit import *')
    print "%s seconds" % t.timeit(num_runs)
    print '1 core'
    t = timeit.Timer("slow_function();slow_function()", 'from coreit import *')
    print "%s seconds" % t.timeit(num_runs)

if __name__ == '__main__':
    test()
