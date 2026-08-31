# RC1 Firmware Work Area

The Python RC1 module is a behavior emulator only. Production firmware requires:

- selected MCU, secure element and threat model;
- immutable/root boot stage and signed update chain;
- anti-rollback and protected monotonic counter;
- authenticated narrow host protocol;
- hardware safe-state defaults;
- watchdog, brownout and thermal/power interlocks;
- debug lifecycle and factory-test authorization;
- key injection/provisioning ceremony and audit records;
- fuzzing, fault injection, recovery and negative tests;
- independent execution receipt generation.
