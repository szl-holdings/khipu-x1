# KHIPU Driver Boundary

Status: **DESIGN ONLY**.

The production Linux boundary should provide:

- device discovery and exact identity;
- bitstream/firmware attestation readback;
- IOMMU-aware DMA buffers;
- descriptor/completion queues;
- interrupts or polled completion;
- reset, abort, timeout and health reporting;
- zeroization and process isolation;
- stable userspace ABI with compatibility negotiation;
- tracepoints and measured telemetry;
- robust malformed-input and fault handling.

No kernel module should be written until the host interface and target FPGA are
selected. Start with an emulator transport and a userspace VFIO/UIO path only if
its security limitations are explicitly accepted.
