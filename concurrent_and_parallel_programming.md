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
- 