const { run } = require('./run');
const { db } = require('./admin');

// returns points
// question -> firebase question
module.exports.evaluate = async function(question, code) {
  try {
    var doc = await db
      .collection("datasets")
      .doc(question)
      .get();
    if (doc.exists) {
      var data = doc.data()["dataset"];
      var points = 0;
      for (var i = 0; i < data.length; i++) {
        var ok = await run(
          code,
          data[i].stdin,
          "-Wall -std=c++14 -O2 -o a.out source_file.cpp",
          data[i].stdout,
          "7"
        );
        var verdict = ok.verdict;
        if (verdict == 0) points += Number(data[i].marks);
      }
      return points;
    } else {
      throw new Error("Question doesn't exists");
    }
  } catch (err) {
    console.error(err);
    return 0;
  }
}