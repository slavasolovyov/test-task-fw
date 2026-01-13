from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "category": {"id": 1, "name": "Dogs"},
                "name": "doggie",
                "photoUrls": ["https://example.com/photo.jpg"],
                "tags": [{"id": 1, "name": "tag1"}],
                "status": "available"
            }
        }
    )
    
    id: Optional[int] = None
    category: Optional[Category] = None
    name: str = Field(..., description="Pet name")
    photoUrls: List[str] = Field(..., description="List of photo URLs")
    tags: Optional[List[Tag]] = None
    status: Optional[str] = Field(None, description="Pet status: available, pending, sold")