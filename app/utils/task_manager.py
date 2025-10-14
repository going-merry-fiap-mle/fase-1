import threading
import uuid


class TaskStatus:
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


class TaskManager:

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tasks: dict[str, dict[str, str | None]] = {}

    def create_task(self) -> str:
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = {"status": TaskStatus.PENDING, "message": None}
        return task_id

    def set_status(self, task_id: str, status: str, message: str | None = None) -> None:
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]["status"] = status
                self._tasks[task_id]["message"] = message

    def get_task(self, task_id: str) -> dict[str, str | None] | None:
        with self._lock:
            return self._tasks.get(task_id)


default_task_manager = TaskManager()
