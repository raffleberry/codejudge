const { db } = require("./admin");

exports.questions = async (req, res) => {
  console.log(req.body.qid);
  db.collection("questions")
    .where("questionId", "==", req.body.qid)
    .get().then(doc => {
      if (doc.docs.length === 0) {
        res.status(404).json();
      } else {
        res.status(200).json(doc.docs[0].data());
      }
    })
    .catch(error => res.status(500).json({error}));
};
