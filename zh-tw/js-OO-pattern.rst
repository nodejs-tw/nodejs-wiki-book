***********************
Javascript 物件導向設計
***********************

在javascript中，一切都是物件，但是總感覺少了什麼。

::

    var dipsy = { name: "dipsy", color: "green", sayHello: function(){ console.log("Hello!");} };
    var po = { name: "po", color: "red", sayHello: function(){ console.log("Hello!");} };
    var lala = { name: "lala", color: "yellow", sayHello: function(){ console.log("Hello!");} };

這樣的方式很不經濟，這樣的設計也沒有重用性可言，這時候你應該會想到物件導向語言中常有的class。由這個class可以產出一堆長得差不多的「徒子徒孫」，也就是實例。

但是javascript中(還)沒有Class，怎麼辦呢？
這時我們就要自己動手寫一個了...

javascript類別實作
==================


實作private attributes
======================


類別的繼承
==========


類別的靜態方法與屬性
====================
