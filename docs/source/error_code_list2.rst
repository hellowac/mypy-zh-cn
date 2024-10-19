.. _error-codes-optional:

可选检查的错误代码(Error codes for optional checks)
==============================================================

本节记录了 mypy 仅在启用某些选项时生成的各种错误代码。有关错误代码及其配置的一般文档，请参阅 :ref:`error-codes` 。 :ref:`error-code-list` 记录了默认启用的错误代码。

.. note::

   本节中的示例使用 :ref:`inline configuration <inline-config>` 指定 mypy 选项。您还可以通过使用 :ref:`configuration file <config-file>` 或 :ref:`command-line options <command-line>` 设置相同的选项。

.. _code-type-arg:

检查类型参数是否存在 [type-arg]
------------------------------------------

如果您使用 :option:`--disallow-any-generics <mypy --disallow-any-generics>`，mypy 要求每个泛型类型为每个类型参数提供值。例如，类型 ``list`` 或 ``dict`` 将被拒绝。您应该使用像 ``list[int]`` 或 ``dict[str, int]`` 这样的类型。任何省略的泛型类型参数都会获得隐式的 ``Any`` 值。类型 ``list`` 相当于 ``list[Any]``，等等。

示例：

.. code-block:: python

    # mypy: disallow-any-generics

    # 错误: 泛型类型 "list" 缺少类型参数  [type-arg]
    def remove_dups(items: list) -> list:
        ...

.. _code-no-untyped-def:

检查每个函数是否有注释 [no-untyped-def]
------------------------------------------------------------

如果您使用 :option:`--disallow-untyped-defs <mypy --disallow-untyped-defs>`，mypy 要求所有函数都有注释（可以是 Python 3 注释或类型注解）。

示例：

.. code-block:: python

    # mypy: disallow-untyped-defs

    def inc(x):  # 错误: 函数缺少类型注解  [no-untyped-def]
        return x + 1

    def inc_ok(x: int) -> int:  # OK
        return x + 1

    class Counter:
         # 错误: 函数缺少类型注解  [no-untyped-def]
         def __init__(self):
             self.value = 0

    class CounterOk:
         # OK: 如果 "__init__" 不接受任何参数，则需要显式的 "-> None"
         def __init__(self) -> None:
             self.value = 0

.. _code-redundant-cast:

检查类型转换是否冗余 [redundant-cast]
-------------------------------------------------

如果您使用 :option:`--warn-redundant-casts <mypy --warn-redundant-casts>`，当类型转换的源类型与目标类型相同时，mypy 将生成错误。

示例：

.. code-block:: python

    # mypy: warn-redundant-casts

    from typing import cast

    Count = int

    def example(x: Count) -> int:
        # 错误: 转换为 "int" 的操作是冗余的  [redundant-cast]
        return cast(int, x)

.. _code-redundant-self:

检查方法是否具有冗余的 Self 注解 [redundant-self]
--------------------------------------------------------------------------

如果方法在返回类型或非 self 参数的类型中使用了 ``Self`` 类型，则不需要显式注解 ``self`` 参数。这种注解在 :pep:`673` 中是允许的，但属于冗余。如果启用此错误代码，mypy 将生成错误，如果存在冗余的 ``Self`` 类型。

示例：

.. code-block:: python

   # mypy: enable-error-code="redundant-self"

   from typing import Self

   class C:
       # 错误: 第一个方法参数的 "Self" 注解冗余
       def copy(self: Self) -> Self:
           return type(self)()

.. _code-comparison-overlap:

检查比较是否重叠 [comparison-overlap]
-----------------------------------------------------------

如果您使用 :option:`--strict-equality <mypy --strict-equality>`，mypy 将生成错误，如果它认为比较操作总是为真或为假。这些通常是错误。有时 mypy 可能过于严格，比较实际上是有用的。您可以仅在特定行上使用 ``# type: ignore[comparison-overlap]`` 来忽略该问题，而不是在所有地方禁用严格相等检查。

示例：

.. code-block:: python

    # mypy: strict-equality

    def is_magic(x: bytes) -> bool:
        # 错误: 非重叠的相等检查（左操作数类型: "bytes",
        #        右操作数类型: "str"）  [comparison-overlap]
        return x == 'magic'

我们可以通过将字符串字面量更改为字节字面量来修复错误：

.. code-block:: python

    # mypy: strict-equality

    def is_magic(x: bytes) -> bool:
        return x == b'magic'  # OK

.. _code-no-untyped-call:

检查未注解的函数未被调用 [no-untyped-call]
------------------------------------------------------------

如果您使用 :option:`--disallow-untyped-calls <mypy --disallow-untyped-calls>`，mypy 在您在注解函数中调用未注解的函数时生成错误。

示例：

.. code-block:: python

    # mypy: disallow-untyped-calls

    def do_it() -> None:
        # 错误: 在类型上下文中调用未注解的函数 "bad"  [no-untyped-call]
        bad()

    def bad():
        ...

.. _code-no-any-return:

检查函数不返回 Any 值 [no-any-return]
-------------------------------------------------------------

如果您使用 :option:`--warn-return-any <mypy --warn-return-any>`，mypy 将生成错误，如果您在注解为返回非 ``Any`` 值的函数中返回 ``Any`` 类型的值。

示例：

.. code-block:: python

    # mypy: warn-return-any

    def fields(s):
         return s.split(',')

    def first_field(x: str) -> str:
        # 错误: 从声明为返回 "str" 的函数返回 Any  [no-any-return]
        return fields(x)[0]

.. _code-no-any-unimported:

检查由于缺少导入而没有 Any 组件的类型 [no-any-unimported]
----------------------------------------------------------------------------------

如果您使用 :option:`--disallow-any-unimported <mypy --disallow-any-unimported>`，mypy 如果类型的某个组件变为 ``Any``，因为 mypy 无法解析导入，将生成错误。这些“隐形”的 ``Any`` 类型可能会令人惊讶，并意外导致不精确的类型检查。

在此示例中，我们假设 mypy 无法找到模块 ``animals``，这意味着 ``Cat`` 在类型注解中回退为 ``Any``：

.. code-block:: python

    # mypy: disallow-any-unimported

    from animals import Cat  # type: ignore

    # 错误: "feed" 的参数 1 由于未跟随的导入而变为 "Any"  [no-any-unimported]
    def feed(cat: Cat) -> None:
        ...

.. _code-unreachable:

检查语句或表达式是否不可达 [unreachable]
---------------------------------------------------------------

如果您使用 :option:`--warn-unreachable <mypy --warn-unreachable>`，mypy 如果它认为某个语句或表达式将永远不会被执行，则会生成错误。在大多数情况下，这通常是由于不正确的控制流或条件检查意外总是为真或为假。

.. code-block:: python

    # mypy: warn-unreachable

    def example(x: int) -> None:
        # 错误: "or" 的右操作数永远不会被评估  [unreachable]
        assert isinstance(x, int) or x == 'unused'

        return
        # 错误: 语句不可达  [unreachable]
        print('unreachable')

.. _code-deprecated:

检查导入或使用的特性是否已弃用 [deprecated]
--------------------------------------------------------------

默认情况下，如果您的代码通过 ``from mod import depr`` 语句显式导入了已弃用的特性，或以其他方式使用了已弃用的特性或在本地定义了已弃用的特性，mypy 会生成一个通知。当特性被 ``warnings.deprecated`` 装饰时，视为已弃用，如 `PEP 702 <https://peps.python.org/pep-0702>`_ 中所述。您可以通过 ``# type: ignore[deprecated]`` 来静默单个通知，或通过 ``--disable-error-code=deprecated`` 完全关闭此检查。使用 :option:`--report-deprecated-as-error <mypy --report-deprecated-as-error>` 选项以获得更严格的检查，将所有此类通知转换为错误。

.. note::

    ``warnings`` 模块自 Python 3.13 起提供 ``@deprecated`` 装饰器。
    若要在旧版本的 Python 中使用，请从 ``typing_extensions`` 导入它。

示例：

.. code-block:: python

    # mypy: report-deprecated-as-error

    # 错误: abc.abstractproperty 已弃用：已弃用，请使用 'property' 和 'abstractmethod' 替代
    from abc import abstractproperty

    from typing_extensions import deprecated

    @deprecated("use new_function")
    def old_function() -> None:
        print("I am old")

    # 错误: __main__.old_function 已弃用：使用 new_function
    old_function()
    old_function()  # type: ignore[deprecated]


.. _code-redundant-expr:

检查表达式是否冗余 [redundant-expr]
---------------------------------------------------

如果您使用 :option:`--enable-error-code redundant-expr <mypy --enable-error-code>`，mypy 将生成错误，如果它认为某个表达式是冗余的。

.. code-block:: python

    # mypy: enable-error-code="redundant-expr"

    def example(x: int) -> None:
        # 错误: "and" 的左操作数总是为真  [redundant-expr]
        if isinstance(x, int) and x > 0:
            pass

        # 错误: 如果条件总是为真  [redundant-expr]
        1 if isinstance(x, int) else 0

        # 错误: 生成式中的条件总是为真  [redundant-expr]
        [i for i in range(x) if isinstance(i, int)]


.. _code-possibly-undefined:

警告有关仅在某些执行路径中定义的变量 [possibly-undefined]
---------------------------------------------------------------------------------------

如果您使用 :option:`--enable-error-code possibly-undefined <mypy --enable-error-code>`，mypy 将生成错误，如果它无法验证变量在所有执行路径中都会被定义。这包括变量定义出现在循环中、条件分支中、异常处理器中等情况。例如：

.. code-block:: python

    # mypy: enable-error-code="possibly-undefined"

    from collections.abc import Iterable

    def test(values: Iterable[int], flag: bool) -> None:
        if flag:
            a = 1
        z = a + 1  # 错误: 名称 "a" 可能未定义 [possibly-undefined]

        for v in values:
            b = v
        z = b + 1  # 错误: 名称 "b" 可能未定义 [possibly-undefined]

.. _code-truthy-bool:

检查表达式在布尔上下文中不隐式为真 [truthy-bool]
-----------------------------------------------------------------------------

当布尔上下文中的表达式类型未实现 ``__bool__`` 或 ``__len__`` 时发出警告。除非这些中的一个由子类型实现，否则表达式将始终被视为真，并且条件中可能存在错误。

作为例外，``object`` 类型在布尔上下文中是允许的。
在布尔上下文中使用可迭代值有单独的错误代码（见下文）。

.. code-block:: python

    # mypy: enable-error-code="truthy-bool"

    class Foo:
        pass
    foo = Foo()
    # 错误: "foo" 的类型为 "Foo"，未实现 __bool__ 或 __len__，因此在布尔上下文中可能始终为真
    if foo:
         ...

.. _code-truthy-iterable:

检查可迭代对象在布尔上下文中不隐式为真 [truthy-iterable]
-------------------------------------------------------------------------------

如果类型为 ``Iterable`` 的值用作布尔条件，则生成错误，因为 ``Iterable`` 并未实现 ``__len__`` 或 ``__bool__``。

示例：

.. code-block:: python

    from collections.abc import Iterable

    def transform(items: Iterable[int]) -> list[int]:
        # 错误: "items" 的类型为 "Iterable[int]"，在布尔上下文中可能始终为真。考虑使用 "Collection[int]" 替代。  [truthy-iterable]
        if not items:
            return [42]
        return [x + 1 for x in items]

如果 ``transform`` 被调用时传入 ``Generator`` 参数，例如 ``int(x) for x in []``，则该函数将不会返回 ``[42]``，与预期可能不同。当然，``transform`` 可能仅在 ``list`` 或其他容器对象上调用，并且 ``if not items`` 检查实际上是有效的。如果是这种情况，建议将 ``items`` 注解为 ``Collection[int]`` 而不是 ``Iterable[int]``。

.. _code-ignore-without-code:

检查 ``# type: ignore`` 是否包含错误代码 [ignore-without-code]
-------------------------------------------------------------------------

当 ``# type: ignore`` 注释未指定任何错误代码时发出警告。这可以明确忽略的意图，并确保仅静默预期的错误。

示例：

.. code-block:: python

    # mypy: enable-error-code="ignore-without-code"

    class Foo:
        def __init__(self, name: str) -> None:
            self.name = name

    f = Foo('foo')

    # 这行有一个拼写错误，mypy 无法处理，因为：
    # - 预期错误 'assignment'，以及
    # - 意外错误 'attr-defined'
    # 都被静默。
    # 错误: "type: ignore" 注释没有错误代码（考虑使用 "type: ignore[attr-defined]"）
    f.nme = 42  # type: ignore

    # 这一行正确地警告了属性名称中的拼写错误
    # 错误: "Foo" 没有属性 "nme"; 也许是 "name"?
    f.nme = 42  # type: ignore[assignment]

.. _code-unused-awaitable:

检查可等待返回值是否被使用 [unused-awaitable]
------------------------------------------------------------

如果您使用 :option:`--enable-error-code unused-awaitable <mypy --enable-error-code>`，mypy 将生成错误，如果您不使用一个定义了 ``__await__`` 的返回值。

示例：

.. code-block:: python

    # mypy: enable-error-code="unused-awaitable"

    import asyncio

    async def f() -> int: ...

    async def g() -> None:
        # 错误: 类型 "Task[int]" 的值必须被使用
        #        您是否缺少 await？
        asyncio.create_task(f())

您可以将值赋给一个临时的、未使用的变量来静默错误：

.. code-block:: python

    async def g() -> None:
        _ = asyncio.create_task(f())  # 没有错误

.. _code-unused-ignore:

检查 ``# type: ignore`` 注释是否被使用 [unused-ignore]
-------------------------------------------------------------

如果您使用 :option:`--enable-error-code unused-ignore <mypy --enable-error-code>`，或 :option:`--warn-unused-ignores <mypy --warn-unused-ignores>`，mypy 将生成错误，如果您没有使用 ``# type: ignore`` 注释，即如果有注释，但这一行上不会由 mypy 生成任何错误。

示例：

.. code-block:: python

    # 使用 "mypy --warn-unused-ignores ..."

    def add(a: int, b: int) -> int:
        # 错误: 未使用的 "type: ignore" 注释
        return a + b  # type: ignore

请注意，由于此注释的特定性质，唯一可以选择性静默它的方法是显式包含错误代码。还请注意，如果由于代码静态不可达（例如由于平台或版本检查），未使用 ``# type: ignore`` ，则不会显示此错误。

示例：

.. code-block:: python

    # 使用 "mypy --warn-unused-ignores ..."

    import sys

    try:
        # "[unused-ignore]" 是必需的，以便在 Python 3.8 和 3.9 上进行干净的 mypy 运行
        # 此模块在这两个版本中均已添加
        import graphlib  # type: ignore[import,unused-ignore]
    except ImportError:
        pass

    if sys.version_info >= (3, 9):
        # 以下内容在 Python 3.8 或 3.9 上都不会生成错误
        42 + "testing..."  # type: ignore

.. _code-explicit-override:

检查在重写基类方法时是否使用 ``@override`` [explicit-override]
----------------------------------------------------------------------------------------

如果您使用 :option:`--enable-error-code explicit-override <mypy --enable-error-code>` ，mypy 将生成错误，如果您在重写基类方法时未使用 ``@override`` 装饰器。重写 ``__init__`` 或 ``__new__`` 时不会发出错误。请参见 `PEP 698 <https://peps.python.org/pep-0698/#strict-enforcement-per-project>`_。

.. note::

    从 Python 3.12 开始，可以从 ``typing`` 导入 ``@override``。
    若要在旧版本的 Python 中使用，请从 ``typing_extensions`` 导入它。

示例：

.. code-block:: python

    # mypy: enable-error-code="explicit-override"

    from typing import override

    class Parent:
        def f(self, x: int) -> None:
            pass

        def g(self, y: int) -> None:
            pass


    class Child(Parent):
        def f(self, x: int) -> None:  # 错误: 缺少 @override 装饰器
            pass

        @override
        def g(self, y: int) -> None:
            pass

.. _code-mutable-override:

检查可变属性的重写是否安全 [mutable-override]
----------------------------------------------------------------------

`mutable-override` 将启用对可变属性不安全重写的检查。由于历史原因，并且因为这是 Python 中相对常见的模式，因此默认情况下未启用此检查。下面的示例是不安全的，当启用此错误代码时将被标记：

.. code-block:: python

    from typing import Any

    class C:
        x: float
        y: float
        z: float

    class D(C):
        x: int  # 错误: 可变属性的协变重写
                # （基类 "C" 定义的类型为 "float",
                # 表达式的类型为 "int"）[mutable-override]
        y: float  # 正确
        z: Any  # 正确

    def f(c: C) -> None:
        c.x = 1.1
    d = D()
    f(d)
    d.x >> 1  # 这将在运行时崩溃，因为 d.x 现在是 float，而不是 int

.. _code-unimported-reveal:

检查 ``reveal_type`` 是否从 typing 或 typing_extensions 导入 [unimported-reveal]
-------------------------------------------------------------------------------------------

Mypy 以前将 ``reveal_type`` 作为一种特殊的内置函数，仅在类型检查期间存在。在运行时，它会以预期的 ``NameError`` 失败，这可能在生产中造成实际问题，而被 mypy 隐藏。

但是，在 Python3.11 中添加了 :py:func:`typing.reveal_type`。``typing_extensions`` 将此辅助功能移植到所有支持的 Python 版本中。

现在用户可以实际导入 ``reveal_type`` 来确保运行时代码安全。

.. note::

    从 Python 3.11 开始，可以从 ``typing`` 导入 ``reveal_type``。
    若要在旧版本的 Python 中使用，请从 ``typing_extensions`` 导入它。

.. code-block:: python

    # mypy: enable-error-code="unimported-reveal"

    x = 1
    reveal_type(x)  # 注意: 显示的类型是 "builtins.int" \
                    # 错误: 名称 "reveal_type" 未定义

正确用法：

.. code-block:: python

    # mypy: enable-error-code="unimported-reveal"
    from typing import reveal_type   # 或者 `typing_extensions`

    x = 1
    # 这不会引发错误：
    reveal_type(x)  # 注意: 显示的类型是 "builtins.int"

当启用此代码时，使用 ``reveal_locals`` 始终是错误的，因为无法导入它。

.. _code-narrowed-type-not-subtype:

检查 ``TypeIs`` 是否缩小类型 [narrowed-type-not-subtype]
---------------------------------------------------------------

:pep:`742` 要求在使用 ``TypeIs`` 时，缩小的类型必须是原始类型的子类型::

    from typing_extensions import TypeIs

    def f(x: int) -> TypeIs[str]:  # 错误，str 不是 int 的子类型
        ...

    def g(x: object) -> TypeIs[str]:  # 正确
        ...
