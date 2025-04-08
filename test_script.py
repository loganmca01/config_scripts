import argparse
import time

import m5
from m5.objects import Root

import argparse

from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import (
    SimpleProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

# We check for the required gem5 build.

requires(
    isa_required=ISA.X86,
    #coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    coherence_protocol_required=CoherenceProtocol.MESI_THREE_LEVEL,
)

'''
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
 
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=2,
)
'''

from gem5.components.cachehierarchies.ruby.mesi_three_level_cache_hierarchy import (
    MESIThreeLevelCacheHierarchy,
)

cache_hierarchy = MESIThreeLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=12,
    l3_size="512KiB",
    l3_assoc=16,
    num_l3_banks=2,
)

# Memory: Dual Channel DDR4 2400 DRAM device.
# The X86 board only supports 3 GiB of main memory.

memory = DualChannelDDR4_2400(size="1GiB")


processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=4
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

#workload = obtain_resource("x86-ubuntu-24.04-boot-with-systemd")
#board.set_workload(workload)

board.set_kernel_disk_workload(
    
)

def exit_event_handler():
    print("first exit event: kernel booted")
    yield false
    print("second exit event: in after boot")
    yield false
    print("third exit event: after run script")
    yield true
    
simulator = Simulator(
    board = board,
    on_exit_event = {
        ExitEvent.EXIT: exit_event_handler(),
    },
)

simulator.run(10_000_000_000)