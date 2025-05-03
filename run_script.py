import argparse
import time
import os
import subprocess

import m5
from m5.objects import Root

import argparse

from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.boards.arm_board import ArmBoard 
from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import MESITwoLevelCacheHierarchy
from gem5.components.cachehierarchies.ruby.mesi_three_level_cache_hierarchy import MESIThreeLevelCacheHierarchy
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

isa_choices = [
    "X86",
    "ARM",
    "RISCV",
]

cpu_choices = [
    "TIMING",
    "MINOR",
    "O3",
]

workload_choices = [
    "boot-exit",
    "blackscholes",
    "dedup",
    "fluidanimate",
]

parser = argparse.ArgumentParser()

parser.add_argument(
    "--isa",
    type=str,
    required=True,
    choices=isa_choices,
)

parser.add_argument(
    "--cpu",
    type=str,
    required=True,
    choices=cpu_choices,
)

parser.add_argument(
    "--mem",
    type=str,
    required=True,
)

parser.add_argument(
    "--cache",
    type=str,
    required=True,
)

parser.add_argument(
    "--cores",
    type=int,
    required=True,
)

parser.add_argument(
    "--workload",
    type=str,
    required=True,
    choices=workload_choices,
)

args = parser.parse_args()

sizes = args.cache.split(":")

if (len(sizes) == 2):
    cache_hierarchy = MESITwoLevelCacheHierarchy(
        l1d_size=sizes[0],
        l1d_assoc=8,
        l1i_size=sizes[0],
        l1i_assoc=8,
        l2_size=sizes[1],
        l2_assoc=16,
        num_l2_banks=2,
    )
elif (len(sizes) == 3):
    cache_hierarchy = MESIThreeLevelCacheHierarchy(
        l1d_size=sizes[0],
        l1d_assoc=8,
        l1i_size=sizes[0],
        l1i_assoc=8,
        l2_size=sizes[1],
        l2_assoc=12,
        l3_size=sizes[2],
        l3_assoc=16,
        num_l3_banks=2,
    )
else:
    print("error in cache description")
    exit(1)

    
# Note: X86 board only supports 3 GiB of main memory.
memory = DualChannelDDR4_2400(size=args.mem)


if (args.workload == "boot-exit"):
    print("test1")
    processor = SimpleProcessor(
        cpu_type=CPUTypes[args.cpu],
        isa=ISA[args.isa],
        num_cores=args.cores,
    )

    if (args.isa == "X86"):
        board = X86Board(
            clk_freq="3GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy
        )
        workload = obtain_resource("x86-ubuntu-24.04-boot-no-systemd")
        board.set_workload(workload)
    elif (args.isa == "RISCV"):
        board = RiscvBoard(
            clk_freq="3GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )
        workload = obtain_resource("riscv-ubuntu-24.04-boot-no-systemd")
        board.set_workload(workload)
    elif (args.isa == "ARM"):
        board = ArmBoard(
            clk_freq="3GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy
        )
        workload = obtain_resource("arm-ubuntu-24.04-boot-no-systemd")
        board.set_workload(workload)
    else:
        print("error in isa description")
        exit(1)
    def exit_event_handler():
        print("first exit event: kernel booted")
        print(time.strftime("%Y-%m-%d-%H-%M-%S"))
        print("ps: ")
        s = "ps -o pid,psr,comm -p " + str(os.getpid())
        result = subprocess.run(s, shell=True, capture_output=True, text=True)
    
        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)

        s = "cat /proc/" + str(os.getpid()) + "/status"
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)

        yield False
        print("second exit event: in after boot")
        print(time.strftime("%Y-%m-%d-%H-%M-%S"))
        print("ps: ")
        s = "ps -o pid,psr,comm -p " + str(os.getpid())
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)

        s = "cat /proc/" + str(os.getpid()) + "/status"
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)
            
        yield False
        print("third exit event: after run script")
        print(time.strftime("%Y-%m-%d-%H-%M-%S"))
        print("ps: ")
        s = "ps -o pid,psr,comm -p " + str(os.getpid())
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)

        s = "cat /proc/" + str(os.getpid()) + "/status"
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)
            
        yield True

    simulator = Simulator(
        board = board,
        on_exit_event = {
            ExitEvent.EXIT: exit_event_handler(),
        },
    )
else:
    print("test2")

    processor = SimpleSwitchableProcessor(
        starting_core_type=CPUTypes.KVM,
        switch_core_type=CPUTypes[args.cpu],
        isa=ISA[args.isa],
        num_cores=args.cores,
    )


    command = (
        f"cd /home/gem5/parsec-benchmark;"
        + "source env.sh;"
        + f"parsecmgmt -a run -p {args.workload} -c gcc-hooks -i simsmall         -n {args.cores};"
        + "sleep 5;"
        + "m5 exit;"
    )
    board = X86Board(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy
    )
    board.set_kernel_disk_workload(
        kernel=obtain_resource(
            "x86-linux-kernel-4.19.83", resource_version="1.0.0"
        ),
        disk_image=obtain_resource("x86-parsec", resource_version="1.0.0"),
        readfile_contents=command,
    )
    def handle_workbegin():
        print("Done booting Linux")
        processor.switch()
        print(time.strftime("%Y-%m-%d-%H-%M-%S"))
        print("ps: ")
        s = "ps -o pid,psr,comm -p " + str(os.getpid())
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)
        yield False

    def handle_workend():
        print("end of benchmark, stat dump")
        m5.stats.dump()
        print()
        print(time.strftime("%Y-%m-%d-%H-%M-%S"))
        print("ps: ")
        s = "ps -o pid,psr,comm -p " + str(os.getpid())
        result = subprocess.run(s, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("success")
            print(result.stdout)
        else:
            print("error executing command")
            print(result.stderr)
            exit(1)
        yield True

    simulator = Simulator(
        board=board,
        on_exit_event={
            ExitEvent.WORKBEGIN: handle_workbegin(),
            ExitEvent.WORKEND: handle_workend(),
        },
    )
    
simulator.run()
