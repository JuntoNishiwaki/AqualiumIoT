import subprocess
from time import sleep

cmd1 = "ebi-countor.py"
cmd2 = "fig_make.py"
cmd3 = "data_log_tmp.py"

if __name__ == "__main__":
    print "START EBI COUNT"
    run1 = subprocess.call(["python",cmd1])
    time.sleep(1)
    print "START FIG MAKE"
    run2 = subprocess.call(["python",cmd2])
    time.sleep(1)
    print "START DATA LOG"
    run3= subprocess.check_call(["python",cmd3])
    time.sleep(1)
    print "End monitoring"