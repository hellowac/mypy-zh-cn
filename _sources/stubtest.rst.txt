.. _stubtest:

.. program:: stubtest

自动化存根测试(Automatic stub testing)(stubtest)
====================================================

存根文件包含类型注解。有关更多动机和细节，请参阅
`PEP 484 <https://www.python.org/dev/peps/pep-0484/#stub-files>`_。

存根文件的一个常见问题是，它们往往会与实际实现产生差异。Mypy 包含了 ``stubtest`` 工具，可以自动检查存根与实际运行时实现之间的差异。

stubtest 的功能与限制(What stubtest does and does not do)
*********************************************************************

Stubtest 会导入您的代码，并在运行时检查代码对象，例如，使用 :py:mod:`inspect` 模块的功能。然后，stubtest 会分析存根文件，并将二者进行对比，指出存根与运行时实现之间的不同之处。

需要注意的是，这种比较方式有一定的局限性。Stubtest 不会尝试对您的实际代码进行静态分析，而是仅依赖于动态的运行时检查（特别是，这种方式使得 stubtest 在处理扩展模块时表现良好）。然而，这也意味着 stubtest 的可见性有限；例如，它无法判断函数的返回类型是否在存根中正确标注。

为了更清楚地说明，以下是 stubtest 无法做到的几点：

* 类型检查您的代码 —— 请使用 ``mypy`` 代替
* 生成存根 —— 请使用 ``stubgen`` 或 ``pyright --createstub`` 代替
* 基于运行您的应用程序或测试套件生成存根 —— 请使用 ``monkeytype`` 代替
* 将存根应用到代码中以生成内联类型 —— 请使用 ``retype`` 或 ``libcst`` 代替

总而言之，stubtest 非常适合用于确保存根与实现之间的基本一致性，或检查存根的完整性。它被用于测试 Python 官方库存根集合，`typeshed <https://github.com/python/typeshed>`_。

.. warning::

    stubtest 会导入并执行它检查的包中的 Python 代码。

示例(Example)
***************

下面是一个 stubtest 功能的简短示例：

.. code-block:: shell

    $ python3 -m pip install mypy

    $ cat library.py
    x = "hello, stubtest"

    def foo(x=None):
        print(x)

    $ cat library.pyi
    x: int

    def foo(x: int) -> None: ...

    $ python3 -m mypy.stubtest library
    error: library.foo is inconsistent, runtime argument "x" has a default value but stub argument does not
    Stub: at line 3
    def (x: builtins.int)
    Runtime: in file ~/library.py:3
    def (x=None)

    error: library.x variable differs from runtime type Literal['hello, stubtest']
    Stub: at line 1
    builtins.int
    Runtime:
    'hello, stubtest'


使用方法(Usage)
****************

运行 stubtest 可以像 ``stubtest module_to_check`` 一样简单。运行 :option:`stubtest --help` 查看选项的快速摘要。

Stubtest 必须能够导入要检查的代码，因此请确保 mypy 已安装在与要测试的库相同的环境中。在某些情况下，设置 ``PYTHONPATH`` 可以帮助 stubtest 找到要导入的代码。

同样，stubtest 必须能够找到要检查的存根文件。Stubtest 会遵循 ``MYPYPATH`` 环境变量——如果你收到类似“找不到存根”的报错，考虑使用此变量。

请注意，stubtest 需要 mypy 能够分析存根文件。如果 mypy 无法分析存根，可能会出现“由于 mypy 构建错误而无法检查存根”的错误。在这种情况下，你需要先解决这些错误，然后 stubtest 才能运行。尽管这里可能会有一些错误重叠，但 stubtest 并不是运行 mypy 的替代方案。

如果你希望忽略 stubtest 的某些警告，stubtest 提供了一个非常方便的允许列表（allowlist）系统。

本节余下部分记录了 stubtest 的命令行接口。

.. option:: --concise

    使 stubtest 的输出更简洁，每个错误只占一行。

.. option:: --ignore-missing-stub

    忽略存根缺少运行时存在的内容的错误。

.. option:: --ignore-positional-only

    忽略关于参数是否应该是仅限位置参数的错误。

.. option:: --allowlist FILE

    使用文件作为允许列表。可以多次传递以组合多个允许列表。允许列表可以使用 --generate-allowlist 创建，并支持正则表达式。

    允许列表中存在的条目意味着 stubtest 不会为相应的定义生成任何错误。

.. option:: --generate-allowlist

    打印允许列表（到标准输出），以配合 --allowlist 使用。

    在现有项目中引入 stubtest 时，这是静默所有现有错误的简单方法。

.. option:: --ignore-unused-allowlist

    忽略未使用的允许列表条目。

    如果未启用此选项，默认情况下 stubtest 会在允许列表条目不再需要时发出警告。

    请注意，如果允许列表条目是一个匹配空字符串的正则表达式，stubtest 永远不会认为它是未使用的。例如，为了对单个允许列表条目 ``foo.bar`` 获得 `--ignore-unused-allowlist` 的行为，你可以添加一个允许列表条目 ``(foo\.bar)?``。当错误仅发生在特定平台上时，这可能会很有用。

.. option:: --mypy-config-file FILE

    使用指定的 mypy 配置文件来确定 mypy 插件和 mypy 路径。

.. option:: --custom-typeshed-dir DIR

    使用 DIR 中的自定义 typeshed。

.. option:: --check-typeshed

    检查 typeshed 中的所有标准库模块。

.. option:: --help

    显示帮助信息 :-)
