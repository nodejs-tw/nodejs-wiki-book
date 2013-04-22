***********************
Javascript 物件導向設計
***********************

在javascript中，幾乎一切都是物件，在物件導向設計的模式下，應該會常看到這樣的狀況：

.. code-block:: js

    var dipsy = { name: "dipsy", color: "green", sayHello: function(){ console.log("Hello!");} };
    var po = { name: "po", color: "red", sayHello: function(){ console.log("Hello!");} };
    var lala = { name: "lala", color: "yellow", sayHello: function(){ console.log("Hello!");} };

這樣的方式很不經濟，這樣的設計也沒有重用性可言，這時候你應該會想到物件導向語言中常有的class。由這個class可以產出一堆長得差不多的「徒子徒孫」，也就是實例。

但是javascript中(還)沒有Class，怎麼辦呢？
這時我們就要自己動手寫一個了...


javascript類別實作
==================

.. code-block:: js

    var Person = function(name, age) {
        this.name = name;
        this.age = age;
    };

    var p1 = new Person('Kevin',18);

剛接觸js的前端工程師或許沒見過"var p1 = new Person('Kevin',18);"這樣的物件宣告方式，
他其實就相當於以下這四行程式碼：

.. code-block:: js

    var p1 = {};
    Person.call(p1, 'Kevin', 18); // 以p1身分執行Person建構函數
    p1.__proto__ = Person.prototype; // 先別管，後面會提到
    p1.constructer = Person; // 這個物件的建構者是Person

一般在建立物件時，最常見的方法是這樣：

.. code-block:: js

    var obj = {};
    console.log(obj.constructer); // Object(){}

從上面這兩行程式碼可以得知，當我們在建立物件時，其實是由一個存在於global的Object函數來產生他的。
了解到這點以後，你會發現你可以這樣來建立物件：

.. code-block:: js 

    var obj = new Object();



實作private attributes
======================

在物件導向的語言中，有public和private屬性的分別，而在javascript中，我們可以利用「閉包」來製作一個外界無法直接讀取的變數，這樣的特性就如同私有變數了。
現在我們就來看看要如何實作他：

.. code-block:: js

    var Person = function(name, age) {
        var name = name; // private (這句可以省略)
        var age = age;   // private (這句可以省略)
        this.getName = function() { return name };  // public
        this.getAge = function() { return age };    // public
    };

    var p1 = new Person('Kevin',18);

    console.log(p1.name);   // undefined
    console.log(p1.age);    // undefined
    console.log(p1.getName());  // 'Keivn'
    console.log(p1.getAge());   // 18
    
為什麼會有這樣的情況？
原來是因為javascript在進行程式的「預編譯」時，會先將靜態定義的函數給建立出來，這時函數的「視野」(scope)是基於「詞法作用域」的原則來定義。也就是說，他的地盤是在這個函數實際存在的地方，而非被呼叫的地方。
我們再看看下面這個錯誤的例子，或許你就會比較了解：

.. code-block:: js

    var Person = function(name, age) {
        var name = name; // private
        var age = age;   // private
        this.getName = getName;  // public
        this.getAge = getAge;    // public
    };

    var getName = function() { return name };
    var getAge = function() { return age };

    var p1 = new Person('Kevin',18);

    console.log(p1.name);   // undefined
    console.log(p1.age);    // undefined
    console.log(p1.getName());  // undefined
    console.log(p1.getAge());   // undefined

因為function在參考變數時，只會一層一層往外找，
所以上面這段程式碼中，getName及getAge是無法往Person這個建構函數中找age、name這兩個變數的，而以下三個情況都不成立：

    1. getName及getAge所在的scope找不到age、name
    2. getName及getAge所在的scope的外層中找不到age、name（在這個例子中他們已經在最外層了）
    3. 找不到age、name這兩個全域變數



類別的繼承(以prototype實作)
===========================

javascript是個很活的語言，在實作物件導向的「繼承」機制時，大致可以分為兩種作法，這一節講的是「以protoype來實作繼承模式」


什麼是prototype？
-----------------

prototype是函數物件特有的屬性，當利用函數物件來建立一個物件(實例)時，會將prototype這個物件以reference的方式asign給實例的「__proto__」屬性(注意，是雙底線喔)。
之後，__proto__中的所有屬性、方法，就如同這個實例原生擁有的一樣了，舉例來說：

.. code-block:: js

    function Person(name, age) { this.name = name; this.age = age; } 
    Person.prototype.nation = "Taiwan";

    var p1 = new Person("Kevin", "18");

    console.log(p1); // Person {name: "Kevin", age: "18", nation: "Taiwan"}

從上面的code中我們可以看到，雖然我們沒有為p1指定nation，但是因為p1的建構函數的prototype中有這個屬性，所以p1可以藉由__proto__來參考到他的值。


prototype chain
---------------

延續前面的程式碼...如果我們又為p1增加一個屬性"nation"的話會發生什麼事呢？

.. code-block:: js

    p1.nation = "USA";

    console.log(p1); // Person {name: "Kevin", age: "18", nation: "USA", nation: "Taiwan"}
    console.log(p1.nation); // "USA"

這時你會發現p1同時擁有兩個nation的屬性，一個是來自類別(建構函數)的prototype，一個是自身擁有的屬性。
而在呼叫這個屬性時會先找原生的，如果沒有就會往prototype找，還沒有的話就會再找這個prototype物件的類別的prototype找....直到最上層為止，這個概念就是「prototype chain」。
下面這個多層繼承的範例應該能讓你更加了解prototype chain的原理：

.. code-block:: js

    // 哺乳綱 
    function Mammals() { this.blood = "warm"; } 
    
    // 靈長目 
    function Primate() { this.tail = true; this.skin = "hairy"; } 
    Primate.prototype = new Mammals(); 
    
    // 人科 
    function Homo() { this.skin = "smooth"; } 
    Homo.prototype = new Primate(); 

    var human = new Homo(); 
    human.name = "Kevin"; 

    console.log(human.name); // "Kevin", from self. 
    console.log(human.skin); // "smooth", from Homo.
    console.log(human.tail); // "true", from Primate.
    console.log(human.blood); // "warm", from Mammals.


prototype設計模式的漏洞
-----------------------

相信以上的範例應該能讓你對prototype實作的繼承模式有一定的認知，但是這樣實作的繼承模式會有如下的風險：

.. code-block:: js

    function Human() {} 
    Human.prototype.blood = "red"; 
    Human.prototype.body = ["foot","hand"]; 
    
    var john = new Human(); 
    var kevin = new Human(); 
    
    john.blood = "purple"; 
    john.body.push("wing"); 
    
    alert(kevin.blood); // "red" 
    alert(john.blood); // "purple" 
    alert(kevin.body.toString()); // "foot, hand, wing" 
    alert(kevin.body.toString()); // "foot, hand, wing"

從上面的例子可以看到，john因為不明原因而突變以後，不只血變成紫色的，也長出翅膀來了！
但是在john突變之後，kevin的血雖然沒有變色，但是卻莫名其妙長出了翅膀。很明顯的，我們不小心改動到了Human的prototype。
原來在我們為john的blood指定顏色時，javascript會為john這個物件增加一個屬於自己的"blood"屬性，這種情況就跟為物件增加屬性的方式一樣。於是在後來的呼叫時，會先找到john自己的blood屬性。
但要john的body屬性執行push函式時，會發生在john中找不到body的狀況，於是就往上找到了Human.prototype的body屬性，並由他來執行push函式，此時改動到的便是Human.prototype.body了，也就連帶的影響到了無辜的kevin。


類別的繼承(以"call"實作)
========================

call是函數物件特有的方法，他的用途是在指定的作用域中執行這個函數。
有些人對apply或許有印象，他們兩個基本上是一樣的東西，只是傳遞變數的方式不同，這邊我們不多做贅述。
我們直接來看看要如何用它來實作javascript的繼承模式：

.. code-block:: js

    // 哺乳綱
    function Mammals() {
        this.blood = "warm";
    }
    
    // 靈長目
    function Primate() {
        Mammals.call(this); // 記得放前面，不然會蓋掉重複的屬性
        this.tail = true;
        this.skin = "hairy";
    }
    Primate.prototype = new Mammals();
    
    // 人科
    function Homo() {
        Primate.call(this); // 記得放前面，不然會蓋掉重複的屬性
        this.skin = "smooth";
    }
    
    var human = new Homo();
    human.name = "Kevin";
    
    alert(human.name); // "Kevin", from self
    alert(human.skin); // "smooth", from Homo
    alert(human.tail); // "true", from Primate
    alert(human.blood); // "warm", from Mammals


實踐多繼承
==========


實踐Mixin機制
=============


類別的靜態方法與屬性
====================


實現多型
========



