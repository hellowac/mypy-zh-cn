.. _class-basics:

Class 基础(basics)
========================

本节将帮助您开始注解类(class)。包括内置类(Built-in classes)，如 `int`，也遵循相同的规则。

实例和类属性
*****************************

mypy 类型检查器可以检测您是否试图访问缺失的属性，这是一个非常常见的编程错误。为了使这一点正常工作，实例和类属性必须在类内定义或初始化。mypy 推断属性的类型:

.. code-block:: python

   class A:
       def __init__(self, x: int) -> None:
           self.x = x  # Aha，属性 'x' 的类型为 'int'

   a = A(1)
   a.x = 2  # OK!
   a.y = 3  # 错误:“A”没有属性“y”

这有点像每个类都有一个隐式定义的 :py:data:`__slots__ <object.__slots__>` 属性。这只在类型检查期间强制执行，而不是在程序运行时。

您可以在类体中显式声明变量的类型:

.. code-block:: python

   class A:
       x: list[int]  # 声明属性 'x' 的类型为 list[int]

   a = A()
   a.x = [1]     # OK

在 Python 中，类体中定义的变量可以作为类变量或实例变量使用。（如下一节所述，您可以使用 :py:data:`~typing.ClassVar` 注解覆盖此行为。）

类似地，您可以为在方法中定义的实例变量提供显式类型:

.. code-block:: python

   class A:
       def __init__(self) -> None:
           self.x: list[int] = []

       def f(self) -> None:
           self.y: Any = 0

您只能在方法内通过使用 ``self`` 显式赋值来定义实例变量:

.. code-block:: python

   class A:
       def __init__(self) -> None:
           self.y = 1   # 定义 'y'
           a = self
           a.x = 1      # 错误:'x' 未定义

注解 __init__ 方法
***************************

:py:meth:`__init__ <object.__init__>` 方法有些特别——它不返回值。最佳表达方式是 ``-> None``。然而，由于许多人认为这很冗余，如果 **至少有一个参数被注解**，则可以省略 :py:meth:`__init__ <object.__init__>` 方法的返回类型声明。例如，在以下类中，`:py:meth:`__init__ <object.__init__>` 被视为完全注解:

.. code-block:: python

   class C1:
       def __init__(self) -> None:
           self.var = 42

   class C2:
       def __init__(self, arg: int):
           self.var = arg

但是，如果 :py:meth:`__init__ <object.__init__>` 方法没有注解参数且没有返回类型注解，它将被视为未注解的方法:

.. code-block:: python

   class C3:
       def __init__(self):
           # 这个主体不进行类型检查
           self.var = 42 + 'abc'

类属性注解(ClassVar)
***************************

您可以使用 :py:data:`ClassVar[t] <typing.ClassVar>` 注解显式声明特定属性不应在实例上设置:

.. code-block:: python

  from typing import ClassVar

  class A:
      x: ClassVar[int] = 0  # 仅类变量

  A.x += 1  # OK

  a = A()
  a.x = 1  # 错误:无法通过实例赋值给类变量 "x"
  print(a.x)  # OK — 可以通过实例读取

并非所有类变量都需要使用 :py:data:`~typing.ClassVar` 注解。没有 :py:data:`~typing.ClassVar` 注解的属性仍然可以用作类变量。然而，mypy 不会防止它被用作实例变量，如前所述:

.. code-block:: python

  class A:
      x = 0  # 可以用作类或实例变量

  A.x += 1  # OK

  a = A()
  a.x = 1  # 也可以

请注意，:py:data:`~typing.ClassVar` 不是一个类，您不能使用 :py:func:`isinstance` 或 :py:func:`issubclass`。它不会改变 Python 的运行时行为——它仅用于类型检查器，如 mypy（同时也对人类读者有帮助）。

您还可以省略方括号和变量类型，但这可能不会如您所期望:

.. code-block:: python

   class A:
       y: ClassVar = 0  # 类型隐式为 Any!

在这种情况下，属性的类型将隐式为 ``Any`` 。这种行为将来会改变，因为它令人惊讶。

显式的 :py:data:`~typing.ClassVar` 在区分可调用类型的类变量和实例变量时尤其方便。例如:

.. code-block:: python

   from collections.abc import Callable
   from typing import ClassVar

   class A:
       foo: Callable[[int], None]
       bar: ClassVar[Callable[[A, int], None]]
       bad: Callable[[A], None]

   A().foo(42)  # OK
   A().bar(42)  # OK
   A().bad()  # 错误:参数数量不足

.. note::
   :py:data:`~typing.ClassVar` 类型参数不能包含类型变量: ``ClassVar[T]`` 和 ``ClassVar[list[T]]`` 都是无效的，如果 ``T`` 是一个类型变量（有关类型变量的更多信息，请参见 :ref:`generic-classes`）。

重写静态类型方法(override)
***********************************

在重写静态类型方法时，mypy 会检查重写的方法是否具有兼容的签名:

.. code-block:: python

   class Base:
       def f(self, x: int) -> None:
           ...

   class Derived1(Base):
       def f(self, x: str) -> None:   # 错误:'x' 的类型不兼容
           ...

   class Derived2(Base):
       def f(self, x: int, y: int) -> None:  # 错误:参数过多
           ...

   class Derived3(Base):
       def f(self, x: int) -> None:   # OK
           ...

   class Derived4(Base):
       def f(self, x: float) -> None:   # OK:mypy 将 int 视为 float 的子类型
           ...

   class Derived5(Base):
       def f(self, x: int, y: int = 0) -> None:   # OK:接受比基类方法更多的参数
           ...                                       

.. note::

   在重写时，您还可以 **协变(covariantly)** 地重写返回类型。例如，您可以用子类型如 ``list[int]`` 来重写返回类型 ``Iterable[int]`` 。同样，您可以 **逆变(contravariantly)** 重写参数类型 — —子类可以拥有更一般的参数类型。

为了确保在重命名方法时代码保持正确，显式标记一个方法为重写基类方法是很有帮助的。这可以通过 ``@override`` 装饰器实现。 ``@override`` 可以从 Python 3.12 开始从 ``typing`` 导入，或者从 ``typing_extensions`` 导入以用于较旧的 Python 版本。如果基类方法在重写方法未重命名的情况下被重命名，mypy 将显示错误:

.. code-block:: python

   from typing import override

   class Base:
       def f(self, x: int) -> None:
           ...
       def g_renamed(self, y: str) -> None:
           ...

   class Derived1(Base):
       @override
       def f(self, x: int) -> None:   # OK
           ...

       @override
       def g(self, y: str) -> None:   # 错误:未找到对应的基类方法
           ...

.. note::

   使用 :ref:`--enable-error-code explicit-override <code-explicit-override>` 来要求方法重写使用 ``@override`` 装饰器。缺少时会产生错误。

您还可以使用动态类型的方法重写静态类型的方法。这允许动态类型代码重写库类中定义的方法，而不必担心它们的类型签名。

如往常一样，依赖动态类型代码可能不安全。因为在运行时没有强制执行重写方法返回的值与原始返回类型兼容，注解在运行时无效:

.. code-block:: python

   class Base:
       def inc(self, x: int) -> int:
           return x + 1

   class Derived(Base):
       def inc(self, x):   # 重写，动态类型
           return 'hello'  # 与 'Base' 不兼容，但没有 mypy 错误

抽象基类和多重继承(Abstract)
**********************************************

Mypy 支持 Python 的 :doc:`抽象基类 <python:library/abc>` (ABCs)。抽象类至少有一个抽象方法或属性，任何具体（非抽象）子类必须实现这些方法或属性。您可以使用 :py:class:`abc.ABCMeta` 元类和 :py:func:`@abc.abstractmethod <abc.abstractmethod>` 函数装饰器定义抽象基类。示例:

.. code-block:: python

   from abc import ABCMeta, abstractmethod

   class Animal(metaclass=ABCMeta):
       @abstractmethod
       def eat(self, food: str) -> None: pass

       @property
       @abstractmethod
       def can_walk(self) -> bool: pass

   class Cat(Animal):
       def eat(self, food: str) -> None:
           ...  # 省略实现

       @property
       def can_walk(self) -> bool:
           return True

   x = Animal()  # 错误:'Animal' 是抽象的，因为缺少 'eat' 和 'can_walk'
   y = Cat()     # OK

请注意，即使您省略了 :py:class:`~abc.ABCMeta` 元类，mypy 仍会检查未实现的抽象方法。这在元类可能导致运行时元类冲突时特别有用。

由于无法创建 ABC 的实例，因此它们最常用于类型注解。例如，以下方法接受包含任意动物（具体的 `Animal` 子类实例）的任意可迭代对象:

.. code-block:: python

   def feed_all(animals: Iterable[Animal], food: str) -> None:
       for animal in animals:
           animal.eat(food)

关于 ABC 的工作方式，有一个重要的特性——一个类是否为抽象类在某种程度上是隐式的。在下面的示例中，由于 `Derived` 继承了来自 `Base` 的抽象方法 `f`，并且没有显式实现它，因此 `Derived` 被视为抽象基类。定义 `Derived` 时，mypy 不会产生错误，因为这是一个有效的 ABC:

.. code-block:: python

   from abc import ABCMeta, abstractmethod

   class Base(metaclass=ABCMeta):
       @abstractmethod
       def f(self, x: int) -> None: pass

   class Derived(Base):  # 无错误 - Derived 隐式为抽象类
       def g(self) -> None:
           ...

但是，尝试创建 `Derived` 的实例会被拒绝:

.. code-block:: python

   d = Derived()  # 错误:'Derived' 是抽象的

.. note::

   忘记实现抽象方法是一个常见错误。如上所示，在这种情况下，类定义不会产生错误，但任何尝试构造实例的行为都会被标记为错误。

Mypy 允许您省略抽象方法的主体，但如果您这样做，通过 `super()` 调用该方法是不安全的。例如:

.. code-block:: python

   from abc import abstractmethod
   class Base:
       @abstractmethod
       def foo(self) -> int: pass
       @abstractmethod
       def bar(self) -> int:
           return 0
   class Sub(Base):
       def foo(self) -> int:
           return super().foo() + 1  # 错误:调用 "Base" 的抽象方法 "foo"
                                     # 通过 super() 调用带有简单主体的抽象方法是不安全的
       @abstractmethod
       def bar(self) -> int:
           return super().bar() + 1  # 这是可以的。

一个类可以继承任意数量的类，包括抽象类和具体类。与普通重写一样，动态类型的方法可以重写或实现任何基类中定义的静态类型方法，包括在抽象基类中定义的抽象方法。

您可以使用常规属性或实例变量来实现抽象属性。

槽（Slots）
***************

当一个类显式定义了 :std:term:`__slots__` 时，mypy 会检查所有赋值的属性是否是 ``__slots__`` 的成员：

.. code-block:: python

  class Album:
      __slots__ = ('name', 'year')

      def __init__(self, name: str, year: int) -> None:
         self.name = name
         self.year = year
         # 错误：尝试为类型 "Album" 的 "__slots__" 赋值 "released"，但不在 "__slots__" 中
         self.released = True

  my_album = Album('Songs about Python', 2021)

Mypy 仅在以下条件下检查属性赋值与 ``__slots__`` 的一致性：

1. 所有基类（除了内置类）必须显式定义 ``__slots__`` （这反映了 Python 的语义）。

2. ``__slots__`` 不包括 ``__dict__``。如果 ``__slots__`` 包含 ``__dict__`` ，则可以设置任意属性，类似于未定义 ``__slots__`` 时的行为（这也反映了 Python 的语义）。

3. ``__slots__`` 中的所有值必须是字符串字面量。