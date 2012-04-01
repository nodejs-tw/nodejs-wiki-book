/**
 * Module dependencies.
 */
var express = require('express');
var app = express.createServer();
var port = 3000;
// Example requests:
//     curl http://localhost:3000/user/0
//     curl http://localhost:3000/user/0/edit
//     curl http://localhost:3000/user/1
//     curl http://localhost:3000/user/1/edit (unauthorized since this is not you)
//     curl -X DELETE http://localhost:3000/user/0 (unauthorized since you are not an admin)
// Dummy users
var users = [{
  id: 0,
  name: 'tj',
  email: 'tj@vision-media.ca',
  role: 'member'
}, {
  id: 1,
  name: 'ciaran',
  email: 'ciaranj@gmail.com',
  role: 'member'
}, {
  id: 2,
  name: 'aaron',
  email: 'aaron.heckmann+github@gmail.com',
  role: 'admin'
}];

console.log(global);
function loadUser(req, res, next) {
  // You would fetch your user from the db
    console.log("load user function");
  var user = users[req.params.id];
  if (user) {
    req.user = user;
    next();
  } else {
    next(new Error('Failed to load user ' + req.params.id));
  }
}

function andRestrictToSelf(req, res, next) {
  // If our authenticated user is the user we are viewing
  // then everything is fine :)
  if (req.authenticatedUser.id == req.user.id) {
    next();
  } else {
    // You may want to implement specific exceptions
    // such as UnauthorizedError or similar so that you
    // can handle these can be special-cased in an error handler
    // (view ./examples/pages for this)
    next(new Error('Unauthorized'));
  }
}

function andRestrictTo(role) {
  return function (req, res, next) {
    if (req.authenticatedUser.role == role) {
      next();
    } else {
      next(new Error('Unauthorized'));
    }
  }
}
// Middleware for faux authentication
// you would of course implement something real,
// but this illustrates how an authenticated user
// may interact with middleware
app.use(function (req, res, next) {
  console.log("first middle ware");
  req.authenticatedUser = users[0];
  next();
});
app.use(function (req, res, next) {
  console.log("second middle ware");
  //req.authenticatedUser = users[0];
  next();
});
app.get('/', function (req, res) {
  console.log(" \/ function");
  res.redirect('/user/0');
});
app.get('/user/:id', loadUser, function (req, res) {
  res.send('Viewing user ' + req.user.name);
});
app.get('/user/:id/edit', loadUser, andRestrictToSelf, function (req, res) {
  res.send('Editing user ' + req.user.name);
});
app.del('/user/:id', loadUser, andRestrictTo('admin'), function (req, res) {
  res.send('Deleted user ' + req.user.name);
});


function testfn(req, res, next) {
    console.log("test fn");
    next();
}

app.get('/test/:id', loadUser, testfn, function (req, res) {
  console.log("get function.");
  res.send('Viewing user ' + req.user.name);
});



app.listen(port);
console.log('Express app started on port 3000');
