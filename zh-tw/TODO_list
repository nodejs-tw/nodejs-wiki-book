**************************************
用 Express 和 MongoDB 寫一個 todo list
**************************************

練習一種語言或是 framework 最快的入門方式就是寫一個 todo list 了. 他包含了基本的 C.R.U.D. ( 新增, 讀取, 更新, 刪除 ). 這篇文章將用 node.js 裡最通用的 framework Express 架構 application 和 MongoDB 來儲存資料.

原始檔
======

Live Demo <http://dreamerslab.com/blog/tw/write-a-todo-list-with-express-and-mongodb/>

功能
====

*無需登入, 用 cookie 來辨別每一問使用者
*可以新增, 讀取, 更新, 刪除待辦事項( todo item )

安裝
====
開發環境
開始之前請確定你已經安裝了 node.js, Express 和 MongoDB, 如果沒有可以參考下列文章.
*How to setup a node.js development environment on Mac OSX Lion<http://dreamerslab.com/blog/tw/how-to-setup-a-node-js-development-environment-on-mac-osx-lion/>
*How to setup a node.js development environment on Ubuntu 11.04<http://dreamerslab.com/blog/tw/how-to-setup-a-node-js-development-environment-on-ubuntu-11-04/>
*How to setup a node.js development environment on Windows<http://dreamerslab.com/blog/tw/how-to-setup-a-node-js-development-environment-on-windows/>

node.js 套件
============
參考文件 : npm basic commands<http://dreamerslab.com/blog/en/npm-basic-commands/>
*安裝 Express
:: 
    $ npm install express@2.5.11 -g

這個練習裡我們用 Mongoose 這個 ORM. 為何會需要一個必須定義 schema 的 ORM 來操作一個 schema-less 的資料庫呢? 原因是在一般的網站資料結構的關聯, 驗證都是必須處理的問題. Mongoose 在這方面可以幫你省去很多功夫. 我們會在後面才看如何安裝.
