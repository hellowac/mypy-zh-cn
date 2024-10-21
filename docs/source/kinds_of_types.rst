类型的种类(kinds)
==================

到目前为止，我们主要限制在内置类型。此部分介绍几种额外类型。您可能需要其中的一些来进行任何非平凡程序的类型检查。

Class 类型
***********

每个类(class)也是有效类型。任何子类(subclass)的实例也与所有超类兼容——因此，所有值都与 :py:class:`object` 类型兼容（顺便提一下，也与后面讨论的 ``Any`` 类型兼容）。Mypy 分析类的主体，以确定实例中可用的方法和属性。以下示例使用了子类：

.. code-block:: python

   class A:
       def f(self) -> int:  # self 的类型推断为 (A)
           return 2

   class B(A):
       def f(self) -> int:
            return 3
       def g(self) -> int:
           return 4

   def foo(a: A) -> None:
       print(a.f())  # 3
       a.g()         # 错误：“A”没有属性“g”

   foo(B())  # OK（B 是 A 的子类）

Any 类型
************

带有 ``Any`` 类型的值是动态类型的。Mypy 无法了解此类值的可能运行时类型。对该值的任何操作都是允许的，这些操作仅在运行时检查。当您无法使用更精确的类型时，可以将 ``Any`` 作为“逃生阀”。

``Any`` 与每个其他类型兼容，反之亦然。您可以自由地将 ``Any`` 类型的值赋给更精确类型的变量：

.. code-block:: python

   a: Any = None
   s: str = ''
   a = 2     # OK（将 "int" 赋给 "Any"）
   s = a     # OK（将 "Any" 赋给 "str"）

声明（和推断）类型在运行时被忽略（或 *擦除*）。它们基本上被视为注释，因此上述代码不会生成运行时错误，即使 ``s`` 在运行时获取了 ``int`` 值，而 ``s`` 的声明类型实际上是 ``str``!使用 ``Any`` 类型时需要小心，因为它们允许您对 mypy 进行“欺骗”，这可能会隐藏错误。

如果您未定义函数的返回值或参数类型，则这些默认都是 ``Any``：

.. code-block:: python

   def show_heading(s) -> None:
       print('=== ' + s + ' ===')  # 没有静态类型检查，因为 s 的类型是 Any

   show_heading(1)  # OK（仅在运行时出错；mypy 不会生成错误）

您应该给静态类型函数显式的 ``None`` 返回类型，即使它不返回值，因为这让 mypy 捕获额外的类型错误：

.. code-block:: python

   def wait(t: float):  # 隐式 Any 返回值
       print('Waiting...')
       time.sleep(t)

   if wait(2) > 1:   # Mypy 没有捕获这个错误!
       ...

如果我们使用显式的 ``None`` 返回类型，mypy 将捕获错误：

.. code-block:: python

   def wait(t: float) -> None:
       print('Waiting...')
       time.sleep(t)

   if wait(2) > 1:   # 错误：无法比较 None 和 int
       ...

``Any`` 类型在 :ref:`dynamic-typing` 部分有更详细的讨论。

.. note::

  没有任何类型的函数签名是动态类型的。动态类型函数的主体不会进行静态检查，局部变量具有隐式 ``Any`` 类型。这使得将遗留 Python 代码迁移到 mypy 更加容易，因为 mypy 不会对动态类型函数进行抱怨。

.. _tuple-types:

Tuple 类型
***********

类型 ``tuple[T1, ..., Tn]`` 表示具有项类型 ``T1``、...、``Tn`` 的元组：

.. code-block:: python

   # 在 Python 3.8 及更早版本中使用 `typing.Tuple`
   def f(t: tuple[int, str]) -> None:
       t = 1, 'foo'    # OK
       t = 'foo', 1    # 类型检查错误

这种元组类型具有确切的特定项数（上例中为 2）。元组也可以用作不可变的可变长度序列。您可以使用类型 ``tuple[T, ...]`` (带有文字 ``...``，这是语法的一部分）来实现此目的。例如：

.. code-block:: python

    def print_squared(t: tuple[int, ...]) -> None:
        for n in t:
            print(n, n ** 2)

    print_squared(())           # OK
    print_squared((1, 3, 5))    # OK
    print_squared([1, 2])       # 错误：仅元组有效

.. note::

   通常，使用 ``Sequence[T]`` 而不是 ``tuple[T, ...]`` 更好，因为
   :py:class:`~collections.abc.Sequence` 也与列表和其他非元组序列兼容。

.. note::

   ``tuple[...]`` 在 Python 3.6 及更高版本中作为基类是有效的，并且在存根文件中始终有效。在早期的 Python 版本中，您有时可以通过使用命名元组作为基类来解决此限制（见 :ref:`named-tuples` 部分）。

.. _callable-types:

Callable 类型（以及 lambdas）
**********************************

您可以在静态类型代码中传递函数对象和绑定方法。接受参数 ``A1``、...、``An`` 并返回 ``Rt`` 的函数类型为 ``Callable[[A1, ..., An], Rt]``。示例：

.. code-block:: python

   from collections.abc import Callable

   def twice(i: int, next: Callable[[int], int]) -> int:
       return next(next(i))

   def add(i: int) -> int:
       return i + 1

   print(twice(3, add))   # 5

.. note::

    如果您使用 Python 3.8 或更早版本，请从 ``typing`` 导入
    :py:data:`Callable[...] <typing.Callable>` 而不是 ``collections.abc``。

可调用类型只能包含位置参数，且只能是没有默认值的参数。这涵盖了大多数可调用类型的用法，但有时这并不够。Mypy 识别一种特殊形式 ``Callable[..., T]`` （带有文字 ``...`` ），可以用于不太典型的情况。它与返回类型与 ``T`` 兼容的任意可调用对象兼容，无论参数的数量、类型或种类如何。Mypy 允许您使用任意参数调用这样的可调用值，而不进行任何检查——在这方面，它们的处理方式类似于 ``(*args: Any, **kwargs: Any)`` 的函数签名。示例：

.. code-block:: python

   from collections.abc import Callable

   def arbitrary_call(f: Callable[..., int]) -> int:
       return f('x') + f(y=2)  # OK

   arbitrary_call(ord)   # 无静态错误，但在运行时失败
   arbitrary_call(open)  # 错误：不返回 int
   arbitrary_call(1)     # 错误：'int' 不是可调用的

在需要更精确或复杂的回调类型的情况下，可以使用灵活的 :ref:`回调协议 <callback_protocols>`。匿名函数也受到支持。匿名函数的参数和返回值类型不能显式给出；它们始终根据上下文使用双向类型推断进行推断：

.. code-block:: python

   l = map(lambda x: x + 1, [1, 2, 3])   # 推断 x 为 int，l 为 list[int]

如果您想显式给出参数或返回值类型，可以使用普通的、可能是嵌套的函数定义。

可调用类型也可以用于类型对象，匹配它们的 ``__init__`` 或 ``__new__`` 签名：

.. code-block:: python

    from collections.abc import Callable

    class C:
        def __init__(self, app: str) -> None:
            pass

    CallableType = Callable[[str], C]

    def class_or_callable(arg: CallableType) -> None:
        inst = arg("my_app")
        reveal_type(inst)  # 推断类型为 "C"

这在您希望 ``arg`` 既可以是返回 ``C`` 实例的 ``Callable``，又可以是 ``C`` 本身的类型时非常有用。这同样适用于 :ref:`回调协议 <callback_protocols>`。


.. _union-types:
.. _alternative_union_syntax:

Union 类型
***********

Python 函数通常接受两种或多种不同类型的值。您可以使用 :ref:`重载 <function-overloading>` 来表示这一点，但联合类型通常更方便。

使用 ``T1 | ... | Tn`` 构造一个联合类型。例如，如果一个参数的类型为 ``int | str`` ，那么整数和字符串都是有效的参数值。

您可以使用 :py:func:`isinstance` 检查来将联合类型缩小到更具体的类型：

.. code-block:: python

   def f(x: int | str) -> None:
       x + 1     # 错误：str + int 不是有效的
       if isinstance(x, int):
           # 这里 x 的类型是 int。
           x + 1      # 正确
       else:
           # 这里 x 的类型是 str。
           x + 'a'    # 正确

   f(1)    # 正确
   f('x')  # 正确
   f(1.1)  # 错误

.. note::

    只有当操作对 *每个* 联合项都是有效时，联合类型的操作才是有效的。这就是为什么通常需要使用 :py:func:`isinstance` 检查先将联合类型缩小到非联合类型。这也意味着建议避免将联合类型用作函数的返回类型，因为调用者可能需要在对值进行任何有意义的操作之前使用 :py:func:`isinstance`。

Python 3.9 及更早版本只部分支持此语法。相反，您可以使用传统的 ``Union[T1, ..., Tn]`` 类型构造函数。示例：

.. code-block:: python

   from typing import Union

   def f(x: Union[int, str]) -> None:
       ...

在不支持运行时新语法的 Python 版本中，如果您使用 ``from __future__ import annotations`` （请参阅 :ref:`runtime_troubles` ），也可以在某些限制下使用新语法：

.. code-block:: python

   from __future__ import annotations

   def f(x: int | str) -> None:   # 在 Python 3.7 及更高版本中有效
       ...

.. _strict_optional:

Optional 和 None 类型
********************************

您可以使用 ``T | None`` 来定义一个允许 ``None`` 值的类型变体，例如 ``int | None``。这被称为 *可选类型(optional type)*：

.. code-block:: python

   def strlen(s: str) -> int | None:
       if not s:
           return None  # 正确
       return len(s)

   def strlen_invalid(s: str) -> int:
       if not s:
           return None  # 错误：None 与 int 不兼容
       return len(s)

为了支持 Python 3.9 及更早版本，您可以使用 :py:data:`~typing.Optional` 类型修饰符，例如 ``Optional[int]`` （ ``Optional[X]`` 是 ``Union[X, None]`` 的首选简写）：

.. code-block:: python

   from typing import Optional

   def strlen(s: str) -> Optional[int]:
       ...

大多数操作不允许在未保护的 ``None`` 或 *可选* 值（带有可选类型的值）上进行：

.. code-block:: python

   def my_inc(x: int | None) -> int:
       return x + 1  # 错误：无法将 None 与 int 相加

相反，需要显式的 ``None`` 检查。Mypy 拥有强大的类型推断能力，允许您使用常规 Python 习惯来防范 ``None`` 值。例如，mypy 识别 ``is None`` 检查：

.. code-block:: python

   def my_inc(x: int | None) -> int:
       if x is None:
           return 0
       else:
           # 在这里，x 的推断类型仅为 int。
           return x + 1

由于在 if 条件中检查了 ``None``，mypy 会推断出 else 块中的 ``x`` 类型为 ``int``。

其他支持的检查以防范 ``None`` 值包括 ``if x is not None``、``if x`` 和 ``if not x``。此外，mypy 还理解逻辑表达式中的 ``None`` 检查：

.. code-block:: python

   def concat(x: str | None, y: str | None) -> str | None:
       if x is not None and y is not None:
           # 此时 x 和 y 都不为 None
           return x + y
       else:
           return None

有时，mypy 不会意识到一个值永远不是 ``None``。这通常发生在类实例可以处于部分定义状态的情况，其中某个属性在对象构造期间初始化为 ``None``，但一个方法假设该属性不再是 ``None``。Mypy 会对此可能的 ``None`` 值提出警告。您可以在方法中使用 ``assert x is not None`` 来解决此问题：

.. code-block:: python

   class Resource:
       path: str | None = None

       def initialize(self, path: str) -> None:
           self.path = path

       def read(self) -> str:
           # 我们要求对象已初始化。
           assert self.path is not None
           with open(self.path) as f:  # 正确
              return f.read()

   r = Resource()
   r.initialize('/foo/bar')
   r.read()

在将变量初始化为 ``None`` 时，``None`` 通常是一个空的占位符值，实际值有不同的类型。这就是为什么您需要在像上面的 ``Resource`` 类的情况下对属性进行注解：

.. code-block:: python

    class Resource:
        path: str | None = None
        ...

这同样适用于在方法中定义的属性：

.. code-block:: python

    class Counter:
        def __init__(self) -> None:
            self.count: int | None = None

通常不使用任何初始值来为属性赋值会更简单。这样，您就不需要使用可选类型，也可以避免 ``assert ... is not None`` 检查。如果您在类体中对属性进行了注解，则不需要初始值：

.. code-block:: python

   class Container:
       items: list[str]  # 无初始值

Mypy 通常使用对变量的第一次赋值来推断该变量的类型。然而，如果您在同一作用域内同时赋值 ``None`` 值和非 ``None`` 值，mypy 通常可以在没有注解的情况下正确处理：

.. code-block:: python

   def f(i: int) -> None:
       n = None  # 推断类型为 'int | None'，因为下面的赋值
       if i > 0:
            n = i
       ...

有时，您可能会收到错误消息 "无法确定 <something> 的类型"。在这种情况下，您应该添加显式的 ``... | None`` 注解。

.. note::

   ``None`` 是只有一个值 ``None`` 的类型。``None`` 也用作没有返回值的函数的返回类型，即隐式返回 ``None`` 的函数。

.. note::

   Python 解释器在内部使用 ``NoneType`` 作为 ``None`` 的类型，但在类型注解中始终使用 ``None``。后者更简短且更易读。( ``NoneType`` 在 Python 3.10+ 中作为 :py:data:`types.NoneType` 可用，但在早期版本的 Python 中根本没有暴露。）

.. note::

    类型 ``Optional[T]`` *并不* 意味着带有默认值的函数参数。它仅仅意味着 ``None`` 是有效的参数值。这是一个常见的误解，因为 ``None`` 是参数的常见默认值，而带有默认值的参数有时被称为 *可选(optional)* 参数(parameters)（或参数(arguments)）。

.. _type-aliases:

Type 别名(aliases)
********************

在某些情况下，类型名称可能会变得冗长且难以输入，特别是当它们被频繁使用时：

.. code-block:: python

   def f() -> list[dict[tuple[int, str], set[int]]] | tuple[str, list[str]]:
       ...

当出现这种情况时，您可以通过将类型赋值给变量来定义类型别名（这是一种 *隐式类型别名*）：

.. code-block:: python

   AliasType = list[dict[tuple[int, str], set[int]]] | tuple[str, list[str]]

   # 现在我们可以使用 AliasType 替代完整名称：

   def f() -> AliasType:
       ...

.. note::

    类型别名并不创建新类型。它只是另一种类型的简写符号——它与目标类型等价，除了 :ref:`generic aliases <generic-type-aliases>`。

Python 3.12 引入了 ``type`` 语句用于定义 *显式类型别名*。显式类型别名消除了歧义，并通过明确意图来提高可读性：

.. code-block:: python

   type AliasType = list[dict[tuple[int, str], set[int]]] | tuple[str, list[str]]

   # 现在我们可以使用 AliasType 替代完整名称：

   def f() -> AliasType:
       ...

关于何时定义隐式类型别名可能会产生困惑——例如，当别名包含前向引用、无效类型或违反类型别名声明的其他限制时。由于未注解变量与类型别名之间的区别是隐式的，模棱两可或不正确的类型别名声明默认会定义为普通变量，而不是类型别名。

使用 ``type`` 语句定义的别名具有以下特性，这将它们与隐式类型别名区分开来：

* 定义可以包含前向引用，而无需使用字符串文字转义，因为它是惰性求值的。
* 别名可以在类型注解、类型参数和类型转换中使用，但不能在需要类对象的上下文中使用。例如，它不能作为基类，也不能用于构造实例。

还有一种旧的语法用于定义显式类型别名，该语法在 Python 3.10 中引入（:pep:`613`）：

.. code-block:: python

   from typing import TypeAlias  # 在 Python 3.9 及更早版本中使用 "from typing_extensions"

   AliasType: TypeAlias = list[dict[tuple[int, str], set[int]]] | tuple[str, list[str]]

.. _named-tuples:

Named tuples
************

Mypy 识别命名元组，并可以对定义或使用它们的代码进行类型检查。在这个例子中，我们可以检测尝试访问缺失属性的代码：

.. code-block:: python

    Point = namedtuple('Point', ['x', 'y'])
    p = Point(x=1, y=2)
    print(p.z)  # 错误：Point 没有属性 'z'

如果使用 :py:func:`namedtuple <collections.namedtuple>` 定义命名元组，则所有项被假定为 ``Any`` 类型。也就是说，mypy 不知道项的类型。您可以使用 :py:class:`~typing.NamedTuple` 来定义项类型：

.. code-block:: python

    from typing import NamedTuple

    Point = NamedTuple('Point', [('x', int),
                                 ('y', int)])
    p = Point(x=1, y='x')  # 参数类型不兼容 "str"; 期望 "int"

Python 3.6 引入了一种替代的基于类的命名元组语法：

.. code-block:: python

    from typing import NamedTuple

    class Point(NamedTuple):
        x: int
        y: int

    p = Point(x=1, y='x')  # 参数类型不兼容 "str"; 期望 "int"

.. note::

  如果任何 ``NamedTuple`` 对象有效，您可以在类型注解中使用原始的 ``NamedTuple`` “伪类(pseudo-class)”。

  例如，它在反序列化时可能很有用：

  .. code-block:: python

    def deserialize_named_tuple(arg: NamedTuple) -> Dict[str, Any]:
        return arg._asdict()

    Point = namedtuple('Point', ['x', 'y'])
    Person = NamedTuple('Person', [('name', str), ('age', int)])

    deserialize_named_tuple(Point(x=1, y=2))  # 正确
    deserialize_named_tuple(Person(name='Nikita', age=18))  # 正确

    # 错误：参数 1 的类型 "Tuple[int, int]" 不兼容; 期望 "NamedTuple"
    deserialize_named_tuple((1, 2))

  请注意，此行为高度实验性，非标准，可能不被其他类型检查器和 IDE 支持。

.. _type-of-class:

类对象的类型
*************************

（自由改编自 :pep:`PEP 484: 类对象的类型 <484#the-type-of-class-objects>` 。）

有时，您想要讨论继承自给定类的类对象。这可以用 ``type[C]`` 来表示（在 Python 3.8 及以下版本中使用 :py:class:`typing.Type[C] <typing.Type>`），其中 ``C`` 是一个类。换句话说，当 ``C`` 是类的名称时，使用 ``C`` 注解参数表示该参数是 ``C`` 的实例（或其子类），而使用 ``type[C]`` 作为参数注解表示该参数是派生自 ``C`` 的类对象（或 ``C`` 本身）。

假设以下类：

.. code-block:: python

   class User:
       # 定义字段如 name, email

   class BasicUser(User):
       def upgrade(self):
           """升级到 Pro"""

   class ProUser(User):
       def pay(self):
           """支付账单"""

注意，``ProUser`` 并不继承自 ``BasicUser``。

以下是一个函数，如果您传递正确的类对象，它将创建这些类的实例：

.. code-block:: python

   def new_user(user_class):
       user = user_class()
       # （这里我们可以将用户对象写入数据库）
       return user

我们该如何注解这个函数呢？如果不能对 ``type`` 进行参数化，我们能做的最好的是：

.. code-block:: python

   def new_user(user_class: type) -> User:
       # 与之前相同的实现

这似乎是合理的，除了在以下示例中，mypy 不知道 ``buyer`` 变量的类型是 ``ProUser``：

.. code-block:: python

   buyer = new_user(ProUser)
   buyer.pay()  # 被拒绝，User 上没有该方法

但是，使用 ``type[C]`` 语法和带有上界的类型变量（见 :ref:`type-variable-upper-bound`），我们可以做得更好（Python 3.12 语法）：

.. code-block:: python

   def new_user[U: User](user_class: type[U]) -> U:
       # 与之前相同的实现

使用旧版语法（Python 3.11 及以下）：

.. code-block:: python

   U = TypeVar('U', bound=User)

   def new_user(user_class: type[U]) -> U:
       # 与之前相同的实现

现在，当我们用 ``User`` 的特定子类调用 ``new_user()`` 时，mypy 将推断出正确的结果类型：

.. code-block:: python

   beginner = new_user(BasicUser)  # 推断类型为 BasicUser
   beginner.upgrade()  # OK

.. note::

   对应于 ``type[C]`` 的值必须是实际的类对象，且是 ``C`` 的子类型。它的构造函数必须与 ``C`` 的构造函数兼容。如果 ``C`` 是类型变量，则其上界必须是类对象。

有关 ``type[]`` 和 :py:class:`typing.Type[] <typing.Type>` 的更多详细信息，请参见 :pep:`PEP 484: 类对象的类型 <484#the-type-of-class-objects>`。

.. _generators:

生成器(Generators)
**********************

一个基本的仅用于生成值的生成器，可以简洁地注解为具有返回类型 :py:class:`Iterator[YieldType] <typing.Iterator>` 或 :py:class:`Iterable[YieldType] <typing.Iterable>`。例如：

.. code-block:: python

   def squares(n: int) -> Iterator[int]:
       for i in range(n):
           yield i * i

一个好的原则是尽可能地用最具体的返回类型注解函数。然而，您也应该小心避免将实现细节泄露到函数的公共 API 中。遵循这两个原则时，优先选择 :py:class:`Iterator[YieldType] <typing.Iterator>` 作为生成器函数( :py:class:`Iterable[YieldType] <typing.Iterable>` )的返回类型注解，因为这让 mypy 知道用户能够调用函数返回对象的 :py:func:`next` 方法。不过，要记住，如果您认为 `next()` 可以被调用是实现细节，那么使用 `Iterable` 可能是更好的选择。

如果您希望生成器通过 :py:meth:`~generator.send` 方法接受值或返回值，则应使用 :py:class:`Generator[YieldType, SendType, ReturnType] <typing.Generator>` 泛型类型，而不是 `Iterator` 或 `Iterable`。例如：

.. code-block:: python

   def echo_round() -> Generator[int, float, str]:
       sent = yield 0
       while sent >= 0:
           sent = yield round(sent)
       return 'Done'

注意，与 typing 模块中的许多其他泛型不同， :py:class:`~typing.Generator` 的 `SendType` 是协变的，而不是协变或不变的。

如果您不打算接收或返回值，则应相应地将 `SendType` 或 `ReturnType` 设置为 `None`。例如，我们可以将第一个示例注解为：

.. code-block:: python

   def squares(n: int) -> Generator[int, None, None]:
       for i in range(n):
           yield i * i

这与使用 ``Iterator[int]`` 或 ``Iterable[int]`` 略有不同，因为生成器具有 :py:meth:`~generator.close`、 :py:meth:`~generator.send` 和 :py:meth:`~generator.throw` 方法，而通用的迭代器和可迭代对象则没有。如果您计划在返回的生成器上调用这些方法，请使用 :py:class:`~typing.Generator` 类型，而不是 :py:class:`~typing.Iterator` 或 :py:class:`~typing.Iterable`。
