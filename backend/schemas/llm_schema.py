from pydantic import BaseModel
from typing import Optional, List


class SearchRequest(BaseModel):
    query: str
    file_path: Optional[str] = None 


class ResultItem(BaseModel):
    concept_name: str
    location: str
    value_formula: Optional[str] = None
    formula: Optional[str] = None
    relevance: float
    explanation: str
    business_context: str
    cell_location: str
    sheet_name: str
    formula_type: str

class ExpandedQueryResponse(BaseModel):
    expanded_query: str
    concepts: List[str]
    metrics: List[str]
    formulas: List[str]


class SearchResponse(BaseModel):
    results: List[ResultItem]
    error: Optional[str] = None
