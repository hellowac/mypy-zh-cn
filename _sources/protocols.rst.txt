.. _protocol-types:

协议(Protocol)与结构化子类型
==================================

Python 的类型系统支持两种方式来判断两个对象是否兼容： **名义子类型(nominal subtyping)** 和 **结构化子类型(structural subtyping)** 。

**名义（Nominal）** 子类型是严格基于类的继承层次结构。如果类 ``Dog`` 继承自类 ``Animal``，它就是 ``Animal`` 的子类型。当需要 ``Animal`` 实例时，可以使用 ``Dog`` 实例。这种子类型是 Python 类型系统主要使用的方式：它易于理解，能够生成清晰简明的错误信息，并且与原生的 :py:func:`isinstance <isinstance>` 检查方式匹配——基于类的继承层次。

**结构化（Structural）** 子类型则是基于可以对对象执行的操作。如果类 ``Dog`` 具有类 ``Animal`` 的所有属性和方法，并且类型兼容，那么 ``Dog`` 就是 ``Animal`` 的结构化子类型。

结构化子类型可以看作是鸭子类型的静态等价物，Python 程序员对鸭子类型应该都很熟悉。详见 :pep:`544` ，其中详细说明了 Python 中协议与结构化子类型的规范。

.. _predefined_protocols:

预定义协议(protocols)
************************

:py:mod:`collections.abc` 、:py:mod:`typing` 以及其他标准库模块定义了各种协议类，这些协议类对应于常见的 Python 协议，例如 :py:class:`Iterable[T] <collections.abc.Iterable>`。如果一个类定义了合适的 :py:meth:`__iter__ <object.__iter__>` 方法，mypy 会理解该类实现了可迭代协议，并且与 :py:class:`Iterable[T] <collections.abc.Iterable>` 兼容。比如，下面的 ``IntList`` 是一个可迭代的类，迭代结果是 ``int`` 值：

.. code-block:: python

   from __future__ import annotations

   from collections.abc import Iterator, Iterable

   class IntList:
       def __init__(self, value: int, next: IntList | None) -> None:
           self.value = value
           self.next = next

       def __iter__(self) -> Iterator[int]:
           current = self
           while current:
               yield current.value
               current = current.next

   def print_numbered(items: Iterable[int]) -> None:
       for n, x in enumerate(items):
           print(n + 1, x)

   x = IntList(3, IntList(5, None))
   print_numbered(x)  # OK
   print_numbered([4, 5])  # 也 OK

:ref:`predefined_protocols_reference` 列出了 :py:mod:`collections.abc` 和 :py:mod:`typing` 中定义的各种协议，以及你需要实现每个协议所需定义的方法签名。

.. note::

    ``typing`` 还包含一些过时的协议和抽象基类（ABC）的别名，这些别名在 :py:mod:`collections.abc` 中定义，例如 :py:class:`Iterable[T] <typing.Iterable>`。这些别名仅在 Python 3.8 及更早版本中是必需的，因为 ``collections.abc`` 中的协议在 Python 3.8 中尚不支持下标操作（ ``[]`` ），但 ``typing`` 中的别名一直支持下标操作。在 Python 3.9 及更新版本中，``typing`` 中的别名不提供额外的功能。

简单的用户自定义协议(protocols)
****************************************

你可以通过继承特殊的 ``Protocol`` 类来定义自己的协议类：

.. code-block:: python

   from collections.abc import Iterable
   from typing import Protocol

   class SupportsClose(Protocol):
       # 空方法体（显式 '...'）
       def close(self) -> None: ...

   class Resource:  # 没有继承 SupportsClose 基类!

       def close(self) -> None:
          self.resource.release()

       # ... 其他方法 ...

   def close_all(items: Iterable[SupportsClose]) -> None:
       for item in items:
           item.close()

   close_all([Resource(), open('some/file')])  # OK

``Resource`` 是 ``SupportsClose`` 协议的子类型，因为它定义了兼容的 ``close`` 方法。由 :py:func:`open` 返回的常规文件对象同样兼容该协议，因为它们支持 ``close()`` 方法。

定义子协议和协议子类
***********************************************

你还可以定义子协议。现有协议可以通过多重继承进行扩展和合并。示例：

.. code-block:: python

   # ... 继续之前的示例

   class SupportsRead(Protocol):
       def read(self, amount: int) -> bytes: ...

   class TaggedReadableResource(SupportsClose, SupportsRead, Protocol):
       label: str

   class AdvancedResource(Resource):
       def __init__(self, label: str) -> None:
           self.label = label

       def read(self, amount: int) -> bytes:
           # 一些实现
           ...

   resource: TaggedReadableResource
   resource = AdvancedResource('小心处理')  # OK

注意，从现有协议继承并不会自动将子类变为协议——它只是创建了一个实现给定协议（或协议组）的常规（非协议）类或抽象基类（ABC）。如果你要定义协议， ``Protocol`` 基类必须始终显式存在：

.. code-block:: python

   class NotAProtocol(SupportsClose):  # 这不是一个协议
       new_attr: int

   class Concrete:
      new_attr: int = 0

      def close(self) -> None:
          ...

   # 错误：默认使用名义子类型
   x: NotAProtocol = Concrete()  # 错误!

你还可以在协议中包含方法的默认实现。如果你显式地子类化这些协议，你可以继承这些默认实现。

显式将协议作为基类包括在内也是一种记录你的类实现特定协议的方法，并强制 mypy 验证你的类实现是否与该协议兼容。特别地，省略属性的值或方法体将使其隐式为抽象：

.. code-block:: python

   class SomeProto(Protocol):
       attr: int  # 注意，没有右侧内容
       def method(self) -> str: ...  # 这里确实只是 ...

   class ExplicitSubclass(SomeProto):
       pass

   ExplicitSubclass()  # 错误：无法实例化抽象类 'ExplicitSubclass'
                       # 因为缺少抽象属性 'attr' 和 'method'

同样，显式赋值给协议实例可以要求类型检查器验证你的类是否实现了该协议：

.. code-block:: python

   _proto: SomeProto = cast(ExplicitSubclass, None)

协议属性的不变性(Invariance)
*********************************

协议的一个常见问题是，协议属性是不变的。例如：

.. code-block:: python

   class Box(Protocol):
         content: object

   class IntBox:
         content: int

   def takes_box(box: Box) -> None: ...

   takes_box(IntBox())  # 错误：参数 1 类型 "IntBox" 不兼容；预期为 "Box"
                        # 注意： "IntBox" 的以下成员存在冲突：
                        # 注意：      content: 预期为 "object"，实际为 "int"

这是因为 ``Box`` 将 ``content`` 定义为可变属性。原因如下：

.. code-block:: python

   def takes_box_evil(box: Box) -> None:
       box.content = "asdf"  # 这很糟糕，因为 box.content 应该是一个对象

   my_int_box = IntBox()
   takes_box_evil(my_int_box)
   my_int_box.content + 1  # 哦，TypeError!

可以通过在 ``Box`` 协议中使用 ``@property`` 声明 ``content`` 为只读来解决此问题：

.. code-block:: python

   class Box(Protocol):
       @property
       def content(self) -> object: ...

   class IntBox:
       content: int

   def takes_box(box: Box) -> None: ...

   takes_box(IntBox(42))  # OK

递归协议(Recursive)
*******************

协议可以是递归的（自我引用的）和互递归的。这对于声明抽象的递归集合，如树和链表，非常有用：

.. code-block:: python

   from __future__ import annotations

   from typing import Protocol

   class TreeLike(Protocol):
       value: int

       @property
       def left(self) -> TreeLike | None: ...

       @property
       def right(self) -> TreeLike | None: ...

   class SimpleTree:
       def __init__(self, value: int) -> None:
           self.value = value
           self.left: SimpleTree | None = None
           self.right: SimpleTree | None = None

   root: TreeLike = SimpleTree(0)  # OK

使用 isinstance() 与协议
*********************************

如果你用 ``@runtime_checkable`` 类装饰器装饰协议类，就可以在 :py:func:`isinstance` 中使用它。该装饰器为运行时结构检查添加了基本支持：

.. code-block:: python

   from typing import Protocol, runtime_checkable

   @runtime_checkable
   class Portable(Protocol):
       handles: int

   class Mug:
       def __init__(self) -> None:
           self.handles = 1

   def use(handles: int) -> None: ...

   mug = Mug()
   if isinstance(mug, Portable):  # 在运行时有效!
      use(mug.handles)

:py:func:`isinstance` 也适用于 :py:mod:`typing` 模块中的 :ref:`预定义协议 <predefined_protocols>` ，例如 :py:class:`~typing.Iterable` 。

.. warning::
   使用协议的 :py:func:`isinstance` 在运行时并不是完全安全的。
   例如，方法的签名不会被检查。运行时实现只检查所有协议成员是否存在，
   而不是它们是否具有正确的类型。使用协议的 :py:func:`issubclass` 也只会检查方法的存在性。

.. note::
   使用协议的 :py:func:`isinstance` 可能会意外地慢。
   在许多情况下，使用 :py:func:`hasattr` 检查属性的存在性会更合适。

.. _callback_protocols:

回调协议(Callback)
******************

协议可以用于定义灵活的回调类型，这些类型很难（甚至不可能）使用 :py:class:`Callable[...]` 语法来表达，例如可变参数、重载和复杂的泛型回调。它们通过特殊的 :py:meth:`__call__` 成员定义：

.. code-block:: python

   from collections.abc import Iterable
   from typing import Optional, Protocol

   class Combiner(Protocol):
       def __call__(self, *vals: bytes, maxlen: int | None = None) -> list[bytes]: ...

   def batch_proc(data: Iterable[bytes], cb_results: Combiner) -> bytes:
       for item in data:
           ...

   def good_cb(*vals: bytes, maxlen: int | None = None) -> list[bytes]:
       ...
   def bad_cb(*vals: bytes, maxitems: int | None) -> list[bytes]:
       ...

   batch_proc([], good_cb)  # OK
   batch_proc([], bad_cb)   # 错误!参数 2 的类型不兼容，因为回调中的名称和类型不同

回调协议和 :py:class:`collections.abc.Callable` 类型在大多数情况下可以互换使用。:py:meth:`__call__` 方法中的参数名称必须相同，除非参数是位置参数。示例（使用旧的泛型函数语法）：

.. code-block:: python

   from collections.abc import Callable
   from typing import Protocol, TypeVar

   T = TypeVar('T')

   class Copy(Protocol):
       # '/' 标记位置参数的结束
       def __call__(self, origin: T, /) -> T: ...

   copy_a: Callable[[T], T]
   copy_b: Copy

   copy_a = copy_b  # OK
   copy_b = copy_a  # 也 OK

.. _predefined_protocols_reference:

预定义协议参考(Predefined protocols)
***********************************************

迭代协议
...................

迭代协议在许多上下文中非常有用。例如，它们允许在 for 循环中对对象进行迭代。

collections.abc.Iterable[T]
---------------------------

:ref:`下面的例子 <predefined_protocols>` 定义了一个简单的 :py:meth:`__iter__ <object.__iter__>` 方法的实现：

.. code-block:: python

   def __iter__(self) -> Iterator[T]

另请参见：:py:class:`collections.abc.Iterable`。

collections.abc.Iterator[T]
---------------------------

`collections.abc.Iterator` 协议定义了以下方法：

.. code-block:: python

   def __next__(self) -> T
   def __iter__(self) -> Iterator[T]

另请参见：:py:class:`collections.abc.Iterator`。

集合协议(Collection)
....................

许多集合协议由内置容器类型（如 :py:class:`list` 和 :py:class:`dict`）实现，这些协议对用户定义的集合对象也很有用。

collections.abc.Sized
---------------------

这是一个支持 :py:func:`len(x) <len>` 的对象类型。

.. code-block:: python

   def __len__(self) -> int

另请参见： :py:class:`~collections.abc.Sized`.

collections.abc.Container[T]
----------------------------

这是一个支持 ``in`` 操作的对象类型。

.. code-block:: python

   def __contains__(self, x: object) -> bool

另请参见： :py:class:`~collections.abc.Container`.

collections.abc.Collection[T]
-----------------------------

.. code-block:: python

   def __len__(self) -> int
   def __iter__(self) -> Iterator[T]
   def __contains__(self, x: object) -> bool

另请参见： :py:class:`~collections.abc.Collection`.

One-off protocols
.................

这些协议通常仅在与单个标准库函数或类一起使用时才有用。

collections.abc.Reversible[T]
-----------------------------

这是一个支持 :py:func:`reversed(x) <reversed>` 的对象类型。

.. code-block:: python

   def __reversed__(self) -> Iterator[T]

另请参见： :py:class:`~collections.abc.Reversible`.

typing.SupportsAbs[T]
---------------------

这是一个支持 :py:func:`abs(x) <abs>` 的对象类型。 ``T`` 是 :py:func:`abs(x) <abs>` 返回值的类型。

.. code-block:: python

   def __abs__(self) -> T

另请参见： :py:class:`~typing.SupportsAbs`.

typing.SupportsBytes
--------------------

这是一个支持 :py:class:`bytes(x) <bytes>` 的对象类型。

.. code-block:: python

   def __bytes__(self) -> bytes

另请参见： :py:class:`~typing.SupportsBytes`.

.. _supports-int-etc:

typing.SupportsComplex
----------------------

这是一个支持 :py:class:`complex(x) <complex>` 的对象类型。请注意，不支持任何算术运算。  

.. code-block:: python

   def __complex__(self) -> complex

另请参见： :py:class:`~typing.SupportsComplex`.

typing.SupportsFloat
--------------------

这是一个支持 :py:class:`float(x) <float>` 的对象类型。请注意，不支持任何算术运算。  

.. code-block:: python

   def __float__(self) -> float

另请参见： :py:class:`~typing.SupportsFloat`.

typing.SupportsInt
------------------

这是一个支持 :py:class:`int(x) <int>` 的对象类型。请注意，不支持任何算术运算。

.. code-block:: python

   def __int__(self) -> int

另请参见： :py:class:`~typing.SupportsInt`.

typing.SupportsRound[T]
-----------------------

这是一个支持 :py:func:`round(x) <round>` 的对象类型。  

.. code-block:: python

   def __round__(self) -> T

另请参见： :py:class:`~typing.SupportsRound`.

Async protocols
...............

这些协议在异步代码中可能会很有用。有关更多信息，请参阅 :ref:`async-and-await` 。

collections.abc.Awaitable[T]
----------------------------

.. code-block:: python

   def __await__(self) -> Generator[Any, None, T]

另请参见： :py:class:`~collections.abc.Awaitable`.

collections.abc.AsyncIterable[T]
--------------------------------

.. code-block:: python

   def __aiter__(self) -> AsyncIterator[T]

另请参见： :py:class:`~collections.abc.AsyncIterable`.

collections.abc.AsyncIterator[T]
--------------------------------

.. code-block:: python

   def __anext__(self) -> Awaitable[T]
   def __aiter__(self) -> AsyncIterator[T]

另请参见： :py:class:`~collections.abc.AsyncIterator`.

上下文管理器协议(Context manager)
....................................

上下文管理器有两种协议 —— 一种用于常规上下文管理器，另一种用于异步上下文管理器。这些协议允许定义可以在 ``with`` 和 ``async with`` 语句中使用的对象。

contextlib.AbstractContextManager[T]
------------------------------------

.. code-block:: python

   def __enter__(self) -> T
   def __exit__(self,
                exc_type: type[BaseException] | None,
                exc_value: BaseException | None,
                traceback: TracebackType | None) -> bool | None

另请参见： :py:class:`~contextlib.AbstractContextManager`.

contextlib.AbstractAsyncContextManager[T]
-----------------------------------------

.. code-block:: python

   def __aenter__(self) -> Awaitable[T]
   def __aexit__(self,
                 exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> Awaitable[bool | None]

另请参见： :py:class:`~contextlib.AbstractAsyncContextManager`.
