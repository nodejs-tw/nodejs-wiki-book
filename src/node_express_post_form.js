var http = require('http'),
    url  = require('url'),
    fs   = require("fs"),
    qs   = require('querystring'),
    server;

server = http.createServer(function (req,res) {
    var urlData,
        encode   = "utf8",
        filePath = "view/express_post_example_form.html",
        formData,
        action;

    urlData = url.parse(req.url,true);
    action = urlData.pathname;
    res.writeHead(200, {"Content-Type":"text/html; charset=utf-8"});

    if (action === "/Signup") {
        formData = '';
        req.on("data", function (data) {

            formData += data;

        });

        req.on("end", function () {
            user = qs.parse(formData);
            res.end("<h1>" + user.username + "歡迎您的加入</h1><p>我們已經將會員啟用信寄至" + user.email + "</p>");
        });
    }
    else {
        fs.readFile(filePath, encode, function(err, file) {

            res.write(file);
            res.end();
        });
    }
        
});

server.listen(3000);

console.log('Server跑起來了，現在時間是:' + new Date());
