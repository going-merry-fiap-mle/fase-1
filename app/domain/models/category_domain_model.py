import uuid


class Category:
    def __init__(self, name: str, id: uuid.UUID | None = None) -> None:
        self.id = id if id is not None else uuid.uuid4()
        self.name = name
