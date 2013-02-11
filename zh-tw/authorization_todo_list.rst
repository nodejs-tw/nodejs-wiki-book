************
nodeJS Code Gen Party 10 - 為 ToDo List 增加第三方認證
************

這次 nodeJS Taiwan 社群 code gen party 10 活動，要接續之前 code gen party 8 活動 Ben 做的 ToDo List Sample，增加第三方認證 (OAuth) 功能。

這次的實作以 everyauth 為主，增加基本的使用者帳號密碼驗證功能，再擴充到使用 Facebook 的 OAuth 認證。

`程式碼<https://github.com/jacksctsai/authentication-todo-example>` ｜ `下載<https://github.com/jacksctsai/authentication-todo-example/downloads>`


步驟
====

自 Github clone express-todo-example 並執行

取回程式碼
::
  > git clone https://github.com/dreamerslab/express-todo-example.git
  > cd express-todo-example

安裝相依模組 (照 package.json 定義)
::
  > npm install

啟動 server
::
  > node app.js
  Express server listening on port 3001 in development mode

開啟瀏覽器，確認 server 順利執行
::
  > open http://localhost:3001

安裝認證所需 npm modules
::
  > npm install everyauth

記錄安裝的 everyauth 版本號，這次剛好是 0.2.32。

修改 package.json，增加 everyauth 模組
::
  > vim package.json

依照安裝的 everyauth 版本，修改 package.json
::
    {
        "name"         : "todo",
        "version"      : "0.0.2",
        "private"      : true,
        "dependencies" : {
            "connect"  : "1.8.7",
            "express"  : "2.5.9",
            "ejs"      : ">= 0.0.1",
            "mongoose" : "2.6.7",
            "everyauth" : "0.2.32"
        }
    }


實作帳號密碼登入
================

增加 User mongoose data model

修改 db.js 增加以下程式碼
.. code-block:: js
    var User = new Schema({
        id    : { type : String, unique : true },
        password   : String
    });
    
    mongoose.model( 'User', User );


新增 auth.js，程式碼如下
.. code-block:: js
    var everyauth = require('everyauth');
    var mongoose = require( 'mongoose' );
    var User     = mongoose.model( 'User' );
    
    everyauth.everymodule.findUserById( function (userId, callback) {
        User.
          findOne({ id : userId }).
          run( callback );
      });
    
    everyauth.password
      .getLoginPath('/login') // Login page url
      .postLoginPath('/login') // Url that your login form POSTs to
      .loginView('login')
      .authenticate( function (login, password) {
        var promise = this.Promise();
        User.
          findOne({ id : login , password : password }).
          run( function ( err, user ){
            if ( !user ) {
              err = 'Invalid login';
            }
    
            if( err ) return promise.fulfill( [ err ] );
    
            promise.fulfill( user );
          });
        return promise;
      })
      .loginSuccessRedirect('/') // Where to redirect to after login
      .getRegisterPath('/signup') // Registration url
      .postRegisterPath('/signup') // Url that your registration form POSTs to
      .registerView('signup')
      .validateRegistration( function (newUser) {
        if (!newUser.login || !newUser.password) {
          return ['Either ID or Password is missing.'];
        }
        return null;
      })
      .registerUser( function (newUser) {
        var promise = this.Promise();
        new User({
            id : newUser.login,
            password : newUser.password
        }).save( function ( err, user, count ){
          if( err ) return promise.fulfill( [ err ] );
    
          promise.fulfill( user );
        });
        return promise;
      })
      .registerSuccessRedirect('/') // Url to redirect to after a successful registration
      .loginLocals( {title: 'Login'})
      .registerLocals( {title: 'Sign up'});
    
    module.exports = {
      requireLogin: function( req, res, next ) {
        if (!req.loggedIn) {
          res.redirect( '/' );
          return;
        }
        next();
      }
    };


修改 app.js
.. code-block:: js
    /**
     * Module dependencies.
     */
    
    var express = require( 'express' );
    var everyauth = require('everyauth');
    
    var app = module.exports = express.createServer();
    
    // mongoose setup
    require( './db' );
    
    // autoentication setup
    var auth = require( './auth' );
    
    // add everyauth view helpers to express
    everyauth.helpExpress( app );
    
    var routes = require( './routes' );
    
    // Configuration
    app.configure( 'development', function (){
      app.set( 'views', __dirname + '/views' );
      app.set( 'view engine', 'ejs' );
      app.use( express.favicon());
      app.use( express.static( __dirname + '/public' ));
      app.use( express.logger());
      app.use( express.cookieParser());
      app.use( express.bodyParser());
      //app.use( routes.current_user );
      app.use( express.session({secret: 'nodeTWParty'}) );
      app.use( everyauth.middleware() );
      app.use( app.router );
      app.use( express.errorHandler({ dumpExceptions : true, showStack : true }));
    });
    
    app.configure( 'production', function (){
      app.set( 'views', __dirname + '/views' );
      app.set( 'view engine', 'ejs' );
      app.use( express.cookieParser());
      app.use( express.bodyParser());
      //app.use( routes.current_user );
      app.use( express.session({secret: 'nodeTWParty'}) );
      app.use( everyauth.middleware() );
      app.use( app.router );
      app.use( express.errorHandler());
    });
    
    // Routes
    app.get( '/', routes.index );
    app.post( '/create', auth.requireLogin, routes.create );
    app.get( '/destroy/:id', auth.requireLogin, routes.destroy );
    app.get( '/edit/:id', auth.requireLogin, routes.edit );
    app.post( '/update/:id', auth.requireLogin, routes.update );
    
    app.listen( 3001, '127.0.0.1', function (){
      console.log( 'Express server listening on port %d in %s mode', app.address().port, app.settings.env );
    });



修改 views/index.ejs 如下
::
    <h1 id="page-title"><%= title %></h1>
    
    <% if (everyauth.loggedIn) { %>
    
    <div>
      <center>
        Hi, <%= user.id %>. Good to see you! <a href="/logout">Log out</a>
      </center>
    </div>
    
    <div id="list">
      <form action="/create" method="post" accept-charset="utf-8">
        <div class="item-new">
          <input class="input" type="text" name="content" />
        </div>
      </form>
    
    <% todos.forEach( function ( todo ){ %>
      <div class="item">
        <a class="update-link" href="/edit/<%= todo._id %>" title="Update this todo item"><%= todo.content %></a>
        <a class="del-btn" href="/destroy/<%= todo._id %>" title="Delete this todo item">Delete</a>
      </div>
    <% }); %>
    
    </div>
    
    <% } else { %>
    
    <div>
      <center>
        You are not logged in. <br>
        Please <a href="/login">login</a> or <a href="/signup">sign up</a>.
      </center>
    </div>
    
    <% } %>


在 views 目錄下增加 signup.ejs 檔案
::
    <h1 id="page-title">Sign up</h1>
    
    <% if( typeof(errors) !== 'undefined' ) { %>
    <center>
      <%= errors %>
    </center>
    <% } %>
    
    <div id="list">
      <form action="/signup" method="post" accept-charset="utf-8">
        <div class="item-new">
          ID <input class="input" type="text" name="login" />
        </div>
        <div class="item-new">
          Password <input class="input" type="password" name="password" />
        </div>
        <div class="item-new">
          <input type="submit" value="Submit" />
        </div>
      </form>
    
    </div>


在 views 目錄下增加 login.ejs 檔案
::
    <h1 id="page-title">Login</h1>
    
    <% if( typeof(errors) !== 'undefined' ) { %>
    <center>
      <%= errors %>
    </center>
    <% } %>
    
    <div id="list">
      <form action="/login" method="post" accept-charset="utf-8">
        <div class="item-new">
          ID <input class="input" type="text" name="login" />
        </div>
        <div class="item-new">
          Password <input class="input" type="password" name="password" />
        </div>
        <div class="item-new">
          <input type="submit" value="Login" />
        </div>
      </form>
    
    </div>


修改 routes/index.js 檔案
.. code-block:: js
    var mongoose = require( 'mongoose' );
    var Todo     = mongoose.model( 'Todo' );
    var utils    = require( 'connect' ).utils;
    var everyauth= require( 'everyauth' );
    
    exports.index = function ( req, res, next ){
      if (!req.loggedIn) {
          res.render( 'index', {
              title : 'Express Todo Example',
              todos : []
          });
          return;
      }
    ...

還要把檔案中的 req.cookies.user_id 置換成 req.user.id
到這裡就己經完成網站初步的使用者認證機制了。


建立 Facebook Application
=========================

到 https://developers.facebook.com/apps 建立一個應用程式（名稱無所謂）

App Domains 跟 網站位址（URL）都填：http://local.host:3001/


設定 local.host 網域
====================

Facebook 不接受 localhost 的網域名稱，所以為了要測試，我們改用另一個網域名稱： local.host

要能用這個測試網域名稱，在 Linux / Mac OS X 底下可以
修改 /etc/hosts 檔案來做
::
    > sudo vim /etc/hosts

參考下面內容修改或增加一行
::
    127.0.0.1 localhost local.host

如果是 Windows，則要修改 C:\WINDOWS\system32\drivers\etc\hosts 檔案
::
    127.0.0.1 local.host


實作 Facebook 登入
==================

修改 db.js 檔案
.. code-block:: js
    // 由於 id 是 Facebook 產生的一個代碼，
    // 所以我們加一個欄位 name 當做使用者名稱
    
    var User = new Schema({
    
    id : { type : String, unique : true },
    
    name : String,
    
    profile : String,
    password : String
    
    });

修改 auth.js 檔案，增加以下內容
.. code-block:: js
    everyauth.facebook
      .appId('AppId')
      .appSecret('App Secret')
      .handleAuthCallbackError( function (req, res) {
        res.redirect('/');
      })
      .findOrCreateUser( function (session, accessToken, accessTokExtra, fbUserMetadata) {
        var promise = this.Promise();
        User.findOne({
          id : fbUserMetadata.id
        }).run( function( err, user ){
          if( err ) return promise.fulfill( [ err ] );
          if( user ) {
            promise.fulfill( user );
          } else {
            new User({
              id : fbUserMetadata.id,
              name : fbUserMetadata.name,
              profile : fbUserMetadata
            }).save( function ( err, user, count ){
              if( err ) return promise.fulfill( [ err ] );
    
              promise.fulfill( user );
            });
          }
        });
        return promise;
      })
      .redirectPath('/');

修改 views/index.ejs 檔案
::
    <% if (everyauth.loggedIn) { %>
    <div>
    <center>
    Hi, <%= user.name || user.id %>. Good to see you! <a href="/logout">Log out</a>
    </center>
    </div>
    ...
    <% } else { %>
    ...
    Login with <a href="/auth/facebook">Facebook</a>....
    
    <% } %>


測試 Facebook 登入
==================

重新以 http://local.host:3001/ 網址進入網站測試


後記
====
今天 Ben 在活動結束的時候有提到 password.js。Everyauth 雖然很多人用，照著他的說明也很容易上手，但不可否認的 everyauth 與 express.js 的依賴太深，以致程式碼會有點亂。

針對這個問題 password.js 提供了一個比較乾淨的做法，可以自由的跟其他 web framework 搭配。而且由於 passport.js 切的比較乾淨，未來在增加新的認證提供者（authentication provider）時，要改的程式碼也比較少（因為大部份的認證程式碼都放在獨立的 passport.js strategy 裡了）。

建議對於認證有興趣的朋友可以再研究一下 passport.js。AiNiOOO 原來也是從 everyauth 開始，但後來就改成 passport.js 了。
