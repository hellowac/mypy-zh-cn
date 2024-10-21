附加功能(Additional features)
--------------------------------------

本节讨论了各种未能自然融入前面任一部分的功能。

.. _dataclasses_support:

数据类(Dataclasses)
**********************

:py:mod:`dataclasses` 模块允许定义和自定义简单的无样板类。它们可以使用 :py:func:`@dataclasses.dataclass <python:dataclasses.dataclass>` 装饰器来定义：

.. code-block:: python

    from dataclasses import dataclass, field

    @dataclass
    class Application:
        name: str
        plugins: list[str] = field(default_factory=list)

    test = Application("Testing...")  # 正确
    bad = Application("Testing...", "with plugin")  # 错误: 期望 list[str]

Mypy 将根据用于定义数据类的标志检测特殊方法（如 :py:meth:`__lt__ <object.__lt__>`）。例如：

.. code-block:: python

    from dataclasses import dataclass

    @dataclass(order=True)
    class OrderedPoint:
        x: int
        y: int

    @dataclass(order=False)
    class UnorderedPoint:
        x: int
        y: int

    OrderedPoint(1, 2) < OrderedPoint(3, 4)  # 正确
    UnorderedPoint(1, 2) < UnorderedPoint(3, 4)  # 错误: 不支持的操作数类型

数据类可以是泛型的，并且可以像普通类一样以任何其他方式使用（Python 3.12 语法）：

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class BoxedData[T]:
        data: T
        label: str

    def unbox[T](bd: BoxedData[T]) -> T:
        ...

    val = unbox(BoxedData(42, "<important>"))  # 正确，推断类型为 int

有关更多信息，请参见 :doc:`官方文档 <python:library/dataclasses>` 和 :pep:`557`。

注意事项/已知问题(Caveats/Known Issues)
========================================

:py:mod:`dataclasses` 模块中的某些函数，如 :py:func:`~dataclasses.asdict`，具有不精确（过于宽松）的类型。这将在未来的版本中修复。

Mypy 尚未识别 :py:func:`dataclasses.dataclass <dataclasses.dataclass>` 的别名，并且可能永远不会识别动态计算的装饰器。以下示例**不**有效：

.. code-block:: python

    from dataclasses import dataclass

    dataclass_alias = dataclass
    def dataclass_wrapper(cls):
      return dataclass(cls)

    @dataclass_alias
    class AliasDecorated:
      """
      Mypy 不会将其识别为数据类，因为它是由 `dataclass` 的别名装饰的，而不是由 `dataclass` 本身装饰的。
      """
      attribute: int

    AliasDecorated(attribute=1)  # 错误: 意外的关键字参数


要使 Mypy 识别 :py:func:`dataclasses.dataclass <dataclasses.dataclass>` 的包装器作为数据类装饰器，可以考虑使用 :py:func:`~typing.dataclass_transform` 装饰器（示例使用 Python 3.12 语法）：

.. code-block:: python

    from dataclasses import dataclass, Field
    from typing import dataclass_transform

    @dataclass_transform(field_specifiers=(Field,))
    def my_dataclass[T](cls: type[T]) -> type[T]:
        ...
        return dataclass(cls)


数据类转换(Data Class Transforms)
******************************************

Mypy 支持 :py:func:`~typing.dataclass_transform` 装饰器，如在 `PEP 681 <https://www.python.org/dev/peps/pep-0681/#the-dataclass-transform-decorator>`_ 中所述。

.. note::

    从实用的角度来看，mypy 将假设此类具有内部属性 :code:`__dataclass_fields__`
    （即使它们在运行时可能缺失），并且将假设像 :py:func:`dataclasses.is_dataclass`
    和 :py:func:`dataclasses.fields` 这样的函数会将它们视为数据类
    （即使它们在运行时可能会失败）。

.. _attrs_package:

attrs 包(The attrs package)
**********************************

:doc:`attrs <attrs:index>` 是一个让你定义类而无需编写样板代码的包。Mypy 可以检测该包的使用，并将使用它找到的类型注解为装饰类生成必要的方法定义。
类型注解可以如下添加：

.. code-block:: python

    import attr

    @attrs.define
    class A:
        one: int
        two: int = 7
        three: int = attrs.field(8)

如果你使用 ``auto_attribs=False``，你必须使用 ``attrs.field``：

.. code-block:: python

    import attrs

    @attrs.define
    class A:
        one: int = attrs.field()          # 变量注释 (Python 3.6+)
        two = attrs.field()  # type: int  # 类型注释
        three = attrs.field(type=int)     # type= 参数

Typeshed 有一些“白色谎言”注释以简化类型检查。:py:func:`attrs.field` 和 :py:class:`attrs.Factory` 实际上返回对象，但注释表示这些返回它们期望被分配的类型。
这使得以下代码可以工作：

.. code-block:: python

    import attrs

    @attrs.define
    class A:
        one: int = attrs.field(8)
        two: dict[str, str] = attrs.Factory(dict)
        bad: str = attrs.field(16)   # 错误: 不能将 int 分配给 str

注意事项/已知问题(Caveats/Known Issues)
========================================

* attrs 类和属性的检测仅通过函数名称工作。这意味着如果你有自己的帮助函数，例如 ``return attrs.field()``，mypy 将无法识别它们。

* 所有 mypy 关心的布尔参数必须是字面量 ``True`` 或 ``False``。
  例如，以下代码将无法工作：

  .. code-block:: python

      import attrs
      YES = True
      @attrs.define(init=YES)
      class A:
          ...

* 目前，``converter`` 仅支持命名函数。如果 mypy 找到其他内容，它将抱怨不理解该参数，且 :py:meth:`__init__ <object.__init__>` 中的类型注解将被替换为 ``Any``。

* :ref:`验证器装饰器 <attrs:examples-validators>` 和 `默认装饰器 <https://www.attrs.org/en/stable/examples.html#defaults>`_
  不会针对它们设置/验证的属性进行类型检查。

* mypy 添加的方法定义当前会覆盖任何现有的方法定义。

.. _remote-cache:

使用远程缓存加速 mypy 运行(Using a remote cache to speed up mypy runs)
************************************************************************************

Mypy 以 *增量* 方式执行类型检查，重用先前运行的结果以加速后续运行。如果你在大型代码库中进行类型检查，mypy 有时仍然会比预期的慢。例如，如果你在基于比上次 mypy 运行目标更近的提交创建新分支，mypy 可能不得不处理几乎每个文件，因为大量源文件可能已更改。此情况也可能在你重新基于本地分支之后发生。

Mypy 支持使用 *远程缓存* 来提高上述情况的性能。在大型代码库中，远程缓存有时可以将 mypy 运行速度提高 10 倍或更多。

Mypy 不包括设置此配置所需的所有组件——通常，你必须与 CI（持续集成）或构建系统进行一些简单集成，以配置 mypy 使用远程缓存。本讨论假设你已为要加速的 mypy 构建设置了 CI 系统，并且你正在使用中央 git 存储库。将其概括到不同环境中应该不难。

这里是所需的主要组件：

* 用于存储所有已提交的 mypy 缓存文件的共享存储库。

* CI 构建在每个 CI 构建运行的提交上将 mypy 增量缓存文件上传到共享存储库。

* 开发人员使用的 mypy 的包装脚本，用于启用远程缓存的 mypy 运行。

下面我们将详细讨论每个组件。

缓存文件的共享存储库(Shared repository for cache files)
==================================================================

你需要一个允许你从 CI 构建上传 mypy 缓存文件的存储库，并根据提交 ID 提供缓存文件下载。一个简单的方法是将 ``.mypy_cache`` 目录（包含 mypy 缓存数据）制作成可下载的 *构建工件*，并从你的 CI 构建中提供（具体取决于你的 CI 系统的能力）。或者，你也可以将数据上传到 web 服务器或 S3 等位置。

持续集成构建(Continuous Integration build)
========================================================

CI 构建将运行常规的 mypy 构建，并创建一个包含构建生成的 ``.mypy_cache`` 目录的归档文件。最后，它将把缓存作为构建工件生成，或将其上传到一个 mypy 包装脚本可以访问的存储库。

你的 CI 脚本可能像这样工作：

* 正常运行 mypy。这将生成 ``.mypy_cache`` 目录下的缓存数据。

* 从 ``.mypy_cache`` 目录创建一个 tarball。

* 确定当前 git 主分支的提交 ID（例如，使用 ``git rev-parse HEAD`` )。

* 将 tarball 以从提交 ID 派生的名称上传到共享存储库。

Mypy 包装脚本(Mypy wrapper script)
===============================================

包装脚本由开发人员在开发期间用来本地运行 mypy，而不是直接调用 mypy。包装脚本首先从共享存储库填充本地的 ``.mypy_cache`` 目录，然后运行常规的增量构建。

包装脚本需要一些逻辑来确定本地开发分支所基于的最新中央存储库提交（按约定，git 的 ``origin/master`` 分支）。在典型的 git 设置中，你可以这样做：

.. code::

    git merge-base HEAD origin/master

下一步是根据上述 git 命令生成的合并基础的提交 ID 从共享存储库下载缓存数据( ``.mypy_cache`` 目录的内容）。该脚本将解压缩数据，以便 mypy 从一个全新的 ``.mypy_cache`` 开始。最后，脚本正常运行 mypy。这就是全部!

使用 mypy 守护进程进行缓存(Caching with mypy daemon)
====================================================

你还可以使用 :ref:`mypy 守护进程 <mypy_daemon>` 来进行远程缓存。远程缓存将显著加速启动或重启守护进程后第一次运行的 ``dmypy check``。

mypy 守护进程在缓存文件中需要额外的细粒度依赖数据，而这些数据默认并不包含。要在 CI 构建中使用缓存与 mypy 守护进程一起工作，请在你的 CI 构建中使用 :option:`--cache-fine-grained <mypy --cache-fine-grained>` 选项::

    $ mypy --cache-fine-grained <args...>

此标志将额外信息添加到守护进程的缓存中。为了使用这些额外信息，你还需要在 ``dmypy start`` 或 ``dmypy restart`` 时使用 ``--use-fine-grained-cache`` 选项。示例::

    $ dmypy start -- --use-fine-grained-cache <options...>

现在你的第一次 ``dmypy check`` 运行应该会快得多，因为它可以使用缓存信息来避免处理整个程序。

改进措施(Refinements)
======================

有几个可选的改进措施，可能会进一步改善性能，至少在你的代码库有数十万行或更多时：

* 如果包装脚本确定合并基础自上一次运行以来没有更改，则无需下载缓存数据，最好重用现有的本地缓存数据。

* 如果你使用 mypy 守护进程，你可能希望在每次合并基础或本地分支更改后重启守护进程，以避免在增量构建中处理大量更改，因为这可能比下载缓存数据和重启守护进程要慢得多。

* 如果当前本地分支基于非常新的主提交，远程缓存数据可能尚未为该提交可用，因为构建缓存文件必然会有一些延迟。查看最新的 5 个主提交的缓存数据并使用可用的最新数据可能是个好主意。

* 如果由于某种原因（例如，来自公共网络）远程缓存无法访问，脚本仍然可以回退到常规的增量构建。

* 你可以使用 :option:`--cache-dir <mypy --cache-dir>` 选项为不同的本地分支设置多个本地缓存目录。如果用户切换到一个已经存在的分支，并且已下载的缓存数据已经可用，你可以继续使用现有的缓存数据，而不是重新下载数据。

* 你可以设置 CI 构建以使用远程缓存来加速 CI 构建。如果每个 CI 构建从没有访问到以前构建的缓存文件的新状态开始，这将特别有用。仍然建议运行完整的非增量 mypy 构建来创建缓存数据，因为反复增量更新缓存数据可能会导致长时间内的漂移（可能是由于 mypy 缓存问题）。

.. _extended_callable:

扩展可调用类型(Extended Callable types)
**********************************************

.. note::

   此功能已被弃用。你可以使用
   :ref:`回调协议 <callback_protocols>` 作为替代。

作为一个实验性的 mypy 扩展，你可以指定支持关键字参数、可选参数等的 :py:class:`~collections.abc.Callable` 类型。当你指定 :py:class:`~collections.abc.Callable` 的参数时，可以选择仅提供一个无名位置参数的类型，或者提供一个表示更复杂参数形式的“参数说明符”。这使得能够更接近模拟 Python 中 ``def`` 语句提供的全部可能性。

作为示例，以下是一个复杂的函数定义及其对应的 :py:class:`~collections.abc.Callable`：

.. code-block:: python

   from collections.abc import Callable
   from mypy_extensions import (Arg, DefaultArg, NamedArg,
                                DefaultNamedArg, VarArg, KwArg)

   def func(__a: int,  # 这种约定用于无名参数
            b: int,
            c: int = 0,
            *args: int,
            d: int,
            e: int = 0,
            **kwargs: int) -> int:
       ...

   F = Callable[[int,  # 或 Arg(int)
                 Arg(int, 'b'),
                 DefaultArg(int, 'c'),
                 VarArg(int),
                 NamedArg(int, 'd'),
                 DefaultNamedArg(int, 'e'),
                 KwArg(int)],
                int]

   f: F = func

参数说明符是特殊的函数调用，可以指定参数的以下方面：

- 其类型（基本格式支持的唯一内容）

- 其名称（如果有的话）

- 是否可以省略

- 是否可以或必须使用关键字传递

- 是否为 ``*args`` 参数（表示其余的位置参数）

- 是否为 ``**kwargs`` 参数（表示其余的关键字参数）

以下函数在 ``mypy_extensions`` 中可用于此目的：

.. code-block:: python

   def Arg(type=Any, name=None):
       # 一个普通的、强制性的、位置参数。
       # 如果指定了名称，可以作为关键字传递。

   def DefaultArg(type=Any, name=None):
       # 一个可选的位置参数（即具有默认值）。
       # 如果指定了名称，可以作为关键字传递。

   def NamedArg(type=Any, name=None):
       # 一个强制性的仅关键字参数。

   def DefaultNamedArg(type=Any, name=None):
       # 一个可选的仅关键字参数（即具有默认值）。

   def VarArg(type=Any):
       # 一个 *args 风格的变长位置参数。
       # 单个 VarArg() 说明符表示所有其余的位置参数。

   def KwArg(type=Any):
       # 一个 **kwargs 风格的变长关键字参数。
       # 单个 KwArg() 说明符表示所有其余的关键字参数。

在所有情况下，``type`` 参数默认为 ``Any``，如果省略 ``name`` 参数，则该参数没有名称( ``NamedArg`` 和 ``DefaultNamedArg`` 需要名称）。一个基本的 :py:class:`~collections.abc.Callable` 如下所示：

.. code-block:: python

   MyFunc = Callable[[int, str, int], float]

等价于：

.. code-block:: python

   MyFunc = Callable[[Arg(int), Arg(str), Arg(int)], float]

一个参数类型未指定的 :py:class:`~collections.abc.Callable` 如下所示：

.. code-block:: python

   MyOtherFunc = Callable[..., int]

大致等价于：

.. code-block:: python

   MyOtherFunc = Callable[[VarArg(), KwArg()], int]

.. note::

   上述每个函数在运行时仅返回其 ``type`` 参数，因此参数说明符中包含的信息在运行时不可用。此限制对于与现有的 ``typing.py`` 模块（Python 3.5+ 标准库中存在并通过 PyPI 分发）保持向后兼容是必要的。
