********
NPM 介紹 
********

npm 全名為node package manage，此為node module 管理包，藉由安裝npm 之後可以輕鬆使用npm install xxx 的方式安裝任意模組，安裝模式類似於gem, apt-get 方式，如此管理module 就會更加輕鬆，同時也可以查看目前module 是否為最新版本，進行module 更新。

nodeJS v0.6.3之後版本開始內建npm ，已經安裝v0.6.3版本的使用者，可以不用再執行底下步驟，可以直接使用npm 安裝、移除相關module。當然有興趣自己手動安裝npm 可以查看底下文章說明。

linux 安裝
==========

安裝npm 之前必須安裝 curl，同時確認node 已經安裝完成，環境變數也設定完成，node 版本需為 v0.4.x 以上，底下為安裝指令。

curl http://npmjs.org/install.sh | sh

安裝完成後會看到如下圖

.. image:: ../images/zh-tw/node_npm_linux_install.jpg
   :scale: 100%
   :align: center

接著輸入指令測試

.. code-block:: javascript
npm --v

.. image:: ../images/zh-tw/node_npm_linux_test.jpg
   :scale: 100%
   :align: center

windows 安裝
============

在node.js windows 版本於v0.6.2 之後開始內建npm，在windows環境完成node.js 安裝之後，不需要任何設定，立即可以使用npm指令，對於在windows上的開發者來說,大大降低了環境設定的問題與門檻。

npm 指令測試
============

windows 就必須進入command line，linux 需要進入到terminal 模式底下，輸入指令如下，

.. code-block:: javascript
npm --v

結果如下圖所示,

.. image:: ../images/zh-tw/node_npm_test.png
   :scale: 100%
   :align: center

