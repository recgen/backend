class InfrastructureError(Exception): ...


class LLMError(InfrastructureError):
    def __init__(self, reason: str, *args: object) -> None:
        super().__init__(*args)
        self.reason = reason
