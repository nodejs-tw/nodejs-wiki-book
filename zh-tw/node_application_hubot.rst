*******************************
製作一個 Hubot 的Plurk Adapter
*******************************

應用事項提醒
============

此應用範例以 *CoffeeScript* 編寫，主要程式架構採用 Github 釋放的 Hubot 專案，以下有幾個主要注意事項，請讀者注意，

 * Hubot 一開始的架構，除了內建的兩個 Adapter 之外，其餘都要以 Node.js 的 Module 方式才能運作。
 * Hubot 的 bin/hubot 裡面寫著 npm install 所以不管你怎麼改原始碼也不能改變第一點的狀況。

其實上述都在討論同一件事情： Node.JS 的模組，而且模組不能設定相對路徑之類的來安裝，一定要包裝成 npm 相符和格式才有辦法正確執行。

建立 Adapter
============

首先需要準備兩個檔案，

 * package.json
 * plurk.coffee

有這兩個就足以變成 Node.JS 的模組了，在開始 Coding 之前，先來設定一下 package.json 相依性，

::

    {
		"name": "hubot-plurk",
  		"version": "0.1.1",
	    "main": "./plurk",
	    "dependencies": 
	    {
	    	"hubot": ">=2.0.5",
	    	"oauth": "",
	    	"cron":""
		}
	}

這邊會使用到 Node.JS 的 cron 模組（Module），而登入 Plurk 需要 OAuth 標準授權才行，所以也需要加載 OAuth 模組。

注意：*Hubot 在讀取非內建模組時，會自動在前面加上 hubot- 的前置。*

建立 Robot 跟 API
================

本篇應用基本上程式碼大部分參考 Hubot - Twitter Adapter 來製作，主要差異只有在使用 OAuth 這個模組，Twitter 有 Streaming 可用而 Plurk 則得用 Comet 方式來達到即時讀取。

plurk.coffee 程式碼，


.. code-block:: javascript

	Robot = require("hubot").robot()
	Adapter = require("hubto").adapter()

	EventEmitter = require("events").EventEmitter

	oauth = require("oauth")
	cronJob = require("cron").CronJob

	class Plurk exntends Adapter

	class PlurkStreaming exnteds EventEmitter

先弄個基本架構，主要 Class 皆參考 Twitter Adapter 命名方式，接著再將 Plurk 這個 Class 增加幾個 Method，基本上只要有 run, send, reply 就夠了，而 run 用來做初始化的部分。

.. code-block:: javascript

	class Plurk entends Adapter
  		send: (plurk_id, strings…) ->

  		reply: (plurk_id, strings…) ->

  		run: ->

看起來有點東西，接著來處理主要的Plurk API 結合部分，

.. code-block:: javascript

	class PlurkStreaming extends EventEmitter

		constructor: (options) ->

		plurk: (callback) ->
			#觀察河道
		getChannel: ->
			#取得 Comet 網址
		reply: (plurk_id, message) ->
			#回噗
		acceptFriends: ->
			#接受好友
		get: (path, callback) ->
			#GET 請求
		post: (path, body, callback)->
			#POST 請求（其實是裝飾）
		request: (method, path, body, callback)->
			#主要的 OAuth 請求
		comet: (server, callback)->
    		#噗浪的 Comet 傳回是 JavaScript Callback 要另外處理後才會變成 JSON

然後把注意力集中到 constructor 上，先把建構子弄好。

.. code-block:: javascript

   constructor: (options) ->
    super()
    if options.key? and options.secret? and options.token? and options.token_secret?
      @key = options.key
      @secret = options.secret
      @token = options.token                                                                                                                                                    
      @token_secret = options.token_secret
      #建立 OAuth 連接
      @consumer = new oauth.OAuth(
        "http://www.plurk.com/OAuth/request_token",
        "http://www.plurk.com/OAuth/access_token",
        @key,
        @secret,
        "1.0",
        "http://www.plurk.com/OAuth/authorize".
        "HMAC-SHA1"
      )   
      @domain = "www.plurk.com"
      #初始化取得Comet網址
      do @getChannel
    else
      throw new Error("參數不足，需要 Key, Secret, Token, Token Secret")

接著來處理 request 這個 method。

.. code-block:: javascript

    request: (method, path, body, callback) ->                                                                                                                                
        #記錄一下這次的 Request
        console.log("http://#{@domain}#{path}")

        # Callback 這邊先不丟進去，要用另一種方式處理
        request = @consumer.get("http://#{@domain}#{path}", @token, @token_secret, null)

        request.on "response", (res) ->
          res.on "data", (chunk) ->
            parseResponse(chunk+'', callback)
          res.on "end", (data) ->
            console.log "End Request: #{path}"
          res.on "error", (data) ->
            console.log "Error: " + data

        request.end()

        #處理資料
        parseResponse = (data, callback) ->
          if data.length > 0
            #用 Try/Catch 避免處理 JSON 出錯導致整個中斷
            try
              callback null, JSON.parse(data)
            catch err
              console.log("Error Parse JSON:" + data, err)
              #繼續執行
              callback null, data || {}


大致上就是這樣，上面程式的架構已經將整個 Hubot Plurk Adapter 完成。因為在測試時竟然因為噗浪 Lag 而沒讀到完整的 Comet 資料，然後造成程式異常，為了避免這個問題發生，因此需要加上為了完美呈現需要再加上 Comet 的處理，所以要使用到 EventEmitter 的功能。

.. code-block:: javascript

  	comet: (server, callback) ->
  	#在 Callback 裡面會找不到自身，所以設定區域變數
    	self = @

	#記錄一下這次的 Request
    console.log("[Comet] #{server}")

	Callback 這邊先不丟進去，要用另一種方式處理
    request = @consumer.get("http://#{@domain}#{path}", @token, @token_secret, null)

    request.on "response", (res) ->
      res.on "data", (chunk) ->
        parseResponse(chunk+'', callback)
      res.on "end", (data) ->
        console.log "End Request: #{path}"
        #請求結束，發出事件通知可以進行下一次請求
        self.emit "nextPlurk"
      res.on "error", (data) ->
        console.log "Error: " + data

    request.end()

	#處理資料
    parseResponse = (data, callback) ->
      if data.length > 0
        #用 try/catch 避免失敗中斷
        try
          #去掉 JavaScript 的 Callback
          data = data.match(/CometChannel.scriptCallback\((.+)\);\s*/)
          jsonData = ""

          if data?
            jsonData = JSON.parse(data[1])
          else
            #如果沒有任何 Match 嘗試直接 parse
            jsonData = JSON.parse(data)
        catch err
          console.log("[Comet] Error:", data, err)

        #用 Try/Catch 避免處理 JSON 出錯導致整個中斷
        try
          #只傳入 json 的 data 部分
          callback null, jsonData.data
        catch err
          console.log("[Comet]Error Parse JSON:" + data, err)                                                                                                                   
          #繼續執行
          callback null, data || {}


後面的 get 跟 post 就簡單多了！

.. code-block:: javascript

	get: (path, callback) ->
    	@request("GET", path, null, callback)

	post: (path, body, callback) ->
    	@request("POST", path, body, callback)

接著處理取的 Comet 網址的 getChannel

.. code-block:: javascript

    getChannel: ->
        self = @

    @get "/APP/Realtime/getUserChannel", (error, data) ->
      if !error
        #檢查是否有 comet server
        if data.comet_server?
          self.channel = data.comet_server
          #如果沒有 Channel Ready 就嘗試連接會失敗
          self.emit('channel_ready')

那麼，先來處理 Plurk Adaper 好處理的部份

.. code-block:: javascript

      send: (plruk_id, strings…)->
        #跟 Reply 一樣，直接交給 reply 做
        @reply plurk_id, strings…

      reply: (plurk_id, strings…) ->
        strings.forEach (message) =>
          @bot.reply(plruk_id, message)

接著把 run 處理好就可以上線運作摟！

.. code-block:: javascript

      run: ->
        self = @
        options =
          key: process.env.HUBOT_PLURK_KEY
          secret: process.env.HUBOT_PLURK_SECRET
          token: process.env.HUBOT_PLURK_TOKEN
          token_secret: process.env.HUBOT_PLURK_TOKEN_SECRET

        #創建剛剛的 API
        bot = new PlurkStreaming(options)

        #依照 Twitter 的 new Robot.TextMessage 會沒有反應，所以參考 hubot-minecraft 的方式
        r = @robot.constructor

        #處理噗浪河道訊息
        @doPlurk = (data)->
          #檢查是否為回噗
          if data.response?
            data.content_raw = data.response.content_raw
            data.user_id = data.response.user_id
          #確定有噗浪ID跟訊息
          if data.plurk_id? and data.content_raw
            self.receive new r.TextMessage(data.plurk_id, data.content_raw)

        #取得 Comet Server 完成，開始第一次 Comet 連接
        bot.on "channel_ready", () ->
          bot.plurk self.doPlurk

        #上一次 Comet 完成，繼續 Polling
        bot.on "nextPlurk", ()->
          bot.plurk self.doPlurk

        #定時接受好友邀請
        do bot.acceptFriends

        @bot = bot


終於，完成 Adapter！Hubot 專案裡面的 scripts 資料夾內是互動部分，不需要像 Adapter 如此大費周章處理，只新增檔案並且設計好對白，之後就會回噗了，我開發用的機器人在此，大家可以去跟他玩玩，[http://plurk.com/elct9620_bot](http://plurk.com/elct9620_bot)

原始資料提供
===========

     * [製作一個 Hubot 的噗浪 Adapter](http://revo-skill.frost.tw/blog/2012/03/18/create-a-hubot-plurk-adapter/)

     



