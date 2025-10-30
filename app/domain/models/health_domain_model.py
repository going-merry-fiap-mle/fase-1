class Health:
    def __init__(self, status: str, message: str, data_connectivity: bool) -> None:
        self.status = status
        self.message = message
        self.data_connectivity = data_connectivity
