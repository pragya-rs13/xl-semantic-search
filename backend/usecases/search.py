
from clients.gemini_client import get_gemini_model
from utils.vaildate_schema import validate_and_retry_exapanded_search_output, validate_and_retry_llm_output
from schemas.llm_schema import SearchRequest, ExpandedQueryResponse
from utils.chunk_util import chunk_jsonl
from usecases.rank_response import sort_by_relevance
from logger import logger


def searchPipeline(request: str, jsonl_document):
    model = get_gemini_model()
    
    # step 1
    expand_query_response = expand_query(request, model)
    print(f"[Search Pipeline] Expanded Query Response: {expand_query_response}")
    
    #step 2
    resp = []
    for chunk in chunk_jsonl(jsonl_path=jsonl_document):
        search_documents_response = search_documents(request=request, 
                                                     model=model, 
                                                     expanded_response=expand_query_response, 
                                                     document_chunk=chunk)
        
        if search_documents_response.error: 
            logger.warn(f"Error encountered in LLM response: {search_documents_response.error}")
        else:
            print(
                f"[Search Pipeline] Chunk response: {search_documents_response.results}"
            )
            resp.append(search_documents_response.results)
        
    response = sort_by_relevance(resp)
        
    return response

def expand_query(request: str, model) -> ExpandedQueryResponse:
    expand_prompt = f"""
    You are a semantic search engine.
    Expand the following query into structured details.

    Input query: "{request}"

    Return ONLY valid JSON in this format:
    {{
      "expanded_query": "expanded query in natural language",
      "concepts": ["concept1", "concept2"],
      "metrics": ["metric1", "metric2"],
      "formulas": ["formula1", "formula2"]
    }}
    """

    validated_response = validate_and_retry_exapanded_search_output(model, expand_prompt)
    
    return validated_response

def search_documents(request: SearchRequest, model, expanded_response: ExpandedQueryResponse, document_chunk):
    search_prompt = f"""
    You are a semantic search engine. You are given a query and a list of documents.
    You need to search the documents for the most relevant information.
    The request is: {request}
    Expanded intent of query: {expanded_response.expanded_query}
    Related concepts to the query: {expanded_response.concepts}
    Metrics related to query: {expanded_response.metrics}
    Formulas related (if found in the data): {expanded_response.formulas}
    Return the most relevant results with meaningful context, not just cell references
    Ranking Factors:
    Semantic Relevance: How closely does content match the concept?
    Context Importance: Is this a key metric or supporting calculation?
    Formula Complexity: More sophisticated calculations might be more relevant
    Data Recency: Recent data might be more important than historical
    Consider Including these in response
    Concept Name: What business concept this represents
    Location: Where it's found (with human-readable context)
    Value/Formula: Current value and/or underlying calculation
    Explanation: Why this matches the user's query
    Business Context: What role this plays in the spreadsheet
    
    The document will be sent in chunks, in multiple prompts,
    make sure to give relevance scores properly so that the result can be collected and sorted accordingly
    
    Here is the document chunk: {document_chunk}

Your response should be in the following format:
 A list of objects with the following fields in:
    - concept_name : str
    - location: str in human readable format
    - value_formula: str
    - formula: str
    - relevance: float - the results will be sorted based on this value in the final response
    - explanation: str
    - business_context: str
    - cell_location: str
    - sheet_name: str
    - formula_type: str

    Example:
    [
    {{
        "concept_name": "Gross Margin (Year 1)",
    "location": "Dashboard Sheet, Cell B5 (Key Metrics section)",
    "value_formula": "0.6",
    "explanation": "This cell directly presents the calculated Gross Margin for Year 1, a fundamental profitability metric. While the formula isn't visible in the provided CSV snippet, its presence as a 'Key Metric' indicates high relevance.",
    "business_context": "Gross Margin is crucial for understanding the profitability of sales after accounting for the cost of goods sold. A 60% gross margin suggests a healthy core business operation.",
    "cell_location": "B5",
    "formula": "Not visible in CSV, but represents Gross Margin calculation",
    "formula_type": "Calculated Metric",
    "relevance": 0.95
    }}]
    
    """
    validated_response = validate_and_retry_llm_output(model=model, query=search_prompt)
    
    return validated_response
