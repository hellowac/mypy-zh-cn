字面量类型(Literal types)和枚举(Enums)
=========================================

.. _literal_types:

字面量类型(Literal types)
------------------------------

字面量类型允许你指示一个表达式等于某个特定的原始值。例如，如果我们用类型 ``Literal["foo"]`` 注解一个变量，mypy 会理解这个变量不仅是类型 ``str``，而且特定等于字符串 ``"foo"``。

这个特性主要在注解根据调用者提供的确切值表现不同的函数时很有用。例如，假设我们有一个函数 ``fetch_data(...)``，如果第一个参数为 ``True`` 则返回 ``bytes``，如果为 ``False`` 则返回 ``str``。我们可以使用 ``Literal[...]`` 和重载构造这个函数的精确类型签名：

.. code-block:: python

    from typing import overload, Union, Literal

    # 前两个重载使用 Literal[...] 以便我们可以
    # 拥有精确的返回类型：

    @overload
    def fetch_data(raw: Literal[True]) -> bytes: ...
    @overload
    def fetch_data(raw: Literal[False]) -> str: ...

    # 最后一个重载是一个后备选项，以防调用者
    # 提供一个普通的 bool：

    @overload
    def fetch_data(raw: bool) -> Union[bytes, str]: ...

    def fetch_data(raw: bool) -> Union[bytes, str]:
        # 实现省略
        ...

    reveal_type(fetch_data(True))        # 显示类型为 "bytes"
    reveal_type(fetch_data(False))       # 显示类型为 "str"

    # 未注解的变量将继续具有推断类型 'bool'。

    variable = True
    reveal_type(fetch_data(variable))    # 显示类型为 "Union[bytes, str]"

.. note::

    本页中的示例从 ``typing`` 模块导入 ``Literal``、``Final`` 和
    ``TypedDict``。这些类型在 Python 3.8 中被添加到
    ``typing`` 中，但在 Python 3.4 - 3.7 中也可以通过
    ``typing_extensions`` 包使用。

参数化字面量(Parameterizing)
****************************

字面量类型可以包含一个或多个字面量布尔值、整数、字符串、字节和枚举值。然而，字面量类型 **不能** 包含任意表达式：像 ``Literal[my_string.trim()]``、 ``Literal[x > 3]`` 或 ``Literal[3j + 4]`` 都是非法的。

包含两个或多个值的字面量等价于这些值的并集。因此， ``Literal[-3, b"foo", MyEnum.A]`` 等价于 ``Union[Literal[-3], Literal[b"foo"], Literal[MyEnum.A]]``。这使得编写涉及字面量的更复杂类型变得更方便。

字面量类型还可以包含 ``None``。mypy 会将 ``Literal[None]`` 视为仅仅是 ``None``。这意味着 ``Literal[4, None]``、 ``Literal[4] | None`` 和 ``Optional[Literal[4]]`` 都是等价的。

字面量也可以包含对其他字面量类型的别名。例如，以下程序是合法的：

.. code-block:: python

    PrimaryColors = Literal["red", "blue", "yellow"]
    SecondaryColors = Literal["purple", "green", "orange"]
    AllowedColors = Literal[PrimaryColors, SecondaryColors]

    def paint(color: AllowedColors) -> None: ...

    paint("red")        # 类型检查通过！
    paint("turquoise")  # 类型检查不通过

字面量不能包含其他任何类型或表达式。这意味着 ``Literal[my_instance]``、 ``Literal[Any]``、 ``Literal[3.14]`` 或 ``Literal[{"foo": 2, "bar": 5}]`` 都是非法的。

声明字面量变量(variables)
***************************

您必须显式为变量添加注解，以声明它具有字面量类型：

.. code-block:: python

    a: Literal[19] = 19
    reveal_type(a)          # Revealed type is "Literal[19]"

为了保持向后兼容，没有此注解的变量 **不会** 被视为字面量：

.. code-block:: python

    b = 19
    reveal_type(b)          # Revealed type is "int"

如果您觉得在类型提示中重复变量的值很繁琐，您可以将变量更改为 ``Final`` （参见 :ref:`final_attrs`）：

.. code-block:: python

    from typing import Final, Literal

    def expects_literal(x: Literal[19]) -> None: pass

    c: Final = 19

    reveal_type(c)          # Revealed type is "Literal[19]?"
    expects_literal(c)      # ...and this type checks!

如果您在 ``Final`` 中不提供显式类型，则 ``c`` 的类型变为 *上下文敏感(context-sensitive)* ：mypy 会在执行类型检查之前，尝试在使用时“替换”原始赋值。这就是 ``c`` 的揭示类型为 ``Literal[19]?`` 的原因：末尾的问号反映了这种上下文敏感的特性。

例如，mypy 将几乎像这样类型检查上述程序：

.. code-block:: python

    from typing import Final, Literal

    def expects_literal(x: Literal[19]) -> None: pass

    reveal_type(19)
    expects_literal(19)

这意味着，将变量更改为 ``Final`` 并不完全等同于添加显式的 ``Literal[...]`` 注解，但在实践中常常会导致相同的效果。

上下文敏感类型与真实字面量类型行为差异的主要情况是，当您尝试在未明确期望 ``Literal[...]`` 的地方使用这些类型时。例如，比较和对比在尝试将这些类型追加到列表时发生的情况：

.. code-block:: python

    from typing import Final, Literal

    a: Final = 19
    b: Literal[19] = 19

    # Mypy 在这里会选择推断 list[int]。
    list_of_ints = []
    list_of_ints.append(a)
    reveal_type(list_of_ints)  # Revealed type is "list[int]"

    # 但如果您追加的变量是显式字面量，mypy
    # 会推断为 list[Literal[19]]。
    list_of_lits = []
    list_of_lits.append(b)
    reveal_type(list_of_lits)  # Revealed type is "list[Literal[19]]"


智能索引(indexing)
********************

我们可以使用字面量类型更精确地索引到结构化的异构类型，如元组、命名元组和类型字典。此功能称为 *智能索引(intelligent indexing)*。

例如，当我们使用某个整数索引元组时，推断出的类型通常是元组项类型的并集。然而，如果我们只想获得与某个特定索引对应的类型，可以使用字面量类型，如下所示：

.. code-block:: python

    from typing import TypedDict

    tup = ("foo", 3.4)

    # 使用整数字面量索引给我们该索引的确切类型
    reveal_type(tup[0])  # Revealed type is "str"

    # 但如果我们希望索引是一个变量呢？通常，mypy 不会确切知道索引是什么，因此会返回一个不那么精确的类型：
    int_index = 0
    reveal_type(tup[int_index])  # Revealed type is "Union[str, float]"

    # 但是如果我们使用字面量类型或最终整数，我们可以恢复最初的精度：
    lit_index: Literal[0] = 0
    fin_index: Final = 0
    reveal_type(tup[lit_index])  # Revealed type is "str"
    reveal_type(tup[fin_index])  # Revealed type is "str"

    # 我们也可以对类型字典和字符串键做同样的事情：
    class MyDict(TypedDict):
        name: str
        main_id: int
        backup_id: int

    d: MyDict = {"name": "Saanvi", "main_id": 111, "backup_id": 222}
    name_key: Final = "name"
    reveal_type(d[name_key])  # Revealed type is "str"

    # 您还可以使用字面量的并集进行索引
    id_key: Literal["main_id", "backup_id"]
    reveal_type(d[id_key])    # Revealed type is "int"

.. _tagged_unions:

标记联合(Tagged unions)
**************************

当你有一个类型的联合时，通常可以通过使用 ``isinstance`` 检查来区分联合中的每种类型。例如，如果你有一个类型为 ``Union[int, str]`` 的变量 ``x``，你可以写一些代码，只在 ``x`` 是 int 时运行，如 ``if isinstance(x, int): ...`` 。

然而，并不总是能够或方便这样做。例如，无法使用 ``isinstance`` 来区分两个不同的 TypedDict，因为在运行时，你的变量将只是一个字典。

相反，你可以为你的 TypedDicts *标记(label)* 或 *标签(tag)* 一个独特的字面量类型。然后，你可以通过检查标签来区分每种类型的 TypedDict:

.. code-block:: python

    from typing import Literal, TypedDict, Union

    class NewJobEvent(TypedDict):
        tag: Literal["new-job"]
        job_name: str
        config_file_path: str

    class CancelJobEvent(TypedDict):
        tag: Literal["cancel-job"]
        job_id: int

    Event = Union[NewJobEvent, CancelJobEvent]

    def process_event(event: Event) -> None:
        # 由于我们确保了两个 TypedDict 都有一个名为 'tag' 的键，因此可以安全地使用 'event["tag"]'。
        # 该表达式通常具有类型 Literal["new-job", "cancel-job"]，但下面的检查将把
        # 类型缩小为 Literal["new-job"] 或 Literal["cancel-job"]。
        #
        # 这反过来又将 'event' 的类型缩小为 NewJobEvent 或 CancelJobEvent。
        if event["tag"] == "new-job":
            print(event["job_name"])
        else:
            print(event["job_id"])

虽然此功能在处理 TypedDict 时特别有用，但你也可以使用相同的技术与常规对象、元组或命名元组结合使用。

同样，标签不需要特定为 str 字面量：它们可以是你通常可以在 ``if`` 语句等中缩小的任何类型。例如，你可以将标签设为 int 或 Enum 字面量，甚至是你使用 ``isinstance()`` 缩小的常规类（Python 3.12 语法）：

.. code-block:: python

    class Wrapper[T]:
        def __init__(self, inner: T) -> None:
            self.inner = inner

    def process(w: Wrapper[int] | Wrapper[str]) -> None:
        # 使用 `if isinstance(w, Wrapper[int])` 不起作用：isinstance 要求
        # 第二个参数始终是一个 *擦除* 类型，没有泛型。
        # 这是因为泛型是一个仅用于类型的概念，在运行时并不存在于
        # isinstance 始终可以检查的方式中。
        #
        # 然而，我们可以通过检查 `w.inner` 的类型来缩小 `w` 本身：
        if isinstance(w.inner, int):
            reveal_type(w)  # Revealed type is "Wrapper[int]"
        else:
            reveal_type(w)  # Revealed type is "Wrapper[str]"

此功能在其他编程语言中有时被称为 "和类型(sum types)" 或 "区分联合类型(discriminated union types)"。

穷举检查(Exhaustiveness checking)
******************************************

你可能想检查某段代码是否涵盖了所有可能的 ``Literal`` 或 ``Enum`` 情况。示例：

.. code-block:: python

  from typing import Literal

  PossibleValues = Literal['one', 'two']

  def validate(x: PossibleValues) -> bool:
      if x == 'one':
          return True
      elif x == 'two':
          return False
      raise ValueError(f'Invalid value: {x}')

  assert validate('one') is True
  assert validate('two') is False

在上面的代码中，容易犯错误。你可以
向 ``PossibleValues`` 添加一个新的字面量值，但忘记
在 ``validate`` 函数中处理它：

.. code-block:: python

  PossibleValues = Literal['one', 'two', 'three']

Mypy 不会捕获到 ``'three'`` 没有被涵盖。如果你想让 mypy
执行穷举检查，你需要更新代码以使用
``assert_never()`` 检查：

.. code-block:: python

  from typing import Literal, NoReturn
  from typing_extensions import assert_never

  PossibleValues = Literal['one', 'two']

  def validate(x: PossibleValues) -> bool:
      if x == 'one':
          return True
      elif x == 'two':
          return False
      assert_never(x)

现在，如果你向 ``PossibleValues`` 添加一个新值但不更新 ``validate``
，mypy 会发现错误：

.. code-block:: python

  PossibleValues = Literal['one', 'two', 'three']

  def validate(x: PossibleValues) -> bool:
      if x == 'one':
          return True
      elif x == 'two':
          return False
      # 错误：Argument 1 to "assert_never" has incompatible type "Literal['three']";
      # expected "NoReturn"
      assert_never(x)

如果不需要针对意外值的运行时检查，你可以
在上述示例中省略 ``assert_never`` 调用，mypy
仍然会生成一个关于函数 ``validate`` 未返回值的错误：

.. code-block:: python

  PossibleValues = Literal['one', 'two', 'three']

  # 错误：缺少返回语句
  def validate(x: PossibleValues) -> bool:
      if x == 'one':
          return True
      elif x == 'two':
          return False

穷举检查在匹配语句（Python 3.10 及更高版本）中也受到支持：

.. code-block:: python

  def validate(x: PossibleValues) -> bool:
      match x:
          case 'one':
              return True
          case 'two':
              return False
      assert_never(x)


限制(Limitations)
**********************

Mypy 不会深入理解使用类型为 ``Literal[..]`` 的变量的表达式。例如，如果你有一个类型为 ``Literal[3]`` 的变量 ``a`` 和一个类型为 ``Literal[5]`` 的变量 ``b``，mypy 将推断 ``a + b`` 的类型为 ``int``，**而不是** 类型 ``Literal[8]``。

基本规则是，字面量类型被视为所参数的常规子类型。例如， ``Literal[3]`` 被视为 ``int`` 的子类型，因此会直接继承 ``int`` 的所有方法。这意味着 ``Literal[3].__add__`` 接受与 ``int.__add__`` 相同的参数，并具有相同的返回类型。

枚举(Enums)
--------------

Mypy 对 :py:class:`enum.Enum` 及其子类 :py:class:`enum.IntEnum` 、 :py:class:`enum.Flag` 、 :py:class:`enum.IntFlag` 和 :py:class:`enum.StrEnum` 提供了特殊支持。

.. code-block:: python

  from enum import Enum

  class Direction(Enum):
      up = 'up'
      down = 'down'

  reveal_type(Direction.up)  # Revealed type is "Literal[Direction.up]?"
  reveal_type(Direction.down)  # Revealed type is "Literal[Direction.down]?"

你可以像预期那样使用枚举来注释类型：

.. code-block:: python

  class Movement:
      def __init__(self, direction: Direction, speed: float) -> None:
          self.direction = direction
          self.speed = speed

  Movement(Direction.up, 5.0)  # ok
  Movement('up', 5.0)  # 错误：Argument 1 to "Movement" has incompatible type "str"; expected "Direction"

穷尽性检查(Exhaustiveness checking)
**********************************************

类似于 ``Literal`` 类型， ``Enum`` 也支持穷尽性检查。我们先定义一个枚举：

.. code-block:: python

  from enum import Enum
  from typing import NoReturn
  from typing_extensions import assert_never

  class Direction(Enum):
      up = 'up'
      down = 'down'

现在，让我们使用穷尽性检查：

.. code-block:: python

  def choose_direction(direction: Direction) -> None:
      if direction is Direction.up:
          reveal_type(direction)  # N: Revealed type is "Literal[Direction.up]"
          print('Going up!')
          return
      elif direction is Direction.down:
          print('Down')
          return
      # 这一行永远不会被执行
      assert_never(direction)

如果我们忘记处理某个情况，mypy 会生成错误：

.. code-block:: python

  def choose_direction(direction: Direction) -> None:
      if direction == Direction.up:
          print('Going up!')
          return
      assert_never(direction)  # 错误：Argument 1 to "assert_never" has incompatible type "Direction"; expected "NoReturn"

穷尽性检查在 匹配语句(match statements) 中（Python 3.10 及更高版本）也得到了支持。

枚举的额外检查(Extra)
**********************

Mypy 还尝试以 Python 运行时的方式支持 ``Enum`` 的特殊功能：

- 任何具有值的 ``Enum`` 类都是隐式的 :ref:`final <final_attrs>`。
  这在 CPython 中也是如此：

  .. code-block:: python

    >>> class AllDirection(Direction):
    ...     left = 'left'
    ...     right = 'right'
    Traceback (most recent call last):
      ...
    TypeError: AllDirection: cannot extend enumeration 'Direction'

  Mypy 也会捕捉到这个错误：

  .. code-block:: python

    class AllDirection(Direction):  # 错误：Cannot inherit from final class "Direction"
        left = 'left'
        right = 'right'

- 所有 ``Enum`` 字段也是隐式 ``final`` 。

  .. code-block:: python

    Direction.up = '^'  # 错误：Cannot assign to final attribute "up"

- 所有字段名被检查为唯一。

  .. code-block:: python

     class Some(Enum):
        x = 1
        x = 2  # 错误：Attempted to reuse member name "x" in Enum definition "Some"

- 基类没有冲突，混入类型是正确的。

  .. code-block:: python

    class WrongEnum(str, int, enum.Enum):
        # 错误：Only a single data type mixin is allowed for Enum subtypes, found extra "int"
        ...

    class MixinAfterEnum(enum.Enum, Mixin): # 错误：No base classes are allowed after "enum.Enum"
        ...