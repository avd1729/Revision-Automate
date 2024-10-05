from typing import List

from pydantic import BaseModel

class Response(BaseModel):
    url : str
    key : List[str]
