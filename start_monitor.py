import subprocess
from subprocess import Popen 
from time import sleep

cmd1 = "python ebi-countor.py"
cmd2 = "python fig_make.py"
cmd3 = "python data_log_tmp.py"

if __name__ == "__main__":
    print "START EBI COUNT"
    run1 =Popen(cmd1, shell=True)
    time.sleep(1)
    print "START FIG MAKE"
    run2 = Popen(cmd2, shell=True)
    time.sleep(1)
    print "START DATA LOG"
    run3= Popen(cmd2,shell=True)
    Popen.wait()
    time.sleep(1)
    print "End monitoring"