import json
from pydantic import ValidationError
from schemas.llm_schema import SearchResponse, ExpandedQueryResponse, ResultItem
from logger import logger
from clients.gemini_client import get_gemini_model_name
import re

MAX_RETRIES = 3

def clean_json_fence(raw_text: str) -> str:
    """
    Strip ```json ... ``` or ``` ... ``` fences from Gemini response.
    """
    
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_text.strip()


def validate_and_retry_llm_output(model, query: str) -> SearchResponse:
    """Validates LLM JSON output against Pydantic schema with retries."""
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Tring to generate response for query: {query}")
            response = model.generate_content(model=get_gemini_model_name(), contents=query)
            
            raw_text = clean_json_fence(response.text)
            print(f"****** RAW TEXT: {raw_text}")
            parsed = json.loads(raw_text)
            if isinstance(parsed, str):
                logger.warning(f"Error occurred: {parsed}")
                raise ValueError(f"Expected List got type {type(parsed)}")
            
            validated = SearchResponse(results=[ResultItem(**item) for item in parsed])
            print(f"**** VALIDATED: ****** \n {validated}")
            logger.info(f"Validated LLM response: {validated}")
            return validated
        except (ValidationError, json.JSONDecodeError) as e:
            logger.warning(f"Validation failed (attempt {attempt + 1}): {e}")
            continue

    raise ValueError("LLM response validation failed after retries")

def validate_and_retry_exapanded_search_output(model, query: str) -> ExpandedQueryResponse:
    """Validates LLM JSON output against Pydantic schema with retries."""
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Tring to generate response for query: {query}")
            response = model.generate_content(model=get_gemini_model_name(), contents=query)
            
            raw_text = clean_json_fence(response.text)
            print(f"****** RAW TEXT: {raw_text}")
            parsed = json.loads(raw_text)
            validated = ExpandedQueryResponse(**parsed)
            logger.info(f"Validated LLM response: {validated}")
            return validated
        
        except (ValidationError, json.JSONDecodeError) as e:
            logger.warning(f"Validation failed (attempt {attempt + 1}): {e}")
            continue

    raise ValueError("LLM response validation failed after retries")
