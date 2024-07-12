from bson import ObjectId
from pydantic import BaseModel, Field
from uuid import uuid4

class AsyncBaseModel(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        populate_by_name = True

    @classmethod
    async def model_validate(cls, obj):
        return cls(**obj)
    
class IdBase(AsyncBaseModel):
    id: str = Field(
        ...,
        alias="id",
        title="ID",
        default_factory=lambda: str(uuid4()),
        extra="ignore",
    )

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")