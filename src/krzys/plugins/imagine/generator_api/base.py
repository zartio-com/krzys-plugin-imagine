

class BaseGeneratorApi:
    @staticmethod
    def queue_prompt(positive_prompt: str, negative_prompt: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def is_ready(prompt_id: str) -> bool:
        raise NotImplementedError()

    @staticmethod
    def get_result(prompt_id: str) -> list[bytes]:
        raise NotImplementedError()
