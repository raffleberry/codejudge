const { db } = require("./admin");

const { run } = require("./run");

const { evaluate } = require("./evaluate");

// lang = 7 for c++
// Response:-
// status = 0, if successfully ran
// status = -1, if invalid session
// status = -2, if invalid question
// status = -3, if inactive session
// status = -4, if not authorized
// status = -5, if compile error
async function submit(req, res) {
  try {
    var code = req.body.code,
      lang = req.body.lang,
      sessionId = req.body.sessionId,
      handle = req.body.handle,
      question = req.body.question,
      sampleIn = req.body.sampleIn,
      sampleOut = req.body.sampleOut;

    var sessionDetails = await db.doc(`/session/${sessionId}`).get();

    if (!sessionDetails.exists) {
      return res.json({ status: "-1" });
    } else {
      var data = sessionDetails.data();
      var questions = data["selectedQuestions"];
      var students = data["students"];

      if (data["status"] !== "ongoing") {
        return res.json({ status: "-3" });
      }

      var auth = false;
      for (var i = 0; i < students.length; i++) {
        if (handle === students[i]) {
          auth = true;
          break;
        }
      }
      if (!auth) {
        return res.json({ status: "-4" });
      }
      var valid = false;
      for (var i = 0; i < questions.length; i++) {
        if (questions[i] === question) {
          valid = true;
          break;
        }
      }
      if (!valid) {
        return res.json({ status: "-2" });
      }
    }
    var verd = await run(
      code,
      sampleIn,
      "-Wall -std=c++14 -O2 -o a.out source_file.cpp",
      sampleOut,
      lang
    );
    if (verd.verdict !== 0) {
      return res.status(200).json({ status: "-5", compilerError: verd.status });
    }

    var points = await evaluate(question, code);

    var timestamp = Date.now();

    db.collection("submissions").doc().set({
      code,
      points,
      question,
      handle,
      sessionId,
      submitTime: timestamp
    });

    

    return res.json({ status: "0", points: points });
  } catch (err) {
    console.log(err);
    return res.status(500).json(err);
  }
}

module.exports = submit;
