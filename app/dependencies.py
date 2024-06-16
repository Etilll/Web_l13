from fastapi import Header, HTTPException
from typing import Annotated
async def get_token_header(x_token: Annotated[str,Header()]):
    if x_token != "token":
        raise HTTPException(status_code=400, detail="X-token invalid")