#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2021 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst.
    ("clk100", 0, Pins("AA10"), IOStandard("LVCMOS15")),

    # Serial.
    ("serial", 0,
        Subsignal("tx", Pins("D15")),
        Subsignal("rx", Pins("C18")),
        IOStandard("LVCMOS33")
    ),

    # DDR3 SDRAM.
    ("ddram", 0,
        Subsignal("a",       Pins(
            "AC8 AA7 AA8 AF7 AE7 AC11 V9 Y10",
            "AB11 Y7  Y8 V11  V8  W11 Y11 V7 "),
            IOStandard("SSTL15")),
        Subsignal("ba",      Pins("AC7 AB7 AB9"), IOStandard("SSTL15")),
        Subsignal("ras_n",   Pins("AA9"), IOStandard("SSTL15")),
        Subsignal("cas_n",   Pins("AD8"), IOStandard("SSTL15")),
        Subsignal("we_n",    Pins("AC9"), IOStandard("SSTL15")),
        Subsignal("cs_n",    Pins("AD9"), IOStandard("SSTL15")),
        Subsignal("dm",      Pins(
            "U6 Y3 AB6 AD4"),
            IOStandard("SSTL15")),
        Subsignal("dq",      Pins(
            " V4  W3  U5  U1  U7  U2  V6  V3",
            " Y2  Y1 AA3  V2 AC2  W1 AB2  V1",
            "AA4 AB4 AC4 AC3 AC6  Y6  Y5 AD6",
            "AD1 AE1 AE3 AE2 AE6 AE5 AF3 AF2"),
            IOStandard("SSTL15_T_DCI")),
        Subsignal("dqs_p",   Pins("W6 AB1 AA5 AF5"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n",   Pins("W5 AC1 AB5 AF4"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p",   Pins("W10"),  IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n",   Pins("W9"),   IOStandard("DIFF_SSTL15")),
        Subsignal("cke",     Pins("AB12"), IOStandard("SSTL15")),
        Subsignal("odt",     Pins("AC12"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("AA2"),  IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
        Misc("VCCAUX_IO=HIGH")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = []

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7k325t-ffg676-2", _io, _connectors, toolchain="vivado")

    def create_programmer(self):
        return OpenOCD("openocd_xc7_ft2232.cfg", "bscan_spi_xc7a325t.bit")

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk100", loose=True), 1e9/100e6)
        self.add_platform_command("set_property INTERNAL_VREF 0.750 [get_iobanks 33]")
        self.add_platform_command("set_property INTERNAL_VREF 0.750 [get_iobanks 34]")
