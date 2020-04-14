$("#logOut").on("click", () => {
  localStorage.removeItem("codeJudgeAuthToken");
  localStorage.removeItem("sessionData");
  localStorage.removeItem("currentSession");
  localStorage.removeItem("currentQuestion");
  // localStorage.removeItem();
  // localStorage.removeItem();
  window.location.href = "/login.html";
});