/**
 * @overview
 *
 * @author Caesar Chi
 * @blog clonn.blogspot.com
 * @version 2012/02/26
 */

    // create server.
    var app = require('express').createServer(),
        port = 1337; 

    app.listen(port);

    // normal style
    app.get('/', function(req, res){
        res.send('hello world');
    });

    app.get('/test', function(req, res){
        res.send('test render');
    });

    // parameter style
    app.get('/user/:id', function(req, res){
        res.send('user: ' + req.params.id);
    });

    app.get('/:number', function(req, res){
        res.send('number: ' + req.params.number);
    });

    // REGX style
    app.get(/^\/ip?(?:\/(\d{2,3})(?:\.(\d{2,3}))(?:\.(\d{2,3})))?/, function(req, res){
        res.send(req.params);
    });

    app.get('*', function(req, res){
        res.send('Page not found!', 404);
    });

    console.log('start express server\n');


