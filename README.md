# Nebra WebOS

This project is a operating system simulation which lets user interact with the simulated OS from their browser. The goal of this project to learn about the fundamental workings of an operating system and simulate it using python.
The os simulation engine is wrapped inside fastapi framework which connects to the Next.js frontend for the users to interact.

1. CPU & Instruction Set Architecture (ISA)
A minimal CPU class with registers, a program counter, and status flags (zero, negative, carry, overflow).
A small custom instruction set (Opcode): ADD, SUBTRACT, JMP (unconditional jump), JZ (jump-if-zero), HALT.
Opcode handlers (opcode_handlers.py) that execute each instruction and update CPU flags/registers accordingly.
A Process abstraction with saved register values, program counter, instruction list, and process state.
Basic execution flow verified with a unit test (ADD then HALT correctly updates registers and terminates the process).

3. Scheduling & Kernel
A Scheduler with a ready queue (deque) and a waiting-process table, supporting enqueue_ready, get_next_ready, add_waiting, and mark_ready (round-robin-style readiness handling).
A minimal Kernel that boots by initializing the scheduler and creating the first process (systemd, PID 1).
Scheduler behavior covered by unit tests (ready/waiting transitions, ordering).

5. Memory Management
RAM: a simple byte-addressable memory model (1 MB by default) with bounds-checked read/write.
PTE (Page Table Entry): a compact 3-byte (24-bit) entry encoding a 20-bit physical page number plus present, read/write, and user/kernel protection flags, with multiple construction paths (from raw bytes, from individual fields, or from a packed data block).
MMU (Memory Management Unit): translates virtual addresses to physical addresses via the page table and enforces protection (rejects writes to read-only pages, rejects user-mode access to kernel-only pages, raising page-fault-style exceptions).
MemoryRequest: the abstraction the CPU will use to issue memory reads/writes, tying together the MMU, RAM, and CPU (address/data bus behavior is simplified for now — methods are called directly rather than simulating an actual bus).
Address translation, permission enforcement, and read/write correctness are covered by unit tests, including page-fault scenarios.
