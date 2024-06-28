from pydantic import BaseModel


class TokenFormSchema(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {"example": {"username": "arthur.dent", "password": "Secret42"}}


class TokenDetailSchema(BaseModel):
    access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhcnRodXIuZGVudCIsImV4cCI6MTcyMDExNzgzNn0.olJNjGmfjSTtZC2oQa_whCapKhOt0SOLHD89dvpj4wo",
            }
        }
