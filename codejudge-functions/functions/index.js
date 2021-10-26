const functions = require("firebase-functions");
const express = require("express");
const bodyParser = require("body-parser");
const FBAuth = require("./util/fbAuth");
const submit = require("./util/submit");
const app = express();

//CORS
const cors = require("cors");
app.use(cors());
app.options("*", cors());

const { signup, login } = require("./handlers/users");
const { sessionStart, sessionEnd, sessionActive } = require("./util/session");
const { questions } = require("./util/questions");

app.use(bodyParser.urlencoded({ extended: false }));
//extend limit for bigger codes
app.use(bodyParser.json());

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.post("/submit", FBAuth, submit);
app.post("/signup", signup);
app.post("/login", login);
app.post("/auth", FBAuth, (req, res) => {
  res.status(200).json({ status: "success", handle: req.body.handle });
});

// app.post("/session", session);

//sessions
app.post("/session/start", sessionStart);
app.post("/session/end", sessionEnd);
app.post("/session/active", FBAuth, sessionActive);

app.post("/questions", questions);

app.post("/pushQuestion", (req, res) => {
  const { db } = require("./util/admin");
  var ref = db.collection("questions").doc();
  db.collection("questions")
    .doc(ref.id)
    .set({
      questionId: ref.id,
      statement: req.body.statement
    });

  res.json({});
});
app.post("/pushData", (req, res) => {
  const { db } = require("./util/admin");
  // db.collection("datasets").doc("nHBfqTc0Jwr4H88oCYS8").set(req.body);
  res.json({});
});

app.post("/scoreboard", (req, res) => {
  const { db } = require("./util/admin");
  var sessionId = req.body.sessionId;
  var questionsList = req.body.questionsList;
  var handleList = req.body.handleList;
  if (
    sessionId === undefined ||
    questionsList === undefined ||
    handleList === undefined
  )
    return res.status(400).json({});
  db.collection("submissions")
    .where("sessionId", "==", sessionId)
    .get()
    .then(data => {
      var submissions = [];
      data.forEach(doc => {
        submissions.push(doc.data());
      });
      var scoreboard = [];
      //SHITCODE
      for (var i = 0; i < handleList.length; i++) {
        var handle = {
          handle: handleList[i],
          totalPoints: 0,
          totalTime: 0
        };
        for (var j = 0; j < questionsList.length; j++) {
          var question = {
            points: 0,
            submitTime: 100000000000000000
          };
          var attempts = 0;
          for (var k = 0; k < submissions.length; k++) {
            if (
              submissions[k].handle === handleList[i] &&
              submissions[k].question === questionsList[j]
            ) {
              attempts += 1;
              if (question.points < submissions[k].points) {
                question = submissions[k];
              }
              if (
                question.points === submissions[k].points &&
                question.submitTime > submissions[k].submitTime
              ) {
                question = submissions[k];
              }
            }
          }
          question["attempts"] = attempts;
          handle.totalPoints += question.points;
          handle.totalTime += question.submitTime;
          handle[questionsList[j]] = question;
        }
        scoreboard.push(handle);
      }
      res.status(200).json({ scoreboard });
    })
    .catch(error => {
      console.error(error);
      res.status(500).json({ error });
    });
});

exports.api = functions.https.onRequest(app);
