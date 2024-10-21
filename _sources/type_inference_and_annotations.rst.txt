.. _type-inference-and-annotations:

类型推断和类型注解(annotations)
======================================

类型推断
********

对于大多数变量，如果您没有明确指定其类型，mypy 将根据初始赋值推断出正确的类型。

.. code-block:: python

    # 即使没有注释，Mypy 也会推断这些变量的类型
    i = 1
    reveal_type(i)  # 显示的类型是 "builtins.int"
    l = [1, 2]
    reveal_type(l)  # 显示的类型是 "builtins.list[builtins.int]"


.. note::

    请注意，mypy 在动态类型函数（没有函数类型注解的函数）中不会使用类型推断——在这些函数中，每个局部变量的类型默认为 ``Any``。有关更多细节，请参见 :ref:`dynamic-typing`。

    .. code-block:: python

        def untyped_function():
            i = 1
            reveal_type(i) # 显示的类型是 "Any"
                           # 'reveal_type' 在未检查的函数中总是输出 'Any'


.. _explicit-var-types:

显式变量类型
************

您可以通过使用变量类型注解来覆盖变量的推断类型：

.. code-block:: python

   x: int | str = 1

如果没有类型注解，``x`` 的类型将只是 ``int``。我们使用注释将其类型指定为更一般的 ``int | str`` (该类型表示值可以是 ``int`` 或 ``str`` )。

最佳理解方式是类型注解设置的是变量的类型，而不是表达式的类型。例如，mypy 会对以下代码报错：

.. code-block:: python

   x: int | str = 1.1  # 错误：赋值中的不兼容类型
                       # （表达式的类型为 "float"，变量的类型为 "int | str"）

.. note::

   要显式覆盖表达式的类型，您可以使用
   :py:func:`cast(\<type\>, \<expression\>) <typing.cast>`。
   有关详细信息，请参见 :ref:`casts`。

请注意，您可以在不赋初始值的情况下显式声明变量的类型：

.. code-block:: python

   # 我们只解包两个值，因此没有右侧值
   # 供 mypy 推断 "cs" 的类型：
   a, b, *cs = 1, 2  # 错误：需要为 "cs" 提供类型注解

   rs: list[int]  # 没有赋值!
   p, q, *rs = 1, 2  # OK

显式集合类型
*******************

类型检查器并不总是能够推断列表或字典的类型。这通常发生在创建空列表或字典并将其分配给没有显式变量类型的新变量时。以下示例展示了 mypy 在没有帮助的情况下无法推断类型：

.. code-block:: python

   l = []  # 错误：需要为 "l" 提供类型注解

在这些情况下，您可以通过类型注解显式指定类型：

.. code-block:: python

   l: list[int] = []       # 创建空的 int 列表
   d: dict[str, int] = {}  # 创建空字典（str -> int）

.. note::

   对于像 :py:class:`list`、:py:class:`dict`、:py:class:`tuple` 和 :py:class:`set` 这样的内置集合使用类型参数（例如 ``list[int]`` )仅适用于 Python 3.9 及以上版本。对于 Python 3.8 及更早版本，您必须使用 :py:class:`~typing.List` （例如 ``List[int]`` )、:py:class:`~typing.Dict` 等。

容器类型的兼容性
*********************

快速说明：容器类型有时可能会令人困惑。我们将在 :ref:`variance` 中进一步讨论。例如，以下程序会生成 mypy 错误，因为 mypy 将 ``list[int]`` 视为与 ``list[object]`` 不兼容：

.. code-block:: python

   def f(l: list[object], k: list[int]) -> None:
       l = k  # 错误：赋值中的不兼容类型

上述赋值被禁止的原因是，允许赋值可能导致非整数值存储在 ``int`` 列表中：

.. code-block:: python

   def f(l: list[object], k: list[int]) -> None:
       l = k
       l.append('x')
       print(k[-1])  # 哎呀；在 list[int] 中出现字符串

其他容器类型如 :py:class:`dict` 和 :py:class:`set` 也有类似的行为。

您仍然可以运行上述程序，它会打印 ``x``。这说明静态类型并不影响程序的运行时行为。您可以运行存在类型检查失败的程序，这在进行大规模重构时通常非常有用。因此，您始终可以“绕过”类型系统，而这并不会真正限制您在程序中的操作。

类型推断中的上下文
*******************

类型推断是 *双向的* ，并考虑上下文。

Mypy 会考虑赋值语句左侧变量的类型，从而推断右侧表达式的类型。例如，以下代码将通过类型检查：

.. code-block:: python

   def f(l: list[object]) -> None:
       l = [1, 2]  # 推断 [1, 2] 的类型为 list[object]，而不是 list[int]

值表达式 ``[1, 2]`` 的类型检查结合了它将被赋值给类型为 ``list[object]`` 的变量的额外上下文。这用于推断表达式的类型为 ``list[object]``。

声明的参数类型也用于类型上下文。在这个程序中，mypy 知道空列表 ``[]`` 应该是类型为 ``list[int]``，基于 ``foo`` 中对 ``arg`` 的声明类型：

.. code-block:: python

    def foo(arg: list[int]) -> None:
        print('Items:', ''.join(str(a) for a in arg))

    foo([])  # OK

然而，上下文仅在单个语句内有效。在下面的代码中，mypy 要求为空列表添加注释，因为上下文仅在下一条语句中可用：

.. code-block:: python

    def foo(arg: list[int]) -> None:
        print('Items:', ', '.join(arg))

    a = []  # 错误：需要为 "a" 提供类型注解
    foo(a)

通过添加类型注解来解决这个问题非常简单：

.. code-block:: python

    ...
    a: list[int] = []  # OK
    foo(a)

.. _silencing-type-errors:

静默类型错误
*********************

您可能希望在代码库中的特定行或文件上禁用类型检查。为此，您可以使用 ``# type: ignore`` 注释。

例如，假设您使用的网络框架在最新更新中可以接受一个整数参数传递给 ``run()``，以便在该端口的 localhost 上启动它。代码如下：

.. code-block:: python

    # 在 http://localhost:8000 上启动应用
    app.run(8000)

然而，开发人员忘记更新 ``run`` 的类型注解，因此 mypy 仍然认为 ``run`` 仅期望 ``str`` 类型。这将导致以下错误：

.. code-block:: text

    error: Argument 1 to "run" of "A" has incompatible type "int"; expected "str"

如果您无法直接修复该网络框架，可以通过添加 ``# type: ignore`` 临时禁用该行的类型检查：

.. code-block:: python

    # 在 http://localhost:8000 上启动应用
    app.run(8000)  # type: ignore

这将抑制在该特定行上可能引发的任何 mypy 错误。

您可能还应该在 ``# type: ignore`` 注释中添加更多信息，以解释为什么最初添加了忽略。这可以是指向类型存根负责的存储库中问题的链接，或者是对错误的简短说明。可以使用以下格式：

.. code-block:: python

    # 在 http://localhost:8000 上启动应用
    app.run(8000)  # type: ignore  # `run()` 在 v2.0 中接受一个 `int`，作为端口

类型忽略错误代码
-----------------------

默认情况下，mypy 为每个错误显示一个错误代码：

.. code-block:: text

   error: "str" has no attribute "trim"  [attr-defined]

可以在忽略注释中添加特定的错误代码（例如 ``# type: ignore[attr-defined]`` )，以澄清正在静默的内容。您可以在 :ref:`这里 <silence-error-codes>` 找到有关错误代码的更多信息。

静默错误的其他方法
----------------------------

您可以通过使用 ``Any`` 动态类型来让 mypy 静默特定变量的错误。有关更多信息，请参见 :ref:`dynamic-typing`。

.. code-block:: python

    from typing import Any

    def f(x: Any, y: str) -> None:
        x = 'hello'
        x += 1  # OK

您可以通过在文件顶部添加 ``# mypy: ignore-errors`` 来忽略该文件中的所有 mypy 错误：

.. code-block:: python

    # mypy: ignore-errors
    # 这是一个测试文件，跳过类型检查。
    import unittest
    ...

您还可以在配置文件中指定每个模块的配置选项。示例如下：

.. code-block:: ini

    # 不报告 'package_to_fix_later' 包中的错误
    [mypy-package_to_fix_later.*]
    ignore_errors = True

    # 禁用 'tests' 包中的特定错误代码
    # 同时不要求类型注解
    [mypy-tests.*]
    disable_error_code = var-annotated, has-type
    allow_untyped_defs = True

    # 静默 'library_missing_types' 包中的导入错误
    [mypy-library_missing_types.*]
    ignore_missing_imports = True

最后，给类、方法或函数添加 ``@typing.no_type_check`` 装饰器会导致 mypy 避免对该类、方法或函数进行类型检查，并将其视为没有任何类型注解。

.. code-block:: python

    @typing.no_type_check
    def foo() -> str:
       return 12345  # 没有错误!
