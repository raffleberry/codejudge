var exeBtn = document.getElementById("execute");
var mutex = 0;

function lock() {
  mutex = 1;
  exeBtn.disabled = true;
  exeBtn.classList.add("loading");
}

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
      crossDomain: true,
      url: authUrl + "/submit",
      headers: {
        authorization: "Bearer " + localStorage.getItem("codeJudgeAuthToken")
      },
      method: "POST",
      data: {
        code: code,
        lang: "7",
        sessionId: localStorage.getItem("currentSession"),
        handle: localStorage.getItem("currentStudent"), //implement this
        sampleIn: $("code")[0].innerText,
        sampleOut: $("code")[1].innerText,
        question: localStorage.getItem("currentQuestion")
      },
      success: function(data) {
        $("#resultIcon").removeClass();
        if (data.status === "0") {
          $("#points").text("You scored : " + data.points.toString() + "/100");
          $("#resultIcon").addClass("green check circle outline  icon");
          $("#error").text("");
        } else if (data.status === "-5") {
          $("#error").text(data.compilerError);
          $("#points").text("");
          $("#resultIcon").addClass("red ban icon");
        }
        $("html, body").animate(
          { scrollTop: $("#resultIcon").offset().top },
          500
        );
        unlock();
      },
      error: function(data) {
        if (data.status === 403) {
          window.location.href = "/login.html";
        } else {
          $("#error").text("Internal Server Error. Contact Administrator");
          $("#points").text("");
          $("#resultIcon").addClass("red ban icon");
        }
        unlock();
      }
    });
  }
});
