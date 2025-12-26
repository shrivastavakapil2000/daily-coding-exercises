/**
 * Personalized Daily Quote Generator
 * Frontend JavaScript Logic
 */

// Configuration
const CONFIG = {
    API_ENDPOINT: 'https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/',
    REQUEST_TIMEOUT: 30000, // 30 seconds
    MIN_NAME_LENGTH: 1,
    MAX_NAME_LENGTH: 50
};

// Application State
const AppState = {
    isLoading: false,
    currentQuote: null,
    userName: '',
    error: null,
    lastRequestTime: null
};

// DOM Elements
const Elements = {
    form: null,
    nameInput: null,
    submitBtn: null,
    btnText: null,
    btnLoading: null,
    inputSection: null,
    quoteSection: null,
    errorSection: null,
    quoteText: null,
    quoteFor: null,
    quoteModel: null,
    newQuoteBtn: null,
    retryBtn: null,
    errorText: null,
    nameError: null,
    loadingOverlay: null
};

/**
 * Initialize the application
 */
function initApp() {
    // Get DOM elements
    Elements.form = document.getElementById('quoteForm');
    Elements.nameInput = document.getElementById('nameInput');
    Elements.submitBtn = document.getElementById('submitBtn');
    Elements.btnText = Elements.submitBtn.querySelector('.btn-text');
    Elements.btnLoading = Elements.submitBtn.querySelector('.btn-loading');
    Elements.inputSection = document.getElementById('inputSection');
    Elements.quoteSection = document.getElementById('quoteSection');
    Elements.errorSection = document.getElementById('errorSection');
    Elements.quoteText = document.getElementById('quoteText');
    Elements.quoteFor = document.getElementById('quoteFor');
    Elements.quoteModel = document.getElementById('quoteModel');
    Elements.newQuoteBtn = document.getElementById('newQuoteBtn');
    Elements.retryBtn = document.getElementById('retryBtn');
    Elements.errorText = document.getElementById('errorText');
    Elements.nameError = document.getElementById('nameError');
    Elements.loadingOverlay = document.getElementById('loadingOverlay');

    // Add event listeners
    setupEventListeners();

    // Focus on name input
    Elements.nameInput.focus();

    console.log('✨ Daily Quote Generator initialized');
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Form submission
    Elements.form.addEventListener('submit', handleFormSubmit);

    // Input validation on blur and input
    Elements.nameInput.addEventListener('blur', validateNameInput);
    Elements.nameInput.addEventListener('input', clearInputError);

    // New quote button
    Elements.newQuoteBtn.addEventListener('click', handleNewQuote);

    // Retry button
    Elements.retryBtn.addEventListener('click', handleRetry);

    // Enter key on new quote button
    Elements.newQuoteBtn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            handleNewQuote();
        }
    });
}

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    const name = Elements.nameInput.value.trim();

    // Validate input
    if (!validateNameInput()) {
        return;
    }

    // Update state
    AppState.userName = name;
    AppState.lastRequestTime = Date.now();

    // Generate quote
    await generateQuote(name);
}

/**
 * Validate name input
 */
function validateNameInput() {
    const name = Elements.nameInput.value.trim();
    const errorElement = Elements.nameError;

    // Clear previous errors
    clearInputError();

    // Check if empty
    if (!name) {
        showInputError('Please enter your name');
        return false;
    }

    // Check length
    if (name.length < CONFIG.MIN_NAME_LENGTH) {
        showInputError('Name is too short');
        return false;
    }

    if (name.length > CONFIG.MAX_NAME_LENGTH) {
        showInputError(`Name is too long (max ${CONFIG.MAX_NAME_LENGTH} characters)`);
        return false;
    }

    // Check for valid characters (basic validation)
    const nameRegex = /^[a-zA-Z0-9\s\-'\.]+$/;
    if (!nameRegex.test(name)) {
        showInputError('Please use only letters, numbers, spaces, hyphens, and apostrophes');
        return false;
    }

    return true;
}

/**
 * Show input error
 */
function showInputError(message) {
    Elements.nameError.textContent = message;
    Elements.nameError.classList.add('show');
    Elements.nameInput.setAttribute('aria-invalid', 'true');
    Elements.nameInput.focus();
}

/**
 * Clear input error
 */
function clearInputError() {
    Elements.nameError.classList.remove('show');
    Elements.nameInput.removeAttribute('aria-invalid');
}

/**
 * Generate quote from API
 */
async function generateQuote(name) {
    try {
        // Set loading state
        setLoadingState(true);
        hideAllSections();

        // Make API request
        const quote = await fetchQuoteFromAPI(name);

        // Update state
        AppState.currentQuote = quote;
        AppState.error = null;

        // Display quote
        displayQuote(quote, name);

    } catch (error) {
        console.error('Error generating quote:', error);
        AppState.error = error.message;
        showError(error.message);
    } finally {
        setLoadingState(false);
    }
}

/**
 * Fetch quote from API
 */
async function fetchQuoteFromAPI(name) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CONFIG.REQUEST_TIMEOUT);

    try {
        // Prepare request URL with name parameter
        const url = new URL(CONFIG.API_ENDPOINT);
        if (name) {
            url.searchParams.append('name', name);
        }

        // Make request
        const response = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        // Check response status
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        // Parse JSON response
        const data = await response.json();

        // Validate response structure
        if (!data.quote) {
            throw new Error('Invalid response from server');
        }

        return data;

    } catch (error) {
        clearTimeout(timeoutId);

        // Handle different error types
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        } else if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Unable to connect to the server. Please check your internet connection.');
        } else {
            throw error;
        }
    }
}

/**
 * Display quote in UI
 */
function displayQuote(quoteData, name) {
    // Update quote text
    Elements.quoteText.textContent = quoteData.quote;

    // Update meta information
    if (quoteData.personalized && name) {
        Elements.quoteFor.textContent = `Personalized for ${name}`;
    } else {
        Elements.quoteFor.textContent = 'Daily inspiration';
    }

    Elements.quoteModel.textContent = `Powered by ${quoteData.model || 'AI'}`;

    // Show quote section
    showQuoteSection();

    // Announce to screen readers
    announceToScreenReader(`New quote generated: ${quoteData.quote}`);
}

/**
 * Show error message
 */
function showError(message) {
    Elements.errorText.textContent = message;
    showErrorSection();

    // Announce to screen readers
    announceToScreenReader(`Error: ${message}`);
}

/**
 * Handle new quote request
 */
async function handleNewQuote() {
    if (AppState.isLoading) return;

    const name = AppState.userName;
    await generateQuote(name);
}

/**
 * Handle retry after error
 */
async function handleRetry() {
    if (AppState.isLoading) return;

    hideAllSections();
    showInputSection();
    Elements.nameInput.focus();
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
    AppState.isLoading = isLoading;

    // Update submit button
    Elements.submitBtn.disabled = isLoading;
    Elements.submitBtn.classList.toggle('loading', isLoading);

    // Update new quote button
    if (Elements.newQuoteBtn) {
        Elements.newQuoteBtn.disabled = isLoading;
    }

    // Show/hide loading overlay for longer requests
    if (isLoading) {
        setTimeout(() => {
            if (AppState.isLoading) {
                Elements.loadingOverlay.classList.add('show');
                Elements.loadingOverlay.setAttribute('aria-hidden', 'false');
            }
        }, 1000); // Show overlay after 1 second
    } else {
        Elements.loadingOverlay.classList.remove('show');
        Elements.loadingOverlay.setAttribute('aria-hidden', 'true');
    }
}

/**
 * Show/hide sections
 */
function hideAllSections() {
    Elements.quoteSection.classList.remove('show');
    Elements.errorSection.classList.remove('show');
}

function showInputSection() {
    Elements.inputSection.style.display = 'block';
}

function showQuoteSection() {
    hideAllSections();
    Elements.quoteSection.classList.add('show');
}

function showErrorSection() {
    hideAllSections();
    Elements.errorSection.classList.add('show');
}

/**
 * Announce message to screen readers
 */
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;

    document.body.appendChild(announcement);

    // Remove after announcement
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

/**
 * Utility function to debounce function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Handle keyboard navigation
 */
function setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        // Escape key to close loading overlay or return to input
        if (e.key === 'Escape') {
            if (Elements.loadingOverlay.classList.contains('show')) {
                // Don't close loading overlay with escape
                return;
            }
            
            if (Elements.quoteSection.classList.contains('show') || 
                Elements.errorSection.classList.contains('show')) {
                handleRetry();
            }
        }
    });
}

/**
 * Error handling for uncaught errors
 */
window.addEventListener('error', (event) => {
    console.error('Uncaught error:', event.error);
    
    if (AppState.isLoading) {
        setLoadingState(false);
        showError('An unexpected error occurred. Please try again.');
    }
});

/**
 * Handle network status changes
 */
window.addEventListener('online', () => {
    console.log('Connection restored');
    announceToScreenReader('Internet connection restored');
});

window.addEventListener('offline', () => {
    console.log('Connection lost');
    announceToScreenReader('Internet connection lost');
    
    if (AppState.isLoading) {
        setLoadingState(false);
        showError('Internet connection lost. Please check your connection and try again.');
    }
});

// Initialize app when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// Setup keyboard navigation
setupKeyboardNavigation();