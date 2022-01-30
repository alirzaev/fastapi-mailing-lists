from pydantic import BaseModel
from pydantic.types import constr


class EmailContent(BaseModel):
    subject: constr(max_length=80)

    content: str
