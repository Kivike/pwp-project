import { getResource, deleteResource } from './api.js'

function renderAllPlayers(response) {
    setTitle('Players')
    controlsElem.html(getReturnButton())
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
    playerTable.append('<thead><tr><th scope="col">Name<th><th scope="col"></th></tr></thead>')

    let ptBody = $('<tbody>')

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
    playerTable.append(ptBody)
    playerList.append(playerTable)
    contentElem.append(playerList)
}

function getReturnButton() {
    let button = '<button><a href="/">Return to menu</a>';
    return button
}

export default renderAllPlayers