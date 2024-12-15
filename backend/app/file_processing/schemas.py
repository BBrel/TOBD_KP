from typing import List

from pydantic import BaseModel


class SaveRequest(BaseModel):
    data: List[dict]
