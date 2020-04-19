
/**
 * @param {Object} data 
 */
function renderError(data) {
    //TODO show in error block
    console.error(data);
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
    let button = '<button><a href="/">Return to menu</a>';
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
export { renderError, setTitle, getReturnButton, getContentsElem, getControlsElem }