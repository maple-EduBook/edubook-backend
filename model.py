from pydantic import BaseModel


class GenerateReq(BaseModel):
    post_id: str