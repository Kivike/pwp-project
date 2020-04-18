import { renderError } from './utils.js'

function getResource(href, callback) {
    console.log(href);
    $.ajax({
        url: href,
        success: callback,
        error: renderError
    });
}

function deleteResource(href, callback) {
    $.ajax({
        url: href,
        success: callback,
        type: 'DELETE',
        error: renderError
    });
}

function sendData(href, method, data, callback) {
    $.ajax({
        url: href,
        type: method,
        data: JSON.stringify(data),
        contentType: "application/json",
        processData: false,
        success: callback,
        error: renderError
    });
}

function followLink(event, a, renderer) {
    event.preventDefault();
    getResource($(a).attr("href"), renderer);
}

export { getResource, deleteResource, sendData, followLink }