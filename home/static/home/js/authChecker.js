function checkAuth() {
  var token = localStorage.getItem("codeJudgeAuthToken");
  if (token === null) {
    window.location.href = "/login.html"
  } else {
    
  }
}