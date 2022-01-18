from subprocess import Popen, PIPE
import os
from time import sleep
import argparse
import multiprocessing
from time import time

class Infinity:
    count = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.count += 1
        return self.count

def findPIDByKeyword(keyword):
    result = Popen(['pgrep', str(keyword)],
                            stdout=PIPE, 
                            stderr=PIPE).communicate()[0].decode("utf-8")
    res = result.split("\n")
    if len(res) == 2:
        res = res[0]
        print("Found matched PID: {} => {}".format(keyword, res))
    elif len(res) == 1: 
        print("Can not find any process with keyword: {}".format(keyword))
    else:
        print("Found multiple processes with keyword: {}".format(keyword))
        exit(0)
    return res

def cpu_memory_monitor(pid=None, 
                    keywords=None,
                    interval=5, # seconds
                    samples=None):
    cores = multiprocessing.cpu_count()
    cpuBuffer, memBuffer = [], []
    query = ["%cpu=", "%mem=", "rss="]
    msgs = ""
    try:
        for st in Infinity() if samples is None else range(sample):
            result = [Popen(['ps', '-p', str(pid), '-o', name],
                            stdout=PIPE, 
                            stderr=PIPE).communicate()[0].decode("utf-8")[:-1] for name in query]
            if result == [""]*3:
                print("Failed to find process with PID: {}.".format(pid))
                return None
            else:
                cpuSP, memP, rss = [float(i) for i in result]
                cpu = float(cpuSP) / cores
                mem = float(rss) / 1024
                cpuBuffer.append(cpu)
                memBuffer.append(mem)
                msg = "Sample: {} cpu: {}% memory: {}MB\n".format(st, round(cpu, 2), round(mem, 2))
                print(msg, end="")
                msgs += "TimeStamp[{}] {}".format(time(), msg)
            sleep(interval)
    except KeyboardInterrupt:
        print("\nSampling stopped.")
    def summary(buffer):
        msg = "max: {}\navg: {}\nmin: {}\n".format(
            round(max(buffer), 2),
            round(sum(buffer)/len(buffer), 2),
            round(max(buffer), 2)
        )
        return msg
    msg = "cpuBuffer:\n{}memBuffer:\n{}".format(summary(cpuBuffer), summary(memBuffer))
    print(msg)
    msgs += msg
    with open("cm_mon.log", "w") as logger:
        logger.write(msgs)

    return cpuBuffer, memBuffer

def monPlot(cpu, memory, interval, show=False):
    import matplotlib.pyplot as plt
    import numpy as np
    print("Plotting sampled data.")
    def getX(x):
        return np.linspace(1, len(x), len(x)) * interval
    plt.figure(num=1, figsize=(10,5))
    plt.plot(getX(cpu), cpu)
    plt.xlabel("time(s)")
    plt.ylabel("cpu(%)")
    cpu_file = "cpu.png"
    plt.savefig(cpu_file)
    print("CPU plot figure save to: {}".format(cpu_file))
    plt.figure(num=2, figsize=(10,5))
    plt.plot(getX(memory), memory)
    plt.xlabel("time(s)")
    plt.ylabel("memory(MB)")
    mem_file = "memory.png"
    plt.savefig("memory.png")
    print("Memory plot figure save to: {}".format(mem_file))
    if show:
        plt.show()
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--pid', 
                        type=str, 
                        default=None, 
                        help='PID of the process')
    parser.add_argument('--interval', 
                        type=float, 
                        default=5, 
                        help='Interval of sampling')
    parser.add_argument('--samples', 
                        type=int, 
                        default=None, 
                        help='Sample times')
    parser.add_argument('--plot',
                        action="store_true", 
                        help='should plot')
    parser.add_argument('--show',
                        action="store_true", 
                        help='should show')
    parser.add_argument('--keyword', 
                        type=str, 
                        default=None, 
                        help='keyword of the process.')

    args = parser.parse_args()
    if args.pid is None and args.keyword is None:
        parser.print_help()
        exit(0)
    elif args.pid is not None:
        pid = args.pid
    elif args.keyword is not None:
        pid = findPIDByKeyword(args.keyword)
    buffer = cpu_memory_monitor(pid=pid,
                                interval=args.interval, # seconds
                                samples=args.samples)
    if args.plot:
        monPlot(*buffer, args.interval, args.show)
        