import $ from './jquery.js';

import { getResource, deleteResource, sendData } from './api.js'
import { getReturnButton, getContentsElem, getControlsElem, setTitle } from './utils.js'
import { submitForm } from './form.js'

/**
 * Render game page
 * 
 * @param {Object} data 
 */
function renderGame(data) {
    setTitle(data.name);

    getControlsElem().html(getReturnButton())

    let contents = getContentsElem();
    contents.empty();

    contents.append(renderGametype(data))

    contents.append($('<div/>', {
        class: 'created-at',
        html: 'Created at: ' + data.created
    }));

    let statusDiv = $('<div/>', {class: 'game-status'});
    let statusText = data.status == 0 ? 'active' : 'inactive';

    statusDiv.append('<span>Game is <strong>' + statusText + '</strong></span>')

    if (data.status == 0) {
        let endGameBtn = $('<a>', {html: 'End game'}).click(function(event) {
            endGame(event, data);
        });
        statusDiv.append(endGameBtn);
        endGameBtn.wrap('<button class="btn btn-secondary" />');
    }

    contents.append(statusDiv);

    contents.append($('<div/>', {
        class: "game-host",
        html: 'Game host: ' + data.host
    }));

    renderScores(data);
}

function renderGametype(gameData) {
    const getGametypeHref = gameData['@controls']['gamescr:gametype'].href;

    let gametypeElem = $('<div class="game-type"/>');

    getResource(getGametypeHref, function(res) {
        let content = 'Gametype: ' + gameData.game_type;

        if (res.min_players && res.max_players) {
            if (res.min_players !== res.max_players) {
                content += ' (' + res.min_players + ' - ' + res.max_players + ' players)';
            } else {
                content += ' (' + res.min_players + ' players)';
            }
        } else if (res.min_players) {
            content += ' (' + res.min_players + '+ players)';
        } else if (res.max_players) {
            content += ' (up to ' + res.max_players + ' players)';
        }
        gametypeElem.html(content);
    });
    return gametypeElem;
}
function endGame(event, gameData) {
    sendData(gameData['@controls'].self.href, 'PUT', {
        name: gameData.name,
        game_type: gameData.game_type,
        host: gameData.host,
        status: 1
    }, function(resData, status, response) {
        if (response.status == 201) {
            getResource(gameData['@controls'].self.href, renderGame);
        }
    });
}

/**
 * Do inital rendering of score elements
 * 
 * @param {Object} gameData 
 */
function renderScores(gameData)
{
    let scoreContainer = $('<div class="score-container"/>');
    getContentsElem().append(scoreContainer);

    if (gameData.status == 0) {
        let addScore = renderAddPlayerscore(gameData);
        scoreContainer.append(addScore);
    }

    renderScoreboard(gameData)
}

/**
 * Render scoreboard in place. Can be called again to show updated scores.
 * 
 * @param {Object} gameData 
 */
function renderScoreboard(gameData) {
    let scoreboardContainer = $('.scoreboard-container');
    
    if (scoreboardContainer.length) {
        scoreboardContainer.empty();
    } else {
        scoreboardContainer = $('<div class="scoreboard-container"/>');
        $('.score-container').append(scoreboardContainer);
    }

    scoreboardContainer.append('<h4>Scoreboard</h4>')

    let scoreTable = $('<table class="table">');
    let tableHeader = $('<thead><tr><th scope="col">Player</th><th scope="col">Score</th><th></th></tr></thead>')
    scoreTable.append(tableHeader);

    let tableBody = $('<tbody>');
    scoreTable.append(tableBody);

    getResource(gameData['@controls']['gamescr:scores'].href, function(scoreboardData) {
        scoreboardData.items.forEach(function(item) {
            let row = $('<tr>');
            row.append('<td>' + item.player + '</td>');
            
            let scoreInput = $('<input/>', {
                value: item.score,
                class: 'score',
                disabled: gameData.status != 0
            }).change(function() {
                let input = $(this);
                
                updateScore(item, input.val(), function() {
                    input.removeClass('pending-change');
                });
            });
            
            scoreInput.on('input', function() {
                $(this).addClass('pending-change');
            })
            row.append($('<td>').append(scoreInput));

            let deleteBtn = $('<td><a><button class="btn btn-danger">Delete</button></a></td>');
            
            if (gameData.status != 0) {
                deleteBtn.find('button').attr('disabled', true);
            } 
            deleteBtn.click(function() {
                getResource(item['@controls'].self.href, function(scoreData) {
                    deleteResource(scoreData['@controls']['gamescr:delete'].href, function(deleteResData, status, deleteRes) {
                        if (deleteRes.status === 204) {
                            renderScoreboard(gameData);
                        }
                    });
                });
            });
            row.append(deleteBtn);

            tableBody.append(row);
        });
    });
    scoreboardContainer.append(scoreTable);
}

/**
 * Update score with API
 * Custom submit to avoid having a form
 * 
 * @param {Object} item 
 * @param {String} newScore 
 * @param {Function} callback 
 */
function updateScore(item, newScore, callback) {
    getResource(item['@controls'].self.href, function(resData) {
        const editControl = resData['@controls']['edit'];
        let data = {}

        editControl.schema.required.forEach(function(field) {
            data[field] = item[field]
        });
        data.score = parseFloat(newScore);
        sendData(editControl.href, editControl.method, data, callback, callback)
    });
}

/**
 * Renders and returns "Add player" -element
 * @param {Object} gameData 
 */
function renderAddPlayerscore(gameData) {
    const addScoreControl = gameData['@controls']['gamescr:add-score'];

    let addScoreForm = $('<form class="form-inline">');
    addScoreForm.attr('form-id', 'add-score');
    addScoreForm.attr('action', addScoreControl.href);
    addScoreForm.attr('method', addScoreControl.method);

    let playerSelect = $('<select/>', {
        class: 'form-control field-' + addScoreForm.attr('form-id'),
        'gamescr-field': 'player'
    });
    addScoreForm.append(playerSelect);
    addScoreForm.append($('<button type="submit" class="btn btn-primary">Add player</button>'))

    let gameInput = $('<input>', {
        class: 'field-' + addScoreForm.attr('form-id'),
        'gamescr-field': 'game',
        type: 'hidden'
    });
    addScoreForm.append(gameInput);

    let scoreInput = $('<input>', {
        class: 'field-' + addScoreForm.attr('form-id'),
        'gamescr-field': 'score',
        type: 'hidden'
    });
    addScoreForm.append(scoreInput);

    addScoreForm.submit(function(event) {
        event.preventDefault();
        
        gameInput.val(gameData.name);
        scoreInput.val(0);

        submitForm(event, $(this), addScoreControl.schema, function(res) {
            renderScoreboard(gameData);
        });
    });

    const getPlayersControl = gameData['@controls']['gamescr:all-players'];

    getResource(getPlayersControl.href, function(resData) {
        resData.items.forEach(function(item) {
            playerSelect.append($('<option>', {
                'value': item.name,
                'html': item.name
            }));
        })
    });
    return addScoreForm;
}
export default renderGame;
