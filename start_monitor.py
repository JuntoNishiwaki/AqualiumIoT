import subprocess
from subprocess import Popen
import threading
from time import sleep

cmd1 = "python ebi-countor.py"
cmd2 = "python fig_make.py"
cmd3 = "python data_log_tmp.py"

def func1():
        print ("Ebi coountor")
        proc1 = Popen(cmd1, shell=True)
        popen.wait()

def func2():
        print ("Fig make")
        proc1 = Popen(cmd2, shell=True)
        popen.wait()

def func3():
        print ("Data log")
        proc1 = Popen(cmd2, shell=True)
        popen.wait()

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)
    thread_3 = threading.Thread(target=func3)
    
    thread_1.start()
    thread_2.start()
    thread_3.start()