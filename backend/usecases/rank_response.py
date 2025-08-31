from schemas.llm_schema import ResultItem
from typing import List

def flatten_results(nested_results: List[List[ResultItem]]) -> List[ResultItem]:
    """
    Flatten list of lists of dicts into a single list of dicts.
    """
    return [item for sublist in nested_results for item in sublist]

def sort_by_relevance(response: List[List[ResultItem]])-> List[ResultItem]:
    flattened_results = flatten_results(response)
    
    return sorted(flattened_results, key=lambda x: x.relevance if x.relevance else 0, reverse=True)