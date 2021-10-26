const { db } = require("./admin");

exports.sessionStart = async (req, res) => {
  try {
    req.body.batch.split("|");
    const newSession = {};
    db.collection("session")
      .doc()
      .set(newSession);
  } catch (err) {
    res.status(503).send("Service Unavailable");
  }
};

exports.sessionEnd = async (req, res) => {
  res.send("okok");
};

exports.sessionActive = (req, res) => {
  db.collection("session")
    .where("status", "==", "ongoing")
    .get()
    .then(query => {
      var activeSessions = [];
      query.forEach(doc => {
        activeSessions.push(doc.data());
      });
      res.json({ handle: req.body.handle, data : activeSessions });
    })
    .catch(error => res.status(500).json(error));
};
