.. _type-narrowing:

类型缩小(narrowing)
========================

本节专门介绍几种 mypy 支持的类型缩小技巧。

类型缩小是指您说服类型检查器相信一个更广泛的类型实际上是更具体的类型，例如，类型为 ``Shape`` 的对象实际上是更窄的类型 ``Square``。


类型缩小表达式(expressions)
---------------------------------

缩小类型的最简单方法是使用支持的表达式之一：

- :py:func:`isinstance`，例如 :code:`isinstance(obj, float)` 将把 ``obj`` 缩小为 ``float`` 类型。
- :py:func:`issubclass`，例如 :code:`issubclass(cls, MyClass)` 将把 ``cls`` 缩小为 ``Type[MyClass]``。
- :py:class:`type`，例如 :code:`type(obj) is int` 将把 ``obj`` 缩小为 ``int`` 类型。
- :py:func:`callable`，例如 :code:`callable(obj)` 将把对象缩小为可调用类型。
- :code:`obj is not None` 将对象缩小为其 :ref:`非可选形式 <strict_optional>` 。

类型缩小是上下文相关的。例如，基于条件，mypy 只会在 ``if`` 分支中缩小表达式的类型：

.. code-block:: python

    def function(arg: object):
        if isinstance(arg, int):
            # 类型仅在 ``if`` 分支中缩小
            reveal_type(arg)  # 显示的类型: "builtins.int"
        elif isinstance(arg, str) or isinstance(arg, bool):
            # 在此 ``elif`` 分支中，类型以不同方式缩小：
            reveal_type(arg)  # 显示的类型: "builtins.str | builtins.bool"

            # 后续的缩小操作将进一步缩小类型
            if isinstance(arg, bool):
                reveal_type(arg)  # 显示的类型: "builtins.bool"

        # 回到 ``if`` 语句外，类型没有缩小：
        reveal_type(arg)  # 显示的类型: "builtins.object"

Mypy 理解 ``return`` 或抛出异常可能对对象的类型产生的影响：

.. code-block:: python

    def function(arg: int | str):
        if isinstance(arg, int):
            return

        # 此时 `arg` 不能是 `int`：
        reveal_type(arg)  # 显示的类型: "builtins.str"

我们还可以使用 ``assert`` 在相同上下文中缩小类型：

.. code-block:: python

    def function(arg: Any):
        assert isinstance(arg, int)
        reveal_type(arg)  # 显示的类型: "builtins.int"

.. note::

    使用 :option:`--warn-unreachable <mypy --warn-unreachable>` 时，将类型缩小到某个不可能的状态将被视为错误。

    .. code-block:: python

        def function(arg: int):
            # 错误：无法存在 "int" 和 "str" 的子类：
            # 方法签名不兼容
            assert isinstance(arg, str)

            # 错误：语句不可达
            print("所以 mypy 认为 assert 将始终触发")

    在没有 ``--warn-unreachable`` 的情况下，mypy 只会不检查它认为不可达的代码。有关更多信息，请参见 :ref:`unreachable` 。

    .. code-block:: python

        x: int = 1
        assert isinstance(x, str)
        reveal_type(x)  # 显示的类型是 "builtins.int"
        print(x + '!')  # `mypy` 类型检查通过，但在运行时失败。


issubclass
~~~~~~~~~~

Mypy 还可以使用 :py:func:`issubclass` 来改善与类型和 metaclass 一起工作时的类型推断：

.. code-block:: python

    class MyCalcMeta(type):
        @classmethod
        def calc(cls) -> int:
            ...

    def f(o: object) -> None:
        t = type(o)  # 我们必须在这里使用一个变量
        reveal_type(t)  # 显示的类型是 "builtins.type"

        if issubclass(t, MyCalcMeta):  # `issubclass(type(o), MyCalcMeta)` 不会工作
            reveal_type(t)  # 显示的类型是 "Type[MyCalcMeta]"
            t.calc()  # 可以

callable
~~~~~~~~

Mypy 知道在类型检查期间哪些类型是可调用的，哪些类型不是。因此，我们知道 `callable()` 将返回什么。例如：

.. code-block:: python

    from collections.abc import Callable

    x: Callable[[], int]

    if callable(x):
        reveal_type(x)  # N: 显示的类型是 "def () -> builtins.int"
    else:
        ...  # 将永远不会执行，并且在使用 `--warn-unreachable` 时会引发错误


`callable` 函数甚至可以将联合类型分成可调用和不可调用的部分：

.. code-block:: python

    from collections.abc import Callable

    x: int | Callable[[], int]

    if callable(x):
        reveal_type(x)  # N: 显示的类型是 "def () -> builtins.int"
    else:
        reveal_type(x)  # N: 显示的类型是 "builtins.int"

.. _casts:

Casts
-----

Mypy 支持类型转换，通常用于将静态类型值强制转换为子类型。然而，与 Java 或 C# 等语言不同，mypy 的转换仅用于为类型检查器提供提示，并不会执行运行时类型检查。使用函数 :py:func:`typing.cast` 来执行类型转换：

.. code-block:: python

    from typing import cast

    o: object = [1]
    x = cast(list[int], o)  # OK
    y = cast(list[str], o)  # OK (cast 不执行实际的运行时检查)

要支持像上面那样的运行时检查，我们需要检查列表中所有项的类型，对于大型列表来说，这将非常低效。类型转换用于消除虚假的类型检查器警告，并在类型检查器无法完全理解发生了什么时提供一点帮助。

.. note::

   如果您想执行实际的运行时检查，可以使用断言：

   .. code-block:: python

        def foo(o: object) -> None:
            print(o + 5)  # 错误：无法将 'object' 与 'int' 相加
            assert isinstance(o, int)
            print(o + 5)  # OK：此时 'o' 的类型是 'int'

对于类型为 `Any` 的表达式或将值分配给类型为 `Any` 的变量，您不需要进行类型转换，如前所述。您还可以将 `Any` 用作转换目标类型——这使您能够对结果执行任何操作。例如：

.. code-block:: python

    from typing import cast, Any

    x = 1
    x.whatever()  # 类型检查错误
    y = cast(Any, x)
    y.whatever()  # 类型检查 OK（运行时错误）


.. _type-guards:

User-Defined Type Guards
------------------------

Mypy supports User-Defined Type Guards (:pep:`647`).

A type guard is a way for programs to influence conditional
type narrowing employed by a type checker based on runtime checks.

Basically, a ``TypeGuard`` is a "smart" alias for a ``bool`` type.
Let's have a look at the regular ``bool`` example:

.. code-block:: python

  def is_str_list(val: list[object]) -> bool:
    """Determines whether all objects in the list are strings"""
    return all(isinstance(x, str) for x in val)

  def func1(val: list[object]) -> None:
      if is_str_list(val):
          reveal_type(val)  # Reveals list[object]
          print(" ".join(val)) # Error: incompatible type

The same example with ``TypeGuard``:

.. code-block:: python

  from typing import TypeGuard  # use `typing_extensions` for Python 3.9 and below

  def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
      """Determines whether all objects in the list are strings"""
      return all(isinstance(x, str) for x in val)

  def func1(val: list[object]) -> None:
      if is_str_list(val):
          reveal_type(val)  # list[str]
          print(" ".join(val)) # ok

How does it work? ``TypeGuard`` narrows the first function argument (``val``)
to the type specified as the first type parameter (``list[str]``).

用户定义的类型保护(Type Guards)
---------------------------------

Mypy 支持用户定义的类型保护 (:pep:`647`).

类型保护是一种方法，允许程序根据运行时检查影响类型检查器采用的条件类型缩小。

基本上， ``TypeGuard`` 是对 ``bool`` 类型的一个“智能”别名。我们先来看一个常规的 ``bool`` 示例：

.. code-block:: python

    def is_str_list(val: list[object]) -> bool:
        """确定列表中的所有对象是否都是字符串"""
        return all(isinstance(x, str) for x in val)

    def func1(val: list[object]) -> None:
        if is_str_list(val):
            reveal_type(val)  # 显示类型为 list[object]
            print(" ".join(val))  # 错误：类型不兼容

使用 ``TypeGuard`` 的相同示例：

.. code-block:: python

    from typing import TypeGuard  # 对于 Python 3.9 及以下版本使用 `typing_extensions`

    def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
        """确定列表中的所有对象是否都是字符串"""
        return all(isinstance(x, str) for x in val)

    def func1(val: list[object]) -> None:
        if is_str_list(val):
            reveal_type(val)  # list[str]
            print(" ".join(val))  # 正确

这是如何工作的？ ``TypeGuard`` 将第一个函数参数（ ``val`` ）缩小到作为第一个类型参数指定的类型（ ``list[str]`` ）。

.. note::

    类型缩小 `并不严格 <https://www.python.org/dev/peps/pep-0647/#enforcing-strict-narrowing>`_ . 例如，你可以将 `str` 缩小为 `int`:

    .. code-block:: python

        def f(value: str) -> TypeGuard[int]:
            return True

    注意：由于没有强制执行严格的缩小，因此很容易破坏类型安全。

    然而，决心或缺乏信息的开发者有许多方法可以颠覆类型安全，最常见的方式是使用 ``cast`` 或 ``Any`` 。
    如果一个 Python 开发者花时间学习并在其代码中实现用户定义的类型保护，那么可以安全地假设他们对类型安全感兴趣，并且不会以破坏类型安全或产生无意义结果的方式编写他们的类型保护函数。

泛型 TypeGuards
~~~~~~~~~~~~~~~~~~

``TypeGuard`` 还可以与泛型类型一起使用（Python 3.12 语法）：

.. code-block:: python

  from typing import TypeGuard  # use `typing_extensions` for `python<3.10`

  def is_two_element_tuple[T](val: tuple[T, ...]) -> TypeGuard[tuple[T, T]]:
      return len(val) == 2

  def func(names: tuple[str, ...]):
      if is_two_element_tuple(names):
          reveal_type(names)  # tuple[str, str]
      else:
          reveal_type(names)  # tuple[str, ...]

参数 TypeGuards
~~~~~~~~~~~~~~~~~~~~~~~~~~

 类型保护(Type guard)函数可以接受额外的参数（Python 3.12 语法）：

.. code-block:: python

  from typing import TypeGuard  # 对于 `python<3.10` 使用 `typing_extensions`

  def is_set_of[T](val: set[Any], type: type[T]) -> TypeGuard[set[T]]:
      return all(isinstance(x, type) for x in val)

  items: set[Any]
  if is_set_of(items, str):
      reveal_type(items)  # set[str]

方法 TypeGuards
~~~~~~~~~~~~~~~~~~~~~

方法也可以作为 ``TypeGuard``:

.. code-block:: python

  class StrValidator:
      def is_valid(self, instance: object) -> TypeGuard[str]:
          return isinstance(instance, str)

  def func(to_validate: object) -> None:
      if StrValidator().is_valid(to_validate):
          reveal_type(to_validate)  # Revealed type is "builtins.str"

.. note::

  请注意， ``TypeGuard`` `不会缩小 <https://www.python.org/dev/peps/pep-0647/#narrowing-of-implicit-self-and-cls-parameters>`_  ``self`` 或 ``cls`` 隐式参数的类型。如果需要缩小 ``self`` 或 ``cls`` 的类型，可以将值作为显式参数传递给类型保护函数：

  .. code-block:: python

    class Parent:
        def method(self) -> None:
            reveal_type(self)  # Revealed type is "Parent"
            if is_child(self):
                reveal_type(self)  # Revealed type is "Child"

    class Child(Parent):
        ...

    def is_child(instance: Parent) -> TypeGuard[Child]:
        return isinstance(instance, Child)

赋值表达式 TypeGuards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有时你可能需要创建一个新变量，并同时将其缩小到某个特定类型。这可以通过将 ``TypeGuard`` 与 `:= operator <https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions>`_ 运算符结合使用来实现。

.. code-block:: python

    from typing import TypeGuard  # 使用 `typing_extensions` 适用于 `python<3.10`

    def is_float(a: object) -> TypeGuard[float]:
        return isinstance(a, float)

    def main(a: object) -> None:
        if is_float(x := a):
            reveal_type(x)  # N: Revealed type is 'builtins.float'
            reveal_type(a)  # N: Revealed type is 'builtins.object'
        reveal_type(x)  # N: Revealed type is 'builtins.object'
        reveal_type(a)  # N: Revealed type is 'builtins.object'

这里发生了什么？

1. 我们创建了一个新变量 ``x`` ，并将 ``a`` 的值赋给它。
2. 我们在 ``x`` 上运行 ``is_float()`` 类型保护。
3. 它在 ``if`` 上下文中将 ``x`` 缩小为 ``float`` ，而不影响 ``a`` 。

.. note::

    使用 ``isinstance(x := a, float)`` 也可以实现相同的效果。

局限性(Limitations)
---------------------

Mypy 的分析局限于单个符号，无法跟踪符号之间的关系。例如，在以下代码中，很容易推断出如果 :code:`a` 为 None，则 :code:`b` 不能为 None，因此 :code:`a or b` 将始终是 :code:`C` 的实例，但 Mypy 无法识别这一点：

.. code-block:: python

    class C:
        pass

    def f(a: C | None, b: C | None) -> C:
        if a is not None or b is not None:
            return a or b  # 返回值类型不兼容（获得 "C | None"，预期 "C"）
        return C()

在类型检查器中跟踪这种跨变量条件会增加显著的复杂性和性能开销。

你可以使用 ``assert`` 来说服类型检查器，使用类型转换来覆盖它，或者稍微详细地重写函数：

.. code-block:: python

    def f(a: C | None, b: C | None) -> C:
        if a is not None:
            return a
        elif b is not None:
            return b
        return C()


.. _typeis:

TypeIs
------

Mypy 支持 TypeIs (:pep:`742`).

`TypeIs 窄化函数 <https://typing.readthedocs.io/en/latest/spec/narrowing.html#typeis>`_ 允许你定义自定义类型检查，
这可以在条件的 `if 和 else <https://docs.python.org/3.13/library/typing.html#typing.TypeIs>`_ 分支中缩小变量的类型，类似于内置的 `isinstance()` 函数的工作方式。

TypeIs 是 Python 3.13 中的新特性；对于旧版 Python，可以使用来自 `typing_extensions <https://typing-extensions.readthedocs.io/en/latest/>`_ 的回溯。

考虑以下使用 TypeIs 的示例：

.. code-block:: python

    from typing import TypeIs

    def is_str(x: object) -> TypeIs[str]:
        return isinstance(x, str)

    def process(x: int | str) -> None:
        if is_str(x):
            reveal_type(x)  # Revealed type is 'str'
            print(x.upper())  # Valid: x is str
        else:
            reveal_type(x)  # Revealed type is 'int'
            print(x + 1)  # Valid: x is int

在这个示例中，函数 ``is_str`` 是一个类型缩小函数，返回 ``TypeIs[str]``。在 ``if`` 语句中使用时，``x`` 在 ``if`` 分支中被缩小为 ``str``，在 ``else`` 分支中被缩小为 ``int`` 。

关键点：

- 函数必须接受至少一个位置参数。

- 返回类型被注解为 ``TypeIs[T]``，其中 ``T`` 是你希望缩小的类型。

- 函数必须返回一个 ``bool`` 值。

- 在 ``if`` 分支（当函数返回 ``True`` ）中，参数的类型被缩小到其原始类型和 ``T`` 的交集。

- 在 ``else`` 分支（当函数返回 ``False`` ）中，参数的类型被缩小到其原始类型和 ``T`` 的补集的交集。


TypeIs vs TypeGuard
~~~~~~~~~~~~~~~~~~~

虽然 `TypeIs` 和 `TypeGuard` 都允许你定义自定义类型缩小函数，但它们在重要方面存在差异：

- **类型缩小行为**: `TypeIs` 在 `if` 和 `else` 分支中都缩小类型，而 `TypeGuard` 仅在 `if` 分支中缩小类型。

- **兼容性要求**: `TypeIs` 要求缩小后的类型 `T` 与函数的输入类型兼容。而 `TypeGuard` 没有这个限制。

- **类型推断**: 使用 `TypeIs` ，类型检查器可能通过将现有类型信息与 `T` 结合，推断出更精确的类型。

以下是一个演示 `TypeGuard` 行为的示例：

.. code-block:: python

    from typing import TypeGuard, reveal_type

    def is_str(x: object) -> TypeGuard[str]:
        return isinstance(x, str)

    def process(x: int | str) -> None:
        if is_str(x):
            reveal_type(x)  # Revealed type is "builtins.str"
            print(x.upper())  # ok: x is str
        else:
            reveal_type(x)  # Revealed type is "Union[builtins.int, builtins.str]"
            print(x + 1)  # ERROR: Unsupported operand types for + ("str" and "int")  [operator]

泛型 TypeIs
~~~~~~~~~~~~~~

``TypeIs`` 函数同样可以和泛型一起使用:

.. code-block:: python

    from typing import TypeVar, TypeIs

    T = TypeVar('T')

    def is_two_element_tuple(val: tuple[T, ...]) -> TypeIs[tuple[T, T]]:
        return len(val) == 2

    def process(names: tuple[str, ...]) -> None:
        if is_two_element_tuple(names):
            reveal_type(names)  # Revealed type is 'tuple[str, str]'
        else:
            reveal_type(names)  # Revealed type is 'tuple[str, ...]'


TypeIs 带附加参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TypeIs`` 函数可以接受除了第一个参数之外的附加参数。类型缩小仅适用于第一个参数。

.. code-block:: python

    from typing import Any, TypeVar, reveal_type, TypeIs

    T = TypeVar('T')

    def is_instance_of(val: Any, typ: type[T]) -> TypeIs[T]:
        return isinstance(val, typ)

    def process(x: Any) -> None:
        if is_instance_of(x, int):
            reveal_type(x)  # 显示类型为 'int'
            print(x + 1)  # 正确
        else:
            reveal_type(x)  # 显示类型为 'Any'

方法中的 TypeIs
~~~~~~~~~~~~~~~~~

方法也可以作为 ``TypeIs`` 函数。请注意，在实例方法或类方法中，类型缩小适用于第二个参数（在 ``self`` 或 ``cls`` 之后）。

.. code-block:: python

    class Validator:
        def is_valid(self, instance: object) -> TypeIs[str]:
            return isinstance(instance, str)

        def process(self, to_validate: object) -> None:
            if Validator().is_valid(to_validate):
                reveal_type(to_validate)  # 显示类型为 'str'
                print(to_validate.upper())  # 正确: to_validate 是 str


赋值表达式中的 TypeIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

您可以将赋值表达式运算符 ``:=`` 与 ``TypeIs`` 一起使用，以同时创建新变量并缩小其类型。

.. code-block:: python

    from typing import TypeIs, reveal_type

    def is_float(x: object) -> TypeIs[float]:
        return isinstance(x, float)

    def main(a: object) -> None:
        if is_float(x := a):
            reveal_type(x)  # 显示类型为 'float'
            # x 在这个块中被缩小为 float
            print(x + 1.0)
