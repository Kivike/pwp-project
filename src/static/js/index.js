let ENTRY_POINT = 'http://127.0.0.1:5000/api/'

let headerElem = null
let controlsElem = null
let contentElem = null

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

function renderIndex(response) {
    controlsElem.empty();
    setTitle('Game Score API')

    let controls = response['@controls'];

    let allPlayersBtn = '<button><a href="' + controls['gamescr:all-players']['href'] +
        '" onClick="followLink(event, this, renderAllPlayers)">All Players</a></button>';

    controlsElem.html(allPlayersBtn);

    getResource(controls['gamescr:all-games']['href'], renderAllGames);
}

function renderAllGames(response) {
    let controls = response['@controls']

    controlsElem.append('<button><a href="' + controls['gamescr:add-game']['href'] +
        '" onClick="followLink(event, this, renderNewGame)">New Game</a></button>');

    console.log(response)
}

function renderAllPlayers(response) {
    setTitle('Players')
    controlsElem.html(getReturnButton())
    contentElem.empty()

    console.log(response);
    let addPlayerControl = response['@controls']['gamescr:add-player']

    let addPlayerForm = renderControlForm(addPlayerControl)
    addPlayerForm.addClass("new-player")
    contentElem.append('<h4>' + addPlayerControl.title + '</h4>')
    contentElem.append(addPlayerForm)

    let playerList = $('<div>')
    playerList.append('<h4>All players</h4>')
    let playerTable = $('<table>')
    playerTable.append('<thead><tr><th scope="col">Name<th><th scope="col"></th></tr></thead>')

    let ptBody = $('<tbody>')

    response.items.forEach(function(item) {
        getResource(item['@controls'].self.href, function(response) {
            let playerControls = response['@controls']
            let deleteHref = playerControls['gamescr:delete'].href
            console.log(deleteHref);

            let row = $('<tr>')
            row.append('<td>' + item.name + '</td>');

            //let a = '<a onClick="deleteResource(\'' + deleteHref + '\', playerDeleted)"\>Delete</a>'
            let a = $('<td><a><button>Delete</button></a></td>');
            console.log(a.html())
            a.click(function() {
                deleteResource(deleteHref, function(resData, status, res) {
                    if (res.status === 204) {
                        row.remove();
                    }
                })
            });
            row.append(a)
            ptBody.append(row);
        });
    });
    playerTable.append(ptBody)
    playerList.append(playerTable)
    contentElem.append(playerList)
}

function renderControlForm(control, requiredOnly = false, addSubmitButton = true) {
    let requiredFields = control.schema.required

    let form = $('<form></form>')
    form.attr('action', control.href)
    form.attr('method', control.method)
    form.submit(function(event) {
        submitForm(event, $('form.new-player'), function(res) {
            console.log(res);
        });
    });

    const props = control['schema']['properties']

    for (const propName in props) {
        if (requiredOnly && !control.schema.requiredFields.contains(propName)) {
            return;
        }
        const prop = props[propName]
        let inputDiv = $('<div>')
        const inputId = "gamescr-field-" + propName
        inputDiv.append('<label for="' + inputId + '">' + prop.description + ':</label>')
        inputDiv.append('<input id="' + inputId + '" gamescr-field="' + propName + '"></input>')

        form.append(inputDiv)
    }
    if (addSubmitButton) {
        form.append('<button type="submit">Submit</button>')
    }
    return form
}

function submitForm(event, form, callback) {
    event.preventDefault()

    let formData = {}

    form.find(':input').each(function() {
        let inputElem = $(this)
        let fieldName = inputElem.attr("gamescr-field")
        let fieldValue = inputElem.val()
        formData[fieldName] = fieldValue
        inputElem.val('')
    });

    sendData(form.attr('action'), form.attr('method'), formData, callback);
}

function renderNewGame(response) {
    setTitle('New Game')
    controlsElem.html(getReturnButton())

    console.log(response)

    let control = response['@controls']['gamescr:add-game']
    let props = control.schema.properties
    let nameProp = props.name

    let form =  $('<form class="form-new-game">');

    form.append('<label for="game-name">' + nameProp.description + '</label>')
    form.append('<input type="text" id="game-name"></input>');

    let gametypeContainer = $('<div><label for="gametype-select">Game type:</label></div>')
    let gametypeSelect = $('<select id="gametype-select">')

    gametypeContainer.append(gametypeSelect)
    gametypeSelect.append('<option value="new">-- new --</option>')

    getResource(response['@controls']['gamescr:all-gametypes'].href, function(response) {
        response.items.forEach(function(item) {
            gametypeSelect.append('<option value="' + item.name + '">' + item.name + '</option>')
        })

        let addGametypeControl = response['@controls']['gamescr:add-gametype']
        let addGametypeForm = renderControlForm(addGametypeControl, false, false)
        gametypeContainer.append(addGametypeForm)
    })
    form.append(gametypeContainer)
    form.append(renderHostSelect(response['@controls']['gamescr:all-players']))
    form.append('<button type="submit">Submit</button>')
    form.attr('action', control.href)
    form.attr('method', control.method)
    form.submit(function(event) {
        if (gametypeSelect.options[gametypeSelect.selectedIndex].val() === "new") {
            console.log("POST GANEMTYPE");
        }
        /*submitForm(event, $('form.form-new-game'), function(res) {
            console.log(res);
        });*/
    })
    contentElem.html(form)
}

function renderHostSelect(control) {
    let hostSelect = $('<select id="host-select">')
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

function getReturnButton() {
    let button = '<button><a href="/">Return to menu</a>';
    return button
}

function setTitle(title) {
    headerElem.html('<h3>' + title + '</h3>')
}
function renderError(response) {
    console.error(response);
}

$(document).ready(function () {
    headerElem = $('.header')
    controlsElem = $('.controls')
    contentElem = $('.contents')

    getResource(ENTRY_POINT, renderIndex)
});