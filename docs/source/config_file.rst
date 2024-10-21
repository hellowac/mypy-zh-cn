.. _config-file:

mypy 配置文件(mypy configuration file)
==========================================

Mypy 具有很高的可配置性。这在将类型引入现有代码库时尤其有用。有关该情况的具体建议，请参见 :ref:`existing-code`。

Mypy 支持从文件读取配置设置，优先顺序如下：

    1. ``./mypy.ini``
    2. ``./.mypy.ini``
    3. ``./pyproject.toml``
    4. ``./setup.cfg``
    5. ``$XDG_CONFIG_HOME/mypy/config``
    6. ``~/.config/mypy/config``
    7. ``~/.mypy.ini``

重要的是要理解，配置文件不会合并，因为这会导致歧义。命令行标志 :option:`--config-file <mypy --config-file>` 具有最高优先级，必须正确；否则 mypy 将报告错误并退出。在没有命令行选项的情况下，mypy 将按上述优先顺序查找配置文件。

大多数标志与 :ref:`命令行标志 <command-line>` 密切对应，但在标志名称上存在一些差异，有些标志可能根据正在处理的模块采用不同的值。

一些标志支持用户主目录和环境变量扩展。要引用用户主目录，请在路径开头使用 ``~``。要扩展环境变量，请使用 ``$VARNAME`` 或 ``${VARNAME}``。

配置文件格式(Config file format)
**********************************

配置文件格式是常见的 :doc:`ini 文件 <python:library/configparser>` 格式。它应包含方括号中的部分名称和形式为 `NAME = VALUE` 的标志设置。注释以 ``#`` 字符开头。

- 必须存在名为 ``[mypy]`` 的部分。这指定了全局标志。

- 还可以存在名为 ``[mypy-PATTERN1,PATTERN2,...]`` 的附加部分，其中 ``PATTERN1``、``PATTERN2`` 等是完全限定模块名称的逗号分隔模式，某些组件可以用 '*' 字符替代（例如 ``foo.bar``、``foo.bar.*``、``foo.*.baz`` )。这些部分指定仅适用于模块名称匹配至少一个模式的附加标志。

  形式为 ``qualified_module_name`` 的模式仅匹配命名模块，而 ``dotted_module_name.*`` 匹配 ``dotted_module_name`` 和任何子模块（因此 ``foo.bar.*`` 会匹配 ``foo.bar``、``foo.bar.baz`` 和 ``foo.bar.baz.quux`` )。

  模式也可以是“非结构化”的通配符，其中星号可以出现在名称的中间（例如 ``site.*.migrations.*`` )。星号匹配零个或多个模块组件（因此 ``site.*.migrations.*`` 可以匹配 ``site.migrations`` )。

  .. _config-precedence:

  当选项冲突时，配置的优先顺序为：

    1. 在源文件中的 :ref:`内联配置 <inline-config>` 
    2. 具有具体模块名称的部分( ``foo.bar`` )
    3. 具有“非结构化”通配符模式的部分( ``foo.*.baz`` )，
       在配置文件中后面的部分覆盖前面的部分。
    4. 具有“结构化”通配符模式的部分( ``foo.bar.*`` )，
       更具体的部分覆盖更一般的部分。
    5. 命令行选项。
    6. 顶层配置文件选项。

“结构化”模式（按特异性）和“非结构化”模式（按文件中的顺序）之间的优先级差异是不幸的，并且在未来版本中可能会改变。

.. note::

   :confval:`warn_unused_configs` 标志可能对调试拼写错误的部分名称有用。

.. note::

   配置标志在不同版本之间可能会发生变化。


单个模块和全局选项(Per-module and global options)
**************************************************

某些配置选项可以全局设置（在 ``[mypy]`` 部分）或逐模块设置（在 ``[mypy-foo.bar]`` 这样的部分）。

如果您同时为全局和特定模块设置了选项，模块配置选项将具有优先权。这使您能够设置全局默认值并在逐模块的基础上覆盖它们。如果多个模式部分与某个模块匹配，:ref:`将使用最具体部分的选项 <config-precedence>`，以解决不一致的地方。

一些其他选项，如其描述中所述，仅能在全局部分( ``[mypy]`` )中设置。


反转选项值(Inverting option values)
************************************

取布尔值的选项可以通过在名称前加 ``no_`` 或（在适用时）将前缀从 ``disallow`` 变更为 ``allow`` （反之亦然）来反转。


``mypy.ini`` 示例 (Example)
******************************

以下是一个 ``mypy.ini`` 文件的示例。要使用此配置文件，请将其放置在您代码库的根目录下并运行 mypy。

.. code-block:: ini

    # 全局选项：

    [mypy]
    warn_return_any = True
    warn_unused_configs = True

    # 每模块选项：

    [mypy-mycode.foo.*]
    disallow_untyped_defs = True

    [mypy-mycode.bar]
    warn_return_any = False

    [mypy-somelibrary]
    ignore_missing_imports = True

此配置文件在 ``[mypy]`` 部分指定了两个全局选项。这两个选项将：

1.  在函数返回被推断为类型 ``Any`` 的值时报告错误。

2.  报告 mypy 未使用的任何配置选项。（这将帮助我们在更改配置文件时捕捉拼写错误）。

接下来，此模块指定了三个逐模块选项。前两个选项更改 mypy 对 ``mycode.foo.*`` 和 ``mycode.bar`` 中代码的类型检查，我们在这里假设这两个模块是您编写的。最后一个配置选项更改 mypy 对 ``somelibrary`` 的类型检查，我们在这里假设这是您安装并导入的某个第三方库。这些选项将：

1.  仅在 ``mycode.foo`` 包内选择性地禁止未类型定义的函数——即仅适用于在 ``mycode/foo`` 目录中定义的函数。

2.  仅在 ``mycode.bar`` 内选择性地*禁用*“函数返回任何”警告。这将覆盖我们之前设置的全局默认值。

3.  抑制在您的代码库尝试导入模块 ``somelibrary`` 时生成的任何错误消息。如果 ``somelibrary`` 是缺少类型提示的某个第三方库，这将非常有用。


.. _config-file-import-discovery:

导入发现(Import discovery)
********************************

有关更多信息，请参见命令行文档的 :ref:`导入发现 <import-discovery>` 部分。

.. confval:: mypy_path

    :type: string

    指定在尝试 ``MYPYPATH`` 环境变量中的路径后要使用的路径。如果您希望在代码库中保留存根以及配置文件，这非常有用。多个路径始终用 ``:`` 或 `,` 分隔，无论平台如何。用户主目录和环境变量将被扩展。

    相对路径相对于 mypy 命令的工作目录处理，而不是配置文件。
    使用 ``MYPY_CONFIG_FILE_DIR`` 环境变量来引用相对于配置文件的路径（例如 ``mypy_path = $MYPY_CONFIG_FILE_DIR/src`` )。

    此选项只能在全局部分( ``[mypy]`` )中设置。

    **注意：** 在 Windows 上，使用 UNC 路径以避免使用 ``:`` （例如 ``\\127.0.0.1\X$\MyDir`` ，其中 ``X`` 是驱动器字母）。

.. confval:: files

    :type: 逗号隔开的字符串列表(comma-separated list of strings)

    如果在命令行上未给出，则应由 mypy 检查的路径的以逗号分隔的列表。支持使用 :py:mod:`glob` 进行递归文件匹配，其中 ``*`` （例如 ``*.py`` )匹配当前目录中的文件，而 ``**/`` （例如 ``**/*.py`` )匹配当前目录以下的任何目录中的文件。用户主目录和环境变量将被扩展。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: modules

    :type: 逗号隔开的字符串列表(comma-separated list of strings)

    如果在命令行上未给出，则应由 mypy 检查的包的以逗号分隔的列表。Mypy *将不会* 递归类型检查提供模块的任何子模块。

    此选项只能在全局部分( ``[mypy]`` )中设置。


.. confval:: packages

    :type: 逗号隔开的字符串列表(comma-separated list of strings)

    如果在命令行上未给出，则应由 mypy 检查的包的以逗号分隔的列表。Mypy *将(will)* 递归类型检查提供包的任何子模块。此标志与 :confval:`modules` 相同，除了此行为。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: exclude

    :type: regular expression

    匹配文件名、目录名和路径的正则表达式，mypy 应在递归发现要检查的文件时忽略这些文件。所有平台上使用正斜杠( ``/`` )作为目录分隔符。

    .. code-block:: ini

      [mypy]
      exclude = (?x)(
          ^one\.py$    # 文件名为 "one.py"
          | two\.pyi$  # 或以 "two.pyi" 结尾的文件
          | ^three\.   # 或以 "three." 开头的文件
        )

    制作一个排除多个文件的单一正则表达式，同时保持可读性可能是一项挑战。上述示例演示了一种方法。
    ``(?x)`` 启用后续正则表达式的 ``VERBOSE`` 标志，这
    :py:data:`忽略大多数空格并支持注释 <re.VERBOSE>`。
    上述等价于： ``(^one\.py$|two\.pyi$|^three\.)``。

    有关更多详细信息，请参见 :option:`--exclude <mypy --exclude>`。

    此选项只能在全局部分( ``[mypy]`` )中设置。

    .. note::

       请注意，TOML 的等效项略有不同。它可以是单个字符串（包括多行字符串）——视为单个正则表达式——或一个这样的字符串数组。以下 TOML 示例等同于上述 INI 示例。

       字符串数组：

       .. code-block:: toml

          [tool.mypy]
          exclude = [
              "^one\\.py$",  # TOML 的双引号字符串需要转义反斜杠
              'two\.pyi$',  # 但 TOML 的单引号字符串不需要
              '^three\.',
          ]

       单个多行字符串：

       .. code-block:: toml

          [tool.mypy]
          exclude = '''(?x)(
              ^one\.py$    # 文件名为 "one.py"
              | two\.pyi$  # 或以 "two.pyi" 结尾的文件
              | ^three\.   # 或以 "three." 开头的文件
          )'''  # TOML 的单引号字符串不需要转义反斜杠

       请参见 :ref:`using-a-pyproject-toml`。

.. confval:: namespace_packages

    :type: boolean
    :default: True

    启用 :pep:`420` 风格的命名空间包。有关更多信息，请参见相应的标志 :option:`--no-namespace-packages <mypy --no-namespace-packages>`。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: explicit_package_bases

    :type: boolean
    :default: False

    此标志告诉 mypy 顶级包将基于当前目录或 ``MYPYPATH`` 环境变量或 :confval:`mypy_path` 配置选项中的某个成员。此选项仅在缺少 `__init__.py` 时有用。有关详细信息，请参见 :ref:`将文件路径映射到模块 <mapping-paths-to-modules>`。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: ignore_missing_imports

    :type: boolean
    :default: False

    抑制关于无法解析的导入的错误消息。

    如果在逐模块部分中使用此选项，则模块名称应与*导入的*模块名称匹配，而不是包含导入语句的模块。

.. confval:: follow_imports

    :type: string
    :default: ``normal``

    指定在找到以 ``.py`` 文件形式导入的模块且该模块不属于命令行提供的文件、模块和包时该怎么办。

    四个可能的值为 ``normal``、``silent``、``skip`` 和 ``error``。有关解释，请参见 :option:`--follow-imports <mypy --follow-imports>` 命令行标志的讨论。

    在逐模块部分中使用此选项（可能带有通配符，如本页顶部所述）是防止 mypy 检查您代码部分的好方法。

    如果在逐模块部分中使用此选项，则模块名称应与*导入的*模块名称匹配，而不是包含导入语句的模块。

.. confval:: follow_imports_for_stubs

    :type: boolean
    :default: False

    决定是否即使对于存根( ``.pyi`` )文件也遵循 :confval:`follow_imports` 设置。

    与 :confval:`follow_imports=skip <follow_imports>` 一起使用时，这可以用于抑制对来自 ``typeshed`` 的模块的导入，将其替换为 ``Any``。

    与 :confval:`follow_imports=error <follow_imports>` 一起使用时，这可以用于将对特定 ``typeshed`` 模块的任何使用视为错误。

    .. note::

         这不支持 mypy 守护进程。

.. confval:: python_executable

    :type: string

    指定要检查的 Python 可执行文件的路径，以收集可用的 :ref:`PEP 561 包 <installed-packages>` 列表。用户主目录和环境变量将被扩展。默认为用于运行 mypy 的可执行文件。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: no_site_packages

    :type: boolean
    :default: False

    禁用使用已安装包中的类型信息（见 :pep:`561`）。这还将禁用搜索可用的 Python 可执行文件。这与 :option:`--no-site-packages <mypy --no-site-packages>` 命令行标志的作用相同。

.. confval:: no_silence_site_packages

    :type: boolean
    :default: False

    启用报告在已安装包中生成的错误消息（有关分发类型信息的更多详细信息，请参见 :pep:`561`）。这些错误消息默认被抑制，因为您通常无法控制第三方代码中的错误。

    此选项只能在全局部分（ ``[mypy]`` ）中设置。


平台配置(Platform configuration)
*********************************

.. confval:: python_version

    :type: string

    指定用于解析和检查目标程序的 Python 版本。字符串应为 ``MAJOR.MINOR`` 格式——例如 ``2.7``。默认值为用于运行 mypy 的 Python 解释器的版本。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: platform

    :type: string

    指定目标程序的操作系统平台，例如 ``darwin`` 或 ``win32`` （分别表示 OS X 或 Windows）。默认值为 Python 的 :py:data:`sys.platform` 变量所揭示的当前平台。

    此选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: always_true

    :type: 字符串逗号隔开的列表(comma-separated list of strings)。

    指定一组变量，mypy 将视为总是为真（compile-time constants）。

.. confval:: always_false

    :type: 字符串逗号隔开的列表(comma-separated list of strings)。

    指定一组变量，mypy 将视为总是为假（compile-time constants）。


禁止动态类型(Disallow dynamic typing)
***************************************

有关更多信息，请参见命令行文档的 :ref:`禁止动态类型 <disallow-dynamic-typing>` 部分。

.. confval:: disallow_any_unimported

    :type: boolean
    :default: False

    禁止使用来自未跟踪导入的类型（来自未跟踪导入的任何内容自动被赋予类型 ``Any`` )。

.. confval:: disallow_any_expr

    :type: boolean
    :default: False

    禁止模块中所有类型为 ``Any`` 的表达式。

.. confval:: disallow_any_decorated

    :type: boolean
    :default: False

    禁止在装饰器转换后其签名中包含 ``Any`` 的函数。

.. confval:: disallow_any_explicit

    :type: boolean
    :default: False

    禁止在类型位置（例如类型注解和泛型类型参数）中显式使用 ``Any``。

.. confval:: disallow_any_generics

    :type: boolean
    :default: False

    禁止使用未指定显式类型参数的泛型类型。

.. confval:: disallow_subclassing_any

    :type: boolean
    :default: False

    禁止对类型为 ``Any`` 的值进行子类化。


未类型定义和调用(Untyped definitions and calls)
*****************************************************

有关更多信息，请参见命令行文档的 :ref:`未类型定义和调用 <untyped-definitions-and-calls>` 部分。

.. confval:: disallow_untyped_calls

    :type: boolean
    :default: False

    禁止从具有类型注解的函数调用没有类型注解的函数。请注意，当在模块选项中使用时，它在指定的模块内启用/禁用此检查，而不是对来自该模块的函数，例如如下配置：

    .. code-block:: ini

        [mypy]
        disallow_untyped_calls = True

        [mypy-some.library.*]
        disallow_untyped_calls = False

    将在 ``some.library`` 内禁用此检查，而不是对导入 ``some.library`` 的代码。如果您想选择性地禁用对所有导入 ``some.library`` 的代码的此检查，应该使用 :confval:`untyped_calls_exclude`，例如：

    .. code-block:: ini

        [mypy]
        disallow_untyped_calls = True
        untyped_calls_exclude = some.library

.. confval:: untyped_calls_exclude

    :type: comma-separated list of strings

    选择性地排除在特定包、模块和类中定义的函数和方法，以免触发 :confval:`disallow_untyped_calls` 的作用。这也适用于包的所有子模块（即给定前缀下的所有内容）。注意，此选项不支持逐文件配置，排除列表在全局范围内为您所有代码定义。

.. confval:: disallow_untyped_defs

    :type: boolean
    :default: False

    禁止定义没有类型注解或具有不完整类型注解的函数（是 :confval:`disallow_incomplete_defs` 的超集）。

    例如，它会对 :code:`def f(a, b)` 和 :code:`def f(a: int, b)` 报告错误。

.. confval:: disallow_incomplete_defs

    :type: boolean
    :default: False

    禁止定义具有不完整类型注解的函数，同时仍然允许完全没有注解的定义。

    例如，它会对 :code:`def f(a: int, b)` 报告错误，但不会对 :code:`def f(a, b)` 报告错误。

.. confval:: check_untyped_defs

    :type: boolean
    :default: False

    对没有类型注解的函数内部进行类型检查。

.. confval:: disallow_untyped_decorators

    :type: boolean
    :default: False

    每当具有类型注解的函数被没有注解的装饰器装饰时，报告错误。


.. _config-file-none-and-optional-handling:

None 和 Optional 处理(None and Optional handling)
***********************************************************

有关更多信息，请参见命令行文档的 :ref:`None 和 Optional 处理 <none-and-optional-handling>` 部分。

.. confval:: implicit_optional

    :type: boolean
    :default: False

    使 mypy 将具有 ``None`` 默认值的参数视为具有隐式可选类型( ``T | None`` )。

    **注意：** 在 mypy 版本 0.980 及之前版本中，这一选项默认为 True。

.. confval:: strict_optional

    :type: boolean
    :default: True

    实质上禁用对可选类型和 ``None`` 值的检查。启用此选项后，mypy 通常不会检查 ``None`` 值的使用——它被视为与每种类型兼容。

    .. warning::

        ``strict_optional = false`` 是有害的。避免使用它，并且在完全理解其作用之前，绝对不要使用它。


配置警告(Configuring warnings)
****************************************

有关更多信息，请参见命令行文档的 :ref:`配置警告 <configuring-warnings>` 部分。

.. confval:: warn_redundant_casts

    :type: boolean
    :default: False

    针对将表达式转换为其推断类型的情况发出警告。

    此选项仅可在全局部分( ``[mypy]`` )中设置。

.. confval:: warn_unused_ignores

    :type: boolean
    :default: False

    针对不必要的 ``# type: ignore`` 注释发出警告。

.. confval:: warn_no_return

    :type: boolean
    :default: True

    对某些执行路径缺少返回语句显示错误。

.. confval:: warn_return_any

    :type: boolean
    :default: False

    当从声明了非 ``Any`` 返回类型的函数返回类型为 ``Any`` 的值时，显示警告。

.. confval:: warn_unreachable

    :type: boolean
    :default: False

    当遇到任何经过类型分析推断为不可达或冗余的代码时，显示警告。


抑制错误(Suppressing errors)
************************************

注意：这些配置选项仅在配置文件中可用。命令行选项中没有类似功能。

.. confval:: ignore_errors

    :type: boolean
    :default: False

    忽略所有非致命错误。


其他严格性标志(Miscellaneous strictness flags)
************************************************************

有关更多信息，请参见命令行文档的 :ref:`杂项严格性标志 <miscellaneous-strictness-flags>` 部分。

.. confval:: allow_untyped_globals

    :type: boolean
    :default: False

    使 mypy 抑制因无法完全推断全局和类变量类型而导致的错误。

.. confval:: allow_redefinition

    :type: boolean
    :default: False

    允许在与原始定义相同的块和嵌套级别中以任意类型重新定义变量。
    这种情况下可以很有用的示例：

    .. code-block:: python

       def process(items: list[str]) -> None:
           # 'items' 的类型是 list[str]
           items = [item.split() for item in items]
           # 'items' 现在的类型是 list[list[str]]

    变量必须在重新定义之前使用：

    .. code-block:: python

        def process(items: list[str]) -> None:
           items = "mypy"  # 无效的重新定义为 str，因为变量尚未被使用
           print(items)
           items = "100"  # 有效，items 现在的类型是 str
           items = int(items)  # 有效，items 现在的类型是 int

.. confval:: local_partial_types

    :type: boolean
    :default: False

    禁止从不同作用域中的两个赋值中推断 ``None`` 的变量类型。
    在使用 :ref:`mypy daemon <mypy_daemon>` 时，这总是隐式启用。

.. confval:: disable_error_code

    :type: comma-separated list of strings

    允许全局禁用一个或多个错误代码。

.. confval:: enable_error_code

    :type: comma-separated list of strings

    允许全局启用一个或多个错误代码。

    注意：此选项将覆盖 disable_error_code 选项中的禁用错误代码。

.. confval:: implicit_reexport

    :type: boolean
    :default: True

    默认情况下，导入到模块的值被视为导出，并且 mypy 允许其他模块导入它们。
    当为 false 时，mypy 不会重新导出，除非项目使用 from-as 导入或包含在 ``__all__`` 中。
    注意，mypy 将存根文件视为始终禁用此功能。例如：

    .. code-block:: python

       # 这不会重新导出该值
       from foo import bar
       # 这将重新导出为 bar 并允许其他模块导入它
       from foo import bar as bar
       # 这也将重新导出 bar
       from foo import bar
       __all__ = ['bar']

.. confval:: strict_concatenate

    :type: boolean
    :default: False

    使通过 ``Concatenate`` 添加的参数真正只能是位置参数。

.. confval:: strict_equality

    :type: boolean
    :default: False

    禁止非重叠类型之间的相等检查、身份检查和容器检查。

.. confval:: strict

    :type: boolean
    :default: False

    启用所有可选的错误检查标志。你可以在完整的 :option:`mypy --help` 输出中查看严格模式启用的标志列表。

    注意：由 :confval:`strict` 启用的确切标志列表可能会随时间变化。


配置错误消息(Configuring error messages)
****************************************************

有关更多信息，请参见命令行文档的 :ref:`配置错误消息 <configuring-error-messages>` 部分。

这些选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: show_error_context

    :type: boolean
    :default: False

    在每个错误前加上相关的上下文信息。

.. confval:: show_column_numbers

    :type: boolean
    :default: False

    在错误消息中显示列号。

.. confval:: show_error_code_links

    :type: boolean
    :default: False

    显示指向相应错误代码的文档链接。

.. confval:: hide_error_codes

    :type: boolean
    :default: False

    在错误消息中隐藏错误代码。有关更多信息，请参见 :ref:`error-codes`。

.. confval:: pretty

    :type: boolean
    :default: False

    在错误消息中使用视觉上更优雅的输出：使用软换行，显示源代码片段，并显示错误位置标记。

.. confval:: color_output

    :type: boolean
    :default: True

    显示带有颜色的错误消息。

.. confval:: error_summary

    :type: boolean
    :default: True

    在错误消息后显示简短的摘要行。

.. confval:: show_absolute_path

    :type: boolean
    :default: False

    显示文件的绝对路径。

.. confval:: force_uppercase_builtins

    :type: boolean
    :default: False

    在错误消息中始终使用 ``List`` 而不是 ``list``，
    即使在 Python 3.9+ 中也是如此。

.. confval:: force_union_syntax

    :type: boolean
    :default: False

    在错误消息中始终使用 ``Union[]`` 和 ``Optional[]`` 来表示联合类型
    （而不是 ``|`` 操作符），即使在 Python 3.10+ 中也是如此。

增量模式(Incremental mode)
********************************

这些选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: incremental

    :type: boolean
    :default: True

    启用 :ref:`增量模式 <incremental>`。

.. confval:: cache_dir

    :type: string
    :default: ``.mypy_cache``

    指定 mypy 存储增量缓存信息的位置。
    用户主目录和环境变量将被展开。
    此设置将被 ``MYPY_CACHE_DIR`` 环境变量覆盖。

    注意，只有在启用增量模式时才会读取缓存，
    但总是会写入缓存，除非值设置为 ``/dev/null``
    （UNIX）或 ``nul`` （Windows）。

.. confval:: sqlite_cache

    :type: boolean
    :default: False

    使用 `SQLite`_ 数据库来存储缓存。

.. confval:: cache_fine_grained

    :type: boolean
    :default: False

    为 mypy 守护进程在缓存中包含细粒度的依赖信息。

.. confval:: skip_version_check

    :type: boolean
    :default: False

    使 mypy 使用增量缓存数据，即使它是由不同版本的 mypy 生成的。
    （默认情况下，mypy 将执行版本检查，并在缓存由旧版本的 mypy 写入时重新生成缓存。）

.. confval:: skip_cache_mtime_checks

    :type: boolean
    :default: False

    跳过基于 mtime 的缓存内部一致性检查。


高级选项(Advanced options)
********************************

这些选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: plugins

    :type: comma-separated list of strings

    逗号分隔的 mypy 插件列表。请参见 :ref:`extending-mypy-using-plugins`。

.. confval:: pdb

    :type: boolean
    :default: False

    在致命错误时调用 :mod:`pdb`。

.. confval:: show_traceback

    :type: boolean
    :default: False

    在致命错误时显示回溯信息。

.. confval:: raise_exceptions

    :type: boolean
    :default: False

    在致命错误时引发异常。

.. confval:: custom_typing_module

    :type: string

    指定一个自定义模块，用作 :py:mod:`typing` 模块的替代。

.. confval:: custom_typeshed_dir

    :type: string

    指定 mypy 查找标准库 typeshed 存根的目录，而不是随 mypy 一起提供的 typeshed。
    这主要旨在简化在提交变更之前测试 typeshed 变更的过程，同时也允许您使用 forked 版本的 typeshed。

    用户主目录和环境变量将被展开。

    注意，这不会影响第三方库的存根。要测试第三方存根，
    例如尝试 ``MYPYPATH=stubs/six mypy ...``。

.. confval:: warn_incomplete_stub

    :type: boolean
    :default: False

    发出缺少类型注解的警告，仅在与 :confval:`disallow_untyped_defs` 或 :confval:`disallow_incomplete_defs` 结合使用时相关。


报告生成(Report generation)
**********************************

如果设置了这些选项，mypy 将会在指定的目录中生成指定格式的报告。

.. warning::

  生成报告会禁用增量模式，并可能显著降低您的工作流程效率。建议仅在特定运行时（例如在 CI 中）启用报告。

.. confval:: any_exprs_report

    :type: string

    使 mypy 生成一份文本文件报告，记录您代码库中存在多少类型为 ``Any`` 的表达式。

.. confval:: cobertura_xml_report

    :type: string

    使 mypy 生成一份 Cobertura XML 类型检查覆盖报告。

    要生成此报告，您必须手动安装 `lxml`_ 库或使用 setuptools 附加选项
    ``mypy[reports]`` 指定 mypy 安装。

.. confval:: html_report / xslt_html_report

    :type: string

    使 mypy 生成一份 HTML 类型检查覆盖报告。

    要生成此报告，您必须手动安装 `lxml`_ 库或使用 setuptools 附加选项
    ``mypy[reports]`` 指定 mypy 安装。

.. confval:: linecount_report

    :type: string

    使 mypy 生成一份文本文件报告，记录您代码库中已类型注解和未类型注解的函数及行数。

.. confval:: linecoverage_report

    :type: string

    使 mypy 生成一份 JSON 文件，将每个源文件的绝对文件名映射到属于该文件中已类型注解函数的行号列表。

.. confval:: lineprecision_report

    :type: string

    使 mypy 生成一份平面文本文件报告，包含每个模块的统计信息，例如经过类型检查的行数等。

.. confval:: txt_report / xslt_txt_report

    :type: string

    使 mypy 生成一份文本文件类型检查覆盖报告。

    要生成此报告，您必须手动安装 `lxml`_ 库或使用 setuptools 附加选项
    ``mypy[reports]`` 指定 mypy 安装。

.. confval:: xml_report

    :type: string

    使 mypy 生成一份 XML 类型检查覆盖报告。

    要生成此报告，您必须手动安装 `lxml`_ 库或使用 setuptools 附加选项
    ``mypy[reports]``。


其他(Miscellaneous)
**************************

这些选项只能在全局部分( ``[mypy]`` )中设置。

.. confval:: junit_xml

    :type: string

    使 mypy 生成一份包含类型检查结果的 JUnit XML 测试结果文档。这可以使 mypy 更容易与持续集成（CI）工具集成。

.. confval:: scripts_are_modules

    :type: boolean
    :default: False

    使脚本 ``x`` 成为模块 ``x``，而不是 ``__main__``。这在单次运行中检查多个脚本时非常有用。

.. confval:: warn_unused_configs

    :type: boolean
    :default: False

    警告配置文件中与调用 mypy 时处理的文件不匹配的每个模块部分。
    （这需要使用 :confval:`incremental = False <incremental>` 关闭增量模式。）

.. confval:: verbosity

    :type: integer
    :default: 0

    控制将生成多少调试输出。数字越高，输出越详细。


.. _using-a-pyproject-toml:

使用 pyproject.toml 文件(Using a pyproject.toml file)
******************************************************

可以使用 ``pyproject.toml`` 文件（如 `PEP 518`_ 所指定），而不是使用 ``mypy.ini`` 文件。以下是一些注意事项：

* ``[mypy]`` 部分应在其名称前加上 ``tool.``：

  * 即，``[mypy]`` 应变为 ``[tool.mypy]``

* 模块特定部分应移动到 ``[[tool.mypy.overrides]]`` 部分中：

  * 例如，``[mypy-packagename]`` 应变为：

.. code-block:: toml

  [[tool.mypy.overrides]]
  module = 'packagename'
  ...

* 多模块特定部分可以移动到单个 ``[[tool.mypy.overrides]]`` 部分，模块属性设置为模块数组：

  * 例如，``[mypy-packagename,packagename2]`` 应变为：

.. code-block:: toml

  [[tool.mypy.overrides]]
  module = [
      'packagename',
      'packagename2'
  ]
  ...

* 与 ``ini`` 文件相比，在 ``pyproject.toml`` 文件中对值应注意以下几点：

  * 字符串必须用双引号括起来，如果字符串包含特殊字符，则可以用单引号

  * 布尔值应全部为小写

有关 ``toml`` 文件中允许的内容的更多详细信息，请参阅 `TOML Documentation`_ 。有关 ``pyproject.toml`` 文件布局和结构的更多信息，请参阅 `PEP 518`_ 。

pyproject.toml 示例(Example)
******************************

以下是一个 ``pyproject.toml`` 文件的示例。要使用此配置文件，请将其放置在您的仓库根目录（或附加到现有 ``pyproject.toml`` 文件的末尾）并运行 mypy。

.. code-block:: toml

    # mypy 全局选项：

    [tool.mypy]
    python_version = "2.7"
    warn_return_any = true
    warn_unused_configs = true
    exclude = [
        '^file1\.py$',  # TOML 字面字符串（单引号，无需转义）
        "^file2\\.py$",  # TOML 基本字符串（双引号，反斜杠和其他字符需要转义）
    ]

    # mypy 每模块选项：

    [[tool.mypy.overrides]]
    module = "mycode.foo.*"
    disallow_untyped_defs = true

    [[tool.mypy.overrides]]
    module = "mycode.bar"
    warn_return_any = false

    [[tool.mypy.overrides]]
    module = [
        "somelibrary",
        "some_other_library"
    ]
    ignore_missing_imports = true

.. _lxml: https://pypi.org/project/lxml/
.. _SQLite: https://www.sqlite.org/
.. _PEP 518: https://www.python.org/dev/peps/pep-0518/
.. _TOML Documentation: https://toml.io/
