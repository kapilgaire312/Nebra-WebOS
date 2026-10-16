from os_engine.cpu_architecture.isa import Instruction, Opcode
from os_engine.process.model import Process, ProcessState
from os_engine.scheduler import Scheduler


def test_scheduler():
    proc1 = Process(
        process_id=1,
        process_state=ProcessState.RUNNING,
        saved_program_counter_value=0,
        saved_register_values=[0, 5, 3, 0],
        instructions=[
            Instruction(opcode=Opcode.ADD, operands=["R0", "R1", "R2"]),
        ],
    )

    proc2 = Process(
        process_id=2,
        process_state=ProcessState.RUNNING,
        saved_program_counter_value=0,
        saved_register_values=[0, 5, 3, 0],
        instructions=[
            Instruction(opcode=Opcode.ADD, operands=["R0", "R1", "R2"]),
        ],
    )
    proc3 = Process(
        process_id=3,
        process_state=ProcessState.RUNNING,
        saved_program_counter_value=0,
        saved_register_values=[0, 5, 3, 0],
        instructions=[
            Instruction(opcode=Opcode.ADD, operands=["R0", "R1", "R2"]),
        ],
    )

    # start scheduler

    scheduler = Scheduler()

    assert scheduler.get_next_ready() is None

    scheduler.enqueue_ready(proc1)

    scheduler.enqueue_ready(proc2)

    assert scheduler.get_next_ready() == proc1

    scheduler.add_waiting(proc1)

    scheduler.mark_ready(proc1.process_id)
    assert scheduler.get_next_ready() == proc2
    assert scheduler.get_next_ready() == proc1

    scheduler.mark_ready(5)
    assert scheduler.get_next_ready() is None

    scheduler.add_waiting(proc3)
    assert scheduler.waiting_process[3] == proc3
