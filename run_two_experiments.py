import sys
import time
import subprocess
import os

with open(sys.argv[1], "r") as f:
    contents = f.read()
    f.close()

tests = contents.split("\n")

if (tests[len(tests) - 1] == ""):
    tests = tests[:-1]

num_trials = len(tests)
    
s = ""

current_trial = 0

for test in tests:

    current_trial += 1
    
    args = test.split(" ")

    if ((current_trial % 2) == 1):
        s += "taskset -c 1-9,21-29 perf stat -M "
    else:
        s += "taskset -c 11-19,31-39 perf stat -M "
    s += args[6]
    
    s += " /home/mcallisl/gem5/build/ALL/gem5.opt /home/mcallisl/config_scripts/run_script.py"
        
    s += " --isa " + args[0]
    s += " --cpu " + args[1]
    s += " --mem " + args[2]
    s += " --cache " + args[3]
    s += " --cores " + args[4]
    s += " --workload " + args[5]
    
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")

    time.sleep(2) # make sure experiments don't have same timestamp
    
    s += " &> "
    d = "/home/mcallisl/config_scripts/output_files/"
    for tmp in args:
        d += tmp + "-"

    d = d[:-1]
    s += d + "/" + timestr

    s += " & "

    print()
    print(s)
    print(d)
    print()
    if not os.path.exists(d):
        os.makedirs(d)
        print(os.path.exists(d))

    print(current_trial)
    print(current_trial % 2)
        
    if ((current_trial % 2) == 1 and current_trial != num_trials):
        print("test continue")
        continue
        
    s += "wait"

    print()
    print("test finish")
    print()
    print(s)
    print()

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


    s = ""
