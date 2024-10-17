.. _dynamic-typing:


动态类型代码(Dynamically)
===========================

在 :ref:`getting-started-dynamic-vs-static` 中，我们讨论了函数体内没有任何显式类型注释的情况被称为“动态类型(dynamically typed)”，并且 mypy 不会对其进行检查。在本节中，我们将更详细地讨论这意味着什么，以及如何在更细粒度的基础上启用动态类型。

在您的代码过于复杂以至于 mypy 无法理解的情况下，您可以通过显式地将变量或参数的类型设置为 ``Any`` 来使其动态类型。Mypy 将允许您对类型为 ``Any`` 的值进行基本上任何操作，包括将类型为 ``Any`` 的值赋给任何类型的变量（或反之亦然）。

.. code-block:: python

   from typing import Any

   num = 1         # 静态类型（推断为 int）
   num = 'x'       # 错误：赋值中的不兼容类型（表达式的类型为 "str"，变量的类型为 "int"）

   dyn: Any = 1    # 动态类型（类型为 Any）
   dyn = 'x'       # OK

   num = dyn       # 没有错误，mypy 允许您将类型为 Any 的值赋给任何变量
   num += 1        # 哦，mypy 仍然认为 num 是 int

您可以将 ``Any`` 视为局部禁用类型检查的一种方式。有关您可以使用的其他关闭类型检查器的方法，请参见 :ref:`silencing-type-errors`。

对 Any 值的操作
------------------------

您可以对类型为 ``Any`` 的值执行任何操作，类型检查器不会发出警告：

.. code-block:: python

    def f(x: Any) -> int:
        # 所有这些都是有效的！
        x.foobar(1, y=2)
        print(x[3] + 'f')
        if x:
            x.z = x(2)
        open(x).read()
        return x

从 ``Any`` 值派生的值通常也隐式地具有 ``Any`` 类型，因为 mypy 无法推断出更精确的结果类型。例如，如果您获取一个 ``Any`` 值的属性或调用 ``Any`` 值，结果就是 ``Any``：

.. code-block:: python

    def f(x: Any) -> None:
        y = x.foo()
        reveal_type(y)  # 显示的类型是 "Any"
        z = y.bar("mypy 会允许你对 y 做任何事")
        reveal_type(z)  # 显示的类型是 "Any"

``Any`` 类型可能在程序中传播，除非您小心，否则会使类型检查的效果降低。

没有注释的函数参数也隐式地为 ``Any``：

.. code-block:: python

    def f(x) -> None:
        reveal_type(x)  # 显示的类型是 "Any"
        x.can.do["anything", x]("wants", 2)

您可以使用 :option:`--disallow-untyped-defs <mypy --disallow-untyped-defs>` 标志使 mypy 针对没有类型注释的函数参数发出警告。

缺少类型参数的泛型类型将隐式地将这些参数视为 ``Any``：

.. code-block:: python

    def f(x: list) -> None:
        reveal_type(x)        # 显示的类型是 "builtins.list[Any]"
        reveal_type(x[0])     # 显示的类型是 "Any"
        x[0].anything_goes()  # OK

您可以使用 :option:`--disallow-any-generics <mypy --disallow-any-generics>` 标志使 mypy 针对缺少类型参数的泛型类型发出警告。

最后， ``Any`` 类型泄漏到程序中的另一个主要来源是 mypy 不知道的第三方库。当使用 :option:`--ignore-missing-imports <mypy --ignore-missing-imports>` 标志时，尤其如此。有关此信息，请参见 :ref:`fix-missing-imports` 。

Any 与 object
--------------

类型 :py:class:`object` 是另一种可以具有任意类型实例作为值的类型。
与 ``Any`` 不同，:py:class:`object` 是一种普通的静态类型（类似于 Java 中的 ``Object``），并且仅接受对 *所有* 类型有效的操作。
以下都是有效的操作：

.. code-block:: python

    def f(o: object) -> None:
        if o:
            print(o)
        print(isinstance(o, int))
        o = 2
        o = 'foo'

然而，以下操作会被标记为错误，因为并非所有对象都支持这些操作：

.. code-block:: python

    def f(o: object) -> None:
        o.foo()       # 错误！
        o + 2         # 错误！
        open(o)       # 错误！
        n: int = 1
        n = o         # 错误！

如果您不确定是使用 :py:class:`object` 还是 ``Any``，请使用 :py:class:`object` —— 仅在出现类型检查器警告时才切换到使用 ``Any``。

您可以使用不同的 :ref:`类型缩小 <type-narrowing>` 技巧将 :py:class:`object` 缩小为更具体的类型（子类型），例如 ``int``。对于动态类型的值（类型为 ``Any`` 的值），不需要进行类型缩小。
