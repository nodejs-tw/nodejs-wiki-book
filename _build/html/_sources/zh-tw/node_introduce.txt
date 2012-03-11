************
Node.js 簡介
************

Node.js 是一個高效能、易擴充的網站應用程式開發框架 (Web Application Framework) 。它誕生的原因，是為了讓開發者能夠更容易開發高延展性的網路服務，不需要經過太多複雜的調校、效能調整及程式修改，就能滿足網路服務在不同發展階段對效能的要求。

Ryan Dahl 是 NodeJS 的催生者，目前任職於 Joyent (主機託管服務公司) 。他開發 NodeJS 的目的，就是希望能解決 Apache 在連線數量過高時，緩衝區 (buffer) 和系統資源會很快被耗盡的問題，希望能建立一個新的開發框架以解決這個問題。因此嘗試使用效能十分優秀的 V8 JavaScript Engine ，讓網站開發人員熟悉的 JavaScript 程式語言，也能應用於後端服務程式的開發，並且具有出色的執行效能。

JavaScript 是功能強大的物件導向程式語言，但是在 JavaScript 的官方規格中，主要是定義網頁(以瀏覽器為基礎)應用程式需要的應用程式介面 (API) ，對 JavaScript 程式的應用範圍有所侷限。為使 JavaScript 能夠在更多用途發展， CommonJS 規範一組標準函式庫 (standard library) ，使 JavaScript 的應用範圍能夠和 Ruby 、 Python 及 Java 等語言同樣豐富。撰寫 NodeJS 的 JavaScript 程式碼，符合 CommonJS 規範，可以使用 CommonJS API 為基礎開發程式，並且在不同的 CommonJS 兼容 (compliant) JavaScript 執行環境中，程式碼具有可攜性。

瀏覽器的 JavaScript 與實現 CommonJS 規範的 NodeJS 有何不同呢？瀏覽器的 JavaScript 提供 XMLHttpRequest ，讓程式可以和網頁伺服器建立資料傳輸連線，但這通常只能適用於網站開發的需求，因為我們只能用 XMLHttpRequest 與網頁伺服器通訊，卻無法利用它建立其他類型如 Telnet / FTP / NTP 的伺服器通訊。如果我們想開發網路服務程式，例如 SMTP 電子郵件伺服器，就必須使用 Sockets 建立 TCP (某些服務則用 UDP) 監聽及連線，其他程式語言如 PHP 、 Java 、 Python 、 Perl 及 Ruby 等，在標準開發環境中皆有提供 Sockets API ，而瀏覽器的 JavaScript 基於安全及貼近網站設計需求的考量下，並未將 Sockets 列入標準函式庫之中。 CommonJS 的規範填補這種基礎函式庫功能的空缺，遵循 CommonJS 規範的 NodeJS 可以直接使用 Sockets API 建立各種網路服務程式。

JavaScript 語言本身支援 Lambda 的特性，因此一個匿名函式 (anonymous function) 可以被儲存成一個變數，並當作參數傳遞給另一個函式。

    var proc1 = function(op, x) {
        return op(x);
    }
    
    var op1 = function(x) { return x+1; }
    var op2 = function(x) { return x*x; }
    
    proc1(op1, 3);  // result is 4
    proc1(op2, 5);  // result is 25

另一個 JavaScript 開發者必須掌握的語言特性稱為 Closure 。

NodeJS 符合 CommonJS 的規範，使得 Callback 方式易於實現，也能夠讓更多同好基於 JavaScript 開發符合 NodeJS 的外掛模組 (Module)。

回想以前要寫一個能夠同時容納上百人的上線的網路服務，需要花費多大的苦工，可能10人多就需要經過一次程式調整，而NodeJS就是為了解決這個困境， NodeJS 因此誕生，它是一種利用 V8 Javascript 編譯器，所開發的產品，利用V8 編譯器的高效能，與Javascript 的程式開發特性所產生的網路程式。

開發人員所編寫出來的Javascript 腳本程式，怎麼可能會比其他語言寫出來的網路程式還要快上許多呢？以前的網路程式原理是將使用者每次的連線(connection)都開啟一個執行緒(thread)，當連線爆增的時候將會快速耗盡系統效能，並且容易產生阻塞(block)的發生。

NodeJS對於資源的調校有所不同，當程式接收到一筆連線(connection)，會通知作業系統透過epoll, kqueue, /dev/poll,或select將連線保留，並且放入heap中配置，先讓連線進入休眠(Sleep)狀態，當系統通知時才會觸發連線的callback。這種處理連線方式只會佔用掉記憶體，並不會使用到CPU資源。另外因為採用Javascript 語言的特性，每個request都會有一個callback，如此可以避免發生Block的狀況發生。

基於Callback特性，目前NodeJS大多應用於Comet(long pulling) Request Server，或者是高連線數量的網路服務上，目前也有許多公司將NodeJS設為內部核心網路服務之一。在NodeJS也提供了外掛管理(Node package management)，讓愛好NodeJS輕易開發更多有趣的服務、外掛，並且提供到npm讓全世界使用者快速安裝使用。

本書最後執行測試版本為node.js v0.6.8，相關API 文件可查詢`http://nodejs.org <http://nodejs.org>`
本書所有範例均可於linux, windows 上執行，如遇到任何問題歡迎至`http://nodejs.tw <http://node.js.tw>`，詢問對於node.js 相關問題。
