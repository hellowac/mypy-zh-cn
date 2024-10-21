.. _stubgen:

.. program:: stubgen

自动存根生成(Automatic stub generation) (stubgen)
=====================================================================

存根文件（参见 :pep:`484`）只包含模块公共接口的类型提示，函数体为空。Mypy 可以使用存根文件代替真实实现来提供模块的类型信息。它们对于尚未添加类型提示的第三方模块（并且 typeshed 中没有可用存根）以及 C 扩展模块（mypy 无法直接处理）非常有用。

Mypy 包含的 ``stubgen`` 工具可以自动为 Python 模块和 C 扩展模块生成存根文件( ``.pyi`` 文件）。例如，考虑以下源文件：

.. code-block:: python

   from other_module import dynamic

   BORDER_WIDTH = 15

   class Window:
       parent = dynamic()
       def __init__(self, width, height):
           self.width = width
           self.height = height

   def create_empty() -> Window:
       return Window(0, 0)

Stubgen 可以根据上述文件生成以下存根文件：

.. code-block:: python

   from typing import Any

   BORDER_WIDTH: int = ...

   class Window:
       parent: Any = ...
       width: Any = ...
       height: Any = ...
       def __init__(self, width, height) -> None: ...

   def create_empty() -> Window: ...

Stubgen 生成 *草稿* 存根。自动生成的存根文件通常需要一些手动更新，大多数类型将默认为 ``Any``。如果为最常用的功能添加更精确的类型注解，存根文件将更加有用。

本节的其余部分记录了 stubgen 的命令行接口。运行 :option:`stubgen --help` 可以快速查看选项摘要。

.. note::

  命令行标志可能会在版本之间发生变化。

指定要生成存根的内容(Specifying what to stub)
**********************************************

你可以为想要生成存根的源文件提供 stubgen 路径::

    $ stubgen foo.py bar.py

这将生成存根文件 ``out/foo.pyi`` 和 ``out/bar.pyi``。默认输出目录 ``out`` 可以通过 :option:`-o DIR <-o>` 重写。

你还可以传递目录，stubgen 将递归搜索目录中的所有 ``.py`` 文件并为它们生成存根::

    $ stubgen my_pkg_dir

或者，你可以使用 :option:`-m` 或 :option:`-p` 选项提供模块或包名::

    $ stubgen -m foo -m bar -p my_pkg_dir

选项的详细信息：

.. option:: -m MODULE, --module MODULE

    为给定模块生成存根文件。此标志可以重复多次。

    Stubgen *不会* 为提供的模块的任何子模块递归生成存根。

.. option:: -p PACKAGE, --package PACKAGE

    为给定包生成存根文件。此标志可以重复多次。

    Stubgen *会* 为提供的包的所有子模块递归生成存根。此标志与 :option:`--module` 的区别在于这种行为。

.. note::

   你不能在同一次 stubgen 调用中混合使用路径和 :option:`-m`/:option:`-p` 选项。

Stubgen 应用启发式方法来避免为包含测试或第三方包的子模块生成存根。

指定如何生成存根(Specifying how to generate stubs)
************************************************************

默认情况下，stubgen 会尝试导入目标模块和包。这使 stubgen 能够使用运行时反射来为 C 扩展模块生成存根，并提高生成存根的质量。默认情况下，stubgen 还会使用 mypy 对 Python 模块执行轻量级的语义分析。使用以下标志可以更改默认行为：

.. option:: --no-import

    不尝试导入模块。相反，仅使用 mypy 的正常搜索机制查找源文件。这不支持 C 扩展模块。此标志还会禁用运行时反射功能，mypy 使用该功能查找 ``__all__`` 的值。因此，存根中导出的名称集可能不完整。此标志通常仅在导入模块导致不必要的副作用（如运行测试）时有用。即使没有此选项，stubgen 也会尝试跳过测试模块，但这并不总是有效。

.. option:: --no-analysis

    不对源文件进行语义分析。这可能会生成较差的存根，尤其是某些模块、类和函数别名可能会被表示为 ``Any`` 类型的变量。此标志通常仅在语义分析导致关键的 mypy 错误时有用。不适用于 C 扩展模块。与 :option:`--inspect-mode` 不兼容。

.. option:: --inspect-mode

    导入并检查模块，而不是解析源代码。这是 C 模块和仅有 pyc 文件的包的默认行为。此标志可用于强制检查纯 Python 模块，这些模块使用动态生成的成员，而这些成员在使用代码解析的默认行为时可能会被忽略。隐含 :option:`--no-analysis`，因为分析需要源代码。

.. option:: --doc-dir PATH

    尝试通过解析 ``PATH`` 中的 .rst 文档推断出更好的函数签名。这可能会生成更好的存根，但目前仅适用于 C 扩展模块。

附加标志(Additional flags)
******************************

.. option:: -h, --help

    显示帮助信息并退出。

.. option:: --ignore-errors

    如果在生成存根期间引发异常，继续处理任何剩余的模块，而不是立即因错误失败。

.. option:: --include-private

    在存根中包含被视为私有的定义（如名称为 ``_foo`` 的定义，带有单个前导下划线但没有尾随下划线）。

.. option:: --export-less

    不导出从同一包中的其他模块导入的所有名称。相反，仅导出未在包含导入的模块中引用的导入名称。

.. option:: --include-docstrings

    在存根中包含文档字符串。这将为 Python 函数和类的存根以及 C 扩展函数的存根添加文档字符串。

.. option:: --search-path PATH

    指定模块搜索目录，以冒号分隔（仅在给出 :option:`--no-import` 时使用）。

.. option:: -o PATH, --output PATH

    更改输出目录。默认情况下，存根写入 ``./out`` 目录。如果目录不存在，将自动创建输出目录。输出目录中现有的存根将被覆盖且不会有任何警告。

.. option:: -v, --verbose

    生成更详细的输出。

.. option:: -q, --quiet

    生成较少的详细输出。
