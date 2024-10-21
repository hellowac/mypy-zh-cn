.. _final_attrs:

最终名称, 方法和类(Final)
================================

本节介绍以下相关功能：

1. *Final names* 是在初始化后不应重新赋值的变量或属性。它们对于声明常量很有用。
2. *Final methods* 不应在子类中被重写。
3. *Final classes* 不应被子类化。

所有这些仅由 mypy 强制执行，并且仅在注解代码中。Python 运行时并不强制执行这些规则。

.. note::

    本页中的示例从 ``typing`` 模块导入 ``Final`` 和 ``final``。这些类型在 Python 3.8 中添加到 ``typing``，但在 Python 3.4 - 3.7 中也可以通过 ``typing_extensions`` 包使用。

最终名称(Final names)
----------------------

你可以使用 ``typing.Final`` 限定符来指示某个名称或属性不应被重新赋值、重新定义或重写。这通常对于模块和类级常量很有用，以防止意外修改。Mypy 将在类型检查的代码中防止对最终名称的进一步赋值：

.. code-block:: python

   from typing import Final

   RATE: Final = 3_000

   class Base:
       DEFAULT_ID: Final = 0

   RATE = 300  # 错误：无法赋值给最终属性
   Base.DEFAULT_ID = 1  # 错误：无法重写最终属性

另一个使用 final 属性的用例是保护某些属性不被子类重写：

.. code-block:: python

   from typing import Final

   class Window:
       BORDER_WIDTH: Final = 2.5
       ...

   class ListView(Window):
       BORDER_WIDTH = 3  # 错误：无法重写最终属性

你可以使用 :py:class:`@property <property>` 来使属性只读，但与 ``Final`` 不同，它不适用于模块属性，并且不防止在子类中重写。

语法变体(Syntax variants)
******************************

你可以使用 ``Final`` 的以下形式之一：

* 你可以使用语法 ``Final[<type>]`` 提供一个显式类型。例如：

  .. code-block:: python

     ID: Final[int] = 1

  在这里，mypy 将推断 ``ID`` 的类型为 ``int``。

* 你可以省略类型：

  .. code-block:: python

     ID: Final = 1

  在这里，mypy 将推断 ``ID`` 的类型为 ``Literal[1]``。请注意，与泛型类不同，这 *不是* ``Final[Any]``。

* 在类体和存根文件中，你可以省略右侧，只写 ``ID: Final[int]``。

* 最后，你可以写 ``self.id: Final = 1`` （可选地在方括号中指定类型）。这 *仅* 允许在 :py:meth:`__init__ <object.__init__>` 方法中使用，以便最终实例属性仅在创建实例时赋值一次。

Final详情(Details)
**************************

定义最终名称的两个主要规则如下：

* 每个模块或类对于给定属性最多只能有 *一个(at most one)* 最终声明。不能有具有相同名称的类级别和实例级别常量。

* 必须对最终名称进行 *恰好一个(exactly one)* 赋值。

在类体中声明的没有初始化器的最终属性必须在 :py:meth:`__init__ <object.__init__>` 方法中初始化（你可以在存根文件中省略初始化器）：

.. code-block:: python

   class ImmutablePoint:
       x: Final[int]
       y: Final[int]  # 错误：没有初始化器的最终属性

       def __init__(self) -> None:
           self.x = 1  # 正确

``Final`` 只能作为赋值或变量注解中的最外层类型使用。在其他位置使用它会导致错误。特别是， ``Final`` 不能用于函数参数的注解：

.. code-block:: python

   x: list[Final[int]] = []  # 错误!

   def fun(x: Final[list[int]]) -> None:  # 错误!
       ...

``Final`` 和 :py:data:`~typing.ClassVar` 不应一起使用。Mypy 将根据最终声明是否在类体中或在 :py:meth:`__init__ <object.__init__>` 中初始化，自动推断最终声明的作用域。

最终(Final)属性不能被子类重写（即使使用另一个显式的最终声明）。但是，请注意，最终属性可以覆盖只读属性：

.. code-block:: python

   class Base:
       @property
       def ID(self) -> int: ...

   class Derived(Base):
       ID: Final = 1  # 正确

将名称声明为最终属性仅保证该名称不会被重新绑定到另一个值。它并不使值不可变。你可以使用不可变的 ABC 和容器来防止修改这些值：

.. code-block:: python

   x: Final = ['a', 'b']
   x.append('c')  # 正确

   y: Final[Sequence[str]] = ['a', 'b']
   y.append('x')  # 错误：序列是不可变的
   z: Final = ('a', 'b')  # 也是一个选项

最终方法(Final methods)
--------------------------

与属性一样，有时保护方法不被重写也是很有用的。你可以使用 ``typing.final`` 装饰器来实现这一目的：

.. code-block:: python

   from typing import final

   class Base:
       @final
       def common_name(self) -> None:
           ...

   class Derived(Base):
       def common_name(self) -> None:  # 错误：无法重写最终方法
           ...

这个 ``@final`` 装饰器可以与实例方法、类方法、静态方法和属性一起使用。

对于重载方法，你应该在实现上添加 ``@final`` 以使其成为最终方法（或者在存根中的第一个重载上添加）：

.. code-block:: python

   from typing import final, overload

   class Base:
       @overload
       def method(self) -> None: ...
       @overload
       def method(self, arg: int) -> int: ...
       @final
       def method(self, x=None):
           ...

最终类(Final classes)
--------------------------

你可以将 ``typing.final`` 装饰器应用于类，以向 mypy 指示该类不应被子类化：

.. code-block:: python

   from typing import final

   @final
   class Leaf:
       ...

   class MyLeaf(Leaf):  # 错误：Leaf 不能被子类化
       ...

该装饰器作为 mypy 的声明（并作为人类的文档），但实际上并不会阻止在运行时进行子类化。

以下是一些使用最终类可能有用的情况：

* 一个类并不是为了被子类化而设计的。也许子类化无法按预期工作，或者子类化容易出错。
* 子类化会使代码更难理解或维护。例如，你可能想要防止基类和子类之间不必要的紧耦合。
* 你希望保留将来随意更改类实现的自由，而这些更改可能会破坏子类。

具有 ``@final`` 装饰器且定义了至少一个抽象方法或属性的抽象类将会导致 mypy 生成错误，因为这些属性永远无法实现。

.. code-block:: python

    from abc import ABCMeta, abstractmethod
    from typing import final

    @final
    class A(metaclass=ABCMeta):  # 错误：最终类 A 具有抽象属性 "f"
        @abstractmethod
        def f(self, x: int) -> None: pass
