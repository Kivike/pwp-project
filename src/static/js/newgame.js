
function renderNewGame(response) {
    setTitle('New Game')
    controlsElem.html(getReturnButton())

    console.log(response)

    let control = response['@controls']['gamescr:add-game']
    let props = control.schema.properties
    let nameProp = props.name

    let form =  $('<form>');

    form.append('<input type="text" placeholder="' + nameProp.description + '"></input>');

    let hostSelect = $('<select id="host-select">')
    form.append('<div>').append('<label for="host-select">Host name:</label>').append(hostSelect)

    getResource(response['@controls']['gamescr:all-players'].href, function(response) {
        response.items.forEach(function(item) {
            console.log(item);
            hostSelect.append('<option>' + item.name + '</option>');
            console.log(hostSelect)
        })
    });

    let gametypeSelect = $('<select id="gametype-select">')
    form.append('<div>')
        .append('<label for="gametype-select">Game type:</label>')
        .append(gametypeSelect)

    gametypeSelect.append('<option>-- new --</option>')

    getResource(response['@controls']['gamescr:all-gametypes'].href, function(response) {
        response.items.forEach(function(item) {
            gametypeSelect.append('<option>' + item.name + '</option>')
        })

        let newGametype = $('div')
        newGametype.append('<label for="gametype-name">Name of game type</label>')
        newGametype.append('<input id="gametype-name">')

        newGametype.append('<label for="gametype-min-players>Minimum players (optional):</label>')
        newGametype.append('<input id="gametype-min-players">')

        newGametype.append('<label for="gametype-m-players>Minimum players (optional):</label>')
        newGametype.append('<input id="gametype-min-players">')

    })
    contentElem.html(form)
}