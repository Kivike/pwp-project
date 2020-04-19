import { getResource, sendData } from './api.js'
import { getReturnButton, getContentsElem, getControlsElem, setTitle } from './utils.js'

function renderGame(data) {
    getControlsElem().html(getReturnButton())

    let contents = getContentsElem();
    contents.empty();

    setTitle(data.name);

    contents.append($('<div/>', {
        class: 'game-type',
        html: 'Gametype is ' + data.game_type
    }));

    contents.append($('<div/>', {
        class: 'created-at',
        html: 'Created at ' + data.created
    }));

    let statusDiv = $('<div/>', {class: 'game-status'});
    let status = data.status == 0 ? 'active' : 'ended';

    statusDiv.append('<span>Game is ' + status + '</span>')

    let endGameBtn = $('<a>', {html: 'End game'}).click(function(event) {
        endGame(event, data);
    });
    statusDiv.append(endGameBtn)
    endGameBtn.wrap('<button/>')

    contents.append(statusDiv);

    contents.append($('<div/>', {
        class: "game-host",
        html: 'Game host: ' + data.host
    }));

    renderScoreboad(data);
}

function endGame(event, gameData) {
    sendData(gameData['@controls'].self.href, 'PUT', {
        'name': gameData.name,
        'status': 1
    }, function(res) {
        console.log(res);
    });
}
function renderScoreboad(gameData)
{
    const addScoreControl = gameData['@controls']['gamescr:add-score'];
    const getScoresControl = gameData['@controls']['gamescr:scores'];

    let contents = getContentsElem();

    contents.append('<h4>Scoreboard</h4>')
}

export default renderGame;