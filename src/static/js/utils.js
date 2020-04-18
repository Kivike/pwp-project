function renderError(response) {
    console.error(response);
}

function setTitle(title) {
    const headerElem = $('.header')
    headerElem.html('<h3>' + title + '</h3>')
}

function getReturnButton() {
    let button = '<button><a href="/">Return to menu</a>';
    return button
}

function getContentsElem() {
    return $('.contents')
}

function getControlsElem() {
    return $('.controls')
}
export { renderError, setTitle, getReturnButton, getContentsElem, getControlsElem }