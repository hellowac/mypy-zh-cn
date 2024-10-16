.. _cheat-sheet-py3:

类型提示备忘单
======================

本文档是一个快速备忘单，展示了如何在 Python 中使用各种常见类型的类型注释。

变量
*********

从技术上讲，下面展示的许多类型注释是多余的，因为 mypy 通常可以根据变量的值推断出类型。有关更多细节，请参见 :ref:`type-inference-and-annotations` 。

.. code-block:: python

   # 这是声明变量类型的方式
   age: int = 1

   # 您无需初始化变量即可进行注释
   a: int  # 可以（在分配之前运行时没有值）

   # 这样做在条件分支中可能很有用
   child: bool
   if age < 18:
       child = True
   else:
       child = False


有用的内置类型
*********************

.. code-block:: python

   # 对于大多数类型，只需在注释中使用类型名称
   # 注意，mypy 通常可以根据变量的值推断类型，
   # 所以从技术上讲，这些注释是多余的
   x: int = 1
   x: float = 1.0
   x: bool = True
   x: str = "test"
   x: bytes = b"test"

   # 对于 Python 3.9 及以上版本，集合中项的类型用括号表示
   x: list[int] = [1]
   x: set[int] = {6, 7}

   # 对于映射，需要指定键和值的类型
   x: dict[str, float] = {"field": 2.0}  # Python 3.9+

   # 对于固定大小的元组，指定所有元素的类型
   x: tuple[int, str, float] = (3, "yes", 7.5)  # Python 3.9+

   # 对于可变大小的元组，使用一个类型和省略号
   x: tuple[int, ...] = (1, 2, 3)  # Python 3.9+

   # 在 Python 3.8 及之前版本，集合类型名称大写，类型从 'typing' 模块导入
   from typing import List, Set, Dict, Tuple
   x: List[int] = [1]
   x: Set[int] = {6, 7}
   x: Dict[str, float] = {"field": 2.0}
   x: Tuple[int, str, float] = (3, "yes", 7.5)
   x: Tuple[int, ...] = (1, 2, 3)

   from typing import Union, Optional

   # 在 Python 3.10 及以上版本，使用 | 操作符表示类型可以是几种之一
   x: list[int | str] = [3, 5, "test", "fun"]  # Python 3.10+
   # 在早期版本中，使用 Union
   x: list[Union[int, str]] = [3, 5, "test", "fun"]

   # 使用 X | None 表示可能为 None 的值（Python 3.10+）
   # 在 3.9 及之前版本使用 Optional[X]；Optional[X] 等同于 'X | None'
   x: str | None = "something" if some_condition() else None
   if x is not None:
       # Mypy 理解这里 x 不会是 None，因为有 if 语句
       print(x.upper())
   # 如果您知道某个值由于一些 mypy 无法理解的逻辑永远不会是 None，请使用 assert
   assert x is not None
   print(x.upper())

函数
*********

.. code-block:: python

   from collections.abc import Iterator, Callable
   from typing import Union, Optional

   # 这是如何注释函数定义
   def stringify(num: int) -> str:
       return str(num)

   # 下面是如何指定多个参数
   def plus(num1: int, num2: int) -> int:
       return num1 + num2

   # 如果函数不返回值，使用 None 作为返回类型
   # 默认参数值放在类型注释之后
   def show(value: str, excitement: int = 10) -> None:
       print(value + "!" * excitement)

   # 注意没有类型的参数被视为动态类型（视为 Any）
   # 没有任何注释的函数不会被检查
   def untyped(x):
       x.anything() + 1 + "string"  # 没有错误

   # 这是如何注释可调用（函数）值
   x: Callable[[int, float], float] = f
   def register(callback: Callable[[str], int]) -> None: ...

   # 生成器函数产生整数，因此它实际上是返回整数迭代器的函数
   def gen(n: int) -> Iterator[int]:
       i = 0
       while i < n:
           yield i
           i += 1

   # 当然可以将函数注释分成多行
   def send_email(
       address: str | list[str],
       sender: str,
       cc: list[str] | None,
       bcc: list[str] | None,
       subject: str = '',
       body: list[str] | None = None,
   ) -> bool:
       ...

   # Mypy 理解位置参数和关键字参数
   # 位置参数可以通过以两个下划线开头的名称来标记
   def quux(x: int, /, *, y: int) -> None:
       pass

   quux(3, y=5)  # 正确
   quux(3, 5)  # 错误：位置参数过多
   quux(x=3, y=5)  # 错误：意外的关键字参数 "x"

   # 这表示每个位置参数和每个关键字参数都是 "str"
   def call(self, *args: str, **kwargs: str) -> str:
       reveal_type(args)  # 显示的类型是 "tuple[str, ...]"
       reveal_type(kwargs)  # 显示的类型是 "dict[str, str]"
       request = make_request(*args, **kwargs)
       return self.do_api_query(request)

类
*******

.. code-block:: python

   from typing import ClassVar

   class BankAccount:
       # "__init__" 方法不返回任何内容，所以返回类型为 "None"
       def __init__(self, account_name: str, initial_balance: int = 0) -> None:
           # mypy 会根据参数类型推断实例变量的正确类型
           self.account_name = account_name
           self.balance = initial_balance

       # 实例方法中省略 "self" 的类型
       def deposit(self, amount: int) -> None:
           self.balance += amount

       def withdraw(self, amount: int) -> None:
           self.balance -= amount

   # 用户定义的类可以作为注释中的类型
   account: BankAccount = BankAccount("Alice", 400)
   def transfer(src: BankAccount, dst: BankAccount, amount: int) -> None:
       src.withdraw(amount)
       dst.deposit(amount)

   # 接受 BankAccount 的函数也接受任何 BankAccount 的子类！
   class AuditedBankAccount(BankAccount):
       # 可以选择在类体中声明实例变量
       audit_log: list[str]

       def __init__(self, account_name: str, initial_balance: int = 0) -> None:
           super().__init__(account_name, initial_balance)
           self.audit_log: list[str] = []

       def deposit(self, amount: int) -> None:
           self.audit_log.append(f"Deposited {amount}")
           self.balance += amount

       def withdraw(self, amount: int) -> None:
           self.audit_log.append(f"Withdrew {amount}")
           self.balance -= amount

   audited = AuditedBankAccount("Bob", 300)
   transfer(audited, account, 100)  # 类型检查通过！

   # 可以使用 ClassVar 注释来声明类变量
   class Car:
       seats: ClassVar[int] = 4
       passengers: ClassVar[list[str]]

   # 如果希望动态属性，可以重写 "__setattr__" 或 "__getattr__"
   class A:
       # 允许给任何 A.x 赋值，如果 x 的类型与 "value" 相同
       def __setattr__(self, name: str, value: int) -> None: ...

       # 允许访问任何 A.x，如果 x 与返回类型兼容
       def __getattr__(self, name: str) -> int: ...

   a = A()
   a.foo = 42  # 正常
   a.bar = 'Ex-parrot'  # 类型检查失败

当你感到困惑或情况复杂时
**************************************************

.. code-block:: python

   from typing import Union, Any, Optional, TYPE_CHECKING, cast

   # 要找出 mypy 为程序中任何表达式推断的类型，可以将其包装在 reveal_type() 中。
   # Mypy 将打印出包含类型的错误消息；在运行代码之前请移除它。
   reveal_type(1)  # 揭示的类型是 "builtins.int"

   # 如果你用一个空容器或 "None" 初始化一个变量，你可能需要通过提供显式类型注释来帮助 mypy。
   x: list[str] = []
   x: str | None = None

   # 如果你不知道某个东西的类型，或者它太动态以至于无法写出类型，则使用 Any。
   x: Any = mystery_function()
   # Mypy 将允许你对 x 做任何事情！
   x.whatever() * x["you"] + x("want") - any(x) and all(x) is super  # 没有错误

   # 使用 "type: ignore" 注释来抑制给定行的错误，当你的代码让 mypy 感到困惑或遇到 mypy 的明显错误时。
   # 良好的做法是添加注释解释问题。
   x = confusing_function()  # type: ignore  # confusing_function 不会在这里返回 None，因为 ...

   # "cast" 是一个帮助函数，可以让你覆盖表达式的推断类型。它仅适用于 mypy —— 在运行时没有检查。
   a = [4]
   b = cast(list[int], a)  # 通过
   c = cast(list[str], a)  # 通过尽管这不真实（没有运行时检查）
   reveal_type(c)  # 揭示的类型是 "builtins.list[builtins.str]"
   print(c)  # 仍然打印 [4] ... 对象不会在运行时被改变或转换

   # 如果你想让 mypy 可见但在运行时不会执行的代码，请使用 "TYPE_CHECKING"
   if TYPE_CHECKING:
       import json
   else:
       import orjson as json  # mypy 不知道这一点

在某些情况下，类型注释可能会导致运行时问题，详见 :ref:`runtime_troubles` 来处理这些问题。

请参见 :ref:`silencing-type-errors` 以获取有关如何静默错误的详细信息。

标准“鸭子类型(duck types)”
***************************

在典型的 Python 代码中，许多可以接收列表或字典作为参数的函数只需要它们的参数在某种程度上是“类似列表”或“类似字典”的。特定的“类似列表”或“类似字典”（或其他类似的东西）的含义称为“鸭子类型”，而一些常见的鸭子类型在习惯用法中是标准化的。

.. code-block:: python

   from collections.abc import Mapping, MutableMapping, Sequence, Iterable
   # 或者 'from typing import ...'（在 Python 3.8 中是必需的）

   # 使用 Iterable 表示通用的可迭代对象（任何可以在 "for" 中使用的对象），
   # 使用 Sequence 当需要一个支持 "len" 和 "__getitem__" 的序列时
   def f(ints: Iterable[int]) -> list[str]:
       return [str(x) for x in ints]

   f(range(1, 3))

   # Mapping 描述一个字典-like 对象（具有 "__getitem__"），而我们不会改变它，
   # MutableMapping 描述一个我们可能会改变的对象（具有 "__setitem__"）
   def f(my_mapping: Mapping[int, str]) -> list[int]:
       my_mapping[5] = 'maybe'  # mypy 会对此行发出警告...
       return list(my_mapping.keys())

   f({3: 'yes', 4: 'no'})

   def f(my_mapping: MutableMapping[int, str]) -> set[str]:
       my_mapping[5] = 'maybe'  # ...但 mypy 对此是可以的。
       return set(my_mapping.values())

   f({3: 'yes', 4: 'no'})

   import sys
   from typing import IO

   # 使用 IO[str] 或 IO[bytes] 对于应接受或返回来自 open() 调用的对象的函数
   # （注意 IO 不区分读取、写入或其他模式）
   def get_sys_IO(mode: str = 'w') -> IO[str]:
       if mode == 'w':
           return sys.stdout
       elif mode == 'r':
           return sys.stdin
       else:
           return sys.stdout

你甚至可以使用 :ref:`protocol-types` 创建自己的鸭子类型。

前向引用
******************

.. code-block:: python

   # 你可能想在类定义之前引用一个类。
   # 这被称为“前向引用(forward reference)”。
   def f(foo: A) -> int:  # 这将在运行时失败，显示 'A' 未定义
       ...

   # 然而，如果你添加以下特殊导入：
   from __future__ import annotations
   # 它将在运行时工作，并且类型检查将成功，只要文件中后面有一个同名类
   def f(foo: A) -> int:  # 可以
       ...

   # 另一种选择是将类型放在引号中
   def f(foo: 'A') -> int:  # 也可以
       ...

   class A:
       # 如果你需要在该类的定义中引用一个类作为类型注解，这也可能出现
       @classmethod
       def create(cls) -> A:
           ...

有关更多详细信息，请参阅 :ref:`forward-references`。

装饰器
**********

装饰器函数可以通过泛型来表达。有关详细信息，请参见 :ref:`declaring-decorators` 。使用 Python 3.12 语法的示例：

.. code-block:: python

    from collections.abc import Callable
    from typing import Any

    def bare_decorator[F: Callable[..., Any]](func: F) -> F:
        ...

    def decorator_args[F: Callable[..., Any]](url: str) -> Callable[[F], F]:
        ...

使用 3.12 之前的语法的相同示例：

.. code-block:: python

    from collections.abc import Callable
    from typing import Any, TypeVar

    F = TypeVar('F', bound=Callable[..., Any])

    def bare_decorator(func: F) -> F:
        ...

    def decorator_args(url: str) -> Callable[[F], F]:
        ...

协程与 asyncio
**********************

有关协程和异步代码类型注释的详细信息，请参见 :ref:`async-and-await`。

.. code-block:: python

   import asyncio

   # 协程的类型注释与普通函数相同
   async def countdown(tag: str, count: int) -> str:
       while count > 0:
           print(f'T-minus {count} ({tag})')
           await asyncio.sleep(0.1)
           count -= 1
       return "Blastoff!"
