const axios = require("axios");
/*
    "https://rextester.com/rundotnet/api"
    returns a json with the following data :-
    Result = Output of a program
    Warnings = Warnings, if any, as one string
    Errors = Errors, if any, as one string
    Stats = Execution stats as one string
    {
      "verdict" : `0 = right ans, 1 = wrong ans, 2 = time limit exceed, 3 = Runtime Error`
    }

    for c++ "args" : "-Wall -std=c++14 -O2 -o a.out source_file.cpp"
            "lang" : "7"
*/
  /*
  verdict :-
    -1 = compile error
    0 = AC
    1 = WA
    2 = TLE
    3 = RUNTIME ERROR
    4 = API error
  { vedict, status }
*/

module.exports.run = async function(code, input, args, output, lang) {
  try {
  var payload = {
    LanguageChoice: lang,
    Program: code,
    Input: input,
    CompilerArgs: args
  };
  var resp = await axios.post("https://rextester.com/rundotnet/api", payload);
  var verdict = -1, status = "";
  if (resp.data.Errors != null) {
    if (resp.data.Errors.indexOf("SIGKILL") !== -1) {
      verdict = 2;
    } else if (resp.data.Errors.indexOf("SIGSEGV") !== -1) {
      verdict = 3;
    }
    status = resp.data.Errors;
  } else if (resp.data.Result.trim() !== output.trim()) {
    verdict = 1;
    status = "WA";
  } else {
    verdict = 0;
    status = "AC";
  }
  return {
    verdict,
    status
  };
} catch(error) {
  console.log("Error in run()");
  console.log(error);
  return {
    verdict: 4,
    status: error
  }
}
};