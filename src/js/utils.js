import $ from './jquery.js';

/**
 * @param {Object} data 
 */
function renderError(error) {
    if ("string" === typeof error) {
        $('.error').html(error);
    } else {
        if (error.responseJSON) {
            $('.error').html(error.responseJSON['@error']['@message']);
        }
    }
}

function resetErrors() {
    $('.error').empty()
}
/**
 * Set page title
 * 
 * @param {string} title 
 */
function setTitle(title) {
    const headerElem = $('.header')
    headerElem.html('<h3>' + title + '</h3>')
}

/**
 * Get button that returns to index menu
 */
function getReturnButton() {
    let button = '<button><a id="return-link" href="/">Return to menu</a></button>';
    return button
}

/**
 * Get main page content block
 */
function getContentsElem() {
    return $('.contents')
}

/**
 * Get main page controls block
 */
function getControlsElem() {
    return $('.controls')
}
export { renderError, resetErrors, setTitle, getReturnButton, getContentsElem, getControlsElem }
