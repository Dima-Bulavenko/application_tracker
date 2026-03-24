from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


class OAuthErrorResponse(ErrorResponse):
    error_code: str
    provider: str
