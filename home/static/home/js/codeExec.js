function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

var exeBtn = document.getElementById("execute");
var mutex = 0;

function lock() {
  mutex = 1;
  exeBtn.disabled = true;
  exeBtn.classList.add("loading");
}
var zx;
function unlock() {
  mutex = 0;
  exeBtn.disabled = false;
  exeBtn.classList.remove("loading");
}

exeBtn.addEventListener("click", event => {
  if (mutex == 0) {
    lock();
    var code = editor.getValue();
    $.ajax({
      async: true,
      url: window.location.href + "submit/",
      method: "POST",
      data: {
        code: code,
        lang: "C++",
      },
      headers: { "X-CSRFToken": csrftoken },
      success: function (data) {
        $("#resultIcon").removeClass();
        $("#error").text("");
        $("#points").text("");

        var livetable = document.getElementById("livetable");
        livetable.style.display = null;

        var livedata = document.querySelector("#livetable tbody");
        livedata.innerHTML = "";
        
        if (data.invalid == null) {

          var tr = [];

          var header = document.createElement("tr");
          var c = [document.createElement("td"), document.createElement("td"), document.createElement("td")];
          c[0].textContent = "Test Cases";
          c[1].textContent = "Points";
          c[2].textContent = "Verdict";
          for (var i = 0; i < c.length; i++) {
            header.append(c[i]);
          }
          tr.push(header);

          var index = 1;

          for (var i = 0; i < data.data.length; i++) {
            var tc = data.data[i];
            var ctr = document.createElement("tr");

            var tcn = document.createElement("td");
            tcn.textContent = "Case #" + index.toString();
            ctr.append(tcn);

            var pts = document.createElement("td");
            pts.textContent = tc.points;
            ctr.append(pts);

            var ver = document.createElement("td");
            var ico = document.createElement("i");
            if (tc.runtime_error === true) {
              ver.textContent = "Runtime Error";
              ico.classList.add("red", "ban", "icon");
              ctr.classList.add("negative");
              
            } else if (tc.tle === true) {
              ver.textContent = "Time Limit Exceeded";
              ico.classList.add("clock", "outline", "icon");
              ctr.classList.add("negative");
            } else {
              if (tc.verdict === "Accepted") {
                ver.textContent = "Accepted";
                ico.classList.add("green", "check", "icon");
                ctr.classList.add("positive");
              } else {
                ver.textContent = "Wrong Answer";
                ico.classList.add("red", "close", "icon");
                ctr.classList.add("negative");
              }
            }
            ver.prepend(ico);
            ctr.append(ver);

            tr.push(ctr);

            index += 1;
          }

          $("#points").text("You scored : " + data.points.toString() + "/100");
          
          for (var i = 0; i < tr.length; i++) {
            livedata.append(tr[i]);
          }

        } else {
          $("#points").text("Compile Error");
          $("#resultIcon").addClass("red ban icon");
          var errElem = document.createElement("tr");
          var errData = document.createElement("td");
          errData.textContent = data.data.stderr;
          errElem.append(errData);
          livedata.append(errElem);
        }

        $("html, body").animate(
          { scrollTop: $("#resultIcon").offset().top },
          500
        );
        unlock();
      },
      error: function (data) {
        $("#error").text("Internal Server Error. Contact Administrator");
        $("#points").text("");
        $("#resultIcon").addClass("red ban icon");
        unlock();
      }
    });
  }
});