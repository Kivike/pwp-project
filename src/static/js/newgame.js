import { getResource } from './api.js'
import { setTitle, getReturnButton, getControlsElem, getContentsElem } from './utils.js'
import { submitForm, renderControlForm } from './form.js'

function renderNewGame(response) {
    setTitle('New Game')
    getControlsElem().html(getReturnButton())

    let control = response['@controls']['gamescr:add-game']
    let props = control.schema.properties
    let nameProp = props.name
    let formIdGame = "game"
    let form =  $('<form form-id="' + formIdGame + '" class="form-new-game">');

    form.append('<label for="game-name">' + nameProp.description + '</label>')
    form.append('<input type="text" id="game-name" class="field-' + formIdGame + '" gamescr-field="name"></input>');

    let gametypeContainer = $('<div><label for="gametype-select">Game type:</label></div>')
    let gametypeSelect = $('<select gamescr-field="game_type" id="gametype-select" class="field-' + formIdGame + '">')

    gametypeContainer.append(gametypeSelect)
    gametypeSelect.append('<option value="new">-- new --</option>')

    let addGametypeControl = null

    getResource(response['@controls']['gamescr:all-gametypes'].href, function(response) {
        response.items.forEach(function(item) {
            gametypeSelect.append('<option value="' + item.name + '">' + item.name + '</option>')
        })

        addGametypeControl = response['@controls']['gamescr:add-gametype']
        let addGametypeForm = renderControlForm(addGametypeControl, "gametype", false, false)
        addGametypeForm.attr('action', addGametypeControl.href)
        addGametypeForm.attr('method', addGametypeControl.method)
        addGametypeForm.addClass("form-add-gametype")
        gametypeContainer.append(addGametypeForm)
    });

    form.append(gametypeContainer)
    let hostSelect = renderHostSelect(response['@controls']['gamescr:all-players'])
    hostSelect.find('select').addClass("field-" + formIdGame)
    form.append(hostSelect)
    form.append('<button type="submit">Submit</button>')
    form.attr('action', control.href)
    form.attr('method', control.method)
    form.submit(submitNewGame)
    getContentsElem().html(form)
}

function submitNewGame(event) {
    let submitGame = function() {
        submitForm(event, $('form.form-new-game'), control.schema, function(res) {
            if (res.status === 201) {
                form.find('input,select').each(function() {
                    let el = $(this)
                    el.val("")
                });
            }
        });
    }
    event.preventDefault();
    console.log(addGametypeControl)
    if (gametypeSelect.children("option:selected").val() === "new") {
        let newGametypeName = $('#gamescr-field-gametype-name').val()

        submitForm(event, $('form.form-add-gametype'), addGametypeControl.schema, function(data, status, res) {
            if (res.status === 201) {
                gametypeSelect.val(newGametypeName)

                submitGame();
            }
        });
    } else {
        submitGame();
    }
}

function renderHostSelect(control) {
    let hostSelect = $('<select gamescr-field="host" id="host-select">')
    let hostSelectContainer = $('<div>').append('<label for="host-select">Host name:</label>').append(hostSelect)

    getResource(control.href, function(response) {
        response.items.forEach(function(item) {
            console.log(item);
            hostSelect.append('<option>' + item.name + '</option>');
            console.log(hostSelect)
        })
    });
    return hostSelectContainer;
}

export { renderNewGame as default }