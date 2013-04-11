市面上其實非常多 Socket.io 的文章，所以我寫在這裡其實是筆記居多，不嫌棄的話可以繼續看下去這樣。

WebSocket API
=============

這一項技術其實在 w3c 上面還是 Draft 的狀態，所以，其實你會聽到大部分的人會說，用 Flash 來作會比較穩定一點。而其實 Socket.io 官方 wiki 上面也有提到 FlashScoket.IO 的東西（笑

這個東西是 HTML5 的新的協定，簡單的來說，就是可以讓瀏覽器與後端伺服器之間，經由一個握手（handshake）的動作，來連接一條兩者之間的高速公路。這麼一來，我們就可以瀏覽器與後端伺服器之間，快速的傳遞一些資料。

    `維基百科上的 WebSocket 介紹。<http://zh.wikipedia.org/wiki/WebSocket>`

其中有提到了目前的方式，大多是以輪巡（Polling）的方式來達成，還有一種是 Comet（我實在不知道該怎麼用中文來描述他），而因為 Comet 會在後端伺服器上面佔用連線，且若是非 non-blocking 的伺服器，像是 Apache，很容易會讓 IO 爆炸。所以，後來就出現了長輪巡（Long Polling）與 iframe 改良式的 Comet。

以上的作法大多都以 AJAX（XHR）來去實做，而WebSocket 就解決了許多的問題，而且他是可以雙向溝通的！


溝通的問題
==========

目前其實最流行的方式，還是以 Long Polling 為主，最重要的原因是沒有瀏覽器相容性的問題。

BUT!

如果你的後端伺服器不支援的話，那他就只是一個單純的 Polling 而已。為什麼？

.. code-block:: js

    (function polling() {
        $.ajax({
            url: "http://server",
            type: "post",
            dataType: "json",
            timeout: 30000,
            success: function(data) {
                /* Do something */
            },
            complete: function() {
                /* Polling here. */
                polling();
            }
        });
    })();

上面我做了一件事情，就是等待 30 秒後重複發送一個 ajax 的請求到後端伺服器去。而 Long Polling 的作法是，

前端送了一個請求給後端
後端收到後，回傳資料給前端，並斷開連線
前端收到後，執行 callback，並再次發送一個請求給後端
以上的方式就是一個無窮迴圈，所以，如果後端收到後，沒有斷開連線，那麼前端就只會每 30 秒斷線重連，這樣跟一般的 Polling 其實並沒有兩樣。那，為什麼非 non-blocking 的後端伺服器不行？如果我送一個 ajax 給 Apache，那他把事情做完之後，丟一個回應給前端，也會達成 complete 的條件不是嗎？

是！

::

    <?php
    
    /* 我在 php 睡了 10 秒，再吐資料給剛剛呼叫我的 ajax */
    sleep(10);
    echo json_encode(array('status' => 'ok'));

但是，當你的後端伺服器沒有放開連線時，你只能等待前端 timeout 的時間到了，並且再次發送一次請求時，才能繼續動作。而，屆時後端的資料到底做完了沒呢？答案是：不知道，所以，使用 non-blocking 的後端伺服器多少能避開這些問題。

以上，都是單向的溝通，也是目前流行的方式。

這裡有兩篇 Comet 文章可以看一下：

* `Comet Programming: Using Ajax to Simulate Server Push<http://www.webreference.com/programming/javascript/rg28/index.html>`
* `Comet Programming: the Hidden IFrame Technique<http://www.webreference.com/programming/javascript/rg30/index.html>`


Socket.IO
=========

他做了一件事情，就是把那些溝通的方式全部整合起來，無論前端還是後端，他都幫你打包好。所以，你只要會用就可以了，這樣是不是很佛心呢！

::

    $ npm install socket.io

他所支援的傳輸方式有下列幾種，

* xhr-polling
* xhr-multipart
* htmlfile
* websocket
* flashsocket
* jsonp-polling

除了字面上有 socket 的之外，都是 Polling 與其變種方式，其中 xhr-multipart 也是，他只是把資料拆成好幾個部份來傳送而已。而其中 htmlfile 貌似是 IE 底下的東西，我在大神上面問資料的時候，看到了 ActiveXObject 這幾個字，我就不想理他了。

簡單的後端應用方式，我們可以這樣寫（以下是官方範例)

.. code-block:: js

    var io = require('socket.io').listen(8080);
    
    io.sockets.on('connection', function (socket) {
        socket.emit('news', { hello: 'world' });
        socket.on('my other event', function (data) {
            console.log(data);
        });
    });

而前端是這個樣子，

::

    <script src="/socket.io/socket.io.js"></script>
    <script>
        var socket = io.connect('http://localhost:8080');
        socket.on('news', function (data) {
            console.log(data);
            socket.emit('my other event', { my: 'data' });
        });
    </script>

我們沒有特別去指定 Socket.IO 要用什麼方式來作傳遞，所以他會自己決定，透過目前你的瀏覽器能使用什麼方式，來傳遞我們所需要的資料。這麼說，我們也可以指定傳遞方式，

.. code-block:: js

    var io = require('socket.io').listen(8080);
    
    io.configure('development', function() {
        io.set('transports', [
                'xhr-polling'
                , 'jsonp-polling'
            ]);
    });
    
    io.sockets.on('connection', function (socket) {
        socket.emit('news', { hello: 'world' });
        socket.on('my other event', function (data) {
            console.log(data);
        });
    });

以上述的例子來說，他就會使用 xhr-polling 與 jsonp-polling 兩種方式的其中一種，來傳遞我們的資料。

更多詳細設定，在官方的 wiki 當中有相當詳細的說明，

* `Configuring Socket.IO<https://github.com/LearnBoost/Socket.IO/wiki/Configuring-Socket.IO>`


至於 Socket.IO 在握手（handshake）的處理的部份，在官方 wiki 也有說明，

* `Authorization and handshaking<https://github.com/LearnBoost/socket.io/wiki/Authorizing>`

為什麼要作上述的動作呢？顧名思義就是為了認證的一些流程而衍生出來的需求。我可以在這個過程中查詢 Session 的相關資料，也可以檢查 Cookie，IP Address 或是其他需要處理的資料等等。當然，處理 Cookie 與 Session 則最為常見。


小插曲
======

我們在使用 Socket.IO 的時候，當然不可能將 listen 給綁在 port 80 上面，那是給一般伺服器使用的嘛。所以，我們就有可能會像上述的例子一樣，把他綁在 port 8080 或是之類的額外的連接埠上面。

問題來了，如果綁在其他的連接埠，那麼前端的呼叫的位址就得加上埠號，否則你的動作是會失效的。怎麼解決呢？網路上有一個很玄妙的解法，利用改寫 Socket.IO 的 xhr-polling 對於 XHRPolling 與 XHRPolling 的處理方式，來讓前端不需要加上埠號就能動作，

.. code-block:: js

    io.configure(function() {
        io.set("transports", ["xhr-polling"]);
        io.set("polling duration", 10);
        
        var path = require('path');
        var HTTPPolling = require(path.join(
            path.dirname(require.resolve('socket.io')),'lib', 'transports','http-polling')
        );
        var XHRPolling = require(path.join(
            path.dirname(require.resolve('socket.io')),'lib','transports','xhr-polling')
        );
        
        XHRPolling.prototype.doWrite = function(data) {
            HTTPPolling.prototype.doWrite.call(this);
            
            var headers = {
                'Content-Type': 'text/plain; charset=UTF-8',
                'Content-Length': (data && Buffer.byteLength(data)) || 0
            };
            
            if (this.req.headers.origin) {
                headers['Access-Control-Allow-Origin'] = '*';
                if (this.req.headers.cookie) {
                    headers['Access-Control-Allow-Credentials'] = 'true';
                }
            }
            
            this.response.writeHead(200, headers);
            this.response.write(data);
            this.log.debug(this.name + ' writing', data);
        };
    });

有興趣的人，原文在此，請參閱：How to make Socket.IO work behind nginx (mostly)

另外補上 Nginx 的相關設定，其實並不複雜，就依照一般的 Proxy 去設定即可，

.. code-block:: js

    user www-data;
    worker_processes 4;
    worker_rlimit_nofile 1024;
    
    pid /var/run/nginx.pid;
    
    
    events {
        worker_connections 1024;
        multi_accept on;
        use epoll;
    }
    
    http {
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
    
        server_names_hash_bucket_size 128;
        server_name_in_redirect on;
        client_header_buffer_size 32k;
        large_client_header_buffers 4 32k;
        client_max_body_size 8m;
    
        include /etc/nginx/mime.types;
        default_type application/octet-stream;
    
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
    
        gzip on;
        gzip_vary on;
        gzip_proxied any;
        gzip_comp_level 6;
        gzip_buffers 16 8k;
        gzip_http_version 1.1;
        gzip_disable "MSIE [1-6].(?!.*SV1)";
        gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    
        limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
        limit_req zone=one burst=100 nodelay;
    
        upstream nodejs {
            ip_hash;
            server localhost:3000;
        }
    
        server {
            listen   80;
            server_name jsdc;
    
            root /var/www/mynode;
            index index.html index.htm;
    
            location / {
            proxy_set_header X-Real-IP  $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-NginX-Proxy true;
            proxy_pass http://nodejs/;
            proxy_redirect off;
            }
        }
    }
