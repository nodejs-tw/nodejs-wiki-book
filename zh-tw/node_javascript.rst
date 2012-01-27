********************
JavaScript 與 NodeJS
********************

其實使用 JavaScript 在網頁端與伺服器端的差距並不大，
但是為了使 NodeJS 可以發揮他最強大的能力，
有一些知識還是必要的，
所以還是針對這些主題介紹一下。
其中 Event Loop、Scope 以及 Callback 其實是比較需要了解的基本知識，
cps、currying、flow control是更進階的技巧與應用。

Event Loop
==========

可能很多人在寫Javascript時，並不知道他是怎麼被執行的。這個時候可以參考一下jQuery作者John Resig一篇好文章，介紹事件及timer怎麼在瀏覽器中執行：How JavaScript Timers Work。通常在網頁中，所有的Javascript執行完畢後（這部份全部都在global scope跑，除非執行函數），接下來就是如John Resig解釋的這樣，所有的事件處理函數，以及timer執行的函數，會排在一個queue結構中，利用一個無窮迴圈，不斷從queue中取出函數來執行。這個就是event loop。

（除了John Resig的那篇文章，Nicholas C. Zakas的 "Professional Javascript for Web Developer 2nd edition" 有一個試閱本：http://yuiblog.com/assets/pdf/zakas-projs-2ed-ch18.pdf，598頁剛好也有簡短的說明）

所以在Javascript中，雖然有非同步，但是他並不是使用執行緒。所有的事件或是非同步執行的函數，都是在同一個執行緒中，利用event loop的方式在執行。至於一些比較慢的動作例如I/O、網頁render, reflow等，實際動作會在其他執行緒跑，等到有結果時才利用事件來觸發處理函數來處理。這樣的模型有幾個好處：
沒有執行緒的額外成本，所以反應速度很快
不會有任何程式同時用到同一個變數，不必考慮lock，也不會產生dead lock
所以程式撰寫很簡單
但是也有一些潛在問題：
任一個函數執行時間較長，都會讓其他函數更慢執行（因為一個跑完才會跑另一個）
在多核心硬體普遍的現在，無法用單一的應用程式instance發揮所有的硬體能力
用NodeJS撰寫伺服器程式，碰到的也是一樣的狀況。要讓系統發揮event loop的效能，就要盡量利用事件的方式來組織程式架構。另外，對於一些有可能較為耗時的操作，可以考慮使用 process.nextTick 函數來讓他以非同步的方式執行，避免在同一個函數中執行太久，擋住所有函數的執行。

如果想要測試event loop怎樣在「瀏覽器」中運行，可以在函數中呼叫alert()，這樣會讓所有Javascript的執行停下來，尤其會干擾所有使用timer的函數執行。有一個簡單的例子，這是一個會依照設定的時間間隔嚴格執行動作的動畫，如果時間過了就會跳過要執行的動作。點按圖片以後，人物會快速旋轉，但是在旋轉執行完畢前按下「delay」按鈕，讓alert訊息等久一點，接下來的動畫就完全不會出現了。

Scope 與 Closure
================

要快速理解 JavaScript 的 Scope（變數作用範圍）原理，只要記住他是Lexical Scope就差不多了。簡單地說，變數作用範圍是依照程式定義時（或者叫做程式文本？）的上下文決定，而不是執行時的上下文決定。

為了維護程式執行時所依賴的變數，即使執行時程式運行在原本的scope之外，他的變數作用範圍仍然維持不變。這時程式依賴的自由變數（定義時不是local的，而是在上一層scope定義的變數）一樣可以使用，就好像被關閉起來，所以叫做Closure。用程式看比較好懂：

.. code-block:: js

    function outter(arg1) {
        //arg1及free_variable1對inner函數來說，都是自由變數
        var free_variable1 = 3;
        return function inner(arg2) {
            var local_variable1 =2;//arg2及local_variable1對inner函數來說，都是本地變數
            return arg1 + arg2 + free_variable + local_variable1;
        };
    }

var a = outter(1);//變數a 就是outter函數執行後返回的inner函數
var b = a(4);//執行inner函數，執行時上下文已經在outter函數之外，但是仍然能正常執行，而且可以使用定義在outter函數裡面的arg1及free_variable1變數
console.log(b);//結果10

在Javascript中，scope最主要的單位是函數（另外有global及eval），所以有可能製造出closure的狀況，通常在形式上都是有巢狀的函數定義，而且內側的函數使用到定義在外側函數裡面的變數。

Closure有可能會造成記憶體洩漏，主要是因為被參考的變數無法被垃圾收集機制處理，造成佔用的資源無法釋放，所以使用上必須考慮清楚，不要造成意外的記憶體洩漏。（在上面的例子中，如果a一直未執行，使用到的記憶體就不會被釋放）

跟透過函數的參數把變數傳給函數比較起來，Javascript Engine會比較難對Closure進行最佳化。如果有效能上的考量，這一點也需要注意。

Callback
========

要介紹 Callback 之前，
要先提到 JavaScript 的特色。

JavaScript 是一種函數式語言（functional language），所有Javascript語言內的函數，都是高階函數(higher order function，這是數學名詞，計算機用語好像是first class function，意指函數使用沒有任何限制，與其他物件一樣)。也就是說，函數可以作為函數的參數傳給函數，也可以當作函數的返回值。這個特性，讓Javascript的函數，使用上非常有彈性，而且功能強大。

callback在形式上，其實就是把函數傳給函數，然後在適當的時機呼叫傳入的函數。Javascript使用的事件系統，通常就是使用這種形式。NodeJS中，有一個物件叫做EventEmitter，這是NodeJS事件處理的核心物件，所有會使用事件處理的函數，都會「繼承」這個物件。（這裡說的繼承，實作上應該像是mixin）他的使用很簡單：
可以使用 物件.on(事件名稱, callback函數) 或是 物件.addListener(事件名稱, callback函數) 把你想要處理事件的函數傳入
在 物件 中，可以使用 物件.emit(事件名稱, 參數...) 呼叫傳入的callback函數
這是Observer Pattern的簡單實作，而且跟在網頁中使用DOM的addEventListener使用上很類似，也很容易上手。不過NodeJS是大量使用非同步方式執行的應用，所以程式邏輯幾乎都是寫在callback函數中，當邏輯比較複雜時，大量的callback會讓程式看起來很複雜，也比較難單元測試。舉例來說：

var p_client = new Db('integration_tests_20', new Server("127.0.0.1", 27017, {}), {'pk':CustomPKFactory});
p_client.open(function(err, p_client) {
  p_client.dropDatabase(function(err, done) {
    p_client.createCollection('test_custom_key', function(err, collection) {
      collection.insert({'a':1}, function(err, docs) {
        collection.find({'_id':new ObjectID("aaaaaaaaaaaa")}, function(err, cursor) {
          cursor.toArray(function(err, items) {
            test.assertEquals(1, items.length);
            p_client.close();
          });
        });
      });
    });
  });
});

這是在網路上看到的一段操作mongodb的程式碼，為了循序操作，所以必須在一個callback裡面呼叫下一個動作要使用的函數，這個函數裡面還是會使用callback，最後就形成一個非常深的巢狀。

這樣的程式碼，會比較難進行單元測試。有一個簡單的解決方式，是盡量不要使用匿名函數來當作callback或是event handler。透過這樣的方式，就可以對各個handler做單元測試了。例如：

var http = require('http');
var tools = {
 cookieParser: function(request, response) {
 if(request.headers['Cookie']) {
 //do parsing
 }
 }
};
var server = http.createServer(function(request, response) {
 this.emit('init', request, response);
 //...
});
server.on('init', tools.cookieParser);
server.listen(8080, '127.0.0.1');

更進一步，可以把tools改成外部module，例如叫做tools.js：

module.exports = {
 cookieParser: function(request, response) {
 if(request.headers['Cookie']) {
 //do parsing
 }
 }
};

然後把程式改成：

var http = require('http');

var server = http.createServer(function(request, response) {
 this.emit('init', request, response);
 //...
});
server.on('init', require('./tools').cookieParser);
server.listen(8080, '127.0.0.1');

這樣就可以單元測試cookieParser了。例如使用nodeunit時，可以這樣寫：

var testCase = require('nodeunit').testCase;
module.exports = testCase({
    "setUp": function(cb) {
     this.request = {
     headers: {
     Cookie: 'name1:val1; name2:val2'
     }
     };
     this.response = {};
     this.result = {name1:'val1',name2:'val2'};
        cb();
    },
    "tearDown": function(cb) {
        cb();
    },
    "normal_case": function(test) {
     test.expect(1);
     var obj = require('./tools').cookieParser(this.request, this.response);
     test.deepEqual(obj, this.result);
     test.done();
    }
});

善於利用模組，可以讓程式更好維護與測試。

CPS（Continuation-Passing Style）
================================

cps是callback使用上的特例，形式上就是在函數最後呼叫callback，這樣就好像把函數執行後把結果交給callback繼續運行，所以稱作continuation-passing style。利用cps，可以在非同步執行的情況下，透過傳給callback的這個cps callback來獲知callback執行完畢，或是取得執行結果。例如：

<html>
<body>
<div id="panel" style="visibility:hidden"></div>
</body>
</html>
<script>
var request = new XMLHttpRequest();
request.open('GET', 'test749.txt?timestamp='+new Date().getTime(), true);
request.addEventListener('readystatechange', function(next){
 return function() {
 if(this.readyState===4&&this.status===200) {
 next(this.responseText);//<==傳入的cps callback在動作完成時執行並取得結果進一步處理
 }
 };
}(function(str){//<==這個匿名函數就是cps callback
 document.getElementById('panel').innerHTML=str;
 document.getElementById('panel').style.visibility = 'visible';
}), false);
request.send();
</script>

進一步的應用，也可以參考2-6 流程控制。


函數返回函數與Currying
====================

前面的cps範例裡面，使用了函數返回函數，這是為了把cps callback傳遞給onreadystatechange事件處理函數的方法。（因為這個事件處理函數並沒有設計好會傳送/接收這樣的參數）實際會執行的事件處理函數其實是內層返回的那個函數，之外包覆的這個函數，主要是為了利用Closure，把next傳給內層的事件處理函數。這個方法更常使用的地方，是為了解決一些scope問題。例如：

<script>
var accu=0,count=10;
for(var i=0; i<count; i++) {
  setTimeout(
    function(){
      count--;
      accu+=i;
      if(count<=0)
        console.log(accu)
    }
  , 50)
}
</script>

最後得出的結果會是100，而不是想像中的45，這是因為等到setTimeout指定的函數執行時，變數i已經變成10而離開迴圈了。要解決這個問題，就需要透過Closure來保存變數i：

<script>
var accu=0,count=10;
for(var i=0; i<count; i++) {
  setTimeout(
    function(i) {
     return function(){
     count--;
       accu+=i;
       if(count<=0)
         console.log(accu)
     };
   }(i)
  , 50)
}
//淺藍色底色的部份，是跟上面例子不一樣的地方
</script>

函數返回函數的另外一個用途，是可以暫緩函數執行。例如：

function add(m, n) {
  return m+n;
}
var a = add(20, 10);
console.log(a);

add這個函數，必須同時輸入兩個參數，才有辦法執行。如果我希望這個函數可以先給它一個參數，等一些處理過後再給一個參數，然後得到結果，就必須用函數返回函數的方式做修改：

function add(m) {
  return function(n) {
    return m+n;
  };
}
var wait_another_arg = add(20);//先給一個參數
var a = function(arr) {
  var ret=0;
  for(var i=0;i<arr.length;i++) ret+=arr[i];
  return ret;
}([1,2,3,4]);//計算一下另一個參數
var b = wait_another_arg(a);//然後再繼續執行
console.log(b);

像這樣利用函數返回函數，使得原本接受多個參數的函數，可以一次接受一個參數，直到參數接收完成才執行得到結果的方式，有一個學名就叫做...Currying

綜合以上許多奇技淫巧，就可以透過用函數來處理函數的方式，調整程式流程。接下來看看...


流程控制
=======

（以sync方式使用async函數、避開巢狀callback循序呼叫async callback等奇技淫巧）

建議參考：

* http://howtonode.org/control-flow
* http://howtonode.org/control-flow-part-ii
* http://howtonode.org/control-flow-part-iii
* http://blog.mixu.net/2011/02/02/essential-node-js-patterns-and-snippets

這幾篇都是非常經典的NodeJS/Javascript流程控制好文章（阿，mixu是在介紹一些pattern時提到這方面的主題）。不過我還是用幾個簡單的程式介紹一下做法跟概念：


並發與等待
---------

下面的程式參考了mixu文章中的做法：

var wait = function(callbacks, done) {
 console.log('wait start');
 var counter = callbacks.length;
 var results = [];
 var next = function(result) {//接收函數執行結果，並判斷是否結束執行
 results.push(result);
 if(--counter == 0) {
 done(results);//如果結束執行，就把所有執行結果傳給指定的callback處理
 }
 };
 for(var i = 0; i < callbacks.length; i++) {//依次呼叫所有要執行的函數
 callbacks[i](next);
 }
 console.log('wait end');
}

wait(
 [
 function(next){
 setTimeout(function(){
 console.log('done a');
 var result = 500;
 next(result)
 },500);
 },
 function(next){
 setTimeout(function(){
 console.log('done b');
 var result = 1000;
 next(result)
 },1000);
 },
 function(next){
 setTimeout(function(){
 console.log('done c');
 var result = 1500;
 next(1500)
 },1500);
 }
 ],
 function(results){
 var ret = 0, i=0;
 for(; i<results.length; i++) {
 ret += results[i];
 }
 console.log('done all. result: '+ret);
 }
);

執行結果：
wait start
wait end
done a
done b
done c
done all. result: 3000

可以看出來，其實wait並不是真的等到所有函數執行完才結束執行，而是在所有傳給他的函數執行完畢後（不論同步、非同步），才執行處理結果的函數（也就是done()）

不過這樣的寫法，還不夠實用，因為沒辦法實際讓函數可以等待執行完畢，又能當作事件處理函數來實際使用。上面參考到的Tim Caswell的文章，裡面有一種解法，不過還需要額外包裝（在他的例子中）NodeJS核心的fs物件，把一些函數（例如readFile）用Currying處理。類似像這樣：

var fs = require('fs');
var readFile = function(path) {
    return function(callback, errback) {
        fs.readFile(path, function(err, data) {
            if(err) {
                errback();
            } else {
                callback(data);
            }
        });
    };
}

其他部份可以參考Tim Caswell的文章，他的Do.parallel跟上面的wait差不多意思，這裡只提示一下他沒說到的地方。

另外一種做法是去修飾一下callback，當他作為事件處理函數執行後，再用cps的方式取得結果：

<script>
function Wait(fns, done) {
    var count = 0;
    var results = [];
    this.getCallback = function(index) {
        count++;
        return (function(waitback) {
            return function() {
                var i=0,args=[];
                for(;i<arguments.length;i++) {
                    args.push(arguments[i]);
                }
                args.push(waitback);
                fns[index].apply(this, args);
            };
        })(function(result) {
            results.push(result);
            if(--count == 0) {
                done(results);
            }
        });
    }
}
var a = new Wait(
 [
 function(waitback){
 console.log('done a');
 var result = 500;
 waitback(result)
 },
 function(waitback){
 console.log('done b');
 var result = 1000;
 waitback(result)
 },
 function(waitback){
 console.log('done c');
 var result = 1500;
 waitback(result)
 }
 ],
 function(results){
 var ret = 0, i=0;
 for(; i<results.length; i++) {
 ret += results[i];
 }
 console.log('done all. result: '+ret);
 }
);
var callbacks = [a.getCallback(0),a.getCallback(1),a.getCallback(0),a.getCallback(2)];
//一次取出要使用的callbacks，避免結果提早送出
setTimeout(callbacks[0], 500);
setTimeout(callbacks[1], 1000);
setTimeout(callbacks[2], 1500);
setTimeout(callbacks[3], 2000);
//當所有取出的callbacks執行完畢，就呼叫done()來處理結果
</script>

執行結果：

done a
done b
done a
done c
done all. result: 3500

上面只是一些小實驗，更成熟的作品是Tim Caswell的step：https://github.com/creationix/step

如果希望真正使用同步的方式寫非同步，則需要使用Promise.js這一類的library來轉換非同步函數，不過他結構比較複雜XD（見仁見智，不過有些人認為Promise有點過頭了）：http://blogs.msdn.com/b/rbuckton/archive/2011/08/15/promise-js-2-0-promise-framework-for-javascript.aspx

如果想不透過其他Library做轉換，又能直接用同步方式執行非同步函數，大概就要使用一些需要額外compile原始程式碼的方法了。例如Bruno Jouhier的streamline.js：https://github.com/Sage/streamlinejs


循序執行
-------

循序執行可以協助把非常深的巢狀callback結構攤平，例如用這樣的簡單模組來做（serial.js）：

module.exports = function(funs) {
    var c = 0;
    if(!isArrayOfFunctions(funs)) {
        throw('Argument type was not matched. Should be array of functions.');
    }
    return function() {
        var args = Array.prototype.slice.call(arguments, 0);
        if(!(c>=funs.length)) {
            c++;
            return funs[c-1].apply(this, args);
        }
    };
}

function isArrayOfFunctions(f) {
    if(typeof f !== 'object') return false;
    if(!f.length) return false;
    if(!f.concat) return false;
    if(!f.splice) return false;
    var i = 0;
    for(; i<f.length; i++) {
        if(typeof f[i] !== 'function') return false;
    }
    return true;
}

簡單的測試範例（testSerial.js），使用fs模組，確定某個path是檔案，然後讀取印出檔案內容。這樣會用到兩層的callback，所以測試中有使用serial的版本與nested callbacks的版本做對照：

var serial = require('./serial'),
    fs = require('fs'),
    path = './dclient.js',
    cb = serial([
    function(err, data) {
        if(!err) {
            if(data.isFile) {
                fs.readFile(path, cb);
            }
        } else {
            console.log(err);
        }
    },
    function(err, data) {
        if(!err) {
            console.log('[flattened by searial:]');
            console.log(data.toString('utf8'));
        } else {
            console.log(err);
        }
    }
]);
fs.stat(path, cb);

fs.stat(path, function(err, data) {
    //第一層callback
    if(!err) {
        if(data.isFile) {
            fs.readFile(path, function(err, data) {
                //第二層callback
                if(!err) {
                    console.log('[nested callbacks:]');
                    console.log(data.toString('utf8'));
                } else {
                    console.log(err);
                }
            });
        } else {
            console.log(err);
        }
    }
});

關鍵在於，這些callback的執行是有順序性的，所以利用serial返回的一個函數cb來取代這些callback，然後在cb中控制每次會循序呼叫的函數，就可以把巢狀的callback攤平成循序的function陣列（就是傳給serial函數的參數）。

測試中的./dclient.js是一個簡單的dnode測試程式，放在跟testSerial.js同一個目錄：

var dnode = require('dnode');

dnode.connect(8000, 'localhost',  function(remote) {
    remote.restart(function(str) {
        console.log(str);
        process.exit();
    });
});

執行測試程式後，出現結果：

[flattened by searial:]
var dnode = require('dnode');

dnode.connect(8000, 'localhost',  function(remote) {
    remote.restart(function(str) {
        console.log(str);
        process.exit();
    });
});

[nested callbacks:]
var dnode = require('dnode');

dnode.connect(8000, 'localhost',  function(remote) {
    remote.restart(function(str) {
        console.log(str);
        process.exit();
    });
});

對照起來看，兩種寫法的結果其實是一樣的，但是利用serial.js，巢狀的callback結構就會消失。

不過這樣也只限於順序單純的狀況，如果函數執行的順序比較複雜（不只是一直線），還是需要用功能更完整的流程控制模組比較好，例如 https://github.com/caolan/async 。


