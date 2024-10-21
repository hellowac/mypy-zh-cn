鸭子类型兼容性
-----------------------

在 Python 中，某些类型即使不是彼此的子类，也是兼容的。例如，当期望 ``float`` 对象时， ``int`` 对象也是有效的。Mypy 通过 *鸭子类型兼容性* 支持这一习惯用法。这适用于一小部分内置类型：

* ``int`` 与 ``float`` 和 ``complex`` 兼容。
* ``float`` 与 ``complex`` 兼容。
* ``bytearray`` 和 ``memoryview`` 与 ``bytes`` 兼容。

例如，mypy 会认为在期望 ``float`` 对象时，``int`` 对象也是有效的。因此，像这样的代码既简洁又符合预期：

.. code-block:: python

   import math

   def degrees_to_radians(degrees: float) -> float:
       return math.pi * degrees / 180

   n = 90  # 推断类型为 'int'
   print(degrees_to_radians(n))  # Okay!

您还可以使用 :ref:`protocol-types` 来以更原则和可扩展的方式实现类似效果。协议不适用于 ``int`` 与 ``float`` 的兼容性，因为 ``float`` 不是协议类，而是常规的具体类，许多标准库函数期望具体的 ``float`` (或 ``int`` )实例。
