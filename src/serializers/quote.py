from pydantic import BaseModel, Field


class Quote(BaseModel):
    id: str = Field(alias="_id")
    date_added: str = Field(alias="dateAdded")
    date_modified: str = Field(alias="dateModified")
    author_slug: str = Field(alias="authorSlug")
    content: str
    author: str
    tags: list
    length: int
