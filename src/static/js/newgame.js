import { getResource } from './api.js'
import { setTitle, getReturnButton, getControlsElem, getContentsElem } from './utils.js'
import { submitForm, renderControlForm } from './form.js'

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
    let addGametypeForm = renderControlForm(addGametypeControl, "gametype", false, false)
    addGametypeForm.attr('action', addGametypeControl.href)
    addGametypeForm.attr('method', addGametypeControl.method)
    addGametypeForm.addClass("form-add-gametype")
    gametypeContainer.append(addGametypeForm)

    gametypeSelect.change(function() {
        let value = $(this).val();
        
        if (value === 'new') {
            addGametypeForm.show();
        } else {
            addGametypeForm.hide();
        }
    })

    return gametypeContainer;
}

function submitNewGame(event, addGameControl, addGametypeControl) {
    event.preventDefault();


    let submitGame = function() {
        submitForm(event, $('form.form-new-game'), addGameControl.schema, function(res) {
            if (res.status === 201) {
                form.find('input,select').each(function() {
                    let el = $(this)
                    el.val("")
                });
            }
        });
    }
    if ($('select#gametype-select').children("option:selected").val() === "new") {
        submitGametype(addGametypeControl, submitGame)
    } else {
        submitGame();
    }
}

function submitGametype(addGametypeControl, callback) {
    let newGametypeName = $('#gamescr-field-gametype-name').val()

    submitForm(event, $('form.form-add-gametype'), addGametypeControl.schema, function(data, status, res) {
        if (res.status === 201) {
            $('select#gametype-select').val(newGametypeName)
            callback();
        }
    });
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