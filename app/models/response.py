from typing import Union
from pydantic import BaseModel


class BaseRespondModel(BaseModel):
    data: Union[dict, list, None]
    code: Union[int, None]
    message: Union[str, None]
    error: Union[bool, None]