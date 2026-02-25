from pydantic import BaseModel, EmailStr, Field, constr


class LoginRequest(BaseModel):
    username: constr(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_.-]+$") = Field(...)
    password: constr(min_length=6, max_length=128) = Field(...)


class SearchRequest(BaseModel):
    query: constr(min_length=1, max_length=64) = Field(...)
    limit: int = Field(default=10, ge=1, le=50)


class FeedbackRequest(BaseModel):
    email: EmailStr = Field(...)
    feedback: constr(min_length=1, max_length=500) = Field(...)