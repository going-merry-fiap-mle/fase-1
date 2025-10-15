import uuid
from typing import Optional


class Category:
    def __init__(self, name: str, id: Optional[uuid.UUID] = None) -> None:
        self.id = id if id is not None else uuid.uuid4()
        self.name = name
