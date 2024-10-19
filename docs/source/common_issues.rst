.. _common_issues:


常见问题及解决方案(Common issues and solutions)
======================================================

本节展示了在使用静态类型时需要更新代码的情况，并提供了解决 mypy 不按预期工作的常见问题的思路。静态类型的代码通常与普通的 Python 代码相同（除了类型注解），但有时你需要稍微做些不同的处理。

.. _annotations_needed:

明显错误的代码未报告错误(No errors reported for obviously wrong code)
--------------------------------------------------------------------------------------

有几种常见原因会导致明显错误的代码未被标记为错误。

**包含错误的函数没有添加注解。**

没有任何注解的函数（既没有参数注解，也没有返回类型注解）不会进行类型检查，甚至最明显的类型错误（例如 ``2 + 'a'``）也会静默通过。解决方案是添加注解。如果无法添加注解，可以使用 :option:`--check-untyped-defs <mypy --check-untyped-defs>` 来检查没有注解的函数。

示例：

.. code-block:: python

    def foo(a):
        return '(' + a.split() + ')'  # 无错误！

即使 ``a.split()`` 是一个“显然”的列表（作者可能本意是 ``a.strip()``），但这里不会报错。一旦你添加了注解，错误就会被报告：

.. code-block:: python

    def foo(a: str) -> str:
        return '(' + a.split() + ')'
    # 错误：不支持的操作数类型 + ("str" 和 "list[str]")

如果你不确定该添加什么类型，可以使用 ``Any``，但要小心：

**参与运算的某个值的类型是 'Any'。**

扩展以上示例，如果我们忽略了 ``a`` 的注解，仍不会报错：

.. code-block:: python

    def foo(a) -> str:
        return '(' + a.split() + ')'  # 无错误！

原因是如果 ``a`` 的类型未知，那么 ``a.split()`` 的类型也未知，因此被推断为 ``Any`` 类型，将字符串与 ``Any`` 相加不会报错。

如果你在调试这类情况时遇到问题，:ref:`reveal_type() <reveal-type>` 可能会派上用场。

请注意，有时库存根文件中不精确的类型信息也可能是 ``Any`` 值的来源。

:py:meth:`__init__ <object.__init__>` **方法没有带注解的参数，也没有返回类型注解。**

这基本上是上述两种情况的组合，没有注解的 ``__init__`` 方法可能会导致 ``Any`` 类型泄露到实例变量中：

.. code-block:: python

    class Bad:
        def __init__(self):
            self.value = "asdf"
            1 + "asdf"  # 无错误！

    bad = Bad()
    bad.value + 1           # 无错误！
    reveal_type(bad)        # 显示类型为 "__main__.Bad"
    reveal_type(bad.value)  # 显示类型为 "Any"

    class Good:
        def __init__(self) -> None:  # 明确地返回 None
            self.value = value


**某些导入可能会被静默忽略**。

导致意外 ``Any`` 值的一个常见原因是 :option:`--ignore-missing-imports <mypy --ignore-missing-imports>` 选项。

当你使用 :option:`--ignore-missing-imports <mypy --ignore-missing-imports>` 时，任何找不到的导入模块会被静默替换为 ``Any``。

为了帮助调试，建议不要使用 :option:`--ignore-missing-imports <mypy --ignore-missing-imports>`。正如 :ref:`fix-missing-imports` 中提到的那样，针对每个模块设置 ``ignore_missing_imports=True`` 可以减少意外，强烈建议这样做。

使用 :option:`--follow-imports=skip <mypy --follow-imports>` 选项也可能会导致问题。强烈不建议使用这些选项，除非在相对特殊的情况下。详见 :ref:`follow-imports` 获取更多信息。

**mypy 认为你的一些代码无法到达**。

详见 :ref:`unreachable` 获取更多信息。

**标注为返回非可选类型的函数实际上返回了 'None'，mypy 也没有报错**。

.. code-block:: python

    def foo() -> str:
        return None  # 无错误！

你可能禁用了严格的可选类型检查（详见 :ref:`--no-strict-optional <no_strict_optional>`）。

.. _silencing_checker:

冗余错误与局部静默检查器(Spurious errors and locally silencing the checker)
--------------------------------------------------------------------------------------------------

你可以使用 ``# type: ignore`` 注释来在特定行上静默类型检查器。例如，假设我们的代码使用了 C 扩展模块 ``frobnicate``, 而没有可用的存根。Mypy 将对此抱怨，因为它没有关于该模块的信息：

.. code-block:: python

    import frobnicate  # 错误：没有模块 "frobnicate"
    frobnicate.start()

你可以添加 ``# type: ignore`` 注释来告诉 mypy 忽略此错误：

.. code-block:: python

    import frobnicate  # type: ignore
    frobnicate.start()  # 没问题！

现在第二行是可以的，因为忽略注释使得名称 ``frobnicate`` 获得了隐式 ``Any`` 类型。

.. note::

    你可以使用形式 ``# type: ignore[<code>]`` 仅忽略行上的特定错误。这样你就不太可能静默那些不可安全忽略的意外错误，同时这也会记录注释的目的。有关更多信息，请参见 :ref:`error-codes`。

.. note::

    只有在 mypy 无法找到关于特定模块的信息时，``# type: ignore`` 注释才会将隐式 ``Any`` 类型分配给该名称。因此，如果我们确实有 ``frobnicate`` 的存根可用，那么 mypy 将忽略 ``# type: ignore`` 注释，并像往常一样对存根进行类型检查。

另一种选择是显式将值标注为类型 ``Any`` -- mypy 允许你对 ``Any`` 值执行任意操作。有时对于特定值没有更精确的类型可以使用，尤其是当你使用动态 Python 特性时，例如 :py:meth:`__getattr__ <object.__getattr__>`：

.. code-block:: python

   class Wrapper:
       ...
       def __getattr__(self, a: str) -> Any:
           return getattr(self._wrapped, a)

最后，你可以为生成冗余错误的文件创建一个存根文件（``.pyi``）。Mypy 只会查看存根文件并忽略实现，因为存根文件优先于 ``.py`` 文件。

忽略整个文件(Ignoring a whole file)
------------------------------------------

* 若要仅忽略错误，请使用顶级 ``# mypy: ignore-errors`` 注释。
* 若要仅忽略具有特定错误代码的错误，请使用顶级 ``# mypy: disable-error-code="..."`` 注释。例如：``# mypy: disable-error-code="truthy-bool, ignore-without-code"``。
* 若要用 ``Any`` 替换模块的内容，请使用每个模块的 ``follow_imports = skip``。有关详细信息，请参见 :ref:`Following imports <follow-imports>`。

请注意，在模块顶部（在任何语句之前，包括导入或文档字符串之前）添加 ``# type: ignore`` 注释会导致忽略模块的整个内容。这种行为可能令人惊讶，并导致 "Module ... has no attribute ... [attr-defined]" 错误。

运行时代码问题(Issues with code at runtime)
------------------------------------------------------

惯用的类型注解使用有时可能与某个特定版本的 Python 所认为的合法代码发生冲突。在尝试运行代码时，这可能导致以下一些错误：

* ``ImportError`` 由于循环导入
* ``NameError: name "X" is not defined`` 由于前向引用
* ``TypeError: 'type' object is not subscriptable`` 由于在运行时非泛型类型
* ``ImportError`` 或 ``ModuleNotFoundError`` 由于使用在运行时不可用的存根定义
* ``TypeError: unsupported operand type(s) for |: 'type' and 'type'`` 由于使用新语法

有关解决这些问题的信息，请参见 :ref:`runtime_troubles`。

Mypy 运行速度慢(Mypy runs are slow)
------------------------------------

如果你的 mypy 运行感觉很慢，你可能应该使用 :ref:`mypy daemon <mypy_daemon>`，这可以将增量 mypy 运行的速度提高 10 倍或更多。 :ref:`Remote caching <remote-cache>` 可以使冷启动 mypy 运行速度快几倍。

空集合的类型(Types of empty collections)
----------------------------------------------------

当你将一个空列表或字典赋值给一个新变量时，通常需要指定类型，如前面提到的：

.. code-block:: python

   a: list[int] = []

没有注释的话，mypy 并不总能确定 ``a`` 的确切类型。

在动态类型函数中，你可以使用简单的空列表字面量（因为 ``a`` 的类型将隐式为 ``Any``，并不需要推断），如果该变量的类型在之前已经声明或推断，或者你在同一作用域中执行简单的修改操作（例如列表的 ``append``）：

.. code-block:: python

   a = []  # 可以，因为后面有 append，推断类型为 list[int]
   for i in range(n):
       a.append(i * i)

然而，在更复杂的情况下，可能需要显式的类型注解（mypy 会告诉你这一点）。通常，注释可以使代码更易于理解，因此它不仅帮助 mypy，也帮助每个阅读代码的人！

不兼容类型的重新定义(Redefinitions with incompatible types)
--------------------------------------------------------------------------

函数中的每个名称只有一个“声明”的类型。你可以重用循环索引等，但如果想在单个函数中使用具有多种类型的变量，可能需要使用多个变量（或者可能声明该变量为 ``Any`` 类型）。

.. code-block:: python

   def f() -> None:
       n = 1
       ...
       n = 'x'  # 错误：赋值中的不兼容类型（表达式类型为 "str"，变量类型为 "int"）

.. note::

   使用 :option:`--allow-redefinition <mypy --allow-redefinition>` 标志可以在某些情况下抑制此错误。

请注意，你可以用更 *精确* 或更具体的类型重新定义变量。例如，你可以将一个不支持 ``sort()`` 的序列重新定义为列表并就地排序：

.. code-block:: python

    def f(x: Sequence[int]) -> None:
        # 这里 x 的类型为 Sequence[int]；我们不知道具体类型。
        x = list(x)
        # 这里 x 的类型为 list[int]。
        x.sort()  # 没问题！

有关更多信息，请参见 :ref:`type-narrowing`。

.. _variance:

不变性与协变性(Invariance vs covariance)
------------------------------------------------

大多数可变的泛型集合是不可变的，mypy 默认将所有用户定义的泛型类视为不可变的（有关动机，请参见 :ref:`variance-of-generics`）。这可能会在与类型推断结合时导致一些意外的错误。例如：

.. code-block:: python

   class A: ...
   class B(A): ...

   lst = [A(), A()]  # 推断类型为 list[A]
   new_lst = [B(), B()]  # 推断类型为 list[B]
   lst = new_lst  # mypy 会对此发出警告，因为 List 是不可变的

在这种情况下可能的策略包括：

* 使用显式类型注解：

  .. code-block:: python

     new_lst: list[A] = [B(), B()]
     lst = new_lst  # 没问题

* 对右侧进行复制：

  .. code-block:: python

     lst = list(new_lst) # 也没问题

* 尽可能使用不可变集合作为注释：

  .. code-block:: python

     def f_bad(x: list[A]) -> A:
         return x[0]
     f_bad(new_lst) # 失败

     def f_good(x: Sequence[A]) -> A:
         return x[0]
     f_good(new_lst) # 没问题

将超类型声明为变量类型(Declaring a supertype as variable type)
----------------------------------------------------------------------------

有时，推断的类型是所需类型的子类型（子类）。类型推断使用第一次赋值来推断名称的类型：

.. code-block:: python

   class Shape: ...
   class Circle(Shape): ...
   class Triangle(Shape): ...

   shape = Circle()    # mypy 推断 shape 的类型为 Circle
   shape = Triangle()  # 错误：赋值中的不兼容类型（表达式类型为 "Triangle"，变量类型为 "Circle"）

在上述例子中，你可以为变量提供显式类型：

.. code-block:: python

   shape: Shape = Circle()  # 变量 shape 可以是任何 Shape，而不仅仅是 Circle
   shape = Triangle()       # 没问题

复杂的类型测试(Complex type tests)
------------------------------------

当使用 :py:func:`isinstance <isinstance>`、:py:func:`issubclass <issubclass>` 或 ``type(obj) is some_class`` 类型测试时，mypy 通常可以正确推断类型，甚至对于 :ref:`用户定义的类型保护 <type-guards>`，但对于其他类型的检查，你可能需要添加显式的类型转换：

.. code-block:: python

  from collections.abc import Sequence
  from typing import cast

  def find_first_str(a: Sequence[object]) -> str:
      index = next((i for i, s in enumerate(a) if isinstance(s, str)), -1)
      if index < 0:
          raise ValueError('No str found')

      found = a[index]  # 类型为 "object"，尽管我们知道它是 "str"
      return cast(str, found)  # 需要显式转换以使 mypy 满意

或者，你可以结合一些支持的类型推断技术使用 ``assert`` 语句：

.. code-block:: python

  def find_first_str(a: Sequence[object]) -> str:
      index = next((i for i, s in enumerate(a) if isinstance(s, str)), -1)
      if index < 0:
          raise ValueError('No str found')

      found = a[index]  # 类型为 "object"，尽管我们知道它是 "str"
      assert isinstance(found, str)  # 现在，“found”的类型将缩小为 "str"
      return found  # 不再需要显式的 "cast()"

.. note::

    注意，上述示例中使用的 :py:class:`object` 类型类似于 Java 中的 ``Object`` ：它只支持为 *所有* 对象定义的操作，例如相等性和 :py:func:`isinstance`。相反，类型 ``Any`` 支持所有操作，即使它们可能在运行时失败。如果 ``o`` 的类型是 ``Any``，则上述类型转换就不必要了。

.. note::

   你可以在 :ref:`这里 <type-narrowing>` 阅读更多关于类型缩小技术的内容。

Mypy 中的类型推断旨在在常见情况下表现良好，具有可预测性，并让类型检查器提供有用的错误消息。更强大的类型推断策略往往具有复杂且难以预测的失败模式，可能导致非常混淆的错误消息。权衡之下，作为程序员的你有时需要为类型检查器提供一些帮助。

.. _version_and_platform_checks:

Python 版本和系统平台检查(Python version and system platform checks)
---------------------------------------------------------------------------

Mypy 支持执行 Python 版本检查和平台检查（例如，Windows 与 Posix），忽略在目标 Python 版本或平台上不会运行的代码路径。这使你能够更有效地对支持多个版本的 Python 或多个操作系统的代码进行类型检查。

更具体地说，mypy 将理解在 ``if/elif/else`` 语句中使用 :py:data:`sys.version_info` 和 :py:data:`sys.platform` 检查。例如：

.. code-block:: python

   import sys

   # 区分不同版本的 Python：
   if sys.version_info >= (3, 8):
       # Python 3.8+ 特定的定义和导入
   else:
       # 其他定义和导入

   # 区分不同的操作系统：
   if sys.platform.startswith("linux"):
       # Linux 特定代码
   elif sys.platform == "darwin":
       # Mac 特定代码
   elif sys.platform == "win32":
       # Windows 特定代码
   else:
       # 其他系统

作为特例，你还可以在顶层（未缩进的） ``assert`` 中使用其中一个检查；这会使 mypy 跳过文件的其余部分。示例：

.. code-block:: python

   import sys

   assert sys.platform != 'win32'

   # 此文件的其余部分不适用于 Windows。

其他一些表达式也表现出类似的行为；特别是，:py:data:`~typing.TYPE_CHECKING`、命名为 ``MYPY`` 的变量，以及任何传递给 :option:`--always-true <mypy --always-true>` 或 :option:`--always-false <mypy --always-false>` 的变量名。
（不过，``True`` 和 ``False`` 并未被特殊处理！）

.. note::

   Mypy 当前不支持更复杂的检查，也不为将 :py:data:`sys.version_info` 或 :py:data:`sys.platform` 检查赋予变量任何特殊含义。未来版本的 mypy 可能会有所更改。

默认情况下，mypy 将使用你当前的 Python 版本和当前的操作系统作为 :py:data:`sys.version_info` 和 :py:data:`sys.platform` 的默认值。

要针对不同的 Python 版本，请使用 :option:`--python-version X.Y <mypy --python-version>` 标志。
例如，要验证你的代码在使用 Python 3.8 时是否能通过类型检查，可以从命令行传入 :option:`--python-version 3.8 <mypy --python-version>`。请注意，你并不需要安装 Python 3.8 来执行此检查。

要针对不同的操作系统，请使用 :option:`--platform PLATFORM <mypy --platform>` 标志。
例如，要验证你的代码在 Windows 中是否能通过类型检查，可以传入 :option:`--platform win32 <mypy --platform>`。有关有效平台参数的示例，请参见 :py:data:`sys.platform` 的文档。

.. _reveal-type:


显示表达式的类型(Displaying the type of an expression)
------------------------------------------------------------

你可以使用 ``reveal_type(expr)`` 请求 mypy 显示表达式的推断静态类型。当你不太理解 mypy 如何处理特定代码时，这可能会很有用。示例：

.. code-block:: python

   reveal_type((1, 'hello'))  # Revealed type is "tuple[builtins.int, builtins.str]"

你还可以在文件中的任何行使用 ``reveal_locals()`` 以一次查看所有局部变量的类型。示例：

.. code-block:: python

   a = 1
   b = 'one'
   reveal_locals()
   # Revealed local types are:
   #     a: builtins.int
   #     b: builtins.str
.. note::

   ``reveal_type`` 和 ``reveal_locals`` 仅被 mypy 理解，
   在 Python 中不存在。如果你尝试运行你的程序，你需要在运行代码之前
   移除所有 ``reveal_type`` 和 ``reveal_locals`` 的调用。两者总是可用，
   你无需导入它们。

静默代码检查工具(Silencing linters)
----------------------------------------------

在某些情况下，代码检查工具会抱怨未使用的导入或代码。在这些情况下，你可以在类型注解后添加注释，或者与导入语句在同一行上静默它们：

.. code-block:: python

   # to silence complaints about unused imports
   from typing import List  # noqa
   a = None  # type: List[int]

要在与类型注解相同的行上静默代码检查工具，请将检查注释放在类型注解*之后*：

.. code-block:: python

    a = some_complex_thing()  # type: ignore  # noqa

可变协议成员的协变子类型被拒绝(Covariant subtyping of mutable protocol members is rejected)
---------------------------------------------------------------------------------------------------------

Mypy 拒绝这种情况，因为这可能不安全。
考虑以下示例：

.. code-block:: python

   from typing import Protocol

   class P(Protocol):
       x: float

   def fun(arg: P) -> None:
       arg.x = 3.14

   class C:
       x = 42
   c = C()
   fun(c)  # 这不是安全的
   c.x << 5  # 因为这会失败！

要解决这个问题，请考虑 “突变(mutating)” 是否实际上是协议的一部分。如果不是，则可以在协议定义中使用 :py:class:`@property <property>`：

.. code-block:: python

   from typing import Protocol

   class P(Protocol):
       @property
       def x(self) -> float:
          pass

   def fun(arg: P) -> None:
       ...

   class C:
       x = 42
   fun(C())  # OK

处理冲突的名称(Dealing with conflicting names)
------------------------------------------------------------

假设你有一个类，其方法名与导入的（或内置的）类型相同，而你希望在另一个方法签名中使用该类型。例如：

.. code-block:: python

   class Message:
       def bytes(self):
           ...
       def register(self, path: bytes):  # error: Invalid type "mod.Message.bytes"
           ...

第三行引发错误，因为 mypy 将参数类型 ``bytes`` 视为对该名称方法的引用。除了重命名方法之外，另一种解决方法是使用别名：

.. code-block:: python

   bytes_ = bytes
   class Message:
       def bytes(self):
           ...
       def register(self, path: bytes_):
           ...

使用开发版 mypy(Using a development mypy build)
---------------------------------------------------

你可以从源代码安装最新的开发版本 mypy。克隆 `mypy GitHub 仓库 <https://github.com/python/mypy>`_，然后本地运行 ``pip install``：

.. code-block:: text

    git clone https://github.com/python/mypy.git
    cd mypy
    python3 -m pip install --upgrade .

要安装一个经过 mypyc 编译的开发版本 mypy，请参见 `mypyc wheels 仓库 <https://github.com/mypyc/mypy_mypyc-wheels>`_ 的说明。

变量与类型别名(Variables vs type aliases)
----------------------------------------------

Mypy 具有 *类型别名(type aliases)* 和带有类型如 ``type[...]`` 的变量。这两者之间有细微的不同，理解它们的差异非常重要，以避免陷阱。

1. 带有类型 ``type[...]`` 的变量使用显式类型注解的赋值来定义：

   .. code-block:: python

     class A: ...
     tp: type[A] = A

2. 你可以使用没有显式类型注解的赋值在模块的顶层定义类型别名：

   .. code-block:: python

     class A: ...
     Alias = A

   你还可以使用 ``TypeAlias`` (:pep:`613`) 来定义 *显式类型别名*：

   .. code-block:: python

     from typing import TypeAlias  # 在 Python 3.9 及更早版本中使用 "from typing_extensions"

     class A: ...
     Alias: TypeAlias = A

   在类体或函数内部定义类型别名时，你应该始终使用 ``TypeAlias``。

主要区别在于，别名的目标在静态上是精确已知的，这意味着它们可以用于类型注解和其他 *类型上下文*。类型别名不能有条件地定义（除非使用
:ref:`受支持的 Python 版本和平台检查 <version_and_platform_checks>`）：

   .. code-block:: python

     class A: ...
     class B: ...

     if random() > 0.5:
         Alias = A
     else:
         # error: Cannot assign multiple types to name "Alias" without an
         # explicit "Type[...]" annotation
         Alias = B

     tp: type[object]  # "tp" 是一个带有类型对象值的变量
     if random() > 0.5:
         tp = A
     else:
         tp = B  # 这可以

     def fun1(x: Alias) -> None: ...  # OK
     def fun2(x: tp) -> None: ...  # Error: "tp" is not valid as a type

不兼容的重写(Incompatible overrides)
--------------------------------------------

使用更具体的参数类型重写方法是不安全的，因为这违反了 `Liskov 替代原则 <https://stackoverflow.com/questions/56860/what-is-an-example-of-the-liskov-substitution-principle>`_ 。对于返回类型，使用更一般的返回类型重写方法也是不安全的。

方法重写中的其他不兼容签名更改，例如添加额外的必需参数或移除可选参数，也会生成错误。子类中方法的签名应接受对基类方法的所有有效调用。Mypy 将子类视为基类的子类型。子类的实例在基类的实例有效的所有地方都是有效的。

以下示例演示了安全和不安全的重写：

.. code-block:: python

    from collections.abc import Sequence, Iterable

    class A:
        def test(self, t: Sequence[int]) -> Sequence[str]:
            ...

    class GeneralizedArgument(A):
        # 更一般的参数类型是可以的
        def test(self, t: Iterable[int]) -> Sequence[str]:  # OK
            ...

    class NarrowerArgument(A):
        # 更具体的参数类型不被接受
        def test(self, t: list[int]) -> Sequence[str]:  # Error
            ...

    class NarrowerReturn(A):
        # 更具体的返回类型是可以的
        def test(self, t: Sequence[int]) -> List[str]:  # OK
            ...

    class GeneralizedReturn(A):
        # 更一般的返回类型是错误
        def test(self, t: Sequence[int]) -> Iterable[str]:  # Error
            ...

你可以使用 ``# type: ignore[override]`` 来消除错误。如果你认为类型安全不是必要的，请将其添加到生成错误的行：

.. code-block:: python

    class NarrowerArgument(A):
        def test(self, t: List[int]) -> Sequence[str]:  # type: ignore[override]
            ...

.. _unreachable:

不可达代码(Unreachable code)
--------------------------------

Mypy 可能会将某些代码视为 *不可达*，即使这可能并不明显。重要的是要注意，mypy 将 *不* 检查此类代码。考虑以下示例：

.. code-block:: python

    class Foo:
        bar: str = ''

    def bar() -> None:
        foo: Foo = Foo()
        return
        x: int = 'abc'  # 不可达 -- 无错误

很容易看出，任何在 ``return`` 之后的语句都是不可达的，因此 mypy 不会对下面的错误类型代码进行警告。对于一个更微妙的示例，请考虑以下代码：

.. code-block:: python

    class Foo:
        bar: str = ''

    def bar() -> None:
        foo: Foo = Foo()
        assert foo.bar is None
        x: int = 'abc'  # 不可达 -- 无错误

同样，mypy 不会报告任何错误。``foo.bar`` 的类型是 ``str``，mypy 推断它永远不会是 ``None``。因此 ``assert`` 语句将始终失败，下面的语句将永远不会被执行。（注意，在 Python 中，``None`` 不是一个空引用，而是类型为 ``None`` 的对象。）

在这个例子中，mypy 将继续检查最后一行并报告错误，因为 mypy 认为条件可能为 True 或 False：

.. code-block:: python

    class Foo:
        bar: str = ''

    def bar() -> None:
        foo: Foo = Foo()
        if not foo.bar:
            return
        x: int = 'abc'  # 可达 -- 错误

如果使用 :option:`--warn-unreachable <mypy --warn-unreachable>` 标志，mypy 将对每个不可达代码块生成错误。

缩小范围和内部函数(Narrowing and inner functions)
----------------------------------------------------------

由于 Python 中的闭包是延迟绑定的(https://docs.python-guide.org/writing/gotchas/#late-binding-closures), mypy 不会在内部函数中缩小被捕获变量的类型。这最好通过一个示例来理解：

.. code-block:: python

    def foo(x: int | None) -> Callable[[], int]:
        if x is None:
            x = 5
        print(x + 1)  # mypy 正确推断出此处 x 必须是 int
        def inner() -> int:
            return x + 1  # 但（正确地）对这一行提出了警告

        x = None  # 因为 x 可能会在后面被赋值为 None
        return inner

    inner = foo(5)
    inner()  # 调用时会引发错误

要使这段代码通过类型检查，你可以在 `x` 被缩小后赋值 `y = x`，并在内部函数中使用 `y`，或者在内部函数中添加一个断言。
