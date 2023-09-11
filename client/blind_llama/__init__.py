import os

__all__ = []

try:
    from . import completion
    from .completion import Client, create

    api_key = os.getenv("BLIND_LLAMA_API_KEY", "")
    api_base = "137.116.212.25"
    security_config = {
        "description": "Base config of BlindLlama",
        "expected_pcrs":
        {
            "codebasepcr": "a52bdc8b0fde6ba40ce06532a303e035d55baaf5e657d225093d54b6e05433bc",
            "tpmcert_pcr": "306f9d8b94f17d93dc6e7cf8f5c79d652eb4c6c4d13de2dddc24af416e13ecaf"
        },
        "source_binary": "ghcr.io/mithril-security/text-generation-inference:sha256-5c5f1fbaae44e760fe46c792d8bff31d52cd572c6ade394617f7867b7400cd2d.att",
        "source_code": "https://github.com/mithril-security/text-generation-inference",
        "audit_certificates":
        {
            ""
        }
    }

    __all__ += ["completion", "Client", "create", "api_base", "api_key", "security_config"]

except ImportError as e:
    print(e)
    pass
