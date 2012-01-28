var ip   = "127.0.0.1",
    port = 1337,
    http = require('http');

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World\n');
});

http.listen(port, ip);

console.log("Server running at http://" + ip + ":" + port);
