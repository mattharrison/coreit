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
    #for i in xrange(100000000):
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

# def dump_fact_multiprocess(dburl, start_id, end_id, num_procs=3):
#     from multiprocessing import Process, Queue
#     work_q = Queue()
#     for i in range(start_id, end_id):
#         work_q.put(i)
#     processes = [Process(target=dump_from_q, args=(dburl, work_q)) for i in ran\
# ge(num_procs)]
#     for p in processes:
#         p.start()
#     for p in processes:
#         p.join()

# def dump_from_q(dburl, q):
#     from Queue import Empty
#     while True:
#         try:
#             id = q.get(block=False)
#             print "DUMPING", id
#             dump(dburl, id)
#         except Empty:
#             break


# def dump_fact(start_id, end_id):
#     for i in range(start_id, end_id):
#         print 'dumping', i
#         dump('oracle://app_whs:password@192.168.100.204/item', i)



# def to_csv(data, filename, write_headers=True):
#     """
#     write data (sqlalchemy results, to a csv file that postgres can bulk load)
#     """
#     fout = open(filename, 'w')
#     os.chmod(filename, 0777) # postgres user needs read permission                  #import pdb; pdb.set_trace()                                                    first_row = data.next()
#     fieldnames = [col for col in first_row.keys()]
#     #csv_out = csv.DictWriter(fout, delimiter='|', fieldnames=fieldnames, quote\
# -uu-:---F1  dumporacle.py   Top L1     (Python)---------------------------------
# Mark set
# [ caserver01 ][                 (0*$ bash)                  ][2010-07-01  8:04 ]
