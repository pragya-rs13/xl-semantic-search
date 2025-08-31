# Technical Design Document: Semantic Search System

## Executive Summary

This document outlines the technical architecture and implementation details of a semantic search system designed to process Excel files and provide intelligent search capabilities for business formulas and concepts. The system leverages Google Gemini AI for semantic understanding and employs a multi-step pipeline architecture to deliver relevant, context-aware search results.

## 1. System Overview

### 1.1 Architecture Pattern
The system follows a **Multi-Step LLM Pipeline Architecture** (MCP-like) that separates concerns into distinct processing stages, enabling better error handling, logging, and future optimization opportunities.

### 1.2 Technology Stack
- **Backend**: FastAPI (Python 3.11), Uvicorn ASGI server
- **Frontend**: Vanilla HTML/CSS/JavaScript with Vite build tool
- **AI Service**: Google Gemini 2.0 Flash Exp
- **Data Processing**: Pandas, OpenPyXL for Excel handling
- **Infrastructure**: Docker containerization

## 2. Semantic Understanding Approach

### 2.1 Business Domain Knowledge Integration
The system employs **contextual semantic expansion** to bridge the gap between user queries and business terminology:

- **Term Similarity Mapping**: Identifies business logic relationships (e.g., "gross margin" ↔ "profit margin", "quarterly sales" ↔ "revenue in 3 months")
- **Formula Context Understanding**: Recognizes mathematical relationships and business calculations
- **Domain-Specific Vocabulary**: Maps industry-specific terms to their technical equivalents

### 2.2 NLP Processing Strategy
Rather than implementing traditional NLP libraries (scikit-learn, Hugging Face transformers), the system leverages **pre-trained LLM capabilities** for:

- **Query Intent Recognition**: Understanding the underlying business question
- **Semantic Similarity**: Computing relevance scores between queries and content
- **Context Generation**: Creating business-relevant search contexts

## 3. Query Processing and Result Ranking Methodology

### 3.1 Multi-Step Processing Pipeline

#### Step 1: Query Expansion and Context Generation
```python
# Pseudo-code representation
def expand_query_context(user_query):
    prompt = f"""
    Expand this business query: "{user_query}"
    Generate:
    1. Related business terms
    2. Similar formulas
    3. Business concepts
    4. Industry-specific vocabulary
    """
    return llm.generate(prompt)
```

#### Step 2: Corpus-Based Search
- **Expanded Query Processing**: Uses generated context to create search corpus
- **Content Matching**: Searches Excel data using expanded terminology
- **Pattern Recognition**: Identifies formula patterns and business logic

#### Step 3: ML-Based Relevance Scoring
- **LLM Classification**: Leverages Gemini's classification capabilities
- **Multi-Factor Scoring**: Considers formula type, business context, and relevance
- **Confidence Metrics**: Provides explainable relevance scores

#### Step 4: Result Ranking and Explanation
- **Score-Based Sorting**: Results ranked by relevance confidence
- **Contextual Explanations**: Business context and formula explanations
- **Structured Output**: Consistent response format with metadata

### 3.2 Result Ranking Algorithm
```python
# Simplified ranking logic
def rank_results(search_results, query_context):
    for result in search_results:
        # LLM-based relevance scoring
        relevance_score = llm.classify_relevance(
            query=query_context,
            result=result
        )
        
        # Business context scoring
        business_relevance = score_business_context(result)
        
        # Formula complexity scoring
        formula_score = score_formula_complexity(result)
        
        # Combined weighted score
        result.final_score = (
            relevance_score * 0.6 +
            business_relevance * 0.3 +
            formula_score * 0.1
        )
    
    return sorted(search_results, key=lambda x: x.final_score, reverse=True)
```

## 4. Technical Architecture and Data Structures

### 4.1 High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend      │    │   Google Gemini │
│   (HTML/CSS/JS) │◄── │   (FastAPI)      │◄──►│      AI API     │
|       (Input)   |    | (Excel → JSONL)  |    |                 |
|                 |    | (Data Pipleine)  |    |                 |
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 4.2 Backend Architecture Components

#### 4.2.1 API Layer (FastAPI)
- **Health Check Endpoints**: System monitoring and status
- **Search Endpoints**: File upload and search processing
- **Middleware**: CORS, logging, error handling

#### 4.2.2 Business Logic Layer
 Initialize LLM client
 1. Process uploaded File
 2. Generate search context
 3. Perform semantic search
 4. Rank and return results

#### 4.2.3 Data Processing Layer
- **Excel Parser**: Converts Excel files to structured JSONL format
- **CSV Parser**: Converts CSV files to structured JSONL format
- **Schema Validation**: Ensures data integrity and format consistency
- **Chunking Utilities**: Optimizes data for LLM processing

### 4.3 Frontend Architecture

#### 4.3.1 Component Structure
- **Search Interface**: Query input and file attachment
- **Results Display**: Structured result cards with relevance indicators
- **Loading States**: User feedback during processing

#### 4.3.2 Data Flow
```javascript
// Simplified data flow
async function handleSearch() {
    const formData = new FormData();
    formData.append('query', searchQuery);
    formData.append('file', attachedFile);
    
    const response = await fetch('/api/v1/search', {
        method: 'POST',
        body: formData
    });
    
    const results = await response.json();
    displayResults(results);
}
```

## 5. Performance Considerations and Trade-offs

### 5.1 LLM vs. Traditional NLP Decision

#### 5.1.1 Performance Comparison
- **LLM API Response Time**: ~5-6 seconds
- **Traditional NLP (scikit-learn/transformers)**: ~5+ minutes
- **Decision Rationale**: Hardware constraints and development timeline

#### 5.1.2 Trade-offs Analysis
| Aspect            | LLM Approach          | Traditional NLP                |
|-------------------|-----------------------|--------------------------------|
| **Response Time** | Fast (5-6s)           | Slow (5+ min)                  |
| **Accuracy**      | High (pre-trained)    | Variable (depends on training) |
| **Cost**          | Per-request API cost  | Infrastructure costs           |
| **Maintenance**   | Low (managed service) | High (model updates)           |
| **Scalability**   | API rate limits       | Infrastructure dependent       |

### 5.2 Current Performance Optimizations

#### 5.2.1 File Processing
- **JSONL Conversion**: Optimized format for LLM consumption
- **Chunking Strategy**: Efficient data segmentation
- **Schema Validation**: Early error detection

#### 5.2.2 API Response Optimization
- **Async Processing**: Non-blocking request handling
- **Structured Responses**: Consistent data format
- **Error Handling**: Graceful degradation

## 6. Future Optimizations and Scalability

### 6.1 File Processing Optimization

#### 6.1.1 Content-Based Caching
```python
# Proposed caching strategy
class FileCacheManager:
    def __init__(self):
        self.cache = {}
    
    def get_file_hash(self, file_content):
        return hashlib.sha256(file_content).hexdigest()
    
    def get_cached_processing(self, file_hash):
        return self.cache.get(file_hash)
    
    def cache_processing(self, file_hash, processed_data):
        self.cache[file_hash] = processed_data
```

**Benefits:**
- **Duplicate Processing Prevention**: Skip conversion for identical files
- **Memory Efficiency**: Store only unique file representations
- **Response Time Improvement**: Faster results for repeated files

### 6.2 Semantic Context Caching

#### 6.2.1 Vector Database Integration
- **Context Storage**: Cache semantic contexts in vector database
- **Similarity Search**: Fast retrieval of related contexts
- **Reduced LLM Calls**: Minimize API requests for common queries

#### 6.2.2 Memoization Strategy
```python
# Context caching implementation
class ContextCache:
    def __init__(self, vector_db):
        self.vector_db = vector_db
    
    async def get_cached_context(self, query_hash):
        return await self.vector_db.search(query_hash)
    
    async def cache_context(self, query_hash, context):
        await self.vector_db.store(query_hash, context)
```

## 7. Challenges Faced and Solutions Implemented

### 7.1 Technical Challenges

#### 7.1.1 LLM Response Parsing
**Challenge**: Inconsistent response formats from Gemini API
**Solution**: Implemented robust Pydantic schema validation with retry mechanisms

```python
# Schema validation with retries
async def validate_llm_response(response, max_retries=3):
    for attempt in range(max_retries):
        try:
            validated_data = ResponseSchema(**response)
            return validated_data
        except ValidationError as e:
            if attempt == max_retries - 1:
                raise e
            # Retry with refined prompt
            response = await refine_llm_prompt(response, e)
```

#### 7.1.2 File Format Compatibility
**Challenge**: Supporting multiple Excel formats and structures
**Solution**: Implemented flexible file processors with format detection (for csv and xlsx)

#### 7.1.3 Error Handling and Logging
**Challenge**: Debugging LLM interactions and API failures
**Solution**: Comprehensive logging system with input/output tracking

### 7.2 Business Logic Challenges

#### 7.2.1 Semantic Understanding Accuracy
**Challenge**: Ensuring business term recognition across industries
**Solution**: Context-aware prompting and business domain expansion

#### 7.2.2 Result Relevance Scoring
**Challenge**: Balancing multiple relevance factors
**Solution**: Multi-factor scoring with LLM-based classification

## 8. Data Structures and Schemas

### 8.1 Core Data Models

#### 8.1.1 Search Request Schema
```python
class SearchRequest(BaseModel): # is consumed as multipart form data, class is for demo
    query: str
    file: UploadFile
```

#### 8.1.2 Search Result Schema
```python
class ResultItem(BaseModel): #search result
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
```

### 8.2 Excel Data Processing

#### 8.2.1 JSONL Format Structure
```json
{"sheet": "Cost Analysis",
 "row": 3,
  "cells": 
  [{"cell": "A3", "header": "Cost Category", "value": "Rent", "formula": null},
    {"cell": "B3", "header": "Monthly Cost", "value": 3000.0, "formula": null}, 
    {"cell": "C3", "header": "Annual Cost", "value": "=B3*12", "formula": null}]
    }
```

## 9. Monitoring and Observability

### 9.1 Logging Strategy
- **Input Logging**: Track user queries and file uploads
- **Processing Logs**: Monitor LLM API calls and response times
- **Output Logging**: Record result generation and ranking
- **Error Tracking**: Comprehensive error logging with context

### 9.2 Performance Metrics
- **Response Time**: End-to-end search processing time
- **LLM API Latency**: Gemini API response times
- **File Processing Time**: Excel to JSONL conversion duration
- **Cache Hit Rates**: File and context caching effectiveness

## 10. Conclusion

The semantic search system demonstrates a practical approach to leveraging LLM capabilities for business intelligence applications. By implementing a multi-step pipeline architecture, the system achieves:

- **Fast Response Times**: 5-6 second response times vs. traditional NLP approaches
- **High Accuracy**: Leveraging pre-trained LLM capabilities
- **Scalable Architecture**: Foundation for future optimizations
- **Maintainable Code**: Clear separation of concerns and comprehensive logging

The system's design choices prioritize **performance** and **development efficiency** while maintaining **accuracy** and **scalability**. Future optimizations through caching and vector database integration will further enhance performance and reduce operational costs.

---

*This document serves as a comprehensive technical reference for the semantic search system implementation and can be used for technical reviews and future development planning.* 