from .ai_client import AIClient
from .kurobara_ai import KurobaraAI
from .ikeda_ai import IkedaAI


def get_ai_client(client_name) -> AIClient:
    if client_name == "kurobara":
        return KurobaraAI()
    elif client_name == "ikeda":
        return IkedaAI()
    else:
        raise ValueError(f"Invalid client name: {client_name}")
