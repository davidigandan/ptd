# Introduction and Amdahl's Law

- A sequential program is in one place at a time, while a concurrent program can be in multiple places at the same time- provided that the different components are independent or semi-independent. 
- If we run this program, we can see that it completes much faster using much more cpu load

```Python
## Chapter 1/example1.py

from math import sqrt
from timeit import default_timer as timer
import concurrent.futures
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
    
# Generated list of numbers to test
input = [i for i in range(10 ** 13, 10 **13 + 10**3)]


# sequential
# start = timer()
# result = []
# for i in input:
#     if is_prime(i):
#         result.append(i)
# print('result 1: ', result)
# print('Took: %.2f seconds.' % (timer() - start))
# print(len(result))


# concurrent
start = timer()
result = []
if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(is_prime, i) for i in input]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            if future.result():
                result.append(future.result())

    print('Result 2: ', result)
    print('Took: %.2f seconds. ' % (timer() - start))

```

### Concurrency vs Parallelism

- What's the difference between concurrency and parallelism?
- **Analogy**: Image we are asked to write an essay on the cold war and do some calculus at the same time. We have only one brain (our resource). We can switch between cold war and calculus, so we are working on both tasks at the same time. This is concurrency. When two threads of work (cold war and calculus) are executed at the same time by the same resource. It offers no speed up compared to sequentially writing the two essays - cold war then calculus. But what if we had two brains (double the resources). We could assign each piece of work to each brain. This is parallelism. Since we've doubled our resources, we can complete the total task in half the time. 
- But if concurrency offers no speed up compared to sequential execution, what's the point? What after each paragraph of our essay and after each stage of our calculus computation, we had to have a friend check our work thus far. If we were working sequentially, what would we do when we're done with a paragraph? We'd be left with no work to do. This is inefficient. However, if we are using concurrency and we're working on both threads of work at the same time, despite us only have one resource, we can be more efficient. Every time we finish a paragraph, we move to calculus. Every time we finish a stage of calculus, we move back to write the next paragraph. There's just less idle time for the resource - more efficient. In computation terms, when a thread is I/O bound (network, user input, disk input, etc) our core (resource) can work on another thread of work while the first thread is waiting. 
- Concurrency is about managing the shared resource amongst multiple threads of work. Parallelism is about bringing in more resources to handle the work. 
- Note that if a task isn't I/O bound, and therefore doesn't need concurrency, it may run slower than sequentially when run it concurrently as concurrency has some overhead for coordination.
- A consequence of parallelism is that the results may be out of order.

### Amdahl's Law

- Amdahl's Law gives the formula for calculating potential improvements in speed of a concurrent program by increasing its resources.
- It only concerns parallel execution, but it will give us concurrent execution estimates.

$$
S = T(1)/T(j)
$$

*where S is speedup and  j is the number of processors*

- If there are N workers on a fully parallelizable job, then the time taken to complete the job is:

$$
1/N * Original Time Taken
$$

- But most programs aren't fully parallelizable. They're often a mix. 

$$
\text{Speedup} = \frac{1}{B+\frac{1-B}{j}} 
$$

*where B is sequential fraction and j is the number of processors*

- Amdahl's Law denotes that as we increase the number of processors, the speedup increases, but the gain reduces with each addition of processor. It is impossible to obtain a speedup greater than 1/B
- Consider this: 
- ```py
  # Chapter 2/example 1.py
  import concurrent.futures
  from timeit import default_timer as timer
  import multiprocessing
  from math import sqrt
  import time

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
      result = []

      with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
          # sequential phase
          print("Solving with %i worker(s)." % n_workers )
          start =timer()
          futures = [executor.submit(is_prime, i) for i in input]
          completed_futures = concurrent.futures.as_completed(futures)
          sub_start = timer()
          # concurrent phase

          for i,future in enumerate(completed_futures):
              if future.result():
                  result.append(future.result())

          sub_duration = timer() - sub_start
          duration = timer() - start
          print("Sub took ", sub_duration, "to complete concurrent phase")
          print("Took", duration - sub_duration, "to complete sequential pahse")
          print("Took ", duration, "to complete sequential+concurrent phase")

      # time.sleep(15)


  if __name__ == "__main__":
      input = [i for i in range(10 ** 13, 10 **13 + 10000)]

      for n_workers in range(1, multiprocessing.cpu_count()+1):
          concurrent_solve(n_workers)
          print("_" * 20)
  ```
- Some fraction in this program is sequential, and others concurrent. When we run this on a computer with 12 cores, we get the following results:
- ```
  Solving with 1 worker(s).
  Sub took  20.289581300000464 to complete concurrent phase
  Took 0.1575193999997282 to complete sequential pahse
  Took  20.447100700000192 to complete sequential+concurrent phase
  ____________________
  Solving with 2 worker(s).
  Sub took  10.056327999999667 to complete concurrent phase
  Took 0.13137430000097083 to complete sequential pahse
  Took  10.187702300000637 to complete sequential+concurrent phase
  ____________________
  Solving with 3 worker(s).
  Sub took  7.028111499999795 to complete concurrent phase
  Took 0.14373069999965082 to complete sequential pahse
  Took  7.171842199999446 to complete sequential+concurrent phase
  ____________________
  Solving with 4 worker(s).
  Sub took  5.49527930000022 to complete concurrent phase
  Took 0.15288239999972575 to complete sequential pahse
  Took  5.648161699999946 to complete sequential+concurrent phase
  ____________________
  Solving with 5 worker(s).
  Sub took  4.9697667999998885 to complete concurrent phase
  Took 0.1616593999997349 to complete sequential pahse
  Took  5.131426199999623 to complete sequential+concurrent phase
  ____________________
  Solving with 6 worker(s).
  Sub took  4.482540599999993 to complete concurrent phase
  Took 0.17121059999954014 to complete sequential pahse
  Took  4.653751199999533 to complete sequential+concurrent phase
  ____________________
  Solving with 7 worker(s).
  Sub took  4.146386800000073 to complete concurrent phase
  Took 0.1732584000001225 to complete sequential pahse
  Took  4.3196452000001955 to complete sequential+concurrent phase
  ____________________
  Solving with 8 worker(s).
  Sub took  3.9219788999998855 to complete concurrent phase
  Took 0.18826790000002802 to complete sequential pahse
  Took  4.1102467999999135 to complete sequential+concurrent phase
  ____________________
  Solving with 9 worker(s).
  Sub took  3.782555699999648 to complete concurrent phase
  Took 0.1922231999997166 to complete sequential pahse
  Took  3.9747788999993645 to complete sequential+concurrent phase
  ____________________
  Solving with 10 worker(s).
  Sub took  3.72229790000074 to complete concurrent phase
  Took 0.1890053999995871 to complete sequential pahse
  Took  3.911303300000327 to complete sequential+concurrent phase
  ____________________
  Solving with 11 worker(s).
  Sub took  3.7293712000000596 to complete concurrent phase
  Took 0.19781439999951544 to complete sequential pahse
  Took  3.927185599999575 to complete sequential+concurrent phase
  ____________________
  Solving with 12 worker(s).
  Sub took  3.739317500000652 to complete concurrent phase
  Took 0.20922569999947882 to complete sequential pahse
  Took  3.948543200000131 to complete sequential+concurrent phase
  ```
    - Analysing when the work was done with just 1 worker, we can see the fraction of the work that was concurrent vs sequential. Less than 1% of the work was sequential. Therefore, this is a highly parallelizable task. 
    - The reduction in the time taken during concurrent section (and thus total time taken) demonstrates the highly parralelizable nature of the work. From 20.2seconds to 3.74seconds. 
    - However we see the amount of speedup reduce with each addition of a core. In fact, over 85% of the gains we will ever get from all 12 processes can be achieved with just 4 processes. 
    - We get these diminishing results because:
        - Ahmdal's Law sates that the speedup is limited by the sequential portion of the program contributing overhead
        - Interprocess communication and creation adds overhead

# Threads

- A single process can be composed of multiple threads. Threads in a process often execute concurrently, accessing the same resources such as memory. Threads in the same process share the process's code and context. 
- While processes can share data, it is uncommon. 

### Multithreading

