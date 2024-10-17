.. _mypy_daemon:

.. program:: dmypy

Mypy 守护进程 (mypy 服务)
===========================

除了将 mypy 作为命令行工具运行外，您还可以将其作为一个长时间运行的守护进程（服务器）来运行，并使用命令行客户端向服务器发送类型检查请求。通过这种方式，mypy 可以更快地执行类型检查，因为之前运行时缓存的程序状态保留在内存中，而不必在每次运行时从文件系统读取。服务器还使用更细粒度的依赖追踪，以减少需要执行的工作量。

如果您有一个大型代码库要检查，使用 mypy 守护进程运行 mypy 的速度可能比常规命令行 ``mypy`` 工具快 *10 倍或更多*，尤其是如果您的工作流涉及在小幅修改后重复运行 mypy——这通常是个好主意，因为这样您能更早发现错误。

.. note::

    mypy 守护进程的命令行接口在未来的 mypy 版本中可能会发生变化。

.. note::

    每个 mypy 守护进程支持一个用户和一组源文件，并且它一次只能处理一个类型检查请求。您可以运行多个 mypy 守护进程来检查多个代码库。

基本用法(Basic usage)
**********************

客户端工具 ``dmypy`` 用于控制 mypy 守护进程。
使用 ``dmypy run -- <flags> <files>`` 来检查一组文件（或目录）的类型。这将在守护进程未运行时启动它。您可以在 ``--`` 后使用几乎任意的 mypy 标志。守护进程将始终在当前主机上运行。示例::

    dmypy run -- prog.py pkg/*.py

``dmypy run`` 会自动在配置或 mypy 版本更改时重启守护进程。

初始运行将处理所有代码，可能需要一些时间才能完成，但后续运行将非常快速，尤其是在您只更改了少数文件的情况下。（您可以使用 :ref:`remote caching <remote-cache>` 来加速初始运行。如果您有一个大型代码库，速度提升可能会很显著。）

.. note::

   Mypy 0.780 添加了对 dmypy 中的 following imports 的支持（默认启用）。此功能仍在实验阶段。您可以使用 ``--follow-imports=skip`` 或 ``--follow-imports=error`` 以回退到稳定功能。有关这些功能的详细信息，请参见 :ref:`follow-imports`。

.. note::

    mypy 守护进程需要 ``--local-partial-types`` 并会自动启用它。


守护进程客户端命令(Daemon client commands)
********************************************

虽然 ``dmypy run`` 足以满足大多数使用场景，但一些工作流（例如使用 :ref:`remote caching <remote-cache>` 的工作流）需要对守护进程生命周期进行更精确的控制：

* ``dmypy stop`` 停止守护进程。

* ``dmypy start -- <flags>`` 启动守护进程，但不检查任何文件。您可以在 ``--`` 后使用几乎任意的 mypy 标志。

* ``dmypy restart -- <flags>`` 重启守护进程。标志与 ``dmypy start`` 相同。这相当于先停止再启动。

* 使用 ``dmypy run --timeout SECONDS -- <flags>``（或 ``start`` 或 ``restart``）在不活动后自动关闭守护进程。默认情况下，守护进程会一直运行，直到明确停止。

* ``dmypy check <files>`` 使用已在运行的守护进程检查一组文件。

* ``dmypy recheck`` 检查与最近一次 ``check`` 或 ``recheck`` 命令相同的文件集。（您还可以使用 :option:`--update` 和 :option:`--remove` 选项来更改文件集，并定义应处理哪些文件。）

* ``dmypy status`` 检查守护进程是否正在运行。如果有正在运行的守护进程，则打印诊断信息并以 ``0`` 退出。

使用 ``dmypy --help`` 获取有关未在此讨论的附加命令和命令行选项的帮助，以及 ``dmypy <command> --help`` 获取特定命令选项的帮助。

附加守护进程标志(Additional daemon flags)
**********************************************

.. option:: --status-file FILE

   使用 ``FILE`` 作为存储守护进程运行状态的状态文件。这通常是一个 JSON 文件，包含有关守护进程和连接的信息。默认路径为当前工作目录中的 ``.dmypy.json``。

.. option:: --log-file FILE

   将守护进程的 stdout/stderr 定向到 ``FILE``。这对于调试守护进程崩溃非常有用，因为服务器的追踪信息并不总是由客户端打印。此选项适用于 ``start``、``restart`` 和 ``run`` 命令。

.. option:: --timeout TIMEOUT

   在 ``TIMEOUT`` 秒的不活动后自动关闭服务器。此选项适用于 ``start``、``restart`` 和 ``run`` 命令。

.. option:: --update FILE

   重新检查 ``FILE``，或将其添加到被检查的文件集中（并检查它）。此选项可以重复，仅适用于 ``recheck`` 命令。默认情况下，mypy 找到并检查自上次运行以来更改的所有文件及其依赖文件。然而，如果使用此选项（和/或 :option:`--remove`），mypy 假设只有明确指定的文件已更改。这仅在您检查大量文件并使用外部快速文件系统监视器（如 `watchman`_ 或 `watchdog`_）来确定哪些文件已被编辑或删除时有用。
   *注意：* 此选项从不需要，仅用于性能调优。

.. option:: --remove FILE

   从被检查的文件集中移除 ``FILE``。此选项可以重复，仅适用于 ``recheck`` 命令。有关何时可能有用，请参见上述 :option:`--update`。
   *注意：* 此选项从不需要，仅用于性能调优。

.. option:: --fswatcher-dump-file FILE

   收集当前内部文件状态的信息。此选项仅适用于 ``status`` 命令。此操作将以格式 ``{path: [modification_time, size, content_hash]}`` 将 JSON 转储到 ``FILE``。这对于调试内置文件系统监视器非常有用。*注意：* 这是一个内部标志，格式可能会变化。

.. option:: --perf-stats-file FILE

   将性能分析信息写入 ``FILE``。此选项仅适用于 ``check``、``recheck`` 和 ``run`` 命令。

.. option:: --export-types

   将所有表达式类型存储在内存中以供将来使用。这对于加速后续调用 ``dmypy inspect`` 很有帮助（但会使用更多内存）。仅对 ``check``、``recheck`` 和 ``run`` 命令有效。

静态推断注解(Static inference of annotations)
*******************************************************

mypy 守护进程支持（作为实验性功能）静态推断草拟的函数和方法类型注释。使用 ``dmypy suggest FUNCTION`` 生成格式为 ``(param_type_1, param_type_2, ...) -> ret_type`` 的草拟签名（所有参数的类型均包括在内，包括仅限关键字的参数、``*args`` 和 ``**kwargs``）。

这是一个低级功能，旨在供编辑器集成、IDE 和其他工具使用（例如， `PyCharm 的 mypy 插件`_ ），以自动将注释添加到源文件中，或建议函数签名。

在此示例中，函数 ``format_id()`` 没有注释：

.. code-block:: python

   def format_id(user):
       return f"User: {user}"

   root = format_id(0)

``dmypy suggest`` 使用调用点、返回语句和其他启发式方法（例如查找基类中的签名）推断 ``format_id()`` 接受一个 ``int`` 参数并返回一个 ``str``。使用 ``dmypy suggest module.format_id`` 打印该函数的建议签名。

更一般地，目标函数可以通过两种方式指定：

* 通过其完全限定名称，即 ``[package.]module.[class.]function``。

* 通过其在源文件中的位置，即 ``/path/to/file.py:line``。路径可以是绝对路径或相对路径，``line`` 可以指函数体内的任何行号。

该命令也可用于查找现有不精确注释中一些 ``Any`` 类型的更精确替代方案。

以下标志用于自定义 ``dmypy suggest`` 命令的各个方面。

.. option:: --json

   以 JSON 格式输出签名，以便 `PyAnnotate`_ 能够读取并将签名添加到源文件中。JSON 的格式如下：

   .. code-block:: python

      [{"func_name": "example.format_id",
        "line": 1,
        "path": "/absolute/path/to/example.py",
        "samples": 0,
        "signature": {"arg_types": ["int"], "return_type": "str"}}]

.. option:: --no-errors

   仅生成不会导致检查代码中出现错误的建议。默认情况下，mypy 会尝试找到最精确的类型，即使这会导致一些类型错误。

.. option:: --no-any

   仅生成不包含 ``Any`` 类型的建议。默认情况下，mypy 提出找到的最精确签名，即使它包含 ``Any`` 类型。

.. option:: --flex-any FRACTION

   仅允许建议签名中的某些类型为 ``Any`` 类型。该比例范围为 ``0`` （与 ``--no-any`` 相同）到 ``1``。

.. option:: --callsites

   仅查找给定函数的调用点，而不是建议类型。这将生成一个列表，列出每个调用的行号和实际参数的类型：``/path/to/file.py:line: (arg_type_1, arg_type_2, ...)``。

.. option:: --use-fixme NAME

   对于无法推断的类型，使用一个虚拟名称而不是普通的 ``Any``。这可能有助于提醒用户某个类型无法被推断，需要手动输入。

.. option:: --max-guesses NUMBER

   设置为一个函数尝试的最大类型数量（默认值：``64``）。

静态检查表达式(Statically inspect expressions)
************************************************************

守护进程允许使用 ``dmypy inspect LOCATION`` 命令获取表达式的声明或推断类型（或关于表达式的其他信息，例如已知属性或定义位置）。表达式的位置应按格式 ``path/to/file.py:line:column[:end_line:end_column]`` 指定。行和列均为 1 基数。起始和结束位置均为包含性。这些规则与 mypy 在错误消息中打印错误位置的方式一致。

如果提供了一个范围（即所有 4 个数字），则仅检查与之完全匹配的表达式。如果只提供了一个位置（即 2 个数字，行和列），mypy 将检查所有包含该位置的 *表达式*，从最内层的开始。

考虑以下 Python 代码片段：

.. code-block:: python

   def foo(x: int, longer_name: str) -> None:
       x
       longer_name

要查找 ``x`` 的类型，需要调用 ``dmypy inspect src.py:2:5:2:5`` 或 ``dmypy inspect src.py:2:5``。而对于 ``longer_name``，需要调用 ``dmypy inspect src.py:3:5:3:15``，或者例如 ``dmypy inspect src.py:3:10``。请注意，此命令仅在守护进程成功完成类型检查（没有解析错误）后有效，以便类型被填充，例如使用 ``dmypy check``。在多个表达式与提供的位置匹配的情况下，其类型将以换行符分隔返回。

重要提示：建议使用 :option:`--export-types` 检查文件，否则大多数检查在没有 :option:`--force-reload` 的情况下将无法正常工作。

.. option:: --show INSPECTION

   要对找到的表达式运行哪种检查。目前支持的检查包括：

   * ``type`` （默认）：显示给定表达式的最佳已知类型。
   * ``attrs``：显示表达式有效的属性（例如，用于自动补全）。格式为 ``{"Base1": ["name_1", "name_2", ...]; "Base2": ...}``。名称按方法解析顺序排序。如果表达式指向模块，则模块属性将在类似 ``"<full.module.name>"`` 的键下。
   * ``definition``（实验性）：显示名称表达式或成员表达式的定义位置。格式为 ``path/to/file.py:line:column:Symbol``。如果找到多个定义（例如，对于一个联合属性），它们将用逗号分隔。

.. option:: --verbose

   增加类型字符串表示的详细程度（可以重复）。例如，这将打印实例类型的完全限定名称（如 ``"builtins.str"``），而不仅仅是简短名称（如 ``"str"``）。

.. option:: --limit NUM

   如果位置以 ``line:column`` 给出，这将导致守护进程仅返回最多 ``NUM`` 个最内层表达式的检查结果。值为 0 意味着没有限制（这是默认值）。例如，如果调用 ``dmypy inspect src.py:4:10 --limit=1``，代码如下：

   .. code-block:: python

      def foo(x: int) -> str: ..
      def bar(x: str) -> None: ...
      baz: int
      bar(foo(baz))

   这将只输出一个类型 ``"int"`` （针对 ``baz`` 名称表达式）。而没有限制选项时，它将输出所有三种类型：``"int"``, ``"str"``, 和 ``"None"``。

.. option:: --include-span

   启用此选项后，守护进程将为每个检查结果添加对应表达式的完整范围，格式为 ``1:2:1:4 -> "int"``。在多个表达式匹配同一位置时，这可能会很有用。

.. option:: --include-kind

   启用此选项后，守护进程将为每个检查结果添加对应表达式的类型，格式为 ``NameExpr -> "int"``。如果同时启用了此选项和 :option:`--include-span`，则类型将优先显示，例如 ``NameExpr:1:2:1:4 -> "int"``。

.. option:: --include-object-attrs

   如果进行 ``atts`` 检查，此选项将使守护进程包括 ``object`` 的属性（默认情况下排除）。

.. option:: --union-attrs

   包含有效的某些可能表达式类型的属性（默认情况下返回交集）。这对于具有值的类型变量的联合类型很有用。例如，以下代码：

   .. code-block:: python

      from typing import Union

      class A:
          x: int
          z: int
      class B:
          y: int
          z: int
      var: Union[A, B]
      var

   命令 ``dmypy inspect --show attrs src.py:10:1`` 将返回 ``{"A": ["z"], "B": ["z"]}``，而使用 ``--union-attrs`` 时将返回 ``{"A": ["x", "z"], "B": ["y", "z"]}``。

.. option:: --force-reload

   在检查之前强制重新解析和重新类型检查文件。默认情况下，这仅在需要时执行（例如，文件未从缓存加载或守护进程最初未使用 ``--export-types`` mypy 选项运行），因为重新加载可能很慢（对于非常大的文件，可能需要几秒钟）。

.. TODO: 添加有关查找用法的类似部分，待添加后将其移至单独文件。


.. _watchman: https://facebook.github.io/watchman/
.. _watchdog: https://pypi.org/project/watchdog/
.. _PyAnnotate: https://github.com/dropbox/pyannotate
.. _mypy plugin for PyCharm: https://github.com/dropbox/mypy-PyCharm-plugin
.. _PyCharm 的 mypy 插件: https://github.com/dropbox/mypy-PyCharm-plugin