/**
 * Module dependencies.
 */
var express = require('express');
var app = express.createServer();
var port = 1337;

function middleHandler(req, res, next) {
    console.log("execute middle ware");
    next();
}

app.use(function (req, res, next) {
    console.log("first middle ware");                                                                                                             
    next();
});

app.use(function (req, res, next) {
    console.log("second middle ware");                                                                                                             
    next();
});

app.get('/', middleHandler, function (req, res) {
    console.log("end middleware function");
    res.send("page render finished");
});

app.listen(port);
console.log('start server');
