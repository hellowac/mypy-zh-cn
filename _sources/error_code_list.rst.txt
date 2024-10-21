.. _error-code-list:

默认启用的错误代码(Error codes enabled by default)
============================================================

本节记录了 mypy 在默认选项下可以生成的各种错误代码。有关错误代码的总体文档，请参见 :ref:`error-codes`。 :ref:`error-codes-optional` 文档记录了您可以启用的其他错误代码。

.. _code-attr-defined:

检查属性是否存在 [attr-defined]
------------------------------------------

Mypy 检查在使用点操作符时目标类或模块中是否定义了属性。这适用于获取和设置属性。新属性通过类体中的赋值或方法中对 ``self.x`` 的赋值来定义。这些赋值不会生成 ``attr-defined`` 错误。

示例：

.. code-block:: python

   class Resource:
       def __init__(self, name: str) -> None:
           self.name = name

   r = Resource('x')
   print(r.name)  # OK
   print(r.id)  # 错误: "Resource" 没有属性 "id"  [attr-defined]
   r.id = 5  # 错误: "Resource" 没有属性 "id"  [attr-defined]

如果在 ``from ... import`` 语句中导入的名称在模块中未定义，则也会生成此错误代码（只要目标模块可以找到）：

.. code-block:: python

    # 错误: 模块 "os" 没有属性 "non_existent"  [attr-defined]
    from os import non_existent

对缺失属性的引用被赋予 ``Any`` 类型。在上述示例中，``non_existent`` 的类型将是 ``Any``，这在您静默错误时可能很重要。

.. _code-union-attr:

检查每个联合项中属性是否存在 [union-attr]
-----------------------------------------------------------

如果您访问具有联合类型的值的属性，mypy 会检查该属性是否在该联合中的 *每个* 类型中定义。否则，该操作可能在运行时失败。这也适用于可选类型。

示例：

.. code-block:: python

   class Cat:
       def sleep(self) -> None: ...
       def miaow(self) -> None: ...

   class Dog:
       def sleep(self) -> None: ...
       def follow_me(self) -> None: ...

   def func(animal: Cat | Dog) -> None:
       # OK: 'sleep' 对 Cat 和 Dog 都是定义的
       animal.sleep()
       # 错误: "Cat | Dog" 的项 "Cat" 没有属性 "follow_me"  [union-attr]
       animal.follow_me()

您可以通过使用 ``assert isinstance(obj, ClassName)`` 或 ``assert obj is not None`` 来告诉 mypy 您知道该类型比 mypy 认为的更具体，从而通常绕过这些错误。

.. _code-name-defined:

检查名称是否定义 [name-defined]
-----------------------------------------

Mypy 期望所有名称的引用在活动作用域中都有相应的定义，例如赋值、函数定义或导入。这可以捕捉到缺失的定义、缺失的导入和拼写错误。

以下示例错误地调用了 ``sort()`` 而不是 :py:func:`sorted`：

.. code-block:: python

    x = sort([3, 2, 4])  # 错误: 名称 "sort" 未定义  [name-defined]

.. _code-used-before-def:

检查变量在定义之前是否被使用 [used-before-def]
-----------------------------------------------------------------------

如果名称在定义之前被使用，mypy 将生成一个错误。虽然名称定义检查可以捕捉到未定义名称的问题，但如果变量被使用然后在作用域内稍后定义，它不会标记。used-before-def 检查将捕捉到这种情况。

示例：

.. code-block:: python

    print(x)  # 错误: 名称 "x" 在定义之前被使用 [used-before-def]
    x = 123

.. _code-call-arg:

检查调用中的参数 [call-arg]
-----------------------------------

Mypy 期望参数的数量和名称与被调用函数匹配。请注意，参数类型检查有一个单独的错误代码 ``arg-type``。

示例：

.. code-block:: python

    def greet(name: str) -> None:
         print('hello', name)

    greet('jack')  # OK
    greet('jill', 'jack')  # 错误: "greet" 的参数过多 [call-arg]

.. _code-arg-type:

检查参数类型 [arg-type]
-------------------------------

Mypy 检查调用中的参数类型是否与被调用函数的签名中声明的参数类型匹配（如果存在的话）。

示例：

.. code-block:: python

    def first(x: list[int]) -> int:
        return x[0] if x else 0

    t = (5, 4)
    # 错误: 对 "first" 的参数 1 的类型不兼容 "tuple[int, int]";
    #        期望 "list[int]"  [arg-type]
    print(first(t))

.. _code-call-overload:

检查对重载函数的调用 [call-overload]
---------------------------------------------------

当您调用一个重载函数时，mypy 检查至少一个重载项的签名是否与调用中的参数类型匹配。

示例：

.. code-block:: python

   from typing import overload

   @overload
   def inc_maybe(x: None) -> None: ...

   @overload
   def inc_maybe(x: int) -> int: ...

   def inc_maybe(x: int | None) -> int | None:
        if x is None:
            return None
        else:
            return x + 1

   inc_maybe(None)  # OK
   inc_maybe(5)  # OK

   # 错误: "inc_maybe" 没有重载变体与参数类型 "float" 匹配  [call-overload]
   inc_maybe(1.2)

.. _code-valid-type:

检查类型的有效性 [valid-type]
------------------------------------

Mypy 检查每个类型注解以及任何表示类型的表达式是否有效。有效类型的示例包括类、联合类型、可调用类型、类型别名和字面量类型。无效类型的示例包括裸整数字面量、函数、变量和模块。

以下示例错误地将函数 ``log`` 用作类型：

.. code-block:: python

    def log(x: object) -> None:
        print('log:', repr(x))

    # 错误: 函数 "t.log" 作为类型无效  [valid-type]
    def log_all(objs: list[object], f: log) -> None:
        for x in objs:
            f(x)

您可以使用 :py:class:`~collections.abc.Callable` 作为可调用对象的类型：

.. code-block:: python

    from collections.abc import Callable

    # OK
    def log_all(objs: list[object], f: Callable[[object], None]) -> None:
        for x in objs:
            f(x)

.. _code-var-annotated:

当变量类型不明确时要求注解 [var-annotated]
--------------------------------------------------------------

在某些情况下，mypy 无法在没有显式注解的情况下推断变量的类型。Mypy 将此视为错误。这通常发生在您使用空集合或 ``None`` 初始化变量时。如果 mypy 无法推断集合项的类型，它将把它无法推断的类型部分替换为 ``Any`` 并生成错误。

带错误的示例：

.. code-block:: python

    class Bundle:
        def __init__(self) -> None:
            # 错误: "items" 需要类型注解
            #        （提示: "items: list[<type>] = ..."）  [var-annotated]
            self.items = []

    reveal_type(Bundle().items)  # list[Any]

为了解决此问题，我们添加显式注解：

.. code-block:: python

    class Bundle:
        def __init__(self) -> None:
            self.items: list[str] = []  # OK

    reveal_type(Bundle().items)  # list[str]

.. _code-override:

检查重写的有效性 [override]
--------------------------------------

Mypy 检查被重写的方法或属性是否与基类兼容。子类中的方法必须接受基类方法接受的所有参数，并且返回类型必须符合基类中的返回类型（Liskov 替代原则）。

在子类中，参数类型可以更一般（即可以反变）。返回类型可以在子类中缩小（即可以协变）。在子类方法中定义额外参数是可以的，只要所有额外参数都有默认值或可以省略（例如 ``*args`` )。

示例：

.. code-block:: python

   class Base:
       def method(self,
                  arg: int) -> int | None:
           ...

   class Derived(Base):
       def method(self,
                  arg: int | str) -> int:  # OK
           ...

   class DerivedBad(Base):
       # 错误: "method" 的参数 1 与 "Base" 不兼容  [override]
       def method(self,
                  arg: bool) -> int:
           ...

.. _code-return:

检查函数是否返回值 [return]
--------------------------------------------

如果函数具有非 ``None`` 返回类型，mypy 期望该函数始终显式返回一个值（或引发异常）。函数不应在末尾退出，因为这通常是一个错误。

示例：

.. code-block:: python

    # 错误: 缺少返回语句  [return]
    def show(x: int) -> int:
        print(x)

    # 错误: 缺少返回语句  [return]
    def pred1(x: int) -> int:
        if x > 0:
            return x - 1

    # OK
    def pred2(x: int) -> int:
        if x > 0:
            return x - 1
        else:
            raise ValueError('not defined for zero')

.. _code-empty-body:

检查函数的主体不为空 [empty-body]
-----------------------------------------------------------------------

此错误代码类似于 ``[return]`` 代码，但专门针对具有空主体的函数和方法（如果它们注解了非平凡返回类型）。这种区分的存在是因为在某些上下文中，空主体是有效的，例如用于抽象方法或在存根文件中。此外，旧版本的 mypy 一直无条件允许空主体的函数，因此拥有专门的错误代码简化了跨版本兼容性。

请注意，在 *协议* 中，方法的空主体是允许的，并且这样的方​​法被视为隐式抽象：

.. code-block:: python

   from abc import abstractmethod
   from typing import Protocol

   class RegularABC:
       @abstractmethod
       def foo(self) -> int:
           pass  # OK
       def bar(self) -> int:
           pass  # 错误: 缺少返回语句  [empty-body]

   class Proto(Protocol):
       def bar(self) -> int:
           pass  # OK

.. _code-return-value:

检查返回值是否兼容 [return-value]
----------------------------------------------------

Mypy 检查返回的值是否与函数的类型签名兼容。

示例：

.. code-block:: python

   def func(x: int) -> str:
       # 错误: 返回值类型不兼容（得到 "int"，预期 "str"）  [return-value]
       return x + 1

.. _code-assignment:

检查赋值语句中的类型 [assignment]
------------------------------------------------

Mypy 检查赋值表达式是否与赋值目标（或目标）兼容。

示例：

.. code-block:: python

    class Resource:
        def __init__(self, name: str) -> None:
            self.name = name

    r = Resource('A')

    r.name = 'B'  # OK

    # 错误: 赋值中的类型不兼容（表达式类型为 "int"，
    #        变量类型为 "str"）  [assignment]
    r.name = 5

.. _code-method-assign:

检查赋值目标是否为方法 [method-assign]
------------------------------------------------------------

一般来说，将类对象或实例上的方法赋值（即猴子补丁）在类型方面是模糊的，因为 Python 的静态类型系统无法表达绑定和未绑定可调用类型之间的区别。考虑以下示例：

.. code-block:: python

   class A:
       def f(self) -> None: pass
       def g(self) -> None: pass

   def h(self: A) -> None: pass

   A.f = h  # h 的类型是 Callable[[A], None]
   A().f()  # 这有效
   A.f = A().g  # A().g 的类型是 Callable[[], None]
   A().f()  # ...但这在运行时也有效

为了防止模糊性，mypy 默认会标记这两个赋值。如果禁用此错误代码，mypy 将把所有方法赋值中的赋值值视为未绑定，因此只有第二个赋值仍会生成错误。

.. note::

    此错误代码是更通用的 ``[assignment]`` 代码的子代码。

.. _code-type-var:

检查类型变量值 [type-var]
-------------------------------------

Mypy 检查类型变量的值是否与值限制或上限类型兼容。

示例（Python 3.12 语法）：

.. code-block:: python

    def add[T1: (int, float)](x: T1, y: T1) -> T1:
        return x + y

    add(4, 5.5)  # OK

    # 错误: "add" 的类型变量 "T1" 的值不能是 "str"  [type-var]
    add('x', 'y')

.. _code-operator:

检查各种运算符的使用 [operator]
------------------------------------------

Mypy 检查操作数是否支持二元或一元操作，例如 ``+`` 或 ``~`` 。索引操作非常常见，以至于它们有自己的错误代码 ``index`` （见下文）。

示例：

.. code-block:: python

   # 错误: 不支持的操作数类型用于 +（"int" 和 "str"）  [operator]
   1 + 'x'

.. _code-index:

检查索引操作 [index]
---------------------------------

Mypy 检查索引操作中索引值（如 ``x[y]`` )是否支持索引，并且索引表达式是否具有有效的类型。

示例：

.. code-block:: python

   a = {'x': 1, 'y': 2}

   a['x']  # OK

   # 错误: 对于 "dict[str, int]" 的无效索引类型 "int"；预期类型 "str"  [index]
   print(a[1])

   # 错误: 对于 "dict[str, int]" 的无效索引类型 "bytes"；预期类型 "str"  [index]
   a[b'x'] = 4

.. _code-list-item:

检查列表项 [list-item]
----------------------------

在使用 ``[item, ...]`` 构造列表时，mypy 检查每个项是否与从周围上下文推断出的列表类型兼容。

示例：

.. code-block:: python

    # 错误: 列表项 0 的类型不兼容 "int"；预期 "str"  [list-item]
    a: list[str] = [0]

.. _code-dict-item:

检查字典项 [dict-item]
----------------------------

在使用 ``{key: value, ...}`` 或 ``dict(key=value, ...)`` 构造字典时，mypy 检查每个键和值是否与从周围上下文推断出的字典类型兼容。

示例：

.. code-block:: python

    # 错误: 字典条目 0 的类型不兼容 "str": "str"；预期 "str": "int"  [dict-item]
    d: dict[str, int] = {'key': 'value'}

.. _code-typeddict-item:

检查 TypedDict 项 [typeddict-item]
--------------------------------------

在构造 TypedDict 对象时，mypy 检查每个键和值是否与从周围上下文推断出的 TypedDict 类型兼容。

在获取 TypedDict 项时，mypy 检查键是否存在。在对 TypedDict 进行赋值时，mypy 检查键和值是否有效。

示例：

.. code-block:: python

    from typing import TypedDict

    class Point(TypedDict):
        x: int
        y: int

    # 错误: 类型不兼容（表达式类型为 "float"，
    #        TypedDict 项 "x" 的类型为 "int"）  [typeddict-item]
    p: Point = {'x': 1.2, 'y': 4}

.. _code-typeddict-unknown-key:

检查 TypedDict 键 [typeddict-unknown-key]
--------------------------------------------

在构造 TypedDict 对象时，mypy 检查定义中是否包含未知键，以捕获无效键和拼写错误。另一方面，当将带有额外键的先前构造的 TypedDict 值作为参数传递给函数时，mypy 不会生成错误，因为 TypedDict 值支持结构子类型（“静态鸭子类型”），假设在构造时已验证了这些键。示例：

.. code-block:: python

    from typing import TypedDict

    class Point(TypedDict):
        x: int
        y: int

    class Point3D(Point):
        z: int

    def add_x_coordinates(a: Point, b: Point) -> int:
        return a["x"] + b["x"]

    a: Point = {"x": 1, "y": 4}
    b: Point3D = {"x": 2, "y": 5, "z": 6}

    add_x_coordinates(a, b)  # OK

    # 错误: TypedDict "Point" 的额外键 "z"  [typeddict-unknown-key]
    add_x_coordinates(a, {"x": 1, "y": 4, "z": 5})

使用未知键设置 TypedDict 项也会生成此错误，因为这可能是拼写错误：

.. code-block:: python

    a: Point = {"x": 1, "y": 2}
    # 错误: TypedDict "Point" 的额外键 "z"  [typeddict-unknown-key]
    a["z"] = 3

读取未知键将生成更一般（且更严重）的 ``typeddict-item`` 错误，这可能会导致运行时异常：

.. code-block:: python

    a: Point = {"x": 1, "y": 2}
    # 错误: TypedDict "Point" 没有键 "z"  [typeddict-item]
    _ = a["z"]

.. note::

    此错误代码是更广泛的 ``[typeddict-item]`` 代码的子代码。

.. _code-has-type:

检查目标的类型是否已知 [has-type]
---------------------------------------------

当 mypy 未能推断出被引用变量的任何类型时，有时会生成错误。这可能发生在引用在源文件中稍后初始化的变量，以及在形成导入循环的模块之间的引用。当发生这种情况时，引用将隐式获得 ``Any`` 类型。

在此示例中，``x`` 和 ``y`` 的定义是循环的：

.. code-block:: python

   class Problem:
       def set_x(self) -> None:
           # 错误: 无法确定 "y" 的类型  [has-type]
           self.x = self.y

       def set_y(self) -> None:
           self.y = self.x

要解决此错误，可以为目标变量或属性添加显式类型注解。有时，您还可以重新组织代码，使变量的定义在源文件中早于对该变量的引用。解开循环导入也可能有帮助。

我们为 ``y`` 属性添加显式注释以解决此问题：

.. code-block:: python

   class Problem:
       def set_x(self) -> None:
           self.x = self.y  # OK

       def set_y(self) -> None:
           self.y: int = self.x  # 在此处添加注释

.. _code-import:

检查导入问题 [import]
----------------------------------------

如果 mypy 无法解析 `import` 语句，则会生成错误。这是 `import-not-found` 和 `import-untyped` 的父错误代码。

请参见 :ref:`ignore-missing-imports` 以了解如何解决这些错误。

.. _code-import-not-found:

检查导入目标是否可以找到 [import-not-found]
--------------------------------------------------------

如果 mypy 找不到导入模块的源代码或存根文件，则会生成错误。

示例：

.. code-block:: python

    # 错误: 找不到名为 "m0dule_with_typo" 的模块的实现或库存根  [import-not-found]
    import m0dule_with_typo

请参见 :ref:`ignore-missing-imports` 以了解如何解决这些错误。

.. _code-import-untyped:

检查导入目标是否可以找到 [import-untyped]
--------------------------------------------------------

如果 mypy 能找到导入模块的源代码，但该模块不提供类型注解（通过 :ref:`PEP 561 <installed-packages>`），则会生成错误。

示例：

.. code-block:: python

    # 错误: "bs4" 的库存根未安装  [import-untyped]
    import bs4
    # 错误: 跳过分析 "no_py_typed": 模块已安装，但缺少库存根或 py.typed 标记  [import-untyped]
    import no_py_typed

在某些情况下，可以通过安装适当的存根包来修复这些错误。有关详细信息，请参见 :ref:`ignore-missing-imports`。

.. _code-no-redef:

检查每个名称是否仅定义一次 [no-redef]
-----------------------------------------------

如果在同一命名空间中有多个名称定义，mypy 可能会生成错误。原因是这通常是一个错误，因为第二个定义可能会覆盖第一个定义。此外，mypy 通常无法确定引用是指向第一个还是第二个定义，这会影响类型检查。

如果您忽略此错误，对定义名称的所有引用都将引用 *第一个* 定义。

示例：

.. code-block:: python

   class A:
       def __init__(self, x: int) -> None: ...

   class A:  # 错误: 名称 "A" 在第 1 行已经定义  [no-redef]
       def __init__(self, x: str) -> None: ...

   # 错误: "A" 的参数 1 类型不兼容 "str"；预期 "int"
   #        （第一个定义胜出!）
   A('x')

.. _code-func-returns-value:

检查被调用函数是否返回值 [func-returns-value]
---------------------------------------------------------------

如果您调用返回类型为 ``None`` 的函数且不忽略返回值，mypy 将报告错误，因为这通常（但并非总是）是编程错误。

在此示例中，``if f()`` 检查总是为假，因为 ``f`` 返回 ``None``：

.. code-block:: python

   def f() -> None:
       ...

   # OK: 我们不处理返回值
   f()

   # 错误: "f" 不返回值（它仅返回 None）  [func-returns-value]
   if f():
        print("not false")

.. _code-abstract:

检查抽象类的实例化 [abstract]
--------------------------------------------------

如果您尝试实例化抽象基类（ABC），mypy 会生成错误。抽象基类是至少包含一个抽象方法或属性的类。（参见 :py:mod:`abc` 模块文档）

有时，由于未实现的抽象方法，类会意外变为抽象类。在这种情况下，您需要为该方法提供实现，使类变为具体类（非抽象类）。

示例：

.. code-block:: python

    from abc import ABCMeta, abstractmethod

    class Persistent(metaclass=ABCMeta):
        @abstractmethod
        def save(self) -> None: ...

    class Thing(Persistent):
        def __init__(self) -> None:
            ...

        ...  # 没有 "save" 方法

    # 错误: 无法实例化具有抽象属性 "save" 的抽象类 "Thing"  [abstract]
    t = Thing()

.. _code-type-abstract:

安全处理抽象类型对象类型 [type-abstract]
-----------------------------------------------------------

Mypy 始终允许实例化（调用）类型为 ``type[t]`` 的对象，即使不知道 ``t`` 是否为非抽象类型，因为创建作为对象工厂（自定义构造函数）的函数是一种常见模式。因此，为了防止上述部分中描述的问题，当抽象类型对象作为预期的 ``type[t]`` 传递时，mypy 会给出错误。

示例（Python 3.12 语法）：

.. code-block:: python

   from abc import ABCMeta, abstractmethod

   class Config(metaclass=ABCMeta):
       @abstractmethod
       def get_value(self, attr: str) -> str: ...

   def make_many[T](typ: type[T], n: int) -> list[T]:
       return [typ() for _ in range(n)]  # 如果 typ 是抽象类，将引发错误

   # 错误: 只能在预期为 "type[Config]" 的地方提供具体类 [type-abstract]
   make_many(Config, 5)

.. _code-safe-super:

检查通过 super 调用抽象方法是否有效 [safe-super]
---------------------------------------------------------------------

抽象方法通常没有任何默认实现，即其主体为空。在子类中通过 ``super()`` 调用此类方法将导致运行时错误，因此 mypy 阻止您这样做：

.. code-block:: python

   from abc import abstractmethod
   class Base:
       @abstractmethod
       def foo(self) -> int: ...
   class Sub(Base):
       def foo(self) -> int:
           return super().foo() + 1  # 错误: 通过 super() 调用具有
                                     # 平凡主体的 "Base" 的抽象方法 "foo" 是不安全的  [safe-super]
   Sub().foo()  # 这将在运行时崩溃。

Mypy 将以下内容视为平凡主体：``pass`` 语句、字面省略号 ``...``、文档字符串和 ``raise NotImplementedError`` 语句。

.. _code-valid-newtype:

检查 NewType 的目标 [valid-newtype]
-------------------------------------------

:py:class:`~typing.NewType` 定义的目标必须是类类型。它不能是联合类型、``Any`` 或其他各种特殊类型。

如果目标是从 mypy 无法找到其源的模块导入的，也会出现此错误，因为此类定义被 mypy 视为具有 ``Any`` 类型的值。示例：

.. code-block:: python

   from typing import NewType

   # "acme" 的源代码对 mypy 不可用
   from acme import Entity  # type: ignore

   # 错误: NewType(...) 的参数 2 必须可子类化（得到 "Any"）  [valid-newtype]
   UserEntity = NewType('UserEntity', Entity)

要解决此问题，您可以为 mypy 提供对 ``acme`` 源代码的访问，或者为该模块创建一个存根文件。有关更多信息，请参见 :ref:`ignore-missing-imports`。

.. _code-exit-return:

检查 __exit__ 的返回类型 [exit-return]
-----------------------------------------------

如果 mypy 能够确定 :py:meth:`__exit__ <object.__exit__>` 始终返回 ``False``，则 mypy 检查返回类型 *不能* 是 ``bool``。返回类型的布尔值会影响 mypy 认为在 ``with`` 语句后哪些行是可达的，因为任何可以返回 ``True`` 的 :py:meth:`__exit__ <object.__exit__>` 方法都可能吞噬异常。不精确的返回类型可能导致在 ``with`` 语句附近报告神秘错误。

要修复此问题，可以使用 ``typing.Literal[False]`` 或 ``None`` 作为返回类型。在这种情况下，返回 ``None`` 等价于返回 ``False``，因为两者都被视为假值。

示例：

.. code-block:: python

   class MyContext:
       ...
       def __exit__(self, exc, value, tb) -> bool:  # 错误
           print('exit')
           return False

这会产生以下来自 mypy 的输出：

.. code-block:: text

   example.py:3: 错误: "__exit__" 的返回类型为 "bool"，但始终返回 False
   example.py:3: 注意: 使用 "typing_extensions.Literal[False]" 作为返回类型或将其更改为 "None"
   example.py:3: 注意: 如果 "__exit__" 的返回类型表示它可能返回 True，则上下文管理器可能会吞噬异常

您可以使用 ``Literal[False]`` 来修复此错误：

.. code-block:: python

   from typing import Literal

   class MyContext:
       ...
       def __exit__(self, exc, value, tb) -> Literal[False]:  # OK
           print('exit')
           return False

您也可以使用 ``None``：

.. code-block:: python

   class MyContext:
       ...
       def __exit__(self, exc, value, tb) -> None:  # 也 OK
           print('exit')

.. _code-name-match:

检查命名的一致性 [name-match]
--------------------------------------------

在使用基于调用的语法时，命名元组或 TypedDict 的定义必须一致命名。示例：

.. code-block:: python

    from typing import NamedTuple

    # 错误: namedtuple() 的第一个参数应为 "Point2D"，而不是 "Point"
    Point2D = NamedTuple("Point", [("x", int), ("y", int)])

.. _code-literal-required:

检查字面量在预期位置的使用 [literal-required]
------------------------------------------------------------

在某些地方，仅期望使用（字符串）字面量值以便进行静态类型检查，例如 ``TypedDict`` 键或 ``__match_args__`` 项。在这种情况下提供 ``str`` 值的变量将导致错误。请注意，在许多情况下，您还可以使用 ``Final`` 或 ``Literal`` 变量。示例：

.. code-block:: python

   from typing import Final, Literal, TypedDict

   class Point(TypedDict):
       x: int
       y: int

   def test(p: Point) -> None:
       X: Final = "x"
       p[X]  # OK

       Y: Literal["y"] = "y"
       p[Y]  # OK

       key = "x"  # key 的推断类型是 `str`
       # 错误: TypedDict 键必须是字符串字面量；
       #   预期值之一为 ("x", "y")  [literal-required]
       p[key]

.. _code-no-overload-impl:

检查重载函数是否有实现 [no-overload-impl]
-------------------------------------------------------------------------

在存根文件之外，重载函数必须跟随一个非重载的实现。

.. code-block:: python

   from typing import overload

   @overload
   def func(value: int) -> int:
       ...

   @overload
   def func(value: str) -> str:
       ...

   # 下方所需函数的存在被检查
   def func(value):
       pass  # 实际实现

.. _code-unused-coroutine:

检查协程返回值是否被使用 [unused-coroutine]
------------------------------------------------------------

Mypy 确保 async def 函数的返回值不会被忽略，因为这通常是编程错误，因为协程在调用处不会被执行。

.. code-block:: python

   async def f() -> None:
       ...

   async def g() -> None:
       f()  # 错误: 缺少 await
       await f()  # OK

您可以通过将结果分配给临时且未使用的变量来解决此错误：

.. code-block:: python

       _ = f()  # 没有错误

.. _code-top-level-await:

关于顶层 await 表达式发出警告 [top-level-await]
--------------------------------------------------------

此错误代码与一般的 ``[syntax]`` 错误分开，因为在某些环境中（例如 IPython），顶层 ``await`` 是被允许的。在这样的环境中，用户可能希望使用 ``--disable-error-code=top-level-await``，这仍然允许对其他不当使用 ``await`` 的情况产生错误，例如：

.. code-block:: python

   async def f() -> None:
       ...

   top = await f()  # 错误: "await" 在函数外  [top-level-await]

.. _code-await-not-async:

关于在协程外使用 await 表达式发出警告 [await-not-async]
-------------------------------------------------------------------------

``await`` 必须在协程内部使用。

.. code-block:: python

   async def f() -> None:
       ...

   def g() -> None:
       await f()  # 错误: "await" 在协程外 ("async def")  [await-not-async]

.. _code-assert-type:

检查 assert_type 中的类型 [assert-type]
----------------------------------------

传递给 ``assert_type`` 的表达式的推断类型必须与提供的类型匹配。

.. code-block:: python

   from typing_extensions import assert_type

   assert_type([1], list[int])  # OK

   assert_type([1], list[str])  # 错误

.. _code-truthy-function:

检查函数未在布尔上下文中使用 [truthy-function]
-------------------------------------------------------------------

函数在布尔上下文中总是会被评估为真。

.. code-block:: python

    def f():
        ...

    if f:  # 错误: 函数 "Callable[[], Any]" 在布尔上下文中可能始终为真 [truthy-function]
        pass

.. _code-str-format:

检查字符串格式化/插值是否类型安全 [str-format]
--------------------------------------------------------------------

Mypy 会检查 f-string、``str.format()`` 调用和 ``%`` 插值是否有效（当相应的模板是字面字符串时）。这包括检查替换的数量和类型，例如：

.. code-block:: python

    # 错误: 找不到位置格式说明符 1 的替换 [str-format]
    "{} and {}".format("spam")
    "{} and {}".format("spam", "eggs")  # OK
    # 错误: 在字符串格式化过程中未转换所有参数 [str-format]
    "{} and {}".format("spam", "eggs", "cheese")

    # 错误: 字符串插值中的不兼容类型
    # (表达式类型为 "float"，占位符类型为 "int") [str-format]
    "{:d}".format(3.14)

.. _code-str-bytes-safe:

检查隐式字节强制转换 [str-bytes-safe]
-------------------------------------------------------------------

警告可能以意外方式将字节对象转换为字符串的情况。

.. code-block:: python

    b = b"abc"

    # 错误: 如果 x = b'abc' 则 f"{x}" 或 "{}".format(x) 生成 "b'abc'"，而不是 "abc"。
    # 如果这是期望的行为，请使用 f"{x!r}" 或 "{!r}".format(x)。
    # 否则，请解码字节 [str-bytes-safe]
    print(f"The alphabet starts with {b}")

    # OK
    print(f"The alphabet starts with {b!r}")  # 字母表以 b'abc' 开头
    print(f"The alphabet starts with {b.decode('utf-8')}")  # 字母表以 abc 开头

.. _code-overload-overlap:

检查重载函数是否重叠 [overload-overlap]
----------------------------------------------------------------

如果多个 ``@overload`` 变体以潜在不安全的方式重叠，则发出警告。这可以防止以下情况：

.. code-block:: python

    from typing import overload

    class A: ...
    class B(A): ...

    @overload
    def foo(x: B) -> int: ...  # 错误: 重载函数签名 1 和 2 的重叠，返回类型不兼容 [overload-overlap]
    @overload
    def foo(x: A) -> str: ...
    def foo(x): ...

    def takes_a(a: A) -> str:
        return foo(a)

    a: A = B()
    value = takes_a(a)
    # mypy 将认为 value 是 str，但它实际上可以是 int
    reveal_type(value) # 显示类型是 "builtins.str"

请注意，在忽略此错误的情况下，mypy 通常仍会推断出您期望的类型。

有关更多解释，请参见 :ref:`overloading <function-overloading>`。

.. _code-overload-cannot-match:

检查无法匹配的重载签名 [overload-cannot-match]
--------------------------------------------------------------------------

如果 ``@overload`` 变体永远无法匹配，则发出警告，因为之前的重载具有更宽的签名。例如，如果两个重载接受相同的参数，并且第一个重载的每个参数的类型与第二个重载的相应参数的类型相同或更宽，则会发生这种情况。

示例：

.. code-block:: python

    from typing import overload, Union

    @overload
    def process(response1: object, response2: object) -> object:
        ...
    @overload
    def process(response1: int, response2: int) -> int: # 错误: 重载函数签名 2 将永远无法匹配: 签名 1 的参数类型相同或更广 [overload-cannot-match]
        ...

    def process(response1: object, response2: object) -> object:
        return response1 + response2

.. _code-annotation-unchecked:

通知未检查函数中的注释 [annotation-unchecked]
--------------------------------------------------------------------------

有时用户可能会不小心省略函数的注释，而 mypy 将不会检查该函数的主体（除非使用 :option:`--check-untyped-defs <mypy --check-untyped-defs>` 或 :option:`--disallow-untyped-defs <mypy --disallow-untyped-defs>`）。为了避免此类情况被忽视，mypy 将显示一条注释，如果未检查函数中有任何类型注解：

.. code-block:: python

    def test_assignment():  # "-> None" 返回注释缺失
        # 注意: 默认情况下，未类型化函数的主体不被检查，
        # 考虑使用 --check-untyped-defs [annotation-unchecked]
        x: int = "no way"

请注意，mypy 仍将以返回代码 ``0`` 退出，因为这种行为是 :pep:`484` 中规定的。

.. _code-prop-decorator:

装饰器在属性之前不支持 [prop-decorator]
-----------------------------------------------------------

Mypy 目前尚不支持分析位于属性装饰器之前的装饰器。如果装饰器未能保留属性声明的类型，mypy 将无法推断出声明的正确类型。如果装饰器无法移动到 ``@property`` 装饰器之后，则必须使用类型忽略注释：

.. code-block:: python

    class MyClass:
        @special  # type: ignore[prop-decorator]
        @property
        def magic(self) -> str:
            return "xyzzy"

.. note::

    为了向后兼容，此错误代码是通用 ``[misc]`` 代码的子代码。

.. _code-syntax:

报告语法错误 [syntax]
-----------------------------

如果被检查的代码在语法上无效，mypy 会发出语法错误。大多数语法错误，但并非所有，都是 *阻塞错误* ：
它们不能通过 ``# type: ignore`` 注释被忽略。

.. _code-typeddict-readonly-mutated:

只读 TypedDict 的键被修改 [typeddict-readonly-mutated]
-------------------------------------------------------------------

考虑这个示例：

.. code-block:: python

    from datetime import datetime
    from typing import TypedDict
    from typing_extensions import ReadOnly

    class User(TypedDict):
        username: ReadOnly[str]
        last_active: datetime

    user: User = {'username': 'foobar', 'last_active': datetime.now()}
    user['last_active'] = datetime.now()  # OK
    user['username'] = 'other'  # 错误: 只读 TypedDict 键 "key" 被修改 [typeddict-readonly-mutated]

`PEP 705 <https://peps.python.org/pep-0705>`_ 规范了 ``ReadOnly`` 特殊形式在 ``TypedDict`` 对象中的工作原理。

.. _code-misc:

杂项检查 [misc]
---------------------------

Mypy 执行许多其他不常见的检查，这些检查没有特定的错误代码。它们使用 ``misc`` 错误代码。除了用于多个无关错误之外，``misc`` 错误代码并不特殊。例如，您可以通过使用 ``# type: ignore[misc]`` 注释来忽略该类别中的所有错误。由于这些错误不太可能常见，因此在单行上看到两个 *不同* 的 ``misc`` 错误不太可能发生——尽管这确实偶尔会发生。

.. note::

    未来的 mypy 版本可能会为当前使用 ``misc`` 错误代码的一些错误添加新的错误代码。
