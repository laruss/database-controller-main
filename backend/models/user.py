from pydantic_mongo import PydanticMongoModel


class User(PydanticMongoModel):
    name: str
    username: str
