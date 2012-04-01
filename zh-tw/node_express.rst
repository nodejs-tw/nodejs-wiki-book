************
Express 介紹
************

在前面的node.js 基礎當中介紹許多許多開設http 的使用方法及介紹，以及許多基本的node.js 基本應用。

接下來要介紹一個套件稱為express [Express] (http://expressjs.com/) ，這個套件主要幫忙解決許多node.js http server 所需要的基本服務，讓開發http service 變得更為容易，不需要像之前需要透過層層模組（module）才有辦法開始編寫自己的程式。

這個套件是由TJ Holowaychuk 製作而成的套件，裡面包含基本的路由處理(route)，http 資料處理（GET/POST/PUT），另外還與樣板套件（js html template engine）搭配，同時也可以處理許多複雜化的問題。

=Express 安裝=

安裝方式十分簡單，只要透過之前介紹的 NPM 就可以使用簡單的指令安裝，指令如下，

.. code-block::

	npm install -g express

這邊建議需要將此套件安裝成為全域模組，方便日後使用。

=Express 基本操作=

express 的使用也十分簡單，先來建立一個基本的hello world ，

.. code-block:: javascript

	var app = require('express').createServer(),
    	port = 1337; 

	app.listen(port);

	app.get('/', function(req, res){
	    res.send('hello world');
	});

	console.log('start express server\n');

可以從上面的程式碼發現，基本操作與node.js http 的建立方式沒有太大差異，主要差在當我們設定路由時，可以直接透過 app.get 方式設定回應與接受方式。

==Express 路由處理==

Express 對於 http 服務上有許多包裝，讓開發者使用及設定上更為方便，例如有幾個路由設定，那我們就統一藉由 app.get 來處理，

.. code-block:: javascript

	// ... Create http server
    
    app.get('/', function(req, res){
        res.send('hello world');
    });

    app.get('/test', function(req, res){                                                                                                                                       
        res.send('test render');
    });

    app.get('/user/', function(req, res){
        res.send('user page');
    });

如上面的程式碼所表示，app.get 可以帶入兩個參數，第一個是路徑名稱設定，第二個為回應函式(call back function)，回應函式裡面就如同之前的 createServer 方法，裡面包含 request， response 兩個物件可供使用。使用者就可以透過瀏覽器，輸入不同的url 切換到不同的頁面，顯示不同的結果。

路由設定上也有基本的配對方式，讓使用者從瀏覽器輸入的網址可以是一個變數，只要符合型態就可以有對應的頁面產出，例如，

.. code-block:: javascript

	// ... Create http server

    app.get('/user/:id', function(req, res){                                                                                                                                   
        res.send('user: ' + req.params.id);
    }); 

    app.get('/:number', function(req, res){
        res.send('number: ' + req.params.number);
    }); 

裡面使用到:number ，從網址輸入之後就可以直接使用 req.params.number 取得所輸入的資料，變成url 參數使用，當然前面也是可以加上路徑的設定， /user/:id，在瀏覽器上路徑必須符合 /user/xxx，透過 req.params.id 就可以取到 xxx這個字串值。

另外，express 參數處理也提供了路由參數配對處理，也可以透過正規表示法作為參數設定，

.. code-block:: javascript

    var app = require('express').createServer(),
        port = 1337; 

    app.listen(port);

	app.get(/^\/ip?(?:\/(\d{2,3})(?:\.(\d{2,3}))(?:\.(\d{2,3}))(?:\.(\d{2,3})))?/, function(req, res){                                                                                            
	    res.send(req.params);
	});

上面程式碼，可以發現後面路由設定的型態是正規表示法，裡面設定格式為 /ip 之後，必須要加上ip 型態才會符合資料格式，同時取得ip資料已經由正規表示法將資料做分群，因此可以取得ip的四個數字。

此程式執行之後，可以透過瀏覽器測試，輸入網址為 localhost:3000/ip/255.255.100.10，可以從頁面獲得資料，

.. code-block::

	[
		"255",
		"255",
		"100",
		"10"
	]

此章節全部範例程式碼如下，

.. literalinclude:: ../src/node_express_basic.js
   :language: javascript

==Express middleware==

Express 裡面有一個十分好用的應用概念稱為middleware，可以透過 middleware 做出複雜的效果，同時上面也有介紹 next 方法參數傳遞，就是靠 middleware 的概念來傳遞參數，讓開發者可以明確的控制程式邏輯。

.. code-block:: javascript
    
    // .. create http server

    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(express.session());

上面都是一種 middleware 的使用方式，透過 app.use 方式裡面載入函式執行方法，回應函式會包含三個基本參數，response， request， next，其中next 表示下一個 middleware 執行函式，同時會自動將預設三個參數繼續帶往下個函式執行，底下有個實驗，

.. literalinclude:: ../src/node_express_middle_simple.js
   :language: javascript

上面的片段程式執行後，開啟瀏覽器，連結上 localhost:1337/，會發現伺服器回應結果順序如下，

::

    first middle ware
    second middle ware
    execute middle ware
    end middleware function

從上面的結果可以得知，剛才設定的 middleware 都生效了，在 app.use 設定的 middleware 是所有url 皆會執行方法，如果有指定特定方法，就可以使用 app.get 的 middleware 設定，在 app.get 函式的第二個參數，就可以帶入函式，或者是匿名函式，只要函式裡面最後會接受 request, response, next 這三個參數，同時也有正確指定 next 函式的執行時機，最後都會執行到最後一個方法，當然開發者也可以評估程式邏輯要執行到哪一個階段，讓邏輯可以更為分明。

==Express 路由應用==

在實際開發上可能會遇到需要使用參數等方式，混和變數一起使用，express 裡面提供了一個很棒的處理方法 app.all 這個方式，可以先採用基本路由配對，再將設定為每個不同的處理方式，開發者可以透過這個方式簡化自己的程式邏輯，

.. literalinclude:: ../src/node_express_basic_app.js
   :language: javascript

內部宣告一組預設的使用者分別給予名稱設定，藉由app.all 這個方法，可以先將路由雛形建立，再接下來設定 app.get 的路徑格式，只要符合格式就會分配進入對應的方法中，像上面的程式當中，如果使用者輸入路徑為 /user/0 ，除了執行 app.all 程式之後，執行next 方法就會對應到路徑設定為 /user/:id 的這個方法當中。如果使用者輸入路徑為 /user/0/edit ，就會執行到 /user/:id/edit 的對應方法。

==Express GET 應用範例 ==

我們準備一個使用GET方法傳送資料的表單。

.. literalinclude:: ../src/view/express_get_example_form.html
   :language: javascript

這個表單沒有什麼特別的地方，我們只需要看第9行，form使用的method是GET，然後action是"http://localhost:3000/Signup"，等一下我們要來撰寫/Signup這個URL Path的處理程式。

===處理 Signup 行為===

我們知道所謂的GET方法，會透過URL來把表單的值給帶過去，以上面的表單來說，到時候URL會以這樣的形式傳遞

::

    http://localhost:3000/Signup?username=xxx&email=xxx

所以要能處理這樣的資料，必須有以下功能:

 * 解析URL
 * 辨別動作是Signup
 * 解析出username和email

一旦能取得username和email的值，程式就能加以應用了。

處理 Signup 的程式碼雛形，

.. code-block:: javascript

    // load module
    var url  = require('url');

    urlData = url.parse(req.url,true);
    action = urlData.pathname;
    res.writeHead(200, {"Content-Type":"text/html; charset=utf-8"});

    if (action === "/Signup") {
       user = urlData.query;
       res.end("<h1>" + user.username + "歡迎您的加入</h1><p>我們已經將會員啟用信寄至" + user.email + "</p>");
    }

首先需要加載 url module，它是用來協助我們解析URL的模組，接著使用 url.parse 方法，第一個傳入url 字串變數，也就是req.url。另外第二個參數的用意是，設為ture則引進 querystring模組來協助處理，預設是false。它影響到的是 urlData.query，設為true會傳回物件，不然就只是一般的字串。url.parse 會將字串內容整理成一個物件，我們把它指定給urlData。

action 變數作為記錄pathname，這是我們稍後要來判斷目前網頁的動作是什麼。接著先將 html 表頭資訊 (Header)準備好，再來判斷路徑邏輯，如果是 */Signup* 這個動作，就把urlData.query裡的資料指定給user，然後輸出user.username和user.email，把使用者從表單註冊的資料顯示於頁面中。

最後進行程式測試，啟動 node.js 主程式之後，開啟瀏覽器就會看到表單，填寫完畢按下送出，就可以看到結果了。

完整 node.js 程式碼如下，

.. literalinclude:: ../src/node_express_get_form.js
   :language: javascript


==本章節原始資料==

 * [Node.jS初學者筆記(1)-用GET傳送資料] (http://ithelp.ithome.com.tw/question/10087402)

