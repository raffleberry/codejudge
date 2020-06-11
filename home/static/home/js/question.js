var dataElem = document.getElementById('data-script');
var data = JSON.parse(dataElem.textContent);
dataElem.remove()

converter = new showdown.Converter();
$("#question").html(converter.makeHtml(data.statement));