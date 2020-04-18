let ENTRY_POINT = 'http://127.0.0.1:5000/api/'

import renderAllPlayers from './players.js'
import renderNewGame from './newgame.js'
import { getResource, followLink } from './api.js'
import { setTitle, getControlsElem } from './utils.js'

function renderIndex(response) {
    let controlsElem = $('.controls')
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
}


$(document).ready(function () {
    getResource(ENTRY_POINT, renderIndex)
});