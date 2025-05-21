from pydantic import BaseModel



class CheckKeyResponse(BaseModel):
    ok: bool = False
