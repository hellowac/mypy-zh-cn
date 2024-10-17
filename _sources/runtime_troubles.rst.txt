.. _runtime_troubles:

运行时的注解问题(Annotation issues)
========================================================

惯用的类型注解使用有时会与特定 Python 版本所认为的合法代码相冲突。本节描述这些场景，并解释如何让代码重新运行。一般来说，我们有三种工具可供使用：

* 使用 ``from __future__ import annotations`` (:pep:`563`)（这种行为可能在未来的 Python 版本中成为默认）。
* 使用字符串字面量类型或类型注释。
* 使用 ``typing.TYPE_CHECKING`` 。

在讨论具体问题之前，我们先介绍这些工具的使用。

.. _string-literal-types:

字符串字面量类型和类型注释(literal)
--------------------------------------

Mypy 允许使用已弃用的 ``# type:`` 类型注释语法添加类型注解。这在 Python 3.6 之前是必需的，因为早期版本不支持变量的类型注解。例如：

.. code-block:: python

    a = 1  # type: int

    def f(x):  # type: (int) -> int
        return x + 1

    # 函数参数较多时的替代类型注释语法
    def send_email(
        address,     # type: Union[str, List[str]]
        sender,      # type: str
        cc,          # type: Optional[List[str]]
        subject='',
        body=None    # type: List[str]
    ):
    # type: (...) -> bool

类型注释不会引发运行时错误，因为注释不会被 Python 解释执行。

类似地，使用字符串字面量类型可以避免导致运行时错误的注解问题。

任何类型都可以作为字符串字面量输入，并且可以随意将字符串字面量类型与非字符串字面量类型组合：

.. code-block:: python

    def f(a: list['A']) -> None: ...  # OK，防止 NameError，因为 A 在后面定义
    def g(n: 'int') -> None: ...      # 也 OK，虽然没用

字符串字面量类型不需要在 ``# type:`` 注释和 :ref:`存根文件 <stub-files>` 中使用。

字符串字面量类型必须在同一模块中稍后定义（或导入）。它们不能用于解决跨模块的未解析引用。（有关处理导入循环，请参见 :ref:`导入循环 <import-cycles>` 的相关内容。）

.. _future-annotations:

未来(Futrue)的注解导入(PEP 563)
-----------------------------------

本文描述的许多问题是由于 Python 尝试对注解进行求值引起的。未来的 Python 版本（可能是 Python 3.14）将默认不再尝试对函数和变量的注解进行求值。这一行为在 Python 3.7 及更高版本中可以通过使用 ``from __future__ import annotations`` 实现。

这可以被视为对所有函数和变量注解的自动字符串字面量化。请注意，函数和变量的注解仍然需要是有效的 Python 语法。有关详细信息，请参阅：PEP 563。

.. note::

    即使使用了 ``__future__`` 导入，某些场景下仍可能需要字符串字面量或导致错误，通常涉及使用前向引用或泛型的情况，如：

    * 未使用 ``type`` 语句定义的 :ref:`类型别名 <type-aliases>`;
    * :ref:`类型收窄 <type-narrowing>`;
    * 类型定义（参见 :py:class:`~typing.TypeVar`, :py:class:`~typing.NewType`, :py:class:`~typing.NamedTuple`）；
    * 基类(base classes)。

    .. code:: python

        # 基类示例
        from __future__ import annotations

        class A(tuple['B', 'C']): ...  # 此处需要字符串字面量类型
        class B: ...
        class C: ...

.. warning::

    某些库可能需要动态求值注解，例如，通过使用 ``typing.get_type_hints`` 或 ``eval`` 。如果你的注解在求值时会引发错误（例如在 Python 3.9 中使用 :pep:`604` 语法），在使用此类库时需要小心。

.. _typing-type-checking:

typing.TYPE_CHECKING
--------------------

:py:mod:`typing` 模块定义了一个常量 :py:data:`~typing.TYPE_CHECKING`，它在运行时为 ``False``，但在类型检查时被视为 ``True``。

由于 ``if TYPE_CHECKING:`` 语句中的代码不会在运行时执行，它提供了一种方便的方法来告诉 mypy 一些信息，而不会在运行时对代码进行求值。这对于解决 :ref:`导入循环 <import-cycles>` 问题最有用。

.. _forward-references:

类名的前向引用(forward references)
---------------------------------------

Python 不允许在类未定义之前就引用该类对象（即前向引用）。因此，下面的代码不能按预期工作：

.. code-block:: python

   def f(x: A) -> None: ...  # NameError: name "A" is not defined
   class A: ...

从 Python 3.7 开始，你可以添加 ``from __future__ import annotations`` 来解决这个问题，如下所述：

.. code-block:: python

   from __future__ import annotations

   def f(x: A) -> None: ...  # OK
   class A: ...

对于 Python 3.6 及以下版本，你可以将类型作为字符串字面量或类型注释输入：

.. code-block:: python

   def f(x: 'A') -> None: ...  # OK

   # 也可以
   def g(x):  # type: (A) -> None
       ...

   class A: ...

当然，除了使用 future annotations 导入或字符串字面量类型外，你也可以将函数定义移到类定义之后。不过，这并不总是理想或可行的。

.. _import-cycles:

导入循环(Import cycles)
-------------------------------

当模块 A 导入模块 B，而模块 B 又导入模块 A 时（可能是间接的，例如：``A -> B -> C -> A``），就会发生导入循环。有时为了添加类型注解，你需要在模块中添加额外的导入，而这些导入可能会导致之前不存在的循环。这可能会在运行时引发以下错误：

.. code-block:: text

   ImportError: cannot import name 'b' from partially initialized module 'A' (most likely due to a circular import)

如果这些循环在运行程序时成为问题，可以使用一个技巧：如果导入仅用于类型注解，并且你使用了 a) :ref:`future annotations import<future-annotations>` 或 b) 用字符串字面量或类型注释来表示相关注解，你可以将导入放在 ``if TYPE_CHECKING:`` 块中，这样它们在运行时不会被执行。例如：

文件 ``foo.py``:

.. code-block:: python

   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       import bar

   def listify(arg: 'bar.BarClass') -> 'list[bar.BarClass]':
       return [arg]

文件 ``bar.py``:

.. code-block:: python

   from foo import listify

   class BarClass:
       def listifyme(self) -> 'list[BarClass]':
           return listify(self)

.. _not-generic-runtime:

在存根中是泛型但运行时不是的类
----------------------------------------------------------

有些类在类型存根文件中被声明为 :ref:`泛型 <generic-classes>`，但在运行时并不是泛型类。

在 Python 3.8 及更早的版本中，标准库中有几个例子，例如：:py:class:`os.PathLike` 和 :py:class:`queue.Queue`。对这些类进行下标操作会导致运行时错误：

.. code-block:: python

   from queue import Queue

   class Tasks(Queue[str]):  # TypeError: 'type' object is not subscriptable
       ...

   results: Queue[int] = Queue()  # TypeError: 'type' object is not subscriptable

为避免在注解中使用这些泛型时产生错误，只需使用 :ref:`future annotations import <future-annotations>` （对于 Python 3.6 及以下版本可以使用字符串字面量或类型注释）。

当从这些类继承时，要避免错误，情况稍微复杂些，需要使用 :ref:`typing.TYPE_CHECKING <typing-type-checking>` ：

.. code-block:: python

   from typing import TYPE_CHECKING
   from queue import Queue

   if TYPE_CHECKING:
       BaseQueue = Queue[str]  # 仅由 mypy 处理
   else:
       BaseQueue = Queue  # mypy 不会看到，但在运行时执行

   class Tasks(BaseQueue):  # OK
       ...

   task_queue: Tasks
   reveal_type(task_queue.get())  # 显示为 str

如果你的子类也是泛型类，可以使用以下方法（使用泛型类的旧语法）：

.. code-block:: python

   from typing import TYPE_CHECKING, TypeVar, Generic
   from queue import Queue

   _T = TypeVar("_T")
   if TYPE_CHECKING:
       class _MyQueueBase(Queue[_T]): pass
   else:
       class _MyQueueBase(Generic[_T], Queue): pass

   class MyQueue(_MyQueueBase[_T]): pass

   task_queue: MyQueue[str]
   reveal_type(task_queue.get())  # 显示为 str

在 Python 3.9 及更高版本中，我们可以直接继承 ``Queue[str]`` 或 ``Queue[T]``，因为 :py:class:`queue.Queue` 实现了 :py:meth:`~object.__class_getitem__`，因此类对象在运行时可以被下标操作。不过，如果你继承了某些第三方库中定义的泛型类，且这些类的泛型类型仅在存根中声明，那么即使你使用的是新版 Python，仍可能遇到问题。

使用在存根中定义但运行时不存在的类型
-----------------------------------------------

有时你可能使用的类型存根文件定义了一些你希望复用的类型，但这些类型在运行时并不存在。如果直接导入这些类型，代码在运行时会因为 `ImportError` 或 `ModuleNotFoundError` 而失败。与之前的章节类似，你可以通过使用 :ref:`typing.TYPE_CHECKING<typing-type-checking>` 来解决这些问题：

.. code-block:: python

   from __future__ import annotations
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from _typeshed import SupportsRichComparison

   def f(x: SupportsRichComparison) -> None: ...

这里的 `from __future__ import annotations` 是必须的，避免在使用导入的符号时引发 `NameError`。有关更多信息和注意事项，请参见 :ref:`future annotations <future-annotations>` 部分。

.. _generic-builtins:

使用泛型内置类型
----------------------

从 Python 3.9 开始（:pep:`585`），标准库中许多集合类型的类型对象支持在运行时进行下标操作。这意味着你不再需要从 :py:mod:`typing` 模块中导入对应的类型；可以直接使用内置集合或来自 :py:mod:`collections.abc` 的类型：

.. code-block:: python

   from collections.abc import Sequence
   x: list[str]
   y: dict[int, str]
   z: Sequence[str] = x

从 Python 3.7 开始，也有限制性地支持这种语法：如果你使用了 ``from __future__ import annotations``，mypy 会理解这种注解语法。然而，由于 Python 解释器在运行时并不支持这种方式，请务必注意 :ref:`future annotations import <future-annotations>` 部分中提到的注意事项。

使用 X | Y 语法表示联合类型
-----------------------------

从 Python 3.10 开始（:pep:`604`），你可以使用 ``x: int | str`` 来表示联合类型，而不是 ``x: typing.Union[int, str]``。

在 Python 3.7 及更高版本中，也有限制地支持这种语法：如果你使用了 ``from __future__ import annotations`` ，mypy 会理解这种语法在注解、字符串字面量类型、类型注释和存根文件中的使用。然而，由于 Python 解释器在运行时不支持这种方式（如果运行时评估 ``int | str`` ，会引发 ``TypeError: unsupported operand type(s) for |: 'type' and 'type'``），请注意 :ref:`future annotations import <future-annotations>` 部分中提到的注意事项。

使用 typing 模块的新特性
-----------------------------

你可能希望在比某些类型特性添加的 Python 版本更早的版本中使用它们，例如在 Python 3.6 中使用 ``Literal``、``Protocol`` 或 ``TypedDict``。

最简单的方法是从 PyPI 安装并使用 ``typing_extensions`` 包来导入相关的特性，例如：

.. code-block:: python

   from typing_extensions import Literal
   x: Literal["open", "close"]

如果你不希望依赖在更新的 Python 版本中安装 ``typing_extensions`` ，你可以使用以下方式：

.. code-block:: python

   import sys
   if sys.version_info >= (3, 8):
       from typing import Literal
   else:
       from typing_extensions import Literal

   x: Literal["open", "close"]

这与 :pep:`508` 的依赖规范很好地配合： ``typing_extensions; python_version<"3.8"`` 。
