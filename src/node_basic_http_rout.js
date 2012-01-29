var server,
    ip   = "127.0.0.1",
    port = 1337,
    http = require('http'),
    url = require('url');

server = http.createServer(function (req, res) {
  url_parts = url.parse(req.url);
  console.log(url_parts);
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Your rout is :' + url_parts.pathname + '\n');
});

server.listen(port, ip);

console.log("Server running at http://" + ip + ":" + port);
