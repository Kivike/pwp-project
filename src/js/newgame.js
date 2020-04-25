import $ from './jquery.js';
import { getResource } from './api.js'
import { setTitle, getReturnButton, getControlsElem, getContentsElem } from './utils.js'
import { submitForm, renderControlForm } from './form.js'
import renderGame from './game.js'
/**
 * Render page for new game
 * @param {Object} data 
 */
function renderNewGame(data) {
    setTitle('New Game')
    getControlsElem().html(getReturnButton())

    let control = data['@controls']['gamescr:add-game']
    let props = control.schema.properties
    let nameProp = props.name
    let formIdGame = "game"
    let form =  $('<form form-id="' + formIdGame + '" class="form-new-game">');

    let gameName = $('<div class="form-group"/>')
    gameName.append('<label for="game-name">' + nameProp.description + '</label>')
    gameName.append('<input type="text" id="game-name" class="field-' + formIdGame + '" gamescr-field="name"></input>');
    form.append(gameName)

    let addGametypePlaceholder = $('<div/>');
    form.append(addGametypePlaceholder);

    let addGametypeControl = null;

    getResource(data['@controls']['gamescr:all-gametypes'].href, function(response) {
        addGametypeControl = response['@controls']['gamescr:add-gametype'];

        let gametypeSelect = renderGametypeSelect(response, formIdGame)
        addGametypePlaceholder.append(gametypeSelect)
    });

    let hostSelect = renderHostSelect(data['@controls']['gamescr:all-players'])
    hostSelect.find('select').addClass("field-" + formIdGame)
    form.append(hostSelect)
    form.append('<button type="submit">Submit</button>')
    form.attr('action', control.href)
    form.attr('method', control.method)
    form.submit(function(event) {
        submitNewGame(event, control, addGametypeControl)
    });
    getContentsElem().html(form)
}

/**
 * Render form for selecting gametype, and adding new gametype if 'new' gametype is selected
 * 
 * @param {Object} gametypeData 
 * @param {String} formIdGame ID of the main game form
 */
function renderGametypeSelect(gametypeData, formIdGame) {
    let gametypeContainer = $('<div/>')

    let gametypeSelectGroup = $('<div class="form-group"/>')
    gametypeSelectGroup.append('<label for="gametype-select">Game type:</label>')

    let gametypeSelect = $('<select gamescr-field="game_type" id="gametype-select" class="field-' + formIdGame + '">')
    gametypeSelect.append('<option value="new">-- new --</option>')

    gametypeSelectGroup.append(gametypeSelect);
    gametypeContainer.append(gametypeSelectGroup);

    gametypeData.items.forEach(function(item) {
        gametypeSelect.append('<option value="' + item.name + '">' + item.name + '</option>')
    });

    let addGametypeControl = gametypeData['@controls']['gamescr:add-gametype']
    let addGametypeForm = renderControlForm(addGametypeControl, "gametype", null, false, false)
    addGametypeForm.attr('action', addGametypeControl.href)
    addGametypeForm.attr('method', addGametypeControl.method)
    addGametypeForm.addClass("form-add-gametype")
    gametypeContainer.append(addGametypeForm)

    gametypeSelect.change(function() {
        if ($(this).val() === 'new') {
            addGametypeForm.show();
        } else {
            addGametypeForm.hide();
        }
    });

    return gametypeContainer;
}

/**
 * Submit new gametype if not using existing one, and then submit game
 * Switch to page of created game on success
 * 
 * @param {Object} event 
 * @param {Object} addGameControl 
 * @param {Object} addGametypeControl 
 */
function submitNewGame(event, addGameControl, addGametypeControl) {
    event.preventDefault();

    let submitGame = function() {
        submitForm(event, $('form.form-new-game'), addGameControl.schema, function(resData, status, res) {
            if (res.status === 201) {
                getResource(res.getResponseHeader('location'), renderGame);
            } else {
                ///TODO handle error
            }
        });
    }
    if ($('select#gametype-select').children("option:selected").val() === "new") {
        submitGametype(addGametypeControl, submitGame)
    } else {
        submitGame();
    }
}

/**
 * Submit new gametype
 * Calls callback success/error depending on the response
 * 
 * @param {Object} addGametypeControl 
 * @param {Function} success 
 * @param {Function} error
 */
function submitGametype(addGametypeControl, callback, error) {
    let newGametypeName = $('#gamescr-field-gametype-name').val()

    submitForm(event, $('form.form-add-gametype'), addGametypeControl.schema, function(data, status, res) {
        if (res.status === 201) {
            $('select#gametype-select').append($('<option>', {
                value: newGametypeName
            }));
            $('select#gametype-select').val(newGametypeName);
            callback();
        } else {
            error();
        }
    });
}

/**
 * Render selection for host player of the game
 * 
 * @param {Object} control 
 */
function renderHostSelect(control) {
    let hostSelect = $('<select gamescr-field="host" id="host-select">')
    let hostSelectContainer = $('<div>').append('<label for="host-select">Host name:</label>').append(hostSelect)

    getResource(control.href, function(response) {
        response.items.forEach(function(item) {
            hostSelect.append('<option>' + item.name + '</option>');
        })
    });
    return hostSelectContainer;
}

export { renderNewGame as default }
