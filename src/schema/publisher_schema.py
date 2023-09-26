from pydantic import BaseModel, constr


class PublisherBase(BaseModel):
    name: constr(min_length=3, max_length=200)


class PublisherCreate(PublisherBase):
    pass


class PublisherPut(PublisherBase):
    id: int


class PublisherModel(PublisherBase):
    id: int
