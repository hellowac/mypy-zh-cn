泛型(Generics)
================

本节解释如何定义自己的泛型类，这些类接受一个或多个类型参数，类似于内置类型如 ``list[T]``。用户自定义泛型是一个中级高级特性，您可以在不使用它们的情况下取得很大进展——随意跳过本节，稍后再回来。

.. _generic-classes:

定义泛型类(generic classes)
************************************

内置集合类是泛型类。泛型类型在 ``[...]`` 中接受一个或多个类型参数，这些参数可以是任意类型。例如，类型 ``dict[int, str]`` 的类型参数是 ``int`` 和 ``str``，而 ``list[int]`` 的类型参数是 ``int`` 。

程序也可以定义新的泛型类。以下是一个非常简单的泛型类，它表示一个栈（使用 Python 3.12 引入的语法）：

.. code-block:: python

   class Stack[T]:
       def __init__(self) -> None:
           # 创建一个空列表，元素类型为 T
           self.items: list[T] = []

       def push(self, item: T) -> None:
           self.items.append(item)

       def pop(self) -> T:
           return self.items.pop()

       def empty(self) -> bool:
           return not self.items

在 Python 中定义泛型类有两种语法变体。Python 3.12 引入了一种 `新的专用语法 <https://docs.python.org/3/whatsnew/3.12.html#pep-695-type-parameter-syntax>`_ 来定义泛型类（以及函数和类型别名，稍后我们会讨论）。上述示例使用了新语法。大多数示例同时给出新旧（或遗留）语法变体。除非另有说明，它们的工作方式相同——但新语法更具可读性和便利性。

以下是使用旧语法的相同示例（在 Python 3.11 及更早版本中需要，但在新版本中也支持）：

.. code-block:: python

   from typing import TypeVar, Generic

   T = TypeVar('T')  # 定义类型变量 "T"

   class Stack(Generic[T]):
       def __init__(self) -> None:
           # 创建一个空列表，元素类型为 T
           self.items: list[T] = []

       def push(self, item: T) -> None:
           self.items.append(item)

       def pop(self) -> T:
           return self.items.pop()

       def empty(self) -> bool:
           return not self.items

.. note::

    目前没有计划弃用遗留语法。
    您可以自由地混合使用新旧语法变体的代码，甚至在同一个文件中（但 *不能* 在同一个类中）。

``Stack`` 类可以用来表示任何类型的栈：``Stack[int]``、``Stack[tuple[int, str]]`` 等。您可以将 ``Stack[int]`` 理解为上面定义的 ``Stack``，但将所有 ``T`` 的实例替换为 ``int``。

使用 ``Stack`` 类似于内置容器类型：

.. code-block:: python

   # 构造一个空的 Stack[int] 实例
   stack = Stack[int]()
   stack.push(2)
   stack.pop()

   # 错误：Stack 的 "push" 的参数 1 类型不兼容；预期为 "int"
   stack.push('x')

   stack2: Stack[str] = Stack()
   stack2.append('x')

泛型类型的实例构造会进行类型检查（Python 3.12 语法）：

.. code-block:: python

   class Box[T]:
       def __init__(self, content: T) -> None:
           self.content = content

   Box(1)       # 正确，推断类型为 Box[int]
   Box   # 也是正确的

   # 错误：Box 的参数 1 类型不兼容；预期为 "int"
   Box[int]('some string')

以下是使用遗留语法定义的 ``Box`` （Python 3.11 及更早版本）：

.. code-block:: python

   from typing import TypeVar, Generic

   T = TypeVar('T')

   class Box(Generic[T]):
       def __init__(self, content: T) -> None:
           self.content = content

.. note::

    在继续之前，让我们澄清一些术语。
    在 ``class Stack[T]`` 或 ``class Stack(Generic[T])`` 中，名称 ``T`` 声明了一个 *类型参数(type parameter)* ``T`` （属于 ``Stack`` 类）。
    ``T`` 也被称为 *类型变量(type variable)*，尤其是在类型注解中，例如上面 ``push`` 的签名。
    当在类型注解中使用类型 ``Stack[...]`` 时，方括号中的类型被称为 *类型参数(type argument)*。
    这类似于函数参数和实参之间的区别。

.. _generic-subclasses:

定义泛型类的子类(subclasses)
**************************************

用户定义的泛型类和在 :py:mod:`typing` 中定义的泛型类可以作为另一个类（泛型或非泛型）的基类。例如（Python 3.12 语法）：

.. code-block:: python

   from typing import Mapping, Iterator

   # 这是 Mapping 的泛型子类
   class MyMap[KT, VT](Mapping[KT, VT]):
       def __getitem__(self, k: KT) -> VT: ...
       def __iter__(self) -> Iterator[KT]: ...
       def __len__(self) -> int: ...

   items: MyMap[str, int]  # 正确

   # 这是 dict 的非泛型子类
   class StrDict(dict[str, str]):
       def __str__(self) -> str:
           return f'StrDict({super().__str__()})'

   data: StrDict[int, int]  # 错误!StrDict 不是泛型
   data2: StrDict  # 正确

   # 这是一个用户定义的泛型类
   class Receiver[T]:
       def accept(self, value: T) -> None: ...

   # 这是 Receiver 的泛型子类
   class AdvancedReceiver[T](Receiver[T]): ...

以下是使用遗留语法的相同示例（Python 3.11 及更早版本）：

.. code-block:: python

   from typing import Generic, TypeVar, Mapping, Iterator

   KT = TypeVar('KT')
   VT = TypeVar('VT')

   # 这是 Mapping 的泛型子类
   class MyMap(Mapping[KT, VT]):
       def __getitem__(self, k: KT) -> VT: ...
       def __iter__(self) -> Iterator[KT]: ...
       def __len__(self) -> int: ...

   items: MyMap[str, int]  # 正确

   # 这是 dict 的非泛型子类
   class StrDict(dict[str, str]):
       def __str__(self) -> str:
           return f'StrDict({super().__str__()})'

   data: StrDict[int, int]  # 错误!StrDict 不是泛型
   data2: StrDict  # 正确

   # 这是一个用户定义的泛型类
   class Receiver(Generic[T]):
       def accept(self, value: T) -> None: ...

   # 这是 Receiver 的泛型子类
   class AdvancedReceiver(Receiver[T]): ...

.. note::

    如果您希望 mypy 将用户定义的类视为映射，您必须添加显式的 :py:class:`~collections.abc.Mapping` 基类（序列使用 :py:class:`~collections.abc.Sequence` 等）。这是因为 mypy 对这些 ABC 不使用 *结构化子类型*，与使用 :ref:`结构化子类型 <protocol-types>` 的简单协议如 :py:class:`~collections.abc.Iterable` 不同。

在使用遗留语法时，如果其他基类包含类型变量，如上述示例中的 ``Mapping[KT, VT]``，则可以省略 :py:class:`Generic <typing.Generic>` 。如果在基类中包含 ``Generic[...]``，则应列出所有其他基类中存在的类型变量（或更多，如果需要）。类型参数的顺序由以下规则定义：

* 如果存在 ``Generic[...]``，则参数的顺序始终由 ``Generic[...]`` 中的顺序决定。
* 如果基类中没有 ``Generic[...]``，则所有类型参数按字典序收集（即按首次出现顺序）。

示例：

.. code-block:: python

   from typing import Generic, TypeVar, Any

   T = TypeVar('T')
   S = TypeVar('S')
   U = TypeVar('U')

   class One(Generic[T]): ...
   class Another(Generic[T]): ...

   class First(One[T], Another[S]): ...
   class Second(One[T], Another[S], Generic[S, U, T]): ...

   x: First[int, str]        # 这里 T 绑定到 int，S 绑定到 str
   y: Second[int, str, Any]  # 这里 T 是 Any，S 是 int，U 是 str

使用 Python 3.12 语法时，所有类型参数必须始终在类名后立即在 ``[...]`` 中显式定义，并且从不使用 ``Generic[...]`` 基类。

.. _generic-functions:

泛型函数(functions)
***********************

函数也可以是泛型的，即它们可以具有类型参数（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Sequence

   # 一个泛型函数!
   def first[T](seq: Sequence[T]) -> T:
       return seq[0]

以下是使用遗留语法的相同示例（Python 3.11 及更早版本）：

.. code-block:: python

   from typing import TypeVar, Sequence

   T = TypeVar('T')

   # 一个泛型函数!
   def first(seq: Sequence[T]) -> T:
       return seq[0]

与泛型类一样，类型参数 ``T`` 可以替换为任何类型。这意味着 ``first`` 可以接受任何序列类型的参数，返回类型则根据序列项的类型推导。示例：

.. code-block:: python

   reveal_type(first([1, 2, 3]))   # 显示的类型是 "builtins.int"
   reveal_type(first(('a', 'b')))  # 显示的类型是 "builtins.str"

在使用遗留语法时，类型变量的单个定义（例如上面的 ``T`` )可以在多个泛型函数或类中使用。在这个示例中，我们在两个泛型函数中使用相同的类型变量来声明类型参数：

.. code-block:: python

   from typing import TypeVar, Sequence

   T = TypeVar('T')      # 定义类型变量

   def first(seq: Sequence[T]) -> T:
       return seq[0]

   def last(seq: Sequence[T]) -> T:
       return seq[-1]

由于 Python 3.12 语法更简洁，它不需要（也没有）共享类型参数定义的等效方式。

一个变量的类型不能包含类型变量，除非该类型变量在包含的泛型类或函数中被绑定。

在调用泛型函数时，您不能显式地将类型参数的值作为类型参数传递。类型参数的值总是由 mypy 推断。这是无效的：

.. code-block:: python

    first[int]([1, 2])  # 错误：无法在泛型函数中使用 [...] 

如果您确实需要这个功能，可以定义一个带有 ``__call__`` 方法的泛型类。

.. _type-variable-upper-bound:

具有上界的类型变量(Type variables)
****************************************

类型变量还可以限制为具有特定类型的子类型的值。该类型称为类型变量的上界，并在使用 Python 3.12 语法时通过 ``T: <bound>`` 指定。在使用此类型变量 ``T`` 的泛型函数或泛型类的定义中，表示 ``T`` 的类型被假定为其上界的子类型，因此您可以在类型为 ``T`` 的值上使用上界的方法（Python 3.12 语法）：

.. code-block:: python

   from typing import SupportsAbs

   def max_by_abs[T: SupportsAbs[float]](*xs: T) -> T:
       # 我们可以使用 abs()，因为 T 是 SupportsAbs[float] 的子类型。
       return max(xs, key=abs)

上界也可以通过向 :py:class:`~typing.TypeVar` 使用 ``bound=...`` 关键字参数来指定。
以下是使用遗留语法的示例（Python 3.11 及更早版本）：

.. code-block:: python

   from typing import TypeVar, SupportsAbs

   T = TypeVar('T', bound=SupportsAbs[float])

   def max_by_abs(*xs: T) -> T:
       return max(xs, key=abs)

在对这样的函数的调用中，类型 ``T`` 必须被替换为其上界的子类型。继续上述示例：

.. code-block:: python

   max_by_abs(-3.5, 2)   # 正确，类型为 'float'
   max_by_abs(5+6j, 7)   # 正确，类型为 'complex'
   max_by_abs('a', 'b')  # 错误：'str' 不是 SupportsAbs[float] 的子类型

泛型类的类型参数(Type parameters)也可以具有上界，这以相同的方式限制类型参数的有效值。

.. _generic-methods-and-generic-self:

泛型方法和泛型 self
********************************

您还可以定义泛型方法。特别是， ``self`` 参数也可以是泛型的，从而允许方法在访问时返回已知的最精确类型。这样，您可以对一系列设置方法进行类型检查（Python 3.12 语法）：

.. code-block:: python

   class Shape:
       def set_scale[T: Shape](self: T, scale: float) -> T:
           self.scale = scale
           return self

   class Circle(Shape):
       def set_radius(self, r: float) -> 'Circle':
           self.radius = r
           return self

   class Square(Shape):
       def set_width(self, w: float) -> 'Square':
           self.width = w
           return self

   circle: Circle = Circle().set_scale(0.5).set_radius(2.7)
   square: Square = Square().set_scale(0.5).set_width(3.2)

如果不使用泛型 ``self``，最后两行将无法正确进行类型检查，因为 ``set_scale`` 的返回类型将是 ``Shape``，而 ``Shape`` 并未定义 ``set_radius`` 或 ``set_width``。

在使用遗留语法时，只需在方法签名中使用一个不同于 类类型参数(class type parameters)（如果定义了）的类型变量。以下是使用遗留语法的示例（3.11 及更早版本）：

.. code-block:: python

   from typing import TypeVar

   T = TypeVar('T', bound='Shape')

   class Shape:
       def set_scale(self: T, scale: float) -> T:
           self.scale = scale
           return self

   class Circle(Shape):
       def set_radius(self, r: float) -> 'Circle':
           self.radius = r
           return self

   class Square(Shape):
       def set_width(self, w: float) -> 'Square':
           self.width = w
           return self

   circle: Circle = Circle().set_scale(0.5).set_radius(2.7)
   square: Square = Square().set_scale(0.5).set_width(3.2)

其他用法包括工厂方法，例如复制和反序列化方法。对于类方法，您还可以定义泛型 ``cls`` ，使用 ``type[T]`` 或 :py:class:`Type[T] <typing.Type>` （Python 3.12 语法）：

.. code-block:: python

   class Friend:
       other: "Friend | None" = None

       @classmethod
       def make_pair[T: Friend](cls: type[T]) -> tuple[T, T]:
           a, b = cls(), cls()
           a.other = b
           b.other = a
           return a, b

   class SuperFriend(Friend):
       pass

   a, b = SuperFriend.make_pair()

以下是使用遗留语法的相同示例（3.11 及更早版本）：

.. code-block:: python

   from typing import TypeVar

   T = TypeVar('T', bound='Friend')

   class Friend:
       other: "Friend | None" = None

       @classmethod
       def make_pair(cls: type[T]) -> tuple[T, T]:
           a, b = cls(), cls()
           a.other = b
           b.other = a
           return a, b

   class SuperFriend(Friend):
       pass

   a, b = SuperFriend.make_pair()

请注意，当重写具有泛型 ``self`` 的方法时，您必须返回一个泛型 ``self``，或者返回当前类的实例。在后一种情况下，您必须在所有未来的子类中实现此方法。

还要注意，mypy 并不总是能够验证复制或反序列化方法的实现是否返回实际的 self 类型。因此，您可能需要在这些方法内部使 mypy 静默（而不是在调用位置），可能通过使用 ``Any`` 类型或 ``# type: ignore`` 注释。

为了支持常见习惯用法，mypy 允许您以某些不安全的方式使用泛型 self 类型。例如，在参数类型中使用泛型 self 类型是被接受的，即使这不安全（Python 3.12 语法）：

.. code-block:: python

   class Base:
       def compare[T: Base](self: T, other: T) -> bool:
           return False

   class Sub(Base):
       def __init__(self, x: int) -> None:
           self.x = x

       # 这是不安全的（见下文），但允许是因为它是一种常见模式，并且在实践中很少导致问题。
       def compare(self, other: 'Sub') -> bool:
           return self.x > other.x

   b: Base = Sub(42)
   b.compare(Base())  # 运行时错误：'Base' 对象没有属性 'x'

有关 self 类型的某些高级用法，请参见 :ref:`其他示例 <advanced_self>`。

使用 typing.Self 自动注解 self 类型
**************************************

由于上述模式相当常见，mypy 支持了一种更简单的语法，这在 :pep:`673` 中引入，旨在使它们更易于使用。您可以导入特殊类型 ``typing.Self`` ，它会自动转换为具有当前类作为上界的方法级类型参数，并且您无需为 ``self`` (或类方法中的 ``cls`` )提供显式注解。使用 ``Self`` 可以简化前一节中的示例：

.. code-block:: python

   from typing import Self

   class Friend:
       other: Self | None = None

       @classmethod
       def make_pair(cls) -> tuple[Self, Self]:
           a, b = cls(), cls()
           a.other = b
           b.other = a
           return a, b

   class SuperFriend(Friend):
       pass

   a, b = SuperFriend.make_pair()

这种方式比使用显式类型参数更简洁。此外，您可以在属性注解中使用 ``Self`` ，而不仅仅是在方法中。

.. note::

   要在 Python 3.11 之前的版本中使用此功能，您需要从 `typing_extensions` 中导入 ``Self`` （版本 4.0 或更高）。

.. _variance-of-generics:

泛型类型的变体(Variance)
*************************

在子类型关系中，有三种主要的泛型类型：不变(invariant)、协变(covariant)和逆变(contravariant)。假设我们有一对类型 ``A`` 和 ``B``，其中 ``B`` 是 ``A`` 的子类型，定义如下：

* 如果对于泛型类 ``MyCovGen[T]``，``MyCovGen[B]`` 总是为 ``MyCovGen[A]`` 的子类型，则称 ``MyCovGen[T]`` 在类型变量 ``T`` 上是协变(covariant)的。
* 如果对于泛型类 ``MyContraGen[T]``，``MyContraGen[A]`` 总是为 ``MyContraGen[B]`` 的子类型，则称 ``MyContraGen[T]`` 在类型变量 ``T`` 上是逆变(contravariant)的。
* 如果对于泛型类 ``MyInvGen[T]`` 以上都不成立，则称其在 ``T`` 上是不变(invariant)的。

以下是一些简单的示例：

.. code-block:: python

    # 我们将在下面的示例中使用这些类
    class Shape: ...
    class Triangle(Shape): ...
    class Square(Shape): ...

* 大多数不可变容器类型，例如 :py:class:`~collections.abc.Sequence` 和 :py:class:`~frozenset` 是协变的。联合类型在所有联合项中也是协变的： ``Triangle | int`` 是 ``Shape | int`` 的子类型。

  .. code-block:: python

    def count_lines(shapes: Sequence[Shape]) -> int:
        return sum(shape.num_sides for shape in shapes)

    triangles: Sequence[Triangle]
    count_lines(triangles)  # OK

    def foo(triangle: Triangle, num: int) -> None:
        shape_or_number: Union[Shape, int]
        # Triangle 是 Shape，而 Shape 是有效的 Union[Shape, int]
        shape_or_number = triangle

  协变的概念相对直观，但逆变和不变可能更难以理解。

* :py:class:`~collections.abc.Callable` 是一个在参数类型上表现为逆变的类型示例。也就是说， ``Callable[[Shape], int]`` 是 ``Callable[[Triangle], int]`` 的子类型，尽管 ``Shape`` 是 ``Triangle`` 的超类型。要理解这一点，请考虑：

  .. code-block:: python

    def cost_of_paint_required(
        triangle: Triangle,
        area_calculator: Callable[[Triangle], float]
    ) -> float:
        return area_calculator(triangle) * DOLLAR_PER_SQ_FT

    # 这正常工作
    def area_of_triangle(triangle: Triangle) -> float: ...
    cost_of_paint_required(triangle, area_of_triangle)  # OK

    # 但这也可以工作!
    def area_of_any_shape(shape: Shape) -> float: ...
    cost_of_paint_required(triangle, area_of_any_shape)  # OK

  ``cost_of_paint_required`` 需要一个可以计算三角形面积的可调用对象。如果我们给它一个可以计算任意形状（不仅仅是三角形）面积的可调用对象，依然可以正常工作。

* ``list`` 是一种不变的泛型类型。直观地看，它似乎应该是协变的，就像上面的 :py:class:`~collections.abc.Sequence`，但请考虑以下代码：

  .. code-block:: python

     class Circle(Shape):
         # rotate 方法仅在 Circle 中定义，而不在 Shape 中
         def rotate(self): ...

     def add_one(things: list[Shape]) -> None:
         things.append(Shape())

     my_circles: list[Circle] = []
     add_one(my_circles)     # 这似乎是安全的，但...
     my_circles[-1].rotate()  # ...这将失败，因为 my_circles[0] 现在是 Shape，而不是 Circle

  另一个不变类型的示例是 ``dict``。大多数可变容器都是不变的。

在使用 Python 3.12 语法进行泛型时，mypy 会自动推断每个 类类型变量(class type variable) 的最灵活变体(variance)。在此， ``Box`` 将被推断为协变：

.. code-block:: python

   class Box[T]:  # 此类型隐式为协变
       def __init__(self, content: T) -> None:
           self._content = content

       def get_content(self) -> T:
           return self._content

   def look_into(box: Box[Shape]): ...

   my_box = Box(Square())
   look_into(my_box)  # OK，但如果是不可变类型，mypy 会抱怨

这里， ``_content`` 的下划线前缀很重要。如果没有下划线前缀，该类将是不可变的，因为该属性将被理解为公共的、可变的属性（在其他上下文中，单个下划线前缀对 mypy 没有特殊意义）。通过将属性声明为 ``Final``，该类仍然可以被声明为协变：

.. code-block:: python

   from typing import Final

   class Box[T]:  # 此类型隐式为协变
       def __init__(self, content: T) -> None:
           self.content: Final = content

       def get_content(self) -> T:
           return self._content

在使用遗留语法时，mypy 默认假定所有用户定义的泛型都是不变的。要将某个泛型类声明为协变或逆变，可以使用具有特殊关键字参数 ``covariant`` 或 ``contravariant`` 定义的类型变量。例如（Python 3.11 或更早版本）：

.. code-block:: python

   from typing import Generic, TypeVar

   T_co = TypeVar('T_co', covariant=True)

   class Box(Generic[T_co]):  # 此类型被声明为协变
       def __init__(self, content: T_co) -> None:
           self._content = content

       def get_content(self) -> T_co:
           return self._content

   def look_into(box: Box[Shape]): ...

   my_box = Box(Square())
   look_into(my_box)  # OK，但如果是不可变类型，mypy 会抱怨

.. _type-variable-value-restriction:

带值限制的类型变量(Type variables)
*************************************

默认情况下，类型变量可以替换为任何类型，或者任何其上界的子类型，默认上界为 ``object``。然而，有时需要一个只能具有某些特定类型值的类型变量。典型的例子是只能具有 ``str`` 和 ``bytes`` 值的类型变量。这允许我们定义一个可以连接两个字符串或字节对象的函数，但不能用其他类型的参数调用（Python 3.12 语法）：

.. code-block:: python

   def concat[S: (str, bytes)](x: S, y: S) -> S:
       return x + y

   concat('a', 'b')    # 正确
   concat(b'a', b'b')  # 正确
   concat(1, 2)        # 错误!

使用遗留语法（Python 3.11 或更早版本）也可以实现相同的功能：

.. code-block:: python

   from typing import TypeVar

   AnyStr = TypeVar('AnyStr', str, bytes)

   def concat(x: AnyStr, y: AnyStr) -> AnyStr:
       return x + y

无论使用哪种语法，这种类型变量称为具有值限制的类型变量。重要的是，这与联合类型不同，因为不接受 ``str`` 和 ``bytes`` 的组合：

.. code-block:: python

   concat('string', b'bytes')   # 错误!

在这种情况下，这正是我们想要的，因为无法连接字符串和字节对象!如果尝试使用联合类型，类型检查器将抱怨这种可能性：

.. code-block:: python

   def union_concat(x: str | bytes, y: str | bytes) -> str | bytes:
       return x + y  # 错误：无法连接 str 和 bytes

另一个有趣的特例是用 ``str`` 的子类型调用 ``concat()``：

.. code-block:: python

    class S(str): pass

    ss = concat(S('foo'), S('bar'))
    reveal_type(ss)  # 显示的类型是 "builtins.str"

你可能会期望 ``ss`` 的类型是 ``S``，但实际上类型是 ``str``：子类型被提升为类型变量的有效值，在这种情况下是 ``str``。

因此，这与使用 ``str | bytes`` 作为上界有所不同，在那种情况下返回类型将是 ``S`` (见：:ref:`type-variable-upper-bound` ）。使用值限制对 ``concat`` 是正确的，因为 ``concat`` 在上面的示例中实际上返回一个 ``str`` 实例：

.. code-block:: python

    >>> print(type(ss))
    <class 'str'>

在定义泛型类时，你也可以使用具有限制值集的类型变量。例如，类型 :py:class:`Pattern[S] <typing.Pattern>` 用于 :py:func:`re.compile` 的返回值，其中 ``S`` 可以是 ``str`` 或 ``bytes``。正则表达式可以基于字符串或字节模式。

注意，类型变量不能同时具有值限制和上界。

你可能会遇到从 :py:mod:`typing` 导入的 :py:data:`~typing.AnyStr` 。这个特性现在已被弃用，但其含义与我们上面的 ``AnyStr`` 定义相同。

.. _declaring-decorators:

声明装饰器(decorators)
*************************

装饰器通常是接受一个函数作为参数并返回另一个函数的函数。用类型描述这种行为可能有点棘手；我们可以使用类型变量和一种称为 *参数规范(parameter specification)* 的特殊类型变量来实现。

假设我们有以下未注解的装饰器，它保留原始函数的签名，并简单打印被装饰函数的名称：

.. code-block:: python

   def printing_decorator(func):
       def wrapper(*args, **kwds):
           print("Calling", func)
           return func(*args, **kwds)
       return wrapper

我们可以用它来装饰函数 ``add_forty_two``:

.. code-block:: python

   @printing_decorator
   def add_forty_two(value: int) -> int:
       return value + 42

由于 ``printing_decorator`` 没有类型注解，以下代码将不会进行类型检查：

.. code-block:: python

   reveal_type(a)        # 显示的类型是 "Any"
   add_forty_two('foo')  # 没有类型检查错误 :(

这是一个糟糕的状态!如果使用 ``--strict``，mypy 甚至会提醒你这一点：
``Untyped decorator makes function "add_forty_two" untyped``

对于类装饰器，mypy 处理方式不同：装饰类不会抹去其类型，即使装饰器的类型注解不完整。

下面是如何注解装饰器（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Callable
   from typing import Any, cast

   def printing_decorator[F: Callable[..., Any]](func: F) -> F:
       def wrapper(*args, **kwds):
           print("Calling", func)
           return func(*args, **kwds)
       return cast(F, wrapper)

使用遗留语法（Python 3.11 或更早版本）的例子如下：

.. code-block:: python

   from collections.abc import Callable
   from typing import Any, TypeVar, cast

   F = TypeVar('F', bound=Callable[..., Any])

   def printing_decorator(func: F) -> F:
       def wrapper(*args, **kwds):
           print("Calling", func)
           return func(*args, **kwds)
       return cast(F, wrapper)

这仍然存在一些不足之处。首先，我们需要使用不安全的 :py:func:`~typing.cast` 来说服 mypy ``wrapper()`` 具有与 ``func`` 相同的签名 (见 :ref:`casts <casts>`)。

其次，``wrapper()`` 函数的类型检查不够严格，尽管包装函数通常足够小，这不是一个大问题。这也是 ``printing_decorator()`` 中 ``return`` 语句需要调用 :py:func:`~typing.cast` 的原因。

然而，我们可以使用参数规范，使用 ``**P`` 来实现更准确的类型注解（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Callable

   def printing_decorator[**P, T](func: Callable[P, T]) -> Callable[P, T]:
       def wrapper(*args: P.args, **kwds: P.kwargs) -> T:
           print("Calling", func)
           return func(*args, **kwds)
       return wrapper

使用 :py:class:`~typing.ParamSpec` 遗留语法（Python 3.11 或更早版本）的例子如下：

.. code-block:: python

   from collections.abc import Callable
   from typing import TypeVar
   from typing_extensions import ParamSpec

   P = ParamSpec('P')
   T = TypeVar('T')

   def printing_decorator(func: Callable[P, T]) -> Callable[P, T]:
       def wrapper(*args: P.args, **kwds: P.kwargs) -> T:
           print("Calling", func)
           return func(*args, **kwds)
       return wrapper

参数规范还允许你描述修改输入函数签名的装饰器（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Callable

   def stringify[**P, T](func: Callable[P, T]) -> Callable[P, str]:
       def wrapper(*args: P.args, **kwds: P.kwargs) -> str:
           return str(func(*args, **kwds))
       return wrapper

    @stringify
    def add_forty_two(value: int) -> int:
        return value + 42

    a = add_forty_two(3)
    reveal_type(a)      # 显示的类型是 "builtins.str"
    add_forty_two('x')  # 错误：参数 1 的类型不兼容 "str"，期望 "int"

使用遗留语法的同样例子（Python 3.11 或更早版本）：

.. code-block:: python

   from collections.abc import Callable
   from typing import TypeVar
   from typing_extensions import ParamSpec

   P = ParamSpec('P')
   T = TypeVar('T')

   def stringify(func: Callable[P, T]) -> Callable[P, str]:
       def wrapper(*args: P.args, **kwds: P.kwargs) -> str:
           return str(func(*args, **kwds))
       return wrapper

你还可以在装饰器中插入一个参数（Python 3.12 语法）：

.. code-block:: python

    from collections.abc import Callable
    from typing import Concatenate

    def printing_decorator[**P, T](func: Callable[P, T]) -> Callable[Concatenate[str, P], T]:
        def wrapper(msg: str, /, *args: P.args, **kwds: P.kwargs) -> T:
            print("Calling", func, "with", msg)
            return func(*args, **kwds)
        return wrapper

    @printing_decorator
    def add_forty_two(value: int) -> int:
        return value + 42

    a = add_forty_two('three', 3)

使用遗留语法的同样函数（Python 3.11 或更早版本）：

.. code-block:: python

    from collections.abc import Callable
    from typing import TypeVar
    from typing_extensions import Concatenate, ParamSpec

    P = ParamSpec('P')
    T = TypeVar('T')

    def printing_decorator(func: Callable[P, T]) -> Callable[Concatenate[str, P], T]:
        def wrapper(msg: str, /, *args: P.args, **kwds: P.kwargs) -> T:
            print("Calling", func, "with", msg)
            return func(*args, **kwds)
        return wrapper

.. _decorator-factories:

装饰器工厂(factories)
------------------------

接受参数并返回装饰器的函数（也称为二阶装饰器）同样可以通过泛型来支持（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Callable
   from typing import Any

   def route[F: Callable[..., Any]](url: str) -> Callable[[F], F]:
       ...

   @route(url='/')
   def index(request: Any) -> str:
       return 'Hello world'

注意，mypy 推断 ``F`` 被用来使 ``route`` 的返回值成为泛型，而不是使 ``route`` 本身成为泛型，因为 ``F`` 仅用于返回类型。Python 没有显式的语法来标记 ``F`` 仅在返回值中绑定。

使用遗留语法（Python 3.11 或更早版本）的示例如下：

.. code-block:: python

   from collections.abc import Callable
   from typing import Any, TypeVar

   F = TypeVar('F', bound=Callable[..., Any])

   def route(url: str) -> Callable[[F], F]:
       ...

   @route(url='/')
   def index(request: Any) -> str:
       return 'Hello world'

有时同一装饰器支持裸调用和带参数的调用。这可以通过结合使用 :py:func:`@overload <typing.overload>` 来实现（Python 3.12 语法）：

.. code-block:: python

   from collections.abc import Callable
   from typing import Any, overload

   # 裸装饰器使用
   @overload
   def atomic[F: Callable[..., Any]](func: F, /) -> F: ...
   # 带参数的装饰器
   @overload
   def atomic[F: Callable[..., Any]](*, savepoint: bool = True) -> Callable[[F], F]: ...

   # 实现
   def atomic(func: Callable[..., Any] | None = None, /, *, savepoint: bool = True):
       def decorator(func: Callable[..., Any]):
           ...  # 代码在此处
       if func is not None:
           return decorator(func)
       else:
           return decorator

使用遗留语法的同样装饰器示例（Python 3.11 或更早版本）：

.. code-block:: python

   from collections.abc import Callable
   from typing import Any, Optional, TypeVar, overload

   F = TypeVar('F', bound=Callable[..., Any])

   # 裸装饰器使用
   @overload
   def atomic(func: F, /) -> F: ...
   # 带参数的装饰器
   @overload
   def atomic(*, savepoint: bool = True) -> Callable[[F], F]: ...

   # 实现
   def atomic(func: Optional[Callable[..., Any]] = None, /, *, savepoint: bool = True):
       ...  # 与上面相同

泛型协议(protocols)
**********************

Mypy 支持泛型协议（参见 :ref:`protocol-types`）。多个 :ref:`预定义协议 <predefined_protocols>` 是泛型的，例如 :py:class:`Iterable[T] <collections.abc.Iterable>`，您可以定义其他泛型协议。泛型协议主要遵循泛型类的常规规则。示例（Python 3.12 语法）：

.. code-block:: python

   from typing import Protocol

   class Box[T](Protocol):
       content: T

   def do_stuff(one: Box[str], other: Box[bytes]) -> None:
       ...

   class StringWrapper:
       def __init__(self, content: str) -> None:
           self.content = content

   class BytesWrapper:
       def __init__(self, content: bytes) -> None:
           self.content = content

   do_stuff(StringWrapper('one'), BytesWrapper(b'other'))  # OK

   x: Box[float] = ...
   y: Box[int] = ...
   x = y  # 错误 -- Box 是不变的

使用遗留语法（Python 3.11 或更早版本）定义 ``Box`` 的示例如下：

.. code-block:: python

   from typing import Protocol, TypeVar

   T = TypeVar('T')

   class Box(Protocol[T]):
       content: T

请注意，在使用遗留语法时， ``class ClassName(Protocol[T])`` 被允许作为 ``class ClassName(Protocol, Generic[T])`` 的简写，这符合 :pep:`PEP 544: Generic protocols <544#generic-protocols>`。此形式仅在使用遗留语法时有效。

使用遗留语法时，泛型协议与普通泛型类之间有一个重要区别：mypy 检查协议中声明的泛型类型变量的变异性是否与其在协议定义中的使用方式匹配。以下示例中的协议被拒绝，因为类型变量 ``T`` 在返回类型中协变使用，但该类型变量是不变的：

.. code-block:: python

   from typing import Protocol, TypeVar

   T = TypeVar('T')

   class ReadOnlyBox(Protocol[T]):  # 错误: 不变的类型变量 "T" 在期望协变的协议中使用
       def content(self) -> T: ...

以下示例正确使用了协变类型变量：

.. code-block:: python

   from typing import Protocol, TypeVar

   T_co = TypeVar('T_co', covariant=True)

   class ReadOnlyBox(Protocol[T_co]):  # OK
       def content(self) -> T_co: ...

   ax: ReadOnlyBox[float] = ...
   ay: ReadOnlyBox[int] = ...
   ax = ay  # OK -- ReadOnlyBox 是协变的

有关比变体(variance)方面的更多信息，请参见 :ref:`variance-of-generics`。

泛型协议也可以是递归的。示例（Python 3.12 语法）：

.. code-block:: python

   class Linked[T](Protocol):
       val: T
       def next(self) -> 'Linked[T]': ...

   class L:
       val: int
       def next(self) -> 'L': ...

   def last(seq: Linked[T]) -> T: ...

   result = last(L())
   reveal_type(result)  # 显示类型为 "builtins.int"

使用遗留语法（Python 3.11 或更早版本）定义 ``Linked`` 的示例如下：

.. code-block:: python

   from typing import TypeVar

   T = TypeVar('T')

   class Linked(Protocol[T]):
       val: T
       def next(self) -> 'Linked[T]': ...

.. _generic-type-aliases:

泛型类型别名(aliases)
**************************

类型别名(Type aliases)可以是泛型的。在这种情况下，它们可以以两种方式使用。首先，带下标的别名等同于替换类型变量的原始类型。其次，不带下标的别名被视为原始类型，其中类型参数被替换为 ``Any``。

在 Python 3.12 中，引入的 ``type`` 语句用于定义泛型类型别名（它还支持非泛型类型别名）：

.. code-block:: python

    from collections.abc import Callable, Iterable

    type TInt[S] = tuple[int, S]
    type UInt[S] = S | int
    type CBack[S] = Callable[..., S]

    def response(query: str) -> UInt[str]:  # 同样等于 str | int
        ...
    def activate[S](cb: CBack[S]) -> S:        # 同样等于 Callable[..., S]
        ...
    table_entry: TInt  # 同样等于 tuple[int, Any]

    type Vec[T: (int, float, complex)] = Iterable[tuple[T, T]]

    def inproduct[T: (int, float, complex)](v: Vec[T]) -> T:
        return sum(x*y for x, y in v)

    def dilate[T: (int, float, complex)](v: Vec[T], scale: T) -> Vec[T]:
        return ((x * scale, y * scale) for x, y in v)

    v1: Vec[int] = []      # 同样等于 Iterable[tuple[int, int]]
    v2: Vec = []           # 同样等于 Iterable[tuple[Any, Any]]
    v3: Vec[int, int] = [] # 错误: 无效的别名，类型参数过多!

还有一种遗留语法，依赖于 ``TypeVar``。在这里，类型参数的数量必须与泛型类型别名定义中的自由类型变量数量匹配。自由类型变量是指不属于周围类或函数的类型参数。例如（遵循 :pep:`PEP 484: Type aliases <484#type-aliases>`，Python 3.11 及更早版本）：

.. code-block:: python

    from typing import TypeVar, Iterable, Union, Callable

    S = TypeVar('S')

    TInt = tuple[int, S]  # 1 个类型参数，因为只有 S 是自由的
    UInt = Union[S, int]
    CBack = Callable[..., S]

    def response(query: str) -> UInt[str]:  # 同样等于 Union[str, int]
        ...
    def activate(cb: CBack[S]) -> S:        # 同样等于 Callable[..., S]
        ...
    table_entry: TInt  # 同样等于 tuple[int, Any]

    T = TypeVar('T', int, float, complex)

    Vec = Iterable[tuple[T, T]]

    def inproduct(v: Vec[T]) -> T:
        return sum(x*y for x, y in v)

    def dilate(v: Vec[T], scale: T) -> Vec[T]:
        return ((x * scale, y * scale) for x, y in v)

    v1: Vec[int] = []      # 同样等于 Iterable[tuple[int, int]]
    v2: Vec = []           # 同样等于 Iterable[tuple[Any, Any]]
    v3: Vec[int, int] = [] # 错误: 无效的别名，类型参数过多!

类型别名可以像其他名称一样从模块中导入。一个别名还可以指向另一个别名，尽管不建议构建复杂的别名链，因为这会影响代码的可读性，从而削弱使用别名的目的。示例（Python 3.12 语法）：

.. code-block:: python

    from example1 import AliasType
    from example2 import Vec

    # AliasType 和 Vec 是类型别名（上面定义的 Vec）

    def fun() -> AliasType:
        ...

    type OIntVec = Vec[int] | None

使用 ``type`` 语句定义的类型别名不能作为基类，也不能用于构造实例：

.. code-block:: python

    from example1 import AliasType
    from example2 import Vec

    # AliasType 和 Vec 是类型别名（上面定义的 Vec）

    class NewVec[T](Vec[T]):  # 错误: 不能作为基类
        ...

    x = AliasType()  # 错误: 不能用于创建实例

以下是使用遗留语法（Python 3.11 及更早版本）的示例：

.. code-block:: python

    from typing import TypeVar, Generic, Optional
    from example1 import AliasType
    from example2 import Vec

    # AliasType 和 Vec 是类型别名（上面定义的 Vec）

    def fun() -> AliasType:
        ...

    OIntVec = Optional[Vec[int]]

    T = TypeVar('T')

    # 旧式类型别名可以用作基类，您可以使用它们构造实例

    class NewVec(Vec[T]):
        ...

    x = AliasType()

    for i, j in NewVec[int]():
        ...

在泛型别名中使用类型变量的边界或值限制与在泛型类和函数中的效果相同。


新旧语法之间的差异(Differences)
******************************************

在泛型类、函数和类型别名的新语法（Python 3.12 及更高版本）和旧语法之间，除了明显的语法差异外，还有一些显著的区别：

* **类型变量定义的作用域**：使用旧语法定义的类型变量会在周围的命名空间中创建运行时定义，而使用新语法定义的类型变量仅在使用它们的类、函数或类型变量内定义。

* **类型变量的共享**：在使用旧语法时，类型变量的定义可以被共享，但新语法不支持这一点。

* **类型变量的变异性推断**：使用新语法时，类类型变量的变异性总是被推断。

* **前向引用和递归引用**：使用新语法定义的类型别名可以包含前向引用和递归引用，而无需使用字符串文字转义。类型变量的边界和约束也是如此。

* **条件定义类型别名**：新语法允许定义一个泛型别名，其中定义不包含对类型参数的引用。这在条件定义类型别名时偶尔会有用。

* **作为基类和实例化的限制**：使用新语法定义的类型别名不能用作基类，也不能用于构造实例，而使用旧语法定义的别名则可以。


泛型类的内部机制(internals)
*****************************

你可能想知道在运行时索引一个泛型类时会发生什么。索引返回一个 *泛型别名(generic alias)* ，该别名指向原始类，并在实例化时返回原始类的实例（Python 3.12 语法）：

.. code-block:: python

   >>> class Stack[T]: ...
   >>> Stack
   __main__.Stack
   >>> Stack[int]
   __main__.Stack[int]
   >>> instance = Stack[int]()
   >>> instance.__class__
   __main__.Stack

以下是使用旧语法（Python 3.11 及更早版本）的相同示例：

.. code-block:: python

   >>> from typing import TypeVar, Generic
   >>> T = TypeVar('T')
   >>> class Stack(Generic[T]): ...
   >>> Stack
   __main__.Stack
   >>> Stack[int]
   __main__.Stack[int]
   >>> instance = Stack[int]()
   >>> instance.__class__
   __main__.Stack

泛型别名可以像真实类一样被实例化或子类化，但上述示例表明类型变量在运行时被擦除。泛型 ``Stack`` 实例只是普通的Python对象，除了 ``Generic`` 基类通过 ``__class_getitem__`` 重载索引运算符外，没有额外的运行时开销或魔法。即使使用新语法， ``typing.Generic`` 也作为隐式基类包含在内：

.. code-block:: python

   >>> class Stack[T]: ...
   >>> Stack.mro()
   [<class '__main__.Stack'>, <class 'typing.Generic'>, <class 'object'>]

需要注意的是，在Python 3.8及之前，内置类型如 :py:class:`list` 、:py:class:`dict` 等不支持索引。这就是为什么我们在 :py:mod:`~typing` 模块中有别名 :py:class:`~typing.List` 、 :py:class:`~typing.Dict` 等。索引这些别名会给你一个泛型别名，其行为类似于在较新版本的Python中通过直接索引目标类构造的泛型别名：

.. code-block:: python

   >>> # 仅适用于Python 3.8及以下
   >>> # 如果使用Python 3.9或更新版本，优先使用'list[int]'语法
   >>> from typing import List
   >>> List[int]
   typing.List[int]


注意， ``typing`` 中的泛型别名不支持实例化，与对应的内置类不同：

.. code-block:: python

   >>> list[int]()
   []
   >>> from typing import List
   >>> List[int]()
   Traceback (most recent call last):
   ...
   TypeError: Type List cannot be instantiated; use list() instead
