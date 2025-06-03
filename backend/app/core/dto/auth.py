from .config import Model


class Tokens(Model):
    access: str
    refresh: str


class Token(Model):
    token: str
    type: str = "bearer"
