.. _runtime_troubles:

运行时的注解问题
============================

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

Future annotations import (PEP 563)
-----------------------------------

Many of the issues described here are caused by Python trying to evaluate
annotations. Future Python versions (potentially Python 3.14) will by default no
longer attempt to evaluate function and variable annotations. This behaviour is
made available in Python 3.7 and later through the use of
``from __future__ import annotations``.

This can be thought of as automatic string literal-ification of all function and
variable annotations. Note that function and variable annotations are still
required to be valid Python syntax. For more details, see :pep:`563`.

.. note::

    Even with the ``__future__`` import, there are some scenarios that could
    still require string literals or result in errors, typically involving use
    of forward references or generics in:

    * :ref:`type aliases <type-aliases>` not defined using the ``type`` statement;
    * :ref:`type narrowing <type-narrowing>`;
    * type definitions (see :py:class:`~typing.TypeVar`, :py:class:`~typing.NewType`, :py:class:`~typing.NamedTuple`);
    * base classes.

    .. code-block:: python

        # base class example
        from __future__ import annotations

        class A(tuple['B', 'C']): ... # String literal types needed here
        class B: ...
        class C: ...

.. warning::

    Some libraries may have use cases for dynamic evaluation of annotations, for
    instance, through use of ``typing.get_type_hints`` or ``eval``. If your
    annotation would raise an error when evaluated (say by using :pep:`604`
    syntax with Python 3.9), you may need to be careful when using such
    libraries.

.. _typing-type-checking:

typing.TYPE_CHECKING
--------------------

The :py:mod:`typing` module defines a :py:data:`~typing.TYPE_CHECKING` constant
that is ``False`` at runtime but treated as ``True`` while type checking.

Since code inside ``if TYPE_CHECKING:`` is not executed at runtime, it provides
a convenient way to tell mypy something without the code being evaluated at
runtime. This is most useful for resolving :ref:`import cycles <import-cycles>`.

.. _forward-references:

Class name forward references
-----------------------------

Python does not allow references to a class object before the class is
defined (aka forward reference). Thus this code does not work as expected:

.. code-block:: python

   def f(x: A) -> None: ...  # NameError: name "A" is not defined
   class A: ...

Starting from Python 3.7, you can add ``from __future__ import annotations`` to
resolve this, as discussed earlier:

.. code-block:: python

   from __future__ import annotations

   def f(x: A) -> None: ...  # OK
   class A: ...

For Python 3.6 and below, you can enter the type as a string literal or type comment:

.. code-block:: python

   def f(x: 'A') -> None: ...  # OK

   # Also OK
   def g(x):  # type: (A) -> None
       ...

   class A: ...

Of course, instead of using future annotations import or string literal types,
you could move the function definition after the class definition. This is not
always desirable or even possible, though.

.. _import-cycles:

Import cycles
-------------

An import cycle occurs where module A imports module B and module B
imports module A (perhaps indirectly, e.g. ``A -> B -> C -> A``).
Sometimes in order to add type annotations you have to add extra
imports to a module and those imports cause cycles that didn't exist
before. This can lead to errors at runtime like:

.. code-block:: text

   ImportError: cannot import name 'b' from partially initialized module 'A' (most likely due to a circular import)

If those cycles do become a problem when running your program, there's a trick:
if the import is only needed for type annotations and you're using a) the
:ref:`future annotations import<future-annotations>`, or b) string literals or type
comments for the relevant annotations, you can write the imports inside ``if
TYPE_CHECKING:`` so that they are not executed at runtime. Example:

File ``foo.py``:

.. code-block:: python

   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       import bar

   def listify(arg: 'bar.BarClass') -> 'list[bar.BarClass]':
       return [arg]

File ``bar.py``:

.. code-block:: python

   from foo import listify

   class BarClass:
       def listifyme(self) -> 'list[BarClass]':
           return listify(self)

.. _not-generic-runtime:

Using classes that are generic in stubs but not at runtime
----------------------------------------------------------

Some classes are declared as :ref:`generic<generic-classes>` in stubs, but not
at runtime.

In Python 3.8 and earlier, there are several examples within the standard library,
for instance, :py:class:`os.PathLike` and :py:class:`queue.Queue`. Subscripting
such a class will result in a runtime error:

.. code-block:: python

   from queue import Queue

   class Tasks(Queue[str]):  # TypeError: 'type' object is not subscriptable
       ...

   results: Queue[int] = Queue()  # TypeError: 'type' object is not subscriptable

To avoid errors from use of these generics in annotations, just use the
:ref:`future annotations import<future-annotations>` (or string literals or type
comments for Python 3.6 and below).

To avoid errors when inheriting from these classes, things are a little more
complicated and you need to use :ref:`typing.TYPE_CHECKING
<typing-type-checking>`:

.. code-block:: python

   from typing import TYPE_CHECKING
   from queue import Queue

   if TYPE_CHECKING:
       BaseQueue = Queue[str]  # this is only processed by mypy
   else:
       BaseQueue = Queue  # this is not seen by mypy but will be executed at runtime

   class Tasks(BaseQueue):  # OK
       ...

   task_queue: Tasks
   reveal_type(task_queue.get())  # Reveals str

If your subclass is also generic, you can use the following (using the
legacy syntax for generic classes):

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
   reveal_type(task_queue.get())  # Reveals str

In Python 3.9 and later, we can just inherit directly from ``Queue[str]`` or ``Queue[T]``
since its :py:class:`queue.Queue` implements :py:meth:`~object.__class_getitem__`, so
the class object can be subscripted at runtime. You may still encounter issues (even if
you use a recent Python version) when subclassing generic classes defined in third-party
libraries if types are generic only in stubs.

Using types defined in stubs but not at runtime
-----------------------------------------------

Sometimes stubs that you're using may define types you wish to re-use that do
not exist at runtime. Importing these types naively will cause your code to fail
at runtime with ``ImportError`` or ``ModuleNotFoundError``. Similar to previous
sections, these can be dealt with by using :ref:`typing.TYPE_CHECKING
<typing-type-checking>`:

.. code-block:: python

   from __future__ import annotations
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from _typeshed import SupportsRichComparison

    def f(x: SupportsRichComparison) -> None

The ``from __future__ import annotations`` is required to avoid
a ``NameError`` when using the imported symbol.
For more information and caveats, see the section on
:ref:`future annotations <future-annotations>`.

.. _generic-builtins:

Using generic builtins
----------------------

Starting with Python 3.9 (:pep:`585`), the type objects of many collections in
the standard library support subscription at runtime. This means that you no
longer have to import the equivalents from :py:mod:`typing`; you can simply use
the built-in collections or those from :py:mod:`collections.abc`:

.. code-block:: python

   from collections.abc import Sequence
   x: list[str]
   y: dict[int, str]
   z: Sequence[str] = x

There is limited support for using this syntax in Python 3.7 and later as well:
if you use ``from __future__ import annotations``, mypy will understand this
syntax in annotations. However, since this will not be supported by the Python
interpreter at runtime, make sure you're aware of the caveats mentioned in the
notes at :ref:`future annotations import<future-annotations>`.

Using X | Y syntax for Unions
-----------------------------

Starting with Python 3.10 (:pep:`604`), you can spell union types as
``x: int | str``, instead of ``x: typing.Union[int, str]``.

There is limited support for using this syntax in Python 3.7 and later as well:
if you use ``from __future__ import annotations``, mypy will understand this
syntax in annotations, string literal types, type comments and stub files.
However, since this will not be supported by the Python interpreter at runtime
(if evaluated, ``int | str`` will raise ``TypeError: unsupported operand type(s)
for |: 'type' and 'type'``), make sure you're aware of the caveats mentioned in
the notes at :ref:`future annotations import<future-annotations>`.

Using new additions to the typing module
----------------------------------------

You may find yourself wanting to use features added to the :py:mod:`typing`
module in earlier versions of Python than the addition, for example, using any
of ``Literal``, ``Protocol``, ``TypedDict`` with Python 3.6.

The easiest way to do this is to install and use the ``typing_extensions``
package from PyPI for the relevant imports, for example:

.. code-block:: python

   from typing_extensions import Literal
   x: Literal["open", "close"]

If you don't want to rely on ``typing_extensions`` being installed on newer
Pythons, you could alternatively use:

.. code-block:: python

   import sys
   if sys.version_info >= (3, 8):
       from typing import Literal
   else:
       from typing_extensions import Literal

   x: Literal["open", "close"]

This plays nicely well with following :pep:`508` dependency specification:
``typing_extensions; python_version<"3.8"``
