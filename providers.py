from functools import lru_cache
from my_codecs.codecs import Base64Codec, Codec
from my_signers.signers import HMAC, Signer
from settings import settings


@lru_cache
def get_codec() -> Codec:
    # For now, always return Base64; could swap easily
    return Base64Codec()


@lru_cache
def get_signer() -> Signer:
    return HMAC(settings.SIGNER_KEY)
