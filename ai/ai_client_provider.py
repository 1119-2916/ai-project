from .ai_client import AIClient
from .kurobara_ai import KurobaraAI
from .ikeda_ai import IkedaAI
from .meu_ai import MeuAI
from .shapa_ai import ShapaAI


def get_ai_client(client_name) -> AIClient:
    if client_name == "kurobara":
        return KurobaraAI()
    elif client_name == "ikeda":
        return IkedaAI()
    elif client_name == "shapa":
        return ShapaAI()
    elif client_name == "meu":
        return MeuAI()
    else:
        raise ValueError(f"Invalid client name: {client_name}")
