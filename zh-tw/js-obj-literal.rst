*******************
JavaScript 物件實字
*******************

在 JavaScript 最常見也最容易產生一個物件的方式就是用物件實字，但他沒有 private、protected，所以就產生了一種撰碼風格，以 _ 代表 protected，__ 代表 private，當沒有 protected 時 _ 代表 private。

這是一個很簡單的物件實字

.. code-block:: js

    var dog = {
      walk: function () {
      },
      run: function () {
      }
    };

實作 private
============

在物件實字的地方如果有需要用 private 屬性、方法，那就要透過 closure、立即函式。

寫法可能有許多不同的變化，但下面這個是我習慣的作法，用這種方法有幾點好處

    1. 方法寫在 return 的地方也可以透過 _this 去操作物件實字
    2. 在定義時可以按照一般的物件實字寫法去寫，之後再來定義哪些是可公開的方法、屬性

有好處當然也有壞處

    1. 在物件實字內不能使用 this，必須用 _this，因為之後我們真正去操作的物件實字並不是 _this，而是後面回傳的物件實字。
    2. 要建立兩個物件實字，好像有點麻煩...

.. code-block:: js

    var dog = (function () {
      var _this = {
        _name: 'Dog';
        getName: function () {
          return _this.name;
        },
        setName: function (name) {
          _this.name = name;
        }
      };
      return {
        getName: _this.getName,
        setName: _this.setName,
        reset: function () {
          _this.name = 'Dog';
        }
      };
    })();

自動化 private
==============

這裡提供一個方法讓大家方便建立有 private 屬性、方法的物件實字，這裡用之前提過的 _、__ 開頭代表 private 這種程式碼撰寫習慣

.. code-block:: js

    function objLiteral(_this) {
      var i, obj = {}, regex = /^_{1,2}/, tmp;

      function _method(method) {
        return function () {
          return method.apply(_this, arguments);
        };
      }

      for (i in _this) {
        if (_this.hasOwnProperty(i)) {
          tmp = _this[i];
          if (!regex.test(i)) {
            obj[i] = (typeof tmp === 'function' ? _method(tmp) : tmp);
          }
        }
      }

      return obj;
    }

來建立一個物件實字試試看

.. code-block:: js

    var dog = objLiteral({
      _name: 'Dog',
      getName: function () {
        return this._name;
      },
      setName: function (name) {
        this._name = name;
      }
    });

dog 底下有 getName、setName，沒有 _name，而且 method 裡可以使用 this！
