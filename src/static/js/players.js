import { getResource, deleteResource } from './api.js'
import { setTitle, getReturnButton, getControlsElem, getContentsElem } from './utils.js'
import { renderControlForm } from './form.js'

/**
 * Render player list page
 * 
 * @param {Object} data
 */
function renderAllPlayers(data) {
    setTitle('Players')
    getControlsElem().html(getReturnButton())

    let contentElem = getContentsElem()
    contentElem.html(renderAddPlayerForm(data))

    renderPlayersTable(data, function(result) {
        console.log(result);
        contentElem.append(result);
    });
}

/**
 * Render form for creating a new player
 * 
 * @param {Object} playersData 
 */
function renderAddPlayerForm(playersData) {
    let addPlayerContainer = $('<div>')
    let addPlayerControl = playersData['@controls']['gamescr:add-player']

    let addPlayerForm = renderControlForm(addPlayerControl, "player")
    addPlayerForm.addClass("new-player")
    addPlayerContainer.append('<h4>' + addPlayerControl.title + '</h4>')
    addPlayerContainer.append(addPlayerForm);

    return addPlayerContainer;
}

/**
 * Render table of all players
 * Calls the callback once rendering is done
 * 
 * @param {Object} playersData 
 * @param {Function} callback 
 */
function renderPlayersTable(playersData, callback) {
    let playersTableContainer = $('<div/>');
    playersTableContainer.append('<h4>All players</h4>')

    let playerTable = $('<table>')
        .append('<thead><tr><th scope="col">Name<th><th scope="col"></th></tr></thead>')

    let ptBody = $('<tbody>')
    playerTable.append(ptBody)

    playersTableContainer.append(playerTable)

    playersData.items.forEach(function(item, i) {
        getResource(item['@controls'].self.href, function(data) {
            let playerControls = data['@controls']
            let deleteHref = playerControls['gamescr:delete'].href

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

            console.log(i);
            console.log(playersData.items.length);

            if (i === playersData.items.length - 1) {
                // Last item rendered
                callback(playersTableContainer);
            }
        });
    });
}
export default renderAllPlayers
