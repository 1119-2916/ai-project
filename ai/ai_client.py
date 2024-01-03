from abc import ABCMeta, abstractmethod

class AIClient(metaclass=ABCMeta):
    @property
    @abstractmethod
    def bot_id(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def generate_reply(self, message: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def generate_reply_to_including_URL(self, message: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def generate_reply_to_including_image(self, message: str) -> str:
        raise NotImplementedError()
