var tableElem = document.getElementById('table-script');
var tableData = JSON.parse(tableElem.textContent);
tableElem.remove()

tableData.sort((a, b) => (a.status_code > b.status_code) ? 1 : -1);

var table = document.querySelector("table")

tableData.forEach(elem => {
    var row = document.createElement('tr');
    row.setAttribute('class', 'center aligned');
    // name
    var name = document.createElement('td');
    name.textContent = elem.name;
    row.appendChild(name);
    
    // status
    var elemTime = new Date(elem.time);
    var statusElem = document.createElement('td');

    if(elem.status_code === "X") {
        row.appendChild(statusElem);
        statusElem.innerHTML = elem.status_text + '<br>' + String(elemTime.getHours()).padStart(2, '0') + ':' + String(elemTime.getMinutes()).padStart(2, '0') + ", " + elemTime.toDateString();
    } else {
        statusElem.textContent = elem.status_text;
        var timerElem = document.createElement('span');
        timerElem.setAttribute('id', "cdtimer" + elem.id);
        timerElem.setAttribute('class', 'ui large label');
        statusElem.appendChild(document.createElement('br'));
        statusElem.appendChild(timerElem);
        row.appendChild(statusElem);
    }

    // link
    var link = document.createElement('a');
    link.href = "/" + elem.id;
    link.innerText = "Open";
    var tdLink = document.createElement('td');
    tdLink.appendChild(link);
    row.appendChild(tdLink);

    table.appendChild(row);

    // Timer code
    if (elem.status_code !== "X") {
        $("#cdtimer" + elem.id).countdown({
            until: elemTime,
            significant: 3,
            format: 'HMS',
            padZeroes: true,
            compact: true,
        });
    }
});