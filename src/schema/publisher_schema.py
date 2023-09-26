from pydantic import BaseModel


class PublisherBase(BaseModel):
    id: int
    name: str


class PublisherModel(PublisherBase):
    pass
