var fs = require("fs"),
    filename = "static/index.html",
    encode = "utf8";

fs.readFile(filename, encode, function(err, file) {
  console.log(file);
});

