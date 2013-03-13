*********************************************
如何在 Mac OSX Lion 上設定 node.js 的開發環境
*********************************************

================================
用 Homebrew 來安裝及更新 node.js
================================

要在 Mac 上建立一個 node.js 的開發環境有很多方法. 你可以直接下載原始碼自己編譯, 或者是用套件管理系統來幫你解決這些瑣碎的問題. 因為 node.js 還是一個很年輕的專案, 常常會有版本的更新. 手動安裝及更新實在是非常的累人. 若是使用 Homebrew 來幫你處理這些問題可以讓你把時間花在寫程式而不是設定環境上面. 如果你是使用 Ubuntu 的話可以參考這一篇文章:
http://dreamerslab.com/blog/tw/how-to-setup-a-node-js-development-environment-on-ubuntu-11-04


==========
安裝 Xcode
==========
什麼? 我只不過是想寫 server side javascript 而已為什麼要安裝 4.3 GB 的Xcode 4? 嗯… 因為你需要 gcc 來編譯 node.js 和其他的套件. 所以還是乖乖裝吧…


=============
安裝 Homebrew
=============
Homebrew 是我在 Mac 上最喜歡的套件管理系統. 他就像是 Ubuntu 上的 apt-get. 我們會需要他來幫我們安裝 node.js 以及 mongoDB. 如果你還沒聽過他的話現在趕快來試試看吧!
::
    $ /usr/bin/ruby -e "$(/usr/bin/curl -fsSL https://raw.github.com/mxcl/homebrew/master/Library/Contributions/install_homebrew.rb)"

但其實用 nvm( node version management ) 來安裝 node 簡單多了, 他是一個像是 ruby rvm 的東西. 可以讓你切換 node 的版本以利在開發時切換版本. 還有 npm 在 node 0.6.3 之後已經直接包在 node 裡面不需另外安裝了. 所以基本上後面 安裝 npm 可以跳過不看.


============
安裝 node.js
============
用 Homebrew 來安裝 node.js 非常簡單. 只要下面兩行指令就搞定了.
::
    $ brew update
    $ brew install node
上面是舊的安裝方法, 可以不用理會. 用 nvm 安裝非常的簡單, 方法如下:
::
    # clone repo
    $ git clone git://github.com/creationix/nvm.git ~/.nvm
    # enable on terminal open
    $ echo ". ~/.nvm/nvm.sh" >> ~/.bashrc
    # reopen your terminal and do the following
    $ nvm install v0.6.6
    # set default node
    $ nvm alias default v0.6.6
