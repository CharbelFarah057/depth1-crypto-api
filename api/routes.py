from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import Any, Dict
from providers import get_codec, get_signer
from my_codecs.codecs import Codec
from my_signers.signers import Signer

router = APIRouter()


class VerifyRequest(BaseModel):
    signature: str
    data: Any


@router.post("/encrypt")
def encrypt(
    payload: Dict[str, Any] = Body(...), codec: Codec = Depends(get_codec)
) -> Dict[str, Any]:
    return codec.encrypt(payload)


@router.post("/decrypt")
def decrypt(
    payload: Dict[str, Any] = Body(...), codec: Codec = Depends(get_codec)
) -> Dict[str, Any]:
    return codec.decrypt(payload)


@router.post("/sign")
def sign(
    payload: Dict[str, Any] = Body(...), signer: Signer = Depends(get_signer)
) -> Dict[str, str]:
    return {"signature": signer.sign(payload)}


@router.post("/verify", status_code=204)
def verify(req: VerifyRequest, signer: Signer = Depends(get_signer)):
    if not signer.verify(req.signature, req.data):
        raise HTTPException(status_code=400, detail="Invalid signature")
