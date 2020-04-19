import { renderError } from './utils.js'

/**
 * Functions are originally taken from
 * https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/exercise-4-implementing-hypermedia-clients/
 */

/**
 * @param {String} href 
 * @param {Function} callback 
 */
function getResource(href, callback) {
    console.log(href);
    $.ajax({
        url: href,
        success: callback,
        error: renderError
    });
}

/**
 * @param {String}
 * @param {Function} callback 
 */
function deleteResource(href, callback) {
    $.ajax({
        url: href,
        success: callback,
        type: 'DELETE',
        error: renderError
    });
}

/**
 * @param {String} href 
 * @param {String} method 
 * @param {Object} data 
 * @param {Function} callback 
 */
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

/**
 * 
 * @param {Object} event 
 * @param {String} a 
 * @param {Function} callback 
 */
function followLink(event, a, callback) {
    event.preventDefault();
    getResource($(a).attr("href"), callback);
}

export { getResource, deleteResource, sendData, followLink }
