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
import concurrent.futures
from timeit import default_timer as timer
import multiprocessing
from math import sqrt

def is_prime(x):
    if x<2:
        return False
    
    if x==2:
        return True
    
    if x%2 == 0:
        return False
    
    limit = int (sqrt(x)) +1
    for i in range(3, limit, 2):
        if x%i == 0:
            return False
    
    return True


def concurrent_solve(n_workers):
    print("Number of workers: %i." % n_workers )

    result = []

    if __name__ == '__main__':
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
            # concurrent phase
            start =timer()
            futures = [executor.submit(is_prime, i) for i in input]
            completed_futures = concurrent.futures.as_completed(futures)
            stop = timer()
            # sequential phase
            seq_start = timer()

            for i,future in enumerate(completed_futures):
                if future.result():
                    result.append(future.result())

            seq_end = timer()
        print("It took ", stop -start, "to complete concurrent phase")
        print("it took ", seq_end-seq_start, "to complete sequential phase")

input = [i for i in range(10 ** 13, 10 **13 + 1000)]

for n_workers in range(1, multiprocessing.cpu_count()+1):
    concurrent_solve(n_workers)
    print("_" * 20)
