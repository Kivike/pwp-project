let ENTRY_POINT = 'http://127.0.0.1:5000/api/'

import renderAllPlayers from './players.js'
import renderNewGame from './newgame.js'
import renderGame from './game.js'

import { getResource, followLink } from './api.js'
import { setTitle, getControlsElem, getContentsElem } from './utils.js'

function renderIndex(response) {
    setTitle('Game Score API')

    let controls = response['@controls'];

    const allPlayerHref = controls['gamescr:all-players']['href']
    let allPlayersLink = $('<a href="' + allPlayerHref + '" >All Players</a>');

    allPlayersLink.click(function(event) {
        followLink(event, this, renderAllPlayers);
    })

    getControlsElem().append($('<button>').append(allPlayersLink));

    getResource(controls['gamescr:all-games']['href'], renderAllGames);
}

function renderAllGames(response) {
    let controls = response['@controls']

    const newGameHref = controls['gamescr:add-game']['href']
    let newGameLink = $('<a href="' + newGameHref + '">New game</a>')
    newGameLink.click(function(event) {
        console.log(event)
        followLink(event, this, renderNewGame)
    });
    getControlsElem().append($('<button>').append(newGameLink));

    let gameTable = $('<table>').append('<thead><tr><th scope="col">Name<th><th scope="col"></th></tr></thead>')

    let ptBody = $('<tbody>')
    gameTable.append(ptBody)

    getContentsElem().append('<div>').append('<h4>Existing games</h4>').append(gameTable)

    response.items.forEach(function(item) {
        let gameHref = item['@controls'].self.href;

        let row = $('<tr>')
        row.append('<td>' + item.name + '</td>');

        let a = $('<a href="' + gameHref + '"><button>Access</button></a>');

        a.click(function(event) {
            followLink(event, this, renderGame)
        });
        row.append(a)
        a.wrap('<td>')
        ptBody.append(row);
    });
}

$(document).ready(function () {
    getResource(ENTRY_POINT, renderIndex)
});
