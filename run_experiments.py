import sys
import time
import subprocess
import os

if (len(sys.argv) != 2):
    print("error: need one file name as command line arg")
    exit(1)
    
with open(sys.argv[1], "r") as f:
    contents = f.read()
    f.close()

tests = contents.split("\n")

for test in tests:

    args = test.split(" ")
    
    s = "taskset -c 6,36,38 perf stat -M  "
    s += args[6]
    
    s += " /home/mcallisl/gem5/build/ALL/gem5.opt /home/mcallisl/config_scripts/run_script.py"
        
    s += " --isa " + args[0]
    s += " --cpu " + args[1]
    s += " --mem " + args[2]
    s += " --cache " + args[3]
    s += " --cores " + args[4]
    s += " --workload " + args[5]
    
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
    s += " &> "
    d = "/home/mcallisl/config_scripts/output_files/"
    for tmp in args:
        d += tmp + "-"

    d = d[:-1]
    s += d + "/" + timestr

    print(s)
    print(d)
    if not os.path.exists(d):
        os.makedirs(d)
        print(os.path.exists(d))
    
    result = subprocess.run(s, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("success")
        print(result.stdout)
    else:
        print("error executing command")
        print(result.stderr)
        exit(1)
    
    time.sleep(300)

    
    cleanup = subprocess.run("sudo -S sh -c 'echo 3 > /proc/sys/vm/drop_caches'", shell=True, capture_output=True, text=True, input="hfsdfgjghfe")

    if cleanup.returncode == 0:
        print("success")
        print(cleanup.stdout)
    else:
        print("error executing cleanup")
        print(cleanup.stderr)
        exit(1)
    
    
