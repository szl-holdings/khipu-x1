# FPGA / RTL Work Area

Status: **UNAVAILABLE — target platform not selected.**

Do not add vendor-generated binary blobs as if they were source. When the target
is selected, pin:

- FPGA/SOM exact part and board revision;
- toolchain name/version/license requirements;
- IP-core versions and licenses;
- constraints;
- clock/reset assumptions;
- memory map and host interface;
- synthesis/implementation commands;
- reproducibility limitations;
- bitstream digest and build receipt.

First RTL slice: descriptor queue, status registers, monotonic counter,
DMA loopback, INT8 tile, RMSNorm, SHA3 commitment engine and interrupt.
