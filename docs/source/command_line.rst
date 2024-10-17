.. _command-line:

.. program:: mypy

mypy命令行(command line)
===================================

本节记录了 mypy 的命令行接口。您可以通过运行 :option:`mypy --help` 查看可用标志的快速摘要。

.. note::

   命令行标志可能在不同版本之间发生变化。

指定类型检查的内容(what to type check)
***************************************

默认情况下，您可以通过传递希望 mypy 检查的路径来指定要进行类型检查的代码::

    $ mypy foo.py bar.py some_directory

请注意，目录会递归检查。

Mypy 还允许您以几种其他方式指定要进行类型检查的代码。以下是相关标志的简要总结；有关完整细节，请参见 :ref:`running-mypy`。

.. option:: -m MODULE, --module MODULE

    要求 mypy 对提供的模块进行类型检查。此标志可以重复多次。

    Mypy *不会* 递归检查提供的模块的任何子模块。

.. option:: -p PACKAGE, --package PACKAGE

    要求 mypy 对提供的包进行类型检查。此标志可以重复多次。

    Mypy *会* 递归检查提供的包的任何子模块。此标志的行为与 :option:`--module` 相同，除了这一点。

.. option:: -c PROGRAM_TEXT, --command PROGRAM_TEXT

    要求 mypy 对提供的字符串作为程序进行类型检查。

.. option:: --exclude

    一个正则表达式，用于匹配文件名、目录名和路径，mypy 在递归发现要检查的文件时应忽略这些匹配项。所有平台上均使用正斜杠。

    例如，为了避免发现任何名为 `setup.py` 的文件，您可以传递 ``--exclude '/setup\.py$'``。同样，您可以通过 e.g. ``--exclude /build/`` 忽略发现具有给定名称的目录，或者通过 ``--exclude /project/vendor/`` 忽略与子路径匹配的目录。要忽略多个文件/目录/路径，您可以多次提供 --exclude 标志，例如 ``--exclude '/setup\.py$' --exclude '/build/'``。

    请注意，此标志仅影响递归目录树发现，即当 mypy 在发现要检查的目录树或包的子模块中的文件时。如果您明确传递一个文件或模块，它仍然会被检查。例如，``mypy --exclude '/setup.py$'
    but_still_check/setup.py``。

    特别地，``--exclude`` 不影响 mypy 的 :ref:`导入跟踪 <follow-imports>`。您可以使用每个模块的 :confval:`follow_imports` 配置选项，进一步避免 mypy 跟踪导入并检查您不希望被检查的代码。

    请注意，mypy 永远不会递归发现名为 "site-packages"、"node_modules" 或 "__pycache__" 的文件和目录，或那些名称以句点开头的文件和目录，正如 ``--exclude
    '/(site-packages|node_modules|__pycache__|\..*)/$'`` 所示。Mypy 也不会递归发现扩展名不是 ``.py`` 或 ``.pyi`` 的文件。


可选参数(arguments)
***************************

.. option:: -h, --help

    显示帮助信息并退出。

.. option:: -v, --verbose

    显示更详细的信息。

.. option:: -V, --version

    显示程序的版本号并退出。

.. option:: -O FORMAT, --output FORMAT {json}

    设置自定义输出格式。

.. _config-file-flag:

配置文件(Config file)
***********************

.. option:: --config-file CONFIG_FILE

    此标志使 mypy 从指定文件读取配置设置。

    默认情况下，设置从当前目录中的 ``mypy.ini``, ``.mypy.ini``, ``pyproject.toml`` 或 ``setup.cfg`` 读取。设置会覆盖 mypy 的内置默认值，命令行标志也可以覆盖设置。

    指定 :option:`--config-file= <--config-file>` （不带文件名）将忽略 *所有* 配置文件。

    请参见 :ref:`config-file` 了解配置文件的语法。

.. option:: --warn-unused-configs

    此标志使 mypy 对未使用的 ``[mypy-<pattern>]`` 配置文件部分发出警告。
    （这需要使用 :option:`--no-incremental` 关闭增量模式。）


.. _import-discovery:

导入发现(Import discovery)
********************************

以下标志自定义 mypy 如何发现和跟踪导入。

.. option:: --explicit-package-bases

    此标志告诉 mypy 顶级包将基于当前目录、``MYPYPATH`` 环境变量或 :confval:`mypy_path` 配置选项的某个成员。此选项仅在缺少 `__init__.py` 的情况下有用。有关详细信息，请参见 :ref:`Mapping file paths to modules <mapping-paths-to-modules>`。

.. option:: --ignore-missing-imports

    此标志使 mypy 忽略所有缺失的导入。它等同于在代码库中所有未解析的导入上添加 ``# type: ignore`` 注释。

    请注意，此标志 *不* 会抑制关于成功解析的模块中缺失名称的错误。例如，如果有以下文件::

        package/__init__.py
        package/mod.py

    那么 mypy 在使用 :option:`--ignore-missing-imports` 时会生成以下错误：

    .. code-block:: python

        import package.unknown      # 无错误，被忽略
        x = package.unknown.func()  # OK. 'func' 被假定为类型 'Any'

        from package import unknown          # 无错误，被忽略
        from package.mod import NonExisting  # 错误：模块没有属性 'NonExisting'

    有关更多详细信息，请参见 :ref:`ignore-missing-imports`。

.. option:: --follow-imports {normal,silent,skip,error}

    此标志调整 mypy 跟踪未通过命令行显式传递的导入模块的方式。

    默认选项为 ``normal``：mypy 将跟踪并类型检查所有模块。有关其他选项的更多信息，请参见 :ref:`Following imports <follow-imports>`。

.. option:: --python-executable EXECUTABLE

    此标志将使 mypy 从为 Python 可执行文件 ``EXECUTABLE`` 安装的 :pep:`561` 兼容包中收集类型信息。如果未提供，mypy 将使用为运行 mypy 的 Python 可执行文件安装的 PEP 561 兼容包。

    有关如何制作 PEP 561 兼容包的更多信息，请参见 :ref:`installed-packages`。

.. option:: --no-site-packages

    此标志将禁用搜索 :pep:`561` 兼容包。这也将禁用搜索可用的 Python 可执行文件。

    如果 mypy 无法为正在检查的 Python 版本找到 Python 可执行文件，并且您不需要使用 PEP 561 类型的包，则使用此标志。否则，请使用 :option:`--python-executable`。

.. option:: --no-silence-site-packages

    默认情况下，mypy 会抑制在 :pep:`561` 兼容包内生成的任何错误消息。添加此标志将禁用此行为。

.. option:: --fast-module-lookup

    用于扫描搜索路径以解析导入的默认逻辑在某些情况下具有二次最坏情况的行为，例如，当大量文件夹共享顶级命名空间时，如下所示::

        foo/
            company/
                foo/
                    a.py
        bar/
            company/
                bar/
                    b.py
        baz/
            company/
                baz/
                    c.py
        ...

    如果您处于这种情况，可以通过设置 :option:`--fast-module-lookup` 选项来启用实验性的快速路径。

.. option:: --no-namespace-packages

    此标志禁用命名空间包的导入发现（见 :pep:`420`）。特别是，这会阻止发现没有 ``__init__.py`` （或 ``__init__.pyi`` ）文件的包。

    此标志影响 mypy 如何查找命令行中显式传递的模块和包。它还影响 mypy 如何确定命令行中传递的文件的完全限定模块名称。有关详细信息，请参见 :ref:`映射文件路径到模块 <mapping-paths-to-modules>`。


.. _platform-configuration:

平台配置(Platform configuration)
**************************************

默认情况下，mypy 会假定您打算在与运行 mypy 本身相同的操作系统和 Python 版本上运行代码。以下标志允许您修改此行为。

有关如何使用这些标志的更多信息，请参见 :ref:`version_and_platform_checks`。

.. option:: --python-version X.Y

    此标志将使 mypy 将您的代码类型检查为在 Python 版本 X.Y 下运行。未使用此选项时，mypy 默认使用运行 mypy 的 Python 版本。

    此标志将尝试查找对应版本的 Python 可执行文件，以搜索 :pep:`561` 兼容包。如果您希望禁用此功能，请使用 :option:`--no-site-packages` 标志（有关更多详细信息，请参见 :ref:`import-discovery`）。

.. option:: --platform PLATFORM

    此标志将使 mypy 将您的代码类型检查为在给定操作系统下运行。未使用此选项时，mypy 默认使用您当前使用的操作系统。

    ``PLATFORM`` 参数可以是 :py:data:`sys.platform` 支持的任何字符串。

.. _always-true:

.. option:: --always-true NAME

    此标志将把所有名为 ``NAME`` 的变量视为总是为真的编译时常量。此标志可以重复使用。

.. option:: --always-false NAME

    此标志将把所有名为 ``NAME`` 的变量视为总是为假的编译时常量。此标志可以重复使用。


.. _disallow-dynamic-typing:

禁止动态类型(Disallow dynamic typing)
**************************************

``Any`` 类型用于表示具有 :ref:`dynamic type <dynamic-typing>` 的值。``--disallow-any`` 系列标志将禁止在模块中以各种方式使用 ``Any`` 类型——这让我们能够以受控的方式战略性地禁止动态类型的使用。

以下选项可用：

.. option:: --disallow-any-unimported

    此标志禁止使用来自未跟踪导入的类型（此类类型变为 ``Any`` 的别名）。未跟踪导入发生在导入的模块不存在或设置了 :option:`--follow-imports=skip <--follow-imports>` 时。

.. option:: --disallow-any-expr

    此标志禁止模块中所有类型为 ``Any`` 的表达式。如果类型为 ``Any`` 的表达式在模块中的任何地方出现，mypy 将输出错误，除非该表达式立即用作 :py:func:`~typing.cast` 的参数或赋值给具有显式类型注释的变量。

    此外，声明类型为 ``Any`` 的变量或转换为类型 ``Any`` 也是不允许的。请注意，调用参数类型为 ``Any`` 的函数仍然是允许的。

.. option:: --disallow-any-decorated

    此标志禁止在装饰器转换后签名中包含 ``Any`` 的函数。

.. option:: --disallow-any-explicit

    此标志禁止在类型位置中显式使用 ``Any``，如类型注释和泛型类型参数。

.. option:: --disallow-any-generics

    此标志禁止使用未指定显式类型参数的泛型类型。例如，您不能使用裸的 ``x: list``。相反，您必须始终写成 ``x: list[int]``。

.. option:: --disallow-subclassing-any

    此标志在类继承类型为 ``Any`` 的值时报告错误。这可能发生在基类从不存在的模块中导入（使用 :option:`--ignore-missing-imports`）或由于 :option:`--follow-imports=skip <--follow-imports>` 或 ``import`` 语句上的 ``# type: ignore`` 注释而被忽略。

    由于模块被静默处理，导入的类被赋予类型 ``Any``。默认情况下，mypy 会假定子类正确继承了基类，即使实际上可能并非如此。此标志使 mypy 报告错误。

.. _untyped-definitions-and-calls:

未类型化的定义和调用(Untyped definitions and calls)
*****************************************************

以下标志配置 mypy 如何处理未类型化的函数定义或调用。

.. option:: --disallow-untyped-calls

    此标志在函数带有类型注解的情况下，报告调用未定义注解的函数时的错误。

.. option:: --untyped-calls-exclude

    此标志允许有选择性地禁用 :option:`--disallow-untyped-calls`，适用于特定包、模块或类中定义的函数和方法。请注意，每个排除条目作为前缀起作用。例如（假设没有可用的 ``third_party_lib`` 的类型注解）：

    .. code-block:: python

        # mypy --disallow-untyped-calls
        #      --untyped-calls-exclude=third_party_lib.module_a
        #      --untyped-calls-exclude=foo.A
        from third_party_lib.module_a import some_func
        from third_party_lib.module_b import other_func
        import foo

        some_func()  # OK，函数来自模块 `third_party_lib.module_a`
        other_func()  # E: 在类型上下文中调用未类型化函数 "other_func"

        foo.A().meth()  # OK，方法在类 `foo.A` 中定义
        foo.B().meth()  # E: 在类型上下文中调用未类型化函数 "meth"

        # file foo.py
        class A:
            def meth(self): pass
        class B:
            def meth(self): pass

.. option:: --disallow-untyped-defs

    此标志在遇到没有类型注解或带有不完整类型注解的函数定义时报告错误。
    （是 :option:`--disallow-incomplete-defs` 的超集）。

    例如，它会对 :code:`def f(a, b)` 和 :code:`def f(a: int, b)` 报告错误。

.. option:: --disallow-incomplete-defs

    此标志在遇到部分注解的函数定义时报告错误，同时仍允许完全未注解的定义。

    例如，它会对 :code:`def f(a: int, b)` 报告错误，但不会对 :code:`def f(a, b)` 报告错误。

.. option:: --check-untyped-defs

    此标志的严厉程度低于前两个选项——它对每个函数的主体进行类型检查，无论其是否有类型注解。
    （默认情况下，未注解的函数主体不进行类型检查。）

    它将假定所有参数的类型为 ``Any``，并始终推断返回类型为 ``Any``。

.. option:: --disallow-untyped-decorators

    此标志在带有类型注解的函数被未注解的装饰器装饰时报告错误。


.. _none-and-optional-handling:

None 和 Optional 处理(None and Optional handling)
****************************************************

以下标志调整 mypy 如何处理类型为 ``None`` 的值。

.. _implicit-optional:

.. option:: --implicit-optional

    此标志使 mypy 将默认值为 ``None`` 的参数视为具有隐式可选类型（``T | None``）。

    例如，如果设置了此标志，mypy 将假定下面代码片段中的 ``x`` 参数实际上是类型 ``int | None``，因为默认参数为 ``None``：

    .. code-block:: python

        def foo(x: int = None) -> None:
            print(x)

    **注意：** 从 mypy 0.980 开始，此功能默认禁用。

.. _no_strict_optional:

.. option:: --no-strict-optional

    此标志有效地禁用可选类型和 ``None`` 值的检查。使用此选项时，mypy 通常不检查 ``None`` 值的使用——它被视为与每种类型兼容。

    .. warning::

        ``--no-strict-optional`` 是有害的。避免使用它，并且绝对不要在不理解其作用的情况下使用它。


.. _configuring-warnings:

配置警告(Configuring warnings)
****************************************

以下标志为合理但在某种程度上可能存在问题或冗余的代码启用警告。

.. option:: --warn-redundant-casts

    此标志将使 mypy 在代码使用可以安全删除的不必要类型转换时报告错误。

.. option:: --warn-unused-ignores

    此标志将使 mypy 在代码中使用不实际生成错误消息的 ``# type: ignore`` 注释时报告错误。

    此标志与 :option:`--warn-redundant-casts` 标志特别有用，尤其是在您升级 mypy 时。之前，您可能需要添加类型转换或 ``# type: ignore`` 注释，以解决 mypy 中的错误或缺少第三方库的存根。

    这两个标志使您能够发现这些解决方法不再必要的情况。

.. option:: --no-warn-no-return

    默认情况下，当函数在某些执行路径中缺少返回语句时，mypy 将生成错误。唯一的例外是：

    -   函数具有 ``None`` 或 ``Any`` 返回类型
    -   函数具有空主体并被标记为抽象方法、位于协议类中或在存根文件中
    -   执行路径永远不会返回；例如，如果总是引发异常

    传入 :option:`--no-warn-no-return` 将在所有情况下禁用这些错误消息。

.. option:: --warn-return-any

    此标志会使 mypy 在从声明为非 ``Any`` 返回类型的函数中返回类型为 ``Any`` 的值时生成警告。

.. option:: --warn-unreachable

    此标志将在 mypy 遇到经过类型分析确定为不可达或冗余的代码时报告错误。这是一种检测代码中某些类型的错误的有效方式。

    例如，启用此标志将使 mypy 报告 ``x > 7`` 检查是冗余的，并且下面的 ``else`` 块是不可达的。

    .. code-block:: python

        def process(x: int) -> None:
            # 错误：或运算符的右操作数从未被求值
            if isinstance(x, int) or x > 7:
                # 错误：对 + 的不支持操作数类型（"int" 和 "str"）
                print(x + "bad")
            else:
                # 错误：'语句不可达' 错误
                print(x + "bad")

    为了防止 mypy 生成虚假的警告，"语句不可达" 警告将在以下两种情况下被抑制：

    1.  当不可达语句是 ``raise`` 语句、``assert False`` 语句，或调用具有 :py:data:`~typing.NoReturn` 返回类型提示的函数时。换句话说，当不可达语句抛出错误或以某种方式终止程序时。
    2.  当不可达语句被 *故意* 标记为不可达时，使用 :ref:`version_and_platform_checks`。

    .. note::

        当前，mypy 无法检测和报告任何使用 :ref:`type-variable-value-restriction` 的函数中的不可达或冗余代码。

        此限制将在未来的 mypy 版本中移除。

.. option:: --report-deprecated-as-error

    默认情况下，如果您的代码导入或使用了已弃用的特性，mypy 会发出说明。此标志将此类说明转换为错误，导致 mypy 最终以非零退出代码结束。当特性被标记为 ``warnings.deprecated`` 时，视为已弃用。

.. _miscellaneous-strictness-flags:

其他严格性标志(Miscellaneous strictness flags)
***************************************************

本节记录了任何不完全适合上述任何部分的其他标志。

.. option:: --allow-untyped-globals

    此标志使 mypy 抑制由于无法完全推断全局和类变量类型而导致的错误。

.. option:: --allow-redefinition

    默认情况下，mypy 不允许用无关类型重新定义变量。此标志允许在某些上下文中使用任意类型重新定义变量：仅允许在与原始定义相同的块和嵌套深度内进行重新定义。以下示例展示了这种情况的有用性：

    .. code-block:: python

       def process(items: list[str]) -> None:
           # 'items' 的类型是 list[str]
           items = [item.split() for item in items]
           # 'items' 现在的类型是 list[list[str]]

    变量必须在重新定义之前使用：

    .. code-block:: python

        def process(items: list[str]) -> None:
           items = "mypy"  # 无效的重新定义为 str，因为变量尚未使用
           print(items)
           items = "100"  # 有效，items 现在的类型是 str
           items = int(items)  # 有效，items 现在的类型是 int

.. option:: --local-partial-types

    在 mypy 中，部分类型最常见的情况是使用 ``None`` 初始化的变量，但没有显式的 ``X | None`` 注释。默认情况下，mypy 不会检查跨模块顶层或类顶层的部分类型。此标志更改行为，仅允许在本地级别进行部分类型，因此不允许从不同作用域中的两个赋值推断 ``None`` 的变量类型。例如：

    .. code-block:: python

        a = None  # 如果使用 --local-partial-types，这里需要类型注释
        b: int | None = None

        class Foo:
            bar = None  # 如果使用 --local-partial-types，这里需要类型注释
            baz: int | None = None

            def __init__(self) -> None:
                self.bar = 1

        reveal_type(Foo().bar)  # 'int | None'，在没有 --local-partial-types 的情况下

    注意：此选项在 mypy 守护进程中始终隐式启用，并将在未来的 mypy 版本中默认启用。

.. option:: --no-implicit-reexport

    默认情况下，导入到模块的值被视为已导出，mypy 允许其他模块导入它们。此标志更改行为，仅在使用 from-as 导入或包含在 ``__all__`` 中时才重新导出项。注意，这在存根文件中始终视为启用。例如：

    .. code-block:: python

       # 这不会重新导出该值
       from foo import bar

       # 这也不会
       from foo import bar as bang

       # 这将以 bar 重新导出，并允许其他模块导入它
       from foo import bar as bar

       # 这也会重新导出 bar
       from foo import bar
       __all__ = ['bar']

.. option:: --strict-equality

    默认情况下，mypy 允许总是为假的比较，例如 ``42 == 'no'``。使用此标志禁止此类不同类型的比较，以及类似的身份和容器检查：

    .. code-block:: python

       items: list[int]
       if 'some string' in items:  # 错误：非重叠容器检查！
           ...

       text: str
       if text != b'other bytes':  # 错误：非重叠相等检查！
           ...

       assert text is not None  # OK，检查 None 被允许作为特殊情况。

.. option:: --extra-checks

    此标志启用技术上正确但在实际代码中可能不切实际的额外检查。特别是，它禁止在 ``TypedDict`` 更新中的部分重叠，并使通过 ``Concatenate`` 预置的参数仅限于位置参数。例如：

    .. code-block:: python

       from typing import TypedDict

       class Foo(TypedDict):
           a: int

       class Bar(TypedDict):
           a: int
           b: int

       def test(foo: Foo, bar: Bar) -> None:
           # 这在技术上是不安全的，因为 foo 可以在运行时具有 Foo 的子类型，
           # 其中键 "b" 的类型与 int 不兼容，见下文
           bar.update(foo)

       class Bad(Foo):
           b: str
       bad: Bad = {"a": 0, "b": "no"}
       test(bad, bar)

.. option:: --strict

    此标志模式启用所有可选错误检查标志。您可以在完整的 :option:`mypy --help` 输出中查看严格模式启用的标志列表。

    注意：通过运行 :option:`--strict` 启用的标志的确切列表可能会随时间而变化。

.. option:: --disable-error-code

    此标志允许全局禁用一个或多个错误代码。有关更多信息，请参见 :ref:`error-codes`。

    .. code-block:: python

        # 无标志
        x = 'a string'
        x.trim()  # 错误：“str”没有属性“trim”  [attr-defined]

        # 当使用 --disable-error-code attr-defined 时
        x = 'a string'
        x.trim()

.. option:: --enable-error-code

    此标志允许全局启用一个或多个错误代码。有关更多信息，请参见 :ref:`error-codes`。

    注意：此标志将覆盖来自 :option:`--disable-error-code <mypy --disable-error-code>` 标志的禁用错误代码。

    .. code-block:: python

        # 当使用 --disable-error-code attr-defined 时
        x = 'a string'
        x.trim()

        # --disable-error-code attr-defined --enable-error-code attr-defined
        x = 'a string'
        x.trim()  # 错误：“str”没有属性“trim”  [attr-defined]

.. _configuring-error-messages:

配置错误消息(Configuring error messages)
********************************************

以下标志允许您调整 mypy 在错误消息中显示的详细程度。

.. option:: --show-error-context

    此标志将在所有错误前添加“注释”消息，解释错误的上下文。例如，考虑以下程序：

    .. code-block:: python

        class Test:
            def foo(self, x: int) -> int:
                return x + "bar"

    Mypy 通常显示的错误消息如下所示::

        main.py:3: error: Unsupported operand types for + ("int" and "str")

    如果启用此标志，错误消息现在如下所示::

        main.py: note: In member "foo" of class "Test":
        main.py:3: error: Unsupported operand types for + ("int" and "str")

.. option:: --show-column-numbers

    此标志将向错误消息添加列偏移量。
    例如，以下指示在第 12 行第 9 列的错误
    （注意，列偏移量是 0 基的）::

        main.py:12:9: error: Unsupported operand types for / ("int" and "str")

.. option:: --show-error-code-links

    此标志还将显示指向错误代码文档的链接，链接到 mypy 报告的错误代码。
    相应的错误代码将在文档页面中高亮显示。
    如果启用此标志，错误消息现在如下所示::

        main.py:3: error: Unsupported operand types for - ("int" and "str")  [operator]
        main.py:3: note: See 'https://mypy.rtfd.io/en/stable/_refs.html#code-operator' for more info

.. option:: --show-error-end

    此标志将使 mypy 显示错误被检测到的起始位置，以及相关表达式的结束位置。
    这样，各种工具可以轻松突出显示整个错误跨度。格式为
    ``file:line:column:end_line:end_column``。此选项隐含
    ``--show-column-numbers``。

.. option:: --hide-error-codes

    此标志将从错误消息中隐藏错误代码 ``[<code>]``。默认情况下，错误
    代码在每个错误消息后显示::

        prog.py:1: error: "str" has no attribute "trim"  [attr-defined]

    有关更多信息，请参见 :ref:`error-codes`。

.. option:: --pretty

    在错误消息中使用更美观的输出：使用软换行，
    显示源代码片段，并显示错误位置标记。

.. option:: --no-color-output

    此标志将禁用错误消息中的颜色输出，默认情况下启用。

.. option:: --no-error-summary

    此标志将禁用错误摘要。默认情况下，mypy 显示一行摘要
    包括错误总数、包含错误的文件数量和检查的文件数量。

.. option:: --show-absolute-path

    显示文件的绝对路径。

.. option:: --soft-error-limit N

    此标志将调整 mypy 在此之后（有时）禁用报告大多数附加错误的限制。仅在似乎
    大多数剩余错误可能不太有用或可能过于嘈杂时，限制才适用。如果 ``N`` 为负数，则没有限制。默认限制为 -1。

.. option:: --force-uppercase-builtins

    始终在错误消息中使用 ``List`` 而不是 ``list``，
    即使在 Python 3.9+ 中。

.. option:: --force-union-syntax

    始终在错误消息中使用 ``Union[]`` 和 ``Optional[]`` 表示联合类型
    （而不是 ``|`` 运算符），
    即使在 Python 3.10+ 中。


.. _incremental:

增量模式(Incremental mode)
********************************

默认情况下，mypy 会将类型信息存储到缓存中。Mypy 将使用这些信息以避免在再次类型检查代码时进行不必要的重新计算。这可以帮助加快类型检查过程，尤其是在自上次 mypy 运行以来，大部分程序部分没有改变的情况下。

如果您希望加快重新检查代码的速度，超出增量模式所能提供的范围，可以尝试在 :ref:`daemon mode <mypy_daemon>` 中运行 mypy。

.. option:: --no-incremental

    此标志禁用增量模式：mypy 将不再在重新运行时引用缓存。

    请注意，即使禁用增量模式，mypy 仍然会写入缓存：有关更多详细信息，请参见下面的 :option:`--cache-dir` 标志。

.. option:: --cache-dir DIR

    默认情况下，mypy 将所有缓存数据存储在当前目录下名为 ``.mypy_cache`` 的文件夹中。此标志允许您更改该文件夹。此标志在使用 :ref:`remote caching <remote-cache>` 时也可以用于控制缓存的使用。

    如果设置了该选项，则此设置将覆盖 ``MYPY_CACHE_DIR`` 环境变量。

    即使禁用增量模式，mypy 仍然会始终写入缓存，以便“预热”缓存。要禁用写入缓存，请使用 ``--cache-dir=/dev/null`` （UNIX）或 ``--cache-dir=nul`` （Windows）。

.. option:: --sqlite-cache

    使用 `SQLite`_ 数据库来存储缓存。

.. option:: --cache-fine-grained

    在 mypy 守护进程的缓存中包含细粒度的依赖信息。

.. option:: --skip-version-check

    默认情况下，mypy 将忽略由不同版本的 mypy 生成的缓存数据。此标志禁用该行为。

.. option:: --skip-cache-mtime-checks

    跳过基于 mtime 的缓存内部一致性检查。

高级选项(Advanced options)
********************************

以下标志主要适用于有兴趣开发或调试 mypy 内部的人。

.. option:: --pdb

    当 mypy 遇到致命错误时，此标志将调用 Python 调试器。

.. option:: --show-traceback, --tb

    如果设置，此标志将在 mypy 遇到致命错误时显示完整的回溯信息。

.. option:: --raise-exceptions

    在致命错误时引发异常。

.. option:: --custom-typing-module MODULE

    此标志允许您使用自定义模块替代 :py:mod:`typing` 模块。

.. option:: --custom-typeshed-dir DIR

    此标志指定 mypy 查找标准库 typeshed 存根的目录，而不是与 mypy 一起提供的 typeshed。这主要是为了便于在提交变更之前测试 typeshed 的更改，但也允许您使用一个分叉版本的 typeshed。

    请注意，这不会影响第三方库的存根。要测试第三方存根，例如可以尝试 ``MYPYPATH=stubs/six mypy ...``。

.. _warn-incomplete-stub:

.. option:: --warn-incomplete-stub

    此标志修改 :option:`--disallow-untyped-defs` 和
    :option:`--disallow-incomplete-defs` 标志，以便在 typeshed 中缺少类型注释或具有不完整注释时也报告错误。如果两个标志都缺失，:option:`--warn-incomplete-stub` 也不会执行任何操作。

    此标志主要供希望贡献 typeshed 的人使用，以便方便地查找缺口和遗漏。

    如果您希望 mypy 在代码库 *使用* 未类型化的函数时报告错误，无论该函数是否在 typeshed 中定义，请使用 :option:`--disallow-untyped-calls` 标志。有关更多详细信息，请参见 :ref:`untyped-definitions-and-calls`。

.. _shadow-file:

.. option:: --shadow-file SOURCE_FILE SHADOW_FILE

    当请求 mypy 对 ``SOURCE_FILE`` 进行类型检查时，此标志使 mypy 从 ``SHADOW_FILE`` 读取并进行类型检查。然而，诊断仍将引用 ``SOURCE_FILE``。

    多次指定此参数（``--shadow-file X1 Y1 --shadow-file X2 Y2``）将允许 mypy 执行多个替换。

    这允许工具创建临时文件并进行有用的修改，而不必直接更改源文件。例如，假设我们有一个管道为某些变量添加 ``reveal_type``。这个管道在 ``original.py`` 上运行以生成 ``temp.py``。运行 ``mypy --shadow-file original.py temp.py original.py`` 将导致 mypy 对 ``temp.py`` 的内容进行类型检查，而不是 ``original.py``，但错误消息仍将引用 ``original.py``。


报告生成(Report generation)
**********************************

如果设置了这些标志，mypy 将在指定目录中以指定格式生成报告。

.. option:: --any-exprs-report DIR

    使 mypy 生成一个文本文件报告，记录代码库中存在多少类型为 ``Any`` 的表达式。

.. option:: --cobertura-xml-report DIR

    使 mypy 生成一个 Cobertura XML 类型检查覆盖率报告。

    要生成此报告，您必须手动安装 `lxml`_ 库，或指定带有 setuptools 附加项 ``mypy[reports]`` 的 mypy 安装。

.. option:: --html-report / --xslt-html-report DIR

    使 mypy 生成一个 HTML 类型检查覆盖率报告。

    要生成此报告，您必须手动安装 `lxml`_ 库，或指定带有 setuptools 附加项 ``mypy[reports]`` 的 mypy 安装。

.. option:: --linecount-report DIR

    使 mypy 生成一个文本文件报告，记录代码库中已类型化和未类型化的函数及行数。

.. option:: --linecoverage-report DIR

    使 mypy 生成一个 JSON 文件，将每个源文件的绝对文件名映射到该文件中类型化函数所属的行号列表。

.. option:: --lineprecision-report DIR

    使 mypy 生成一个平面文本文件报告，包含每个模块的统计信息，例如有多少行被类型检查等。

.. option:: --txt-report / --xslt-txt-report DIR

    使 mypy 生成一个文本文件类型检查覆盖率报告。

    要生成此报告，您必须手动安装 `lxml`_ 库，或指定带有 setuptools 附加项 ``mypy[reports]`` 的 mypy 安装。

.. option:: --xml-report DIR

    使 mypy 生成一个 XML 类型检查覆盖率报告。

    要生成此报告，您必须手动安装 `lxml`_ 库，或指定带有 setuptools 附加项 ``mypy[reports]`` 的 mypy 安装。

启用不完整/实验性功能(Enabling incomplete/experimental features)
*****************************************************************

.. option:: --enable-incomplete-feature {PreciseTupleTypes, InlineTypedDict}

    某些功能可能需要多个 mypy 版本才能实现，例如由于其复杂性、潜在的向后不兼容性或模糊的语义，这些都需要来自社区的反馈。您可以使用此标志启用这些功能以供早期预览。请注意，并不能保证所有功能最终都会默认启用。在 *少数情况下*，我们可能决定不继续某些功能。

当前不完整/实验性功能列表：

* ``PreciseTupleTypes``：此功能将在各种场景中推断更精确的元组类型。在 :pep:`646` 添加可变参数类型到 Python 类型系统之前，无法表达像“一个包含至少两个整数的元组”这样的类型。可用的最佳类型是 ``tuple[int, ...]``。因此，mypy 对可变长度元组进行了非常宽松的检查。现在，这种类型可以表示为 ``tuple[int, int, *tuple[int, ...]]``。对于这些更精确的类型（当由用户显式 *定义* 时），mypy 例如会警告不安全的索引访问，并一般以类型安全的方式处理它们。然而，为了避免现有代码中的问题，mypy 在技术上能够推断这些精确类型时并不会 *推断* 这些类型。以下是 ``PreciseTupleTypes`` 推断更精确类型的显著示例：

  .. code-block:: python

     numbers: tuple[int, ...]

     more_numbers = (1, *numbers, 1)
     reveal_type(more_numbers)
     # Without PreciseTupleTypes: tuple[int, ...]
     # With PreciseTupleTypes: tuple[int, *tuple[int, ...], int]

     other_numbers = (1, 1) + numbers
     reveal_type(other_numbers)
     # Without PreciseTupleTypes: tuple[int, ...]
     # With PreciseTupleTypes: tuple[int, int, *tuple[int, ...]]

     if len(numbers) > 2:
         reveal_type(numbers)
         # Without PreciseTupleTypes: tuple[int, ...]
         # With PreciseTupleTypes: tuple[int, int, int, *tuple[int, ...]]
     else:
         reveal_type(numbers)
         # Without PreciseTupleTypes: tuple[int, ...]
         # With PreciseTupleTypes: tuple[()] | tuple[int] | tuple[int, int]

* ``InlineTypedDict``：此功能启用非标准语法的内联 :ref:`TypedDicts <typeddict>`，例如：

  .. code-block:: python

     def test_values() -> {"int": int, "str": str}:
         return {"int": 42, "str": "test"}


杂项(Miscellaneous)
**************************

.. option:: --install-types

    此标志使 mypy 使用 pip 安装第三方库中已知缺失的存根包。它将显示将要运行的 pip 命令，并在安装任何内容之前期望确认。出于安全原因，这些存根仅限于一小部分经过类型仓库团队验证的手动选择包。这些包仅包含存根文件，不包含可执行代码。

    如果您使用此选项而不提供任何要类型检查的文件或模块，mypy 将安装在上次 mypy 运行期间建议的存根包。如果有要类型检查的文件或模块，mypy 首先对这些文件进行类型检查，并在运行结束时建议安装缺失的存根，但仅在检测到任何缺失模块的情况下。

    .. note::

        这是 mypy 0.900 中的新功能。之前的 mypy 版本包括一系列第三方包存根，而不是单独安装它们。

.. option:: --non-interactive

   当与 :option:`--install-types <mypy --install-types>` 一起使用时，此选项将导致 mypy 使用 pip 安装所有建议的存根包，而无需确认，然后继续使用已安装的存根进行类型检查，如果提供了一些文件或模块进行检查。

   这在内部实现为最多两次 mypy 运行。第一次运行用于查找缺失的存根包，仅当未找到缺失的存根包时才显示此运行的输出。如果找到缺失的存根包，将进行安装，然后再进行一次运行。

.. option:: --junit-xml JUNIT_XML

    使 mypy 生成一个包含类型检查结果的 JUnit XML 测试结果文档。这可以使 mypy 更容易与持续集成 (CI) 工具集成。

.. option:: --find-occurrences CLASS.MEMBER

    此标志将使 mypy 打印出基于静态类型信息的类成员的所有用法。此功能仍处于实验阶段。

.. option:: --scripts-are-modules

    此标志将给出看起来像脚本的命令行参数（即文件名不以 ``.py`` 结尾），而是从脚本名称派生的模块名称，而不是固定名称 :py:mod:`__main__`。

    这使您可以在一次 mypy 调用中检查多个脚本。（默认的 :py:mod:`__main__` 从技术上讲更为准确，但如果您有许多导入大型包的脚本，则此标志启用的行为通常更方便。）

.. _lxml: https://pypi.org/project/lxml/
.. _SQLite: https://www.sqlite.org/
