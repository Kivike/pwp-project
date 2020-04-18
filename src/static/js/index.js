let ENTRY_POINT = 'http://127.0.0.1:5000/api/'

let headerElem = null
let controlsElem = null
let contentElem = null

import renderAllPlayers from './players.js'
import renderNewGame from './newgame.js'
import { getResource, followLink } from './api.js'

console.log(followLink)
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
        '" onClick="_followLink(event, this, renderNewGame)">New Game</a></button>');
}

function _followLink(event, a, b) {
    event.preventDefault();
    console.log('AA')
    followLink(event, a, b)
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