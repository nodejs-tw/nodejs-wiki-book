/**
 * @overview
 *
 * @author 
 * @version 2012/02/26
 */

    // create server.
    var app = require('express').createServer(),
        port = 1337, 
        users = [
            {name: 'Clonn'},
            {name: 'Chi'}
        ];

    app.listen(port);

    app.all('/user/:id/:op?', function(req, res, next){
        req.user = users[req.params.id];
        if (req.user) {
            next();
        } else {
            next(new Error('cannot find user ' + req.params.id));
        }
    });

    app.get('/user/:id', function(req, res){
        res.send('viewing ' + req.user.name);
    });

    app.get('/user/:id/edit', function(req, res){
        res.send('editing ' + req.user.name);
    });

    app.get('/user/:id/delete', function(req, res){
        res.send('deleting ' + req.user.name);
    });

    app.get('*', function(req, res){
        res.send('Page not found!', 404);
    });

    console.log('start express server\n');


