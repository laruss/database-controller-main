from pydantic_mongo import PydanticMongoModel as PmModel

"""
    Base model for all models in app.
    All models must inherit from this class.
    
    Fields in this class are common for all models 
    and will be used as default fields to return in BC.get_all() method along with id field from PydanticMongoModel.
    
    By defautl:
        - `id` (from PydanticMongoModel)
        - `name` (str)
"""


class BaseAppModel(PmModel):
    name: str
