import $ from './jquery.js';

import { sendData } from './api.js'
import { renderError, resetErrors } from './utils.js'

/**
 * Render a form based on Mason control
 * 
 * @param {Object} control 
 * @param {String} formId 
 * @param {Boolean} requiredOnly Only include required fields?
 * @param {Boolean} addSubmitButton Add submit button to end of form?
 */
function renderControlForm(control, formId, submitCallback, requiredOnly = false, addSubmitButton = true) {
    let form = $('<form></form>')
    form.attr('form-id', formId)
    form.attr('action', control.href)
    form.attr('method', control.method)
    form.submit(function(event) {
        submitForm(event, $('form.new-player'), control.schema, submitCallback);
    });

    const props = control['schema']['properties']

    for (const propName in props) {
        const isRequired = control.schema.required.includes(propName)

        if (requiredOnly && !isRequired) {
            return;
        }
        const prop = props[propName]
        let inputDiv = $('<div>', { class: 'form-group' })
        const inputId = "gamescr-field-" + formId + '-' + propName
        const requiredSpan = isRequired ? '<span class="required">*</span>' : '';
        const label = '<label for="' + inputId + '">' + prop.description + requiredSpan + ':</label>'
        inputDiv.append($(label))
        inputDiv.append('<input class="field-' + formId + '" id="' + inputId + '" gamescr-field="' + propName + '"></input>')

        form.append(inputDiv)
    }
    if (addSubmitButton) {
        form.append('<button type="submit">Submit</button>')
    }
    return form
}

/**
 * @param {Object} event 
 * @param {Object} form 
 * @param {Object} schema 
 * @param {Function} callback 
 */
function submitForm(event, form, schema, callback) {
    event.preventDefault()
    resetErrors();

    let formData = {}

    const formId = form.attr('form-id')
    let isValid = true;

    form.find('input.field-' + formId + ',select.field-' + formId).each(function() {
        let inputElem = $(this)
        let fieldName = inputElem.attr("gamescr-field")
        let fieldValue = inputElem.val()

        let prop = schema.properties[fieldName]

        if (fieldValue !== '' && fieldValue !== null) {
            if (prop.type === 'integer') {
                fieldValue = parseInt(fieldValue);
            } else if (prop.type === 'float') {
                fieldValue = parseFloat(fieldValue);
            }
            formData[fieldName] = fieldValue
        } else {
            if (schema.required.includes(fieldName)) {
                renderError('Missing value for required field "' + fieldName + '"');
                isValid = false;
            }
        }

        inputElem.val('')
    });

    if (isValid) {
        sendData(form.attr('action'), form.attr('method'), formData, callback);
    }
}

export { renderControlForm, submitForm }
