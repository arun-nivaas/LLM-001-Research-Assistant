from pydantic import BaseModel

class ProcessPDFRequest(BaseModel):
    s3_key: str
    api_key: str 
    
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    context: str

