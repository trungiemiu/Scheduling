from typing import List, Tuple, Dict, Optional

class Machine:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.schedule: List[Tuple[float, float, int]] = []
        self.operations: List[Tuple[str, float, float]] = []

    def next_available_time(self) -> float:
        return self.schedule[-1][1] if self.schedule else 0.0

    def can_allocate(self, tools_needed: int, start_time: float, duration: float) -> bool:
        if tools_needed is None:
            return False
        end_time = start_time + duration
        current = 0
        for (s, e, t) in self.schedule:
            if not (end_time <= s or start_time >= e):
                current += t
        return (current + tools_needed) <= self.capacity

    def allocate(self, tools_needed: int, start_time: float, duration: float) -> bool:
        if self.can_allocate(tools_needed, start_time, duration):
            self.schedule.append((start_time, start_time + duration, tools_needed))
            self.schedule.sort()
            return True
        return False

    def add_operation_bar(self, fullname: str, start_time: float, end_time: float) -> None:
        self.operations.append((fullname, start_time, end_time))

    def clear(self) -> None:
        self.schedule.clear()
        self.operations.clear()


class Operation:
    def __init__(self, job_name: str, operation_id: int, time_required: float,
                 tool_requirements: Dict[str, int], setup_time: float = 0.0):
        self.job_name = job_name
        self.operation_id = int(operation_id)
        self.time_required = float(time_required)
        self.tool_requirements = dict(tool_requirements)
        self.setup_time = float(setup_time)


class Job:
    def __init__(self, job_name: str, operations: List[Operation]):
        self.job_name = job_name
        self.operations = sorted(operations, key=lambda o: o.operation_id)

    def get_operation(self, idx: int) -> Optional[Operation]:
        return self.operations[idx] if 0 <= idx < len(self.operations) else None
