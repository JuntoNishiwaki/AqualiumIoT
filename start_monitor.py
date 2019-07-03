import subprocess
from subprocess import Popen
from time import sleep

cmd1 = "python ebi-countor.py"
cmd2 = "python fig-make.py"
cmd3 = "python data_log_tmp.py"

while True:
    try:
        print "Start Monitor"
        proc1 = Popen(cmd1, shell=True)
        proc2 = Popen(cmd2, shell=True)
        proc3 = Popen(cmd3, shell=True)
        popen.wait()
    except:
        print "Retry"


