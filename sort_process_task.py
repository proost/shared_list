import random
import multiprocessing
import time
import copy

manager = multiprocessing.Manager()
shared_list = manager.list(random.sample(range(0,100),10))
lock = manager.Lock()

def main():
    results = list()
    for i in range(10):
        q = multiprocessing.Queue()
        process = multiprocessing.Process(target=job,args=(lock,q))
        process.start()
        results.append(q.get())
    for index,result in enumerate(results):
        result_list,exe_time = result
        print(str(index) + " : " + str(result_list) +"   " + str(exe_time))

def job(
    lock:'lock',
    q:'q'
    ):
    start = time.time()
    lock.acquire()
    sort_list()
    copied_list = copy_list()
    generate_element()
    lock.release()
    end = time.time()
    q.put((copied_list,end-start))

def sort_list():
    global shared_list
    shared_list.sort()

def copy_list() -> 'list':
    global shared_list
    copied_list = copy.deepcopy(shared_list)
    return copied_list

def generate_element():
    global shared_list
    for key,value in enumerate(random.sample(range(0,100),10)):
        shared_list.__setitem__(key,value)

if __name__=="__main__":
    main()
