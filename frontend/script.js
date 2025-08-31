// DOM Elements
const searchInput = document.getElementById('searchInput');
const attachmentInput = document.getElementById('attachmentInput');
const attachmentBtn = document.getElementById('attachmentBtn');
const sendBtn = document.getElementById('sendBtn');
const attachmentPreview = document.getElementById('attachmentPreview');
const loadingState = document.getElementById('loadingState');
const resultsContainer = document.getElementById('resultsContainer');

// State
let attachedFiles;

// Event Listeners
attachmentBtn.addEventListener('click', () => {
    attachmentInput.click();
});

attachmentInput.addEventListener('change', handleFileSelection);
sendBtn.addEventListener('click', handleSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// File Selection Handler
function handleFileSelection(event) {
    const files = Array.from(event.target.files);
    if(files.length > 0) {
        attachedFiles = files[0];
        console.log(attachedFiles);
        updateAttachmentPreview();
    }
}

// Update Attachment Preview
function updateAttachmentPreview() {
    console.log(attachedFiles);
    if (!attachedFiles) {
        attachmentPreview.classList.remove('show');
        return;
    }

    attachmentPreview.classList.add('show');
    attachmentPreview.innerHTML = `
        <div class="attachment-item">
            <span class="attachment-name">${attachedFiles.name}</span>
            <button class="remove-attachment" onclick="removeAttachment()">Remove</button>
        </div>
    `;
}

// Remove Attachment
function removeAttachment() {
    attachedFiles = null;
    attachmentInput.value = ''; // Clear the input
    updateAttachmentPreview();
}

// Search Handler
async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        alert('Please enter a search query');
        return;
    }

    if (!attachedFiles) {
        alert('Please input xlsx or csv file to search in');
        return;
    }

    // Show loading state
    loadingState.classList.remove('hidden');
    resultsContainer.innerHTML = '';

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('query', query);
        
        // Append files
        formData.append(`file`, attachedFiles);

        // Make API call
        const response = await fetch('http://localhost:8001/api/v1/search', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Hide loading state
        loadingState.classList.add('hidden');
        
        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Search error:', error);
        loadingState.classList.add('hidden');
        
        // Show demo data for development
        const demoData = {
            "size": 3,
            "results": [
                {
                    "concept_name": "Gross Margin",
                    "location": "Financial Ratios sheet, cell B2, Year 1",
                    "value_formula": "='3-Year Forecast'!B4/'3-Year Forecast'!B2",
                    "formula": "='3-Year Forecast'!B4/'3-Year Forecast'!B2",
                    "relevance": 0.98,
                    "explanation": "This cell calculates the gross margin for Year 1 by dividing the gross profit by the revenue. Gross margin is a key profitability metric.",
                    "business_context": "Indicates the percentage of revenue remaining after deducting the cost of goods sold.",
                    "cell_location": "B2",
                    "sheet_name": "Financial Ratios",
                    "formula_type": "Financial Ratio"
                },
                {
                    "concept_name": "Operating Margin",
                    "location": "Financial Ratios sheet, cell B3, Year 1",
                    "value_formula": "='3-Year Forecast'!B6/'3-Year Forecast'!B2",
                    "formula": "='3-Year Forecast'!B6/'3-Year Forecast'!B2",
                    "relevance": 0.85,
                    "explanation": "This cell calculates the operating margin for Year 1 by dividing the operating profit by the revenue. Operating margin is a key profitability metric.",
                    "business_context": "Indicates the percentage of revenue remaining after deducting operating expenses and cost of goods sold.",
                    "cell_location": "B3",
                    "sheet_name": "Financial Ratios",
                    "formula_type": "Financial Ratio"
                },
                {
                    "concept_name": "Net Profit Margin",
                    "location": "Financial Ratios sheet, cell B4, Year 1",
                    "value_formula": "='3-Year Forecast'!B10/'3-Year Forecast'!B2",
                    "formula": "='3-Year Forecast'!B10/'3-Year Forecast'!B2",
                    "relevance": 0.72,
                    "explanation": "This cell calculates the net profit margin for Year 1 by dividing the net profit by the revenue. Net profit margin is a key profitability metric.",
                    "business_context": "Indicates the percentage of revenue remaining after deducting all expenses, including taxes and interest.",
                    "cell_location": "B4",
                    "sheet_name": "Financial Ratios",
                    "formula_type": "Financial Ratio"
                }
            ]
        };
        
        displayResults(demoData);
        
        // Show error message (optional)
        console.log('Using demo data - API not available');
    }
}

// Display Results
function displayResults(data) {
    if (!data.results || data.results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <h3>No results found</h3>
                <p>Try adjusting your search query or check your spelling.</p>
            </div>
        `;
        return;
    }

    // Sort by relevance (descending) - backup sort in case backend doesn't sort
    const sortedResults = data.results;

    const resultsHTML = `
        <div class="results-header">
            <h2>Search Results</h2>
            <p class="results-count">Found ${data.size} result${data.size !== 1 ? 's' : ''}</p>
        </div>
        ${sortedResults.map(result => createResultCard(result)).join('')}
    `;

    resultsContainer.innerHTML = resultsHTML;
}

// Create Result Card
function createResultCard(result) {
    const relevanceClass = getRelevanceClass(result.relevance);
    const relevanceText = `${Math.round(result.relevance * 100)}% relevant`;

    return `
        <div class="result-card">
            <div class="result-header">
                <div>
                    <h3 class="result-title">${escapeHtml(result.concept_name)}</h3>
                    <p class="result-location">${escapeHtml(result.location)}</p>
                </div>
                <div class="relevance-badge ${relevanceClass}">
                    ${relevanceText}
                </div>
            </div>

            <div class="formula-container">
                <div class="formula-label">Formula</div>
                <div class="formula-text">${(result.formula)? escapeHtml(result.formula) : "Not Available"}</div>
            </div>

            <p class="result-explanation">${escapeHtml(result.explanation)}</p>

            <p class="business-context">${escapeHtml(result.concept_name)}</p>
            
            <p class="result-context">${escapeHtml(result.business_context)}</p>

            <span class="formula-type-badge">${escapeHtml(result.formula_type)}</span>
            <span class="formula-concept-name-badge">${escapeHtml(result.concept_name)}</span>
            <span class="sheet-name-badge">${escapeHtml(result.sheet_name)}</span>
            <span class="cell-location-badge">${escapeHtml(result.cell_location)}</span>
        </div>
    `;
}

// Get Relevance Class
function getRelevanceClass(relevance) {
    if (relevance >= 0.8) return 'relevance-high';
    if (relevance >= 0.6) return 'relevance-medium';
    return 'relevance-low';
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Formula Finder initialized');
});