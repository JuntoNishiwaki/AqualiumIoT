import sys
import subprocess

#Constant
SENSOR_ID = "28-0213134f0faa"
SENSOR_W1_SLAVE = "/sys/bus/w1/devices/" + SENSOR_ID + "/w1_slave"

def main():
    res = get_water_temp()
    if res is not None:
        wtemp = res.split("=")
        wtemp = round(float(wtemp[-1]) / 1000, 1)
        return wtemp
    else:
        print "cannot read the value."
        sys.exit(1)

def get_water_temp():
  try:
    res = subprocess.check_output(["cat", SENSOR_W1_SLAVE])
    return res
  except:
    return None

if __name__ == "__main__":
  main()