var dataElem = document.getElementById('data-script');
var tableData = JSON.parse(dataElem.textContent);
dataElem.remove()

tableData.sort((a, b) => (a.id > b.id) ? 1 : -1);

var table = document.querySelector("tbody");

var cnt = 0;

tableData.forEach(elem => {
    var row = document.createElement('tr');
    row.setAttribute('class', 'center aligned');
    
    // sl no.
    var slno = document.createElement('td');
    slno.textContent = (++cnt).toString();
    row.appendChild(slno);
        

    // name
    var name = document.createElement('td');
    name.textContent = elem.name;
    row.appendChild(name);
    
    // link
    var link = document.createElement('a');
    link.href = "/" + elem.id;
    link.innerText = "Open";
    var tdLink = document.createElement('td');
    tdLink.appendChild(link);
    row.appendChild(tdLink);

    table.appendChild(row);
});

function theTimer() {
    var timerElem = document.getElementById('timer-script');
    var statusText = document.getElementById('statusText');

    var timerData = JSON.parse(timerElem.textContent);

    var elemTime = new Date(timerData.time);

    var status = document.querySelector("#status");

    var statusElem = document.createElement('div');
    
    statusText.textContent = String(timerData.status_text).split(":")[0];
    if(timerData.status_code === "X") {
        statusElem.innerHTML = String(elemTime.getHours()).padStart(2, '0') + ':' + String(elemTime.getMinutes()).padStart(2, '0') + ", " + elemTime.toDateString();
    } else {
        var timerElem = document.createElement('span');
        timerElem.setAttribute('id', "cdtimer");
        statusElem.appendChild(timerElem);
    }

    status.appendChild(statusElem)

    // Timer code
    if (timerData.status_code !== "X") {
        $("#cdtimer").countdown({
            until: elemTime,
            significant: 3,
            format: 'HMS',
            padZeroes: true,
            compact: true,
        });
    }
}

theTimer();