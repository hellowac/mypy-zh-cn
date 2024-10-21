更多类型
==========

本节介绍了几种额外类型，包括 :py:data:`~typing.NoReturn` 、 :py:class:`~typing.NewType` 和用于异步代码的类型。还讨论了如何使用重载为函数提供更精确的类型。这些仅在特定情况下有用，因此可以随时跳过本节，等到需要时再回来。

以下是本节内容的快速总结：

* :py:data:`~typing.NoReturn` 让您告诉 mypy 某个函数永远不会正常返回。

* :py:class:`~typing.NewType` 让您定义一个类型的变体，该变体在 mypy 中被视为单独的类型，但在运行时与原始类型相同。例如，您可以将 ``UserId`` 作为 ``int`` 的变体，而在运行时它只是一个 ``int``。

* :py:func:`@overload <typing.overload>` 让您定义一个可以接受多个不同签名的函数。如果您需要编码参数与返回类型之间的关系，而这种关系通常很难表达，这将非常有用。

* 异步类型让您可以使用 ``async`` 和 ``await`` 进行程序的类型检查。

.. _noreturn:

NoReturn 类型
*****************

Mypy 提供对从不返回的函数的支持。例如，一个无条件抛出异常的函数：

.. code-block:: python

   from typing import NoReturn

   def stop() -> NoReturn:
       raise Exception('no way')

Mypy 将确保标注为返回 :py:data:`~typing.NoReturn` 的函数确实不会返回，无论是隐式还是显式。Mypy 还会识别在调用此类函数后的代码是不可达的，并相应地进行处理：

.. code-block:: python

   def f(x: int) -> int:
       if x == 0:
           return x
       stop()
       return 'whatever works'  # 在不可达的代码块中没有错误

在早期版本的 Python 中，您需要使用 pip 安装 ``typing_extensions`` 才能在代码中使用 :py:data:`~typing.NoReturn` 。Python 3 命令行：

.. code-block:: text

    python3 -m pip install --upgrade typing-extensions

.. _newtypes:

NewTypes
********

在某些情况下，您可能希望通过创建简单的派生类来避免编程错误，这些派生类仅用于区分某些值与基类实例。例如：

.. code-block:: python

    class UserId(int):
        pass

    def get_by_user_id(user_id: UserId):
        ...

然而，这种方法会引入一些运行时开销。为避免这种情况，typing 模块提供了一个辅助对象 :py:class:`~typing.NewType` ，可以创建几乎没有运行时开销的简单唯一类型。Mypy 将把语句 ``Derived = NewType('Derived', Base)`` 视为与以下定义大致等效：

.. code-block:: python

    class Derived(Base):
        def __init__(self, _x: Base) -> None:
            ...

然而，在运行时，``NewType('Derived', Base)`` 将返回一个虚拟的可调用对象，该对象仅返回其参数：

.. code-block:: python

    def Derived(_x):
        return _x

Mypy 将要求在期望 ``UserId`` 的地方进行从 ``int`` 的显式转换，同时在期望 ``int`` 的地方隐式转换自 ``UserId``。示例：

.. code-block:: python

    from typing import NewType

    UserId = NewType('UserId', int)

    def name_by_id(user_id: UserId) -> str:
        ...

    UserId('user')          # 类型检查失败

    name_by_id(42)          # 类型检查失败
    name_by_id(UserId(42))  # 正常

:py:class:`~typing.NewType` 接受两个参数。第一个参数必须是包含新类型名称的字符串字面量，并且必须与分配新类型的变量名称相等。第二个参数必须是一个适当的可子类化类，即，不能是像 :ref:`union type <union-types>` 这样的类型构造。

:py:class:`~typing.NewType` 返回的可调用对象只接受一个参数；这等同于仅支持一个构造函数，该构造函数接受基类的实例（见上文）。示例：

.. code-block:: python

    from typing import NewType

    class PacketId:
        def __init__(self, major: int, minor: int) -> None:
            self._major = major
            self._minor = minor

    TcpPacketId = NewType('TcpPacketId', PacketId)

    packet = PacketId(100, 100)
    tcp_packet = TcpPacketId(packet)  # 正常

    tcp_packet = TcpPacketId(127, 0)  # 在类型检查器和运行时都失败

您不能对 :py:class:`~typing.NewType` 返回的对象使用 :py:func:`isinstance` 或 :py:func:`issubclass`，也不能对子类化 :py:class:`~typing.NewType` 返回的对象。

.. note::

    与类型别名不同，使用 :py:class:`~typing.NewType` 时将创建一个全新且唯一的类型。 :py:class:`~typing.NewType` 的目的是帮助您检测意外将旧基类型与新派生类型混合在一起的情况。

    例如，以下代码在使用类型别名时将成功通过类型检查：

    .. code-block:: python

        UserId = int

        def name_by_id(user_id: UserId) -> str:
            ...

        name_by_id(3)  # int 和 UserId 是同义的

    但是，使用 :py:class:`~typing.NewType` 的类似示例将无法通过类型检查：

    .. code-block:: python

        from typing import NewType

        UserId = NewType('UserId', int)

        def name_by_id(user_id: UserId) -> str:
            ...

        name_by_id(3)  # int 与 UserId 不相同

.. _function-overloading:

函数重载(overload)
********************

有时，函数的参数和类型之间的关系无法通过 :ref:`union types <union-types>` 捕获。例如，假设我们想编写一个可以接受 x-y 坐标的函数。如果我们只传入一个 x-y 坐标，我们返回一个 ``ClickEvent`` 对象。然而，如果我们传入两个 x-y 坐标，我们返回一个 ``DragEvent`` 对象。

我们编写这个函数的第一次尝试可能如下所示：

.. code-block:: python

    def mouse_event(x1: int,
                    y1: int,
                    x2: int | None = None,
                    y2: int | None = None) -> ClickEvent | DragEvent:
        if x2 is None and y2 is None:
            return ClickEvent(x1, y1)
        elif x2 is not None and y2 is not None:
            return DragEvent(x1, y1, x2, y2)
        else:
            raise TypeError("Bad arguments")

虽然这个函数签名是可行的，但它太宽松：它暗示 ``mouse_event`` 无论我们传入多少个参数都可能返回任意对象。它也不禁止调用者传入错误数量的整数；例如，mypy 会将 ``mouse_event(1, 2, 20)`` 视为有效。

我们可以通过使用 :pep:`overloading <484#function-method-overloading>` 来改善这一点，它允许我们为同一函数提供多个类型注解（签名），以更准确地描述函数的行为：

.. code-block:: python

    from typing import overload

    # 'mouse_event' 的重载 *变体*。
    # 这些变体向类型检查器提供额外信息。
    # 它们在运行时被忽略。

    @overload
    def mouse_event(x1: int, y1: int) -> ClickEvent: ...
    @overload
    def mouse_event(x1: int, y1: int, x2: int, y2: int) -> DragEvent: ...

    # 'mouse_event' 的实际 *实现*。
    # 实现包含实际的运行时逻辑。
    #
    # 它可以有类型提示，也可以没有。如果有，mypy
    # 将检查实现的主体是否与类型提示一致。
    #
    # Mypy 还会检查并确保签名与提供的变体一致。

    def mouse_event(x1: int,
                    y1: int,
                    x2: int | None = None,
                    y2: int | None = None) -> ClickEvent | DragEvent:
        if x2 is None and y2 is None:
            return ClickEvent(x1, y1)
        elif x2 is not None and y2 is not None:
            return DragEvent(x1, y1, x2, y2)
        else:
            raise TypeError("Bad arguments")

这使得 mypy 可以更精确地理解对 ``mouse_event`` 的调用。例如，mypy 将理解 ``mouse_event(5, 25)`` 始终返回 ``ClickEvent`` 类型，并会对调用 ``mouse_event(5, 25, 2)`` 报告错误。

作为另一个示例，假设我们想编写一个自定义容器类，该类实现 :py:meth:`__getitem__ <object.__getitem__>` 方法( ``[]`` 括号索引）。如果该方法接收一个整数，我们返回一个单一项。如果它接收一个 ``slice`` ，我们返回一个 :py:class:`~collections.abc.Sequence` 的项。

我们可以通过使用重载准确地编码参数与返回类型之间的关系，如下所示（Python 3.12 语法）：

.. code-block:: python

    from collections.abc import Sequence
    from typing import overload

    class MyList[T](Sequence[T]):
        @overload
        def __getitem__(self, index: int) -> T: ...

        @overload
        def __getitem__(self, index: slice) -> Sequence[T]: ...

        def __getitem__(self, index: int | slice) -> T | Sequence[T]:
            if isinstance(index, int):
                # 返回 T
            elif isinstance(index, slice):
                # 返回 T 的序列
            else:
                raise TypeError(...)

以下是使用旧版语法（Python 3.11 及之前版本）的相同示例：

.. code-block:: python

    from collections.abc import Sequence
    from typing import TypeVar, overload

    T = TypeVar('T')

    class MyList(Sequence[T]):
        @overload
        def __getitem__(self, index: int) -> T: ...

        @overload
        def __getitem__(self, index: slice) -> Sequence[T]: ...

        def __getitem__(self, index: int | slice) -> T | Sequence[T]:
            if isinstance(index, int):
                # 返回 T
            elif isinstance(index, slice):
                # 返回 T 的序列
            else:
                raise TypeError(...)

.. note::

   如果您只需要将类型变量限制为某些类型或子类型，可以使用 :ref:`value restriction
   <type-variable-value-restriction>`。

函数参数的默认值不会影响其签名——只有默认值的缺失或存在才会影响。因此，为减少冗余，可以在重载定义中用 ``...`` 作为占位符替换默认值：

.. code-block:: python

    from typing import overload

    class M: ...

    @overload
    def get_model(model_or_pk: M, flag: bool = ...) -> M: ...
    @overload
    def get_model(model_or_pk: int, flag: bool = ...) -> M | None: ...

    def get_model(model_or_pk: int | M, flag: bool = True) -> M | None:
        ...


运行时行为(behavior)
-------------------------

重载函数必须由两个或多个重载 *变体* 和一个 *实现* 组成。变体和实现必须在代码中相邻：可以将它们视为一个不可分割的单元。

变体主体必须都是空的；只有实现允许包含代码。这是因为在运行时，变体会被完全忽略：它们被最终的实现函数覆盖。

这意味着重载函数仍然是一个普通的 Python 函数!没有自动调度处理，您必须在实现中手动处理不同的类型（例如，通过使用 ``if`` 语句和 :py:func:`isinstance <isinstance>` 检查）。

如果您在存根文件中添加重载，应该省略实现函数：存根不包含运行时逻辑。

.. note::

   虽然我们可以使用 ``pass`` 关键字留空变体主体，但更常见的约定是使用省略号( ``...`` )字面量。

重载调用时的类型检查(Type checking)
-----------------------------------------

当您调用一个重载函数时，mypy 将通过选择最佳匹配的变体来推断正确的返回类型，同时考虑参数类型和数量。然而，调用永远不会与实现进行类型检查。这就是为什么 mypy 会将像 ``mouse_event(5, 25, 3)`` 的调用报告为无效，即使它与实现签名匹配。

如果有多个同样好的匹配变体，mypy 将选择第一个定义的变体。例如，考虑以下程序：

.. code-block:: python

    # 对于 Python 3.8 及以下版本，您必须使用 `typing.List` 而不是 `list`。例如：
    # from typing import List
    from typing import overload

    @overload
    def summarize(data: list[int]) -> float: ...

    @overload
    def summarize(data: list[str]) -> str: ...

    def summarize(data):
        if not data:
            return 0.0
        elif isinstance(data[0], int):
            # 执行整数特定代码
        else:
            # 执行字符串特定代码

    # 'output' 的类型是什么？float 还是 str？
    output = summarize([])

``summarize([])`` 调用匹配两个变体：一个空列表可以是 ``list[int]`` 或 ``list[str]``。在这种情况下，mypy 将通过选择第一个匹配的变体来打破平局：``output`` 将推断为 ``float`` 类型。实现者有责任确保 ``summarize`` 在运行时以相同的方式打破平局。

然而，“选择第一个匹配”规则有两个例外。首先，如果由于某个参数的类型为 ``Any`` 而匹配多个变体，mypy 将使推断类型也为 ``Any``：

.. code-block:: python

    dynamic_var: Any = some_dynamic_function()

    # output2 的类型为 'Any'
    output2 = summarize(dynamic_var)

其次，如果由于一个或多个参数是联合类型而匹配多个变体，mypy 将使推断类型为匹配变体返回的联合类型：

.. code-block:: python

    some_list: list[int] | list[str]

    # output3 的类型为 'float | str'
    output3 = summarize(some_list)

.. note::

   由于“选择第一个匹配(pick the first match)”规则，更改重载变体的顺序可能会改变 mypy 如何对您的程序进行类型检查。

   为了最小化潜在问题，我们建议您：

   1. 确保您的重载变体按与实现中运行时检查（例如 :py:func:`isinstance <isinstance>` 检查）相同的顺序列出。
   2. 按从最具体到最不具体的顺序排列您的变体和运行时检查。
      （请参见下一小节的示例）。

类型检查的变体(variants)
-----------------------------

Mypy 将对您的重载变体定义执行几项检查，以确保它们按预期行为。首先，mypy 将检查并确保没有重载变体遮蔽后续变体。例如，考虑以下函数，它将两个 ``Expression`` 对象相加，并包含一个特殊案例以处理接收两个 ``Literal`` 类型：

.. code-block:: python

    from typing import overload

    class Expression:
        # ...snip...

    class Literal(Expression):
        # ...snip...

    # 警告 - 第一个重载变体遮蔽了第二个!

    @overload
    def add(left: Expression, right: Expression) -> Expression: ...

    @overload
    def add(left: Literal, right: Literal) -> Literal: ...

    def add(left: Expression, right: Expression) -> Expression:
        # ...snip...

虽然这个代码片段在技术上是类型安全的，但它确实包含一种反模式：第二个变体永远不会被选择!如果我们尝试调用 ``add(Literal(3), Literal(4))``，mypy 将始终选择第一个变体，并将函数调用的类型评估为 ``Expression``，而不是 ``Literal``。这是因为 ``Literal`` 是 ``Expression`` 的子类型，这意味着“选择第一个匹配”规则在考虑第一个重载后总是会停止。

由于拥有一个永远无法匹配的重载变体几乎肯定是一个错误，mypy 将报告错误。要修复错误，我们可以 1) 删除第二个重载或 2) 交换重载的顺序：

.. code-block:: python

    # 现在一切正常 - 变体的顺序从最具体到最不具体正确。

    @overload
    def add(left: Literal, right: Literal) -> Literal: ...

    @overload
    def add(left: Expression, right: Expression) -> Expression: ...

    def add(left: Expression, right: Expression) -> Expression:
        # ...snip...

Mypy 还将对不同的变体进行类型检查，并标记任何具有固有不安全重叠变体的重载。例如，考虑以下不安全的重载定义：

.. code-block:: python

    from typing import overload

    @overload
    def unsafe_func(x: int) -> int: ...

    @overload
    def unsafe_func(x: object) -> str: ...

    def unsafe_func(x: object) -> int | str:
        if isinstance(x, int):
            return 42
        else:
            return "some string"

表面上看，这个函数定义似乎没有问题。然而，当我们尝试这样使用它时，它将导致推断类型与实际运行时类型之间的差异：

.. code-block:: python

    some_obj: object = 42
    unsafe_func(some_obj) + " danger danger"  # 类型检查通过，但在运行时崩溃!

由于 ``some_obj`` 的类型为 :py:class:`object`，mypy 将决定 ``unsafe_func`` 必须返回某种类型为 ``str`` 的值，从而得出上述将通过类型检查的结论。但实际上，``unsafe_func`` 将返回一个整数，导致代码在运行时崩溃!

为了防止这些类型的问题，mypy 将检测并禁止固有不安全重叠的重载，尽可能地进行努力。当以下两个条件都为真时，两个变体被视为不安全重叠：

1. 第一个变体的所有参数都可能与第二个参数兼容。
2. 第一个变体的返回类型与第二个不兼容（例如，不是子类型）。

因此在这个例子中，第一个变体中的 ``int`` 参数是第二个的 ``object`` 参数的子类型，但 ``int`` 返回类型不是 ``str`` 的子类型。两个条件都成立，所以 mypy 会正确标记 ``unsafe_func`` 为不安全。

请注意，在您忽略重叠重载错误的情况下，mypy 通常仍会在调用位置推断出您期望的类型。

然而，mypy 并不会检测到 *所有* 不安全的重载使用。例如，假设我们修改上述代码片段，使其调用 ``summarize`` 而不是 ``unsafe_func``：

.. code-block:: python

    some_list: list[str] = []
    summarize(some_list) + "danger danger"  # 类型安全，但在运行时崩溃!

我们在这里遇到了类似的问题。如果我们只查看重载上的注解，这个程序会通过类型检查。但由于 ``summarize(...)`` 设计为在接收到空列表时偏向返回浮点数，因此这个程序实际上会在运行时崩溃。

mypy 不会将像 ``summarize`` 这样的定义标记为潜在不安全的原因是，如果这样做，将极其困难编写安全的重载。例如，假设我们定义一个具有两个变体的重载，分别接受类型 ``A`` 和 ``B``。即使这两种类型完全不相关，用户仍然可以通过传入某个继承自 ``A`` 和 ``B`` 的第三种类型 ``C`` 的值来触发类似于上述的运行时错误。

幸运的是，这类情况相对较少。这意味着，在设计或使用可能接收看似无关类型实例的重载函数时，您应该保持谨慎。


类型检查的实现(implementation)
---------------------------------

实现的主体会根据提供的类型提示进行类型检查。例如，在上面的 ``MyList`` 示例中，主体中的代码会根据参数列表 ``index: int | slice`` 和返回类型 ``T | Sequence[T]`` 进行检查。如果实现上没有注解，则主体不会进行类型检查。如果您希望强制 mypy 检查主体，可以使用 :option:`--check-untyped-defs <mypy --check-untyped-defs>` 标志（:ref:`更多细节见这里 <untyped-definitions-and-calls>`）。

变体也必须与实现的类型提示兼容。在 ``MyList`` 示例中，mypy 将检查参数类型 ``int`` 和返回类型 ``T`` 是否与第一个变体的 ``int | slice`` 和 ``T | Sequence`` 兼容。对于第二个变体，它验证参数类型 ``slice`` 和返回类型 ``Sequence[T]`` 是否与 ``int | slice`` 和 ``T | Sequence`` 兼容。

.. note::

   上述重载语义是从 mypy 0.620 开始的新特性。

   之前，mypy 对所有重载变体执行类型擦除。例如，前一节中的 ``summarize`` 示例以前是非法的，因为 ``list[str]`` 和 ``list[int]`` 都擦除为 ``list[Any]``。这个限制在 mypy 0.620 中被移除。

   此外，mypy 之前使用不同的算法选择最佳匹配变体。如果该算法未能找到匹配项，则默认为返回 ``Any``。新算法使用“选择第一个匹配”规则，只有在输入参数中也包含 ``Any`` 时，才会回退到返回 ``Any``。


有条件的重载(Conditional)
----------------------------

有时，有条件的定义重载是有用的。常见用例包括在运行时不可用的类型或仅在某些 Python 版本中存在的类型。所有现有的重载规则仍然适用。例如，必须至少有两个重载。

.. note::

    Mypy 只能推断有限数量的条件。
    当前支持的条件包括 :py:data:`~typing.TYPE_CHECKING`、``MYPY``、
    :ref:`version_and_platform_checks`、:option:`--always-true <mypy --always-true>`，
    和 :option:`--always-false <mypy --always-false>` 值。

.. code-block:: python

    from typing import TYPE_CHECKING, Any, overload

    if TYPE_CHECKING:
        class A: ...
        class B: ...


    if TYPE_CHECKING:
        @overload
        def func(var: A) -> A: ...

        @overload
        def func(var: B) -> B: ...

    def func(var: Any) -> Any:
        return var


    reveal_type(func(A()))  # 显示类型为 "A"

.. code-block:: python

    # flags: --python-version 3.10
    import sys
    from typing import Any, overload

    class A: ...
    class B: ...
    class C: ...
    class D: ...


    if sys.version_info < (3, 7):
        @overload
        def func(var: A) -> A: ...

    elif sys.version_info >= (3, 10):
        @overload
        def func(var: B) -> B: ...

    else:
        @overload
        def func(var: C) -> C: ...

    @overload
    def func(var: D) -> D: ...

    def func(var: Any) -> Any:
        return var


    reveal_type(func(B()))  # 显示类型为 "B"
    reveal_type(func(C()))  # 没有 "func" 的重载变体与参数类型 "C" 匹配
        # 可能的重载变体：
        #     def func(var: B) -> B
        #     def func(var: D) -> D
        # 显示类型为 "Any"


.. note::

    在最后一个示例中，mypy 是通过
    :option:`--python-version 3.10 <mypy --python-version>` 执行的。
    因此，条件 ``sys.version_info >= (3, 10)`` 将匹配，
    并且 ``B`` 的重载将被添加。
    对 ``A`` 和 ``C`` 的重载会被忽略!
    对 ``D`` 的重载并不是条件定义的，因此也会被添加。

当 mypy 无法推断某个条件始终为 ``True`` 或始终为 ``False`` 时，会发出错误。

.. code-block:: python

    from typing import Any, overload

    class A: ...
    class B: ...


    def g(bool_var: bool) -> None:
        if bool_var:  # 条件无法推断，无法合并重载
            @overload
            def func(var: A) -> A: ...

            @overload
            def func(var: B) -> B: ...

        def func(var: Any) -> Any: ...

        reveal_type(func(A()))  # 显示类型为 "Any"


.. _advanced_self:

self类型的高级用法(self-types)
**********************************

通常，mypy 不要求实例方法和类方法的第一个参数进行注解。然而，为了实现某些编程模式的更精确静态类型，可能需要进行注解。

在泛型类中的受限方法(Restricted methods)
--------------------------------------------

在泛型类中，有些方法可能仅允许对某些类型参数的值进行调用（Python 3.12 语法）：

.. code-block:: python

   class Tag[T]:
       item: T

       def uppercase_item(self: Tag[str]) -> str:
           return self.item.upper()

   def label(ti: Tag[int], ts: Tag[str]) -> None:
       ti.uppercase_item()  # E: 无效的 self 参数 "Tag[int]" 传递给属性函数
                            # "uppercase_item"，类型为 "Callable[[Tag[str]], str]"
       ts.uppercase_item()  # 这是可以的

这种模式还允许在类型参数本身为泛型的情况下对嵌套类型进行匹配（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Sequence

   class Storage[T]:
       def __init__(self, content: T) -> None:
           self._content = content

       def first_chunk[S](self: Storage[Sequence[S]]) -> S:
           return self._content[0]

   page: Storage[list[str]]
   page.first_chunk()  # OK，类型为 "str"

   Storage(0).first_chunk()  # 错误：无效的 self 参数 "Storage[int]" 传递给属性函数
                             # "first_chunk"，类型为 "Callable[[Storage[Sequence[S]]], S]"

最后，可以在 self类型(self-type) 上使用重载来表达一些复杂方法的精确类型（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Callable
   from typing import overload

   class Tag[T]:
       @overload
       def export(self: Tag[str]) -> str: ...
       @overload
       def export(self, converter: Callable[[T], str]) -> str: ...

       def export(self, converter=None):
           if isinstance(self.item, str):
               return self.item
           return converter(self.item)

特别是，重载 self类型(self-type) 的 :py:meth:`~object.__init__` 方法对于注解泛型类构造函数可能很有用，其中类型参数以非平凡的方式依赖于构造函数参数，参见例如 :py:class:`~subprocess.Popen`。

Mixin 类
-------------

在混入方法中使用宿主类协议作为自类型，可以提高混入类静态类型的代码重用性。例如，可以定义一个协议来定义宿主类的通用功能，而不是在每个混入中添加所需的抽象方法：

.. code-block:: python

   class Lockable(Protocol):
       @property
       def lock(self) -> Lock: ...

   class AtomicCloseMixin:
       def atomic_close(self: Lockable) -> int:
           with self.lock:
               # 执行操作

   class AtomicOpenMixin:
       def atomic_open(self: Lockable) -> int:
           with self.lock:
               # 执行操作

   class File(AtomicCloseMixin, AtomicOpenMixin):
       def __init__(self) -> None:
           self.lock = Lock()

   class Bad(AtomicCloseMixin):
       pass

   f = File()
   b: Bad
   f.atomic_close()  # OK
   b.atomic_close()  # 错误：无效的 self 类型用于 "atomic_close"

请注意，当显式 self类型(self-type) 不是当前类的超类时， *需要* 为协议。在这种情况下，mypy 仅在调用处检查 self类型(self-type) 的有效性。

替代构造函数的精确类型(Precise typing)
------------------------------------------

某些类可能定义替代构造函数。如果这些类是泛型的， self类型(self-type) 允许为它们提供精确的签名（Python 3.12 语法）：

.. code-block:: python

   from typing import Self

   class Base[T]:
       def __init__(self, item: T) -> None:
           self.item = item

       @classmethod
       def make_pair(cls, item: T) -> tuple[Self, Self]:
           return cls(item), cls(item)

   class Sub[T](Base[T]):
       ...

   pair = Sub.make_pair('yes')  # 类型为 "tuple[Sub[str], Sub[str]]"
   bad = Sub[int].make_pair('no')  # 错误：传递给 "Base" 的 "make_pair" 的参数 1
                                   # 类型不兼容，实际类型为 "str"，预期为 "int"

.. _async-and-await:

async/await 注解(Typing)
********************************

Mypy 允许你为使用 ``async/await`` 语法的协程进行类型注解。有关协程的更多信息，请参见 :pep:`492` 和 `asyncio 文档 <python:library/asyncio>`_。

使用 ``async def`` 定义的函数的类型注解与普通函数相似。返回类型注解应与在 ``await`` 协程时预期返回的值的类型相同。

.. code-block:: python

   import asyncio

   async def format_string(tag: str, count: int) -> str:
       return f'T-minus {count} ({tag})'

   async def countdown(tag: str, count: int) -> str:
       while count > 0:
           my_str = await format_string(tag, count)  # 类型被推断为 str
           print(my_str)
           await asyncio.sleep(0.1)
           count -= 1
       return "Blastoff!"

   asyncio.run(countdown("Millennium Falcon", 5))

调用 ``async def`` 函数 *而不等待(without awaiting)* 的结果将自动推断为
类型 :py:class:`Coroutine[Any, Any, T] <collections.abc.Coroutine>`，这是
:py:class:`Awaitable[T] <collections.abc.Awaitable>` 的一个子类型：

.. code-block:: python

   my_coroutine = countdown("Millennium Falcon", 5)
   reveal_type(my_coroutine)  # 显示类型为 "typing.Coroutine[Any, Any, builtins.str]"

.. _async-iterators:

异步迭代器(Asynchronous iterators)
-------------------------------------------

如果你有一个异步迭代器，可以在你的注解中使用 :py:class:`~collections.abc.AsyncIterator` 类型：

.. code-block:: python

   from collections.abc import AsyncIterator
   from typing import Optional
   import asyncio

   class arange:
       def __init__(self, start: int, stop: int, step: int) -> None:
           self.start = start
           self.stop = stop
           self.step = step
           self.count = start - step

       def __aiter__(self) -> AsyncIterator[int]:
           return self

       async def __anext__(self) -> int:
           self.count += self.step
           if self.count == self.stop:
               raise StopAsyncIteration
           else:
               return self.count

   async def run_countdown(tag: str, countdown: AsyncIterator[int]) -> str:
       async for i in countdown:
           print(f'T-minus {i} ({tag})')
           await asyncio.sleep(0.1)
       return "Blastoff!"

   asyncio.run(run_countdown("Serenity", arange(5, 0, -1)))

异步生成器（在 :pep:`525` 中引入）是创建异步迭代器的简单方法：

.. code-block:: python

   from collections.abc import AsyncGenerator
   from typing import Optional
   import asyncio

   # 也可以将此类型注解为返回 AsyncIterator[int]
   async def arange(start: int, stop: int, step: int) -> AsyncGenerator[int, None]:
       current = start
       while (step > 0 and current < stop) or (step < 0 and current > stop):
           yield current
           current += step

   asyncio.run(run_countdown("Battlestar Galactica", arange(5, 0, -1)))

一个常见的误解是，在 ``async def`` 函数中存在 ``yield`` 语句会影响该函数的类型：

.. code-block:: python

   from collections.abc import AsyncIterator

   async def arange(stop: int) -> AsyncIterator[int]:
       # 调用时，arange 返回一个异步迭代器
       # 相当于 Callable[[int], AsyncIterator[int]]
       i = 0
       while i < stop:
           yield i
           i += 1

   async def coroutine(stop: int) -> AsyncIterator[int]:
       # 调用时，coroutine 返回一个可以等待以获取异步迭代器的对象
       # 相当于 Callable[[int], Coroutine[Any, Any, AsyncIterator[int]]]
       return arange(stop)

   async def main() -> None:
       reveal_type(arange(5))  # 显示类型为 "typing.AsyncIterator[builtins.int]"
       reveal_type(coroutine(5))  # 显示类型为 "typing.Coroutine[Any, Any, typing.AsyncIterator[builtins.int]]"

       await arange(5)  # 错误：在 "await" 中类型不兼容（实际类型为 "AsyncIterator[int]"，预期类型为 "Awaitable[Any]"）
       reveal_type(await coroutine(5))  # 显示类型为 "typing.AsyncIterator[builtins.int]"

这在尝试定义基类、协议或重载时有时会出现：

.. code-block:: python

    from collections.abc import AsyncIterator
    from typing import Protocol, overload

    class LauncherIncorrect(Protocol):
        # 因为 launch 没有 yield，这里类型为
        # Callable[[], Coroutine[Any, Any, AsyncIterator[int]]]
        # 而不是
        # Callable[[], AsyncIterator[int]]
        async def launch(self) -> AsyncIterator[int]:
            raise NotImplementedError

    class LauncherCorrect(Protocol):
        def launch(self) -> AsyncIterator[int]:
            raise NotImplementedError

    class LauncherAlsoCorrect(Protocol):
        async def launch(self) -> AsyncIterator[int]:
            raise NotImplementedError
            if False:
                yield 0

    # 重载的类型与实现无关。
    # 特别是，它们的类型不受实现是否包含 `yield` 的影响。
    # 使用 `def` 清楚表明类型是 Callable[..., AsyncIterator[int]]，
    # 而使用 `async def` 则是 Callable[..., Coroutine[Any, Any, AsyncIterator[int]]]
    @overload
    def launch(*, count: int = ...) -> AsyncIterator[int]: ...
    @overload
    def launch(*, time: float = ...) -> AsyncIterator[int]: ...

    async def launch(*, count: int = 0, time: float = 0) -> AsyncIterator[int]:
        # launch 的实现是一个异步生成器，并包含一个 yield
        yield 0
