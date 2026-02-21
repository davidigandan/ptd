# # # Chapter 1/example1.py

# from math import sqrt
# from timeit import default_timer as timer
# import concurrent.futures
# def is_prime(x):
#     if x<2:
#         return False
    
#     if x==2:
#         return True
    
#     if x%2 == 0:
#         return False
    
#     limit = int (sqrt(x)) +1
#     for i in range(3, limit, 2):
#         if x%i == 0:
#             return False
    
#     return True
    
# # Generated list of numbers to test
# input = [i for i in range(10 ** 13, 10 **13 + 10**4)]


# # sequential
# # start = timer()
# # result = []
# # for i in input:
# #     if is_prime(i):
# #         result.append(i)
# # print('result 1: ', result)
# # print('Took: %.2f seconds.' % (timer() - start))
# # print(len(result))




# # concurrent
# start = timer()
# result = []
# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
#         futures = [executor.submit(is_prime, i) for i in input]

#         for i, future in enumerate(concurrent.futures.as_completed(futures)):
#             if future.result():
#                 result.append(future.result())

#     print('Result 2: ', result)
#     print('Took: %.2f seconds. ' % (timer() - start))


# # Chapter 1/example2.py
# from timeit import default_timer as timer
# def f(x):
#     return x*x - x+1

# # sequential
# start = timer()
# result = 3
# for i in range(20):
#     result = f(result)

# print('result is very large. Only printing the last 5 digits: ', result % 100000)
# print('sequential took: %.2f seconds. ' % (timer()-start))


# Chapter 2/example 1.py
# import concurrent.futures
# from timeit import default_timer as timer
# import multiprocessing
# from math import sqrt
# import time

# def is_prime(x):
#     if x<2:
#         return False
    
#     if x==2:
#         return True
    
#     if x%2 == 0:
#         return False
    
#     limit = int (sqrt(x)) +1
#     for i in range(3, limit, 2):
#         if x%i == 0:
#             return False
    
#     return True


# def concurrent_solve(n_workers):
#     result = []
    
#     with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
#         # sequential phase
#         print("Solving with %i worker(s)." % n_workers )
#         start =timer()
#         futures = [executor.submit(is_prime, i) for i in input]
#         completed_futures = concurrent.futures.as_completed(futures)
#         sub_start = timer()
#         # concurrent phase
        
#         for i,future in enumerate(completed_futures):
#             if future.result():
#                 result.append(future.result())

#         sub_duration = timer() - sub_start
#         duration = timer() - start
#         print("Sub took ", sub_duration, "to complete concurrent phase")
#         print("Took", duration - sub_duration, "to complete sequential pahse")
#         print("Took ", duration, "to complete sequential+concurrent phase")

#     # time.sleep(15)


# if __name__ == "__main__":
#     input = [i for i in range(10 ** 13, 10 **13 + 10000)]

#     for n_workers in range(1, multiprocessing.cpu_count()+1):
#         concurrent_solve(n_workers)
#         print("_" * 20)



# Chapter3/my_thread.py
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print("Starting thread %s" % self.name)
        thread_count_down(self.name, self.delay)
        print("Finished thread %s." % self.name)

def thread_count_down(name, delay):
    counter = 5

    while counter:
        time.sleep(delay)
        print("Thread %s counting down: %i..." % (name, counter))
        counter -=1

# # example 1
# thread1 = MyThread('A', 0.5)
# thread2 = MyThread('B', 0.5)

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

# print('Finished')


# example2.py
from math import sqrt


def is_prime(x):
    if x<2:
        print('%i is not a prime number.' % x)
    
    elif x==2:
        print('%i is a prime number.' % x)
    
    elif x%2 == 0:
        print('%i is not a prime number. ' % x)
    
    else:
        limit = int (sqrt(x)) +1
        for i in range(3, limit, 2):
            if x%i == 0:
                print('%i is not a prime number. ' % x)

        print('%i is a prime number.' % x)

import _thread as thread

my_input = [2, 193, 323, 1327, 433785907]

for x in my_input:
   thread.start_new_thread(is_prime, (x,)) 