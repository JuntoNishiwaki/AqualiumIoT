import subprocess
from subprocess import Popen 
from time import sleep

cmd1 = "python ebi-countor_tmp.py"
cmd2 = "python fig_make.py"
cmd3 = "python data_log_tmp.py"

if __name__ == "__main__":
    print "START EBI COUNT"

    run1 =Popen(cmd1, shell=True)
    sleep(1)
    print "START FIG MAKE"

    run2 = Popen(cmd2, shell=True)
    sleep(1)
    print "START DATA LOG"

    run3= Popen(cmd3,shell=True)
    run3.wait()
    sleep(1)
    run1.kill()
    run2.kill()
    run3,kill()

    print "Restart"
    

