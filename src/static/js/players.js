import { getResource, deleteResource } from './api.js'
import { setTitle, getReturnButton, getControlsElem, getContentsElem } from './utils.js'
import { submitForm, renderControlForm } from './form.js'

function renderAllPlayers(response, s, a) {
    setTitle('Players')
    getControlsElem().html(getReturnButton())

    let contentElem = getContentsElem()
    contentElem.empty()

    console.log(response);
    let addPlayerControl = response['@controls']['gamescr:add-player']

    let addPlayerForm = renderControlForm(addPlayerControl, "player")
    addPlayerForm.addClass("new-player")
    contentElem.append('<h4>' + addPlayerControl.title + '</h4>')
    contentElem.append(addPlayerForm)

    let playerList = $('<div>')
    playerList.append('<h4>All players</h4>')

    let playerTable = $('<table>')
        .append('<thead><tr><th scope="col">Name<th><th scope="col"></th></tr></thead>')

    let ptBody = $('<tbody>')
    playerTable.append(ptBody)

    contentElem.append($('<div>')).append('<h4>All players</h4>').append(playerTable)

    response.items.forEach(function(item) {
        getResource(item['@controls'].self.href, function(response) {
            let playerControls = response['@controls']
            let deleteHref = playerControls['gamescr:delete'].href
            console.log(deleteHref);

            let row = $('<tr>')
            row.append('<td>' + item.name + '</td>');

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
}

export default renderAllPlayers