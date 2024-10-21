.. _running-mypy:

运行 mypy 和管理导入(imports)
=================================

:ref:`getting-started` 页面应该已经向您介绍了如何运行 mypy 的基础知识——通过命令行传入您想要进行类型检查的文件和目录::

    $ mypy foo.py bar.py some_directory

本页面将更详细地讨论如何准确指定您希望 mypy 进行类型检查的文件、mypy 如何发现导入的模块，以及如何处理您在此过程中可能遇到的任何问题的建议。

如果您有兴趣了解如何配置 mypy 实际类型检查代码的方式，请参见我们的 :ref:`command-line` 指南。


.. _specifying-code-to-be-checked:

指定要检查的代码(Specifying)
*****************************

Mypy 允许您以几种不同的方式指定要进行类型检查的文件。

1.  首先，您可以传入要进行类型检查的 Python 文件和目录的路径。例如::

        $ mypy file_1.py foo/file_2.py file_3.pyi some/directory

    上述命令告诉 mypy 应该一起对提供的所有文件进行类型检查。此外，mypy 将递归地对任何提供的目录的全部内容进行类型检查。

    有关具体操作的更多详细信息，请参见 :ref:`Mapping file paths to modules <mapping-paths-to-modules>`。

2.  其次，您可以使用 :option:`-m <mypy -m>` 标志（长形式：:option:`--module <mypy --module>`）来指定要进行类型检查的模块名称。模块的名称与您在 Python 程序中导入该模块时使用的名称相同。例如，运行::

        $ mypy -m html.parser

    ...将对模块 ``html.parser`` 进行类型检查（这恰好是一个库的存根）。

    Mypy 将使用与 Python 类似的算法查找模块和导入在文件系统上的位置。有关更多详细信息，请参见 :ref:`finding-imports`。

3.  第三，您可以使用 :option:`-p <mypy -p>` （长形式：:option:`--package <mypy --package>`）标志来指定要进行（递归）类型检查的包。该标志几乎与 :option:`-m <mypy -m>` 标志相同，只是如果您提供包名称，mypy 将递归地对该包的所有子模块和子包进行类型检查。例如，运行::

        $ mypy -p html

    ...将对整个 ``html`` 包（库存根）进行类型检查。相反，如果我们使用 :option:`-m <mypy -m>` 标志，mypy 只会对 ``html`` 的 ``__init__.py`` 文件及从中导入的任何内容进行类型检查。

    请注意，我们可以在命令行中指定多个包和模块。例如::

      $ mypy --package p.a --package p.b --module c

4.  第四，您还可以通过使用 :option:`-c <mypy -c>` （长形式：:option:`--command <mypy --command>`）标志来指示 mypy 直接对小字符串作为程序进行类型检查。例如::

        $ mypy -c 'x = [1, 2]; print(x())'

    ...将对上述字符串进行类型检查作为一个迷你程序（在这种情况下，将报告 ``list[int]`` 不是可调用的）。

您还可以在 :file:`mypy.ini` 文件中使用 :confval:`files` 选项来指定要检查的文件，在这种情况下，您可以简单地运行 ``mypy`` 而不带参数。


从文件读取文件列表(a list of files)
***********************************

最后，任何以 ``@`` 开头的命令行参数都会从 ``@`` 字符后面的文件中读取附加的命令行参数。这主要在您有一个包含要进行类型检查的文件列表的文件时非常有用：可以使用以下方式代替使用 shell 语法::

    $ mypy $(cat file_of_files.txt)

您可以改为使用::

    $ mypy @file_of_files.txt

这个文件在技术上也可以包含任何命令行标志，而不仅仅是文件路径。然而，如果您想配置许多不同的标志，推荐的方法是使用 :ref:`configuration file <config-file>`。

.. _mapping-paths-to-modules:

映射文件路径到到模块(module mapping)
**********************************************************

您可以告诉 mypy 要进行类型检查的主要方式之一是提供 mypy 的路径列表。例如::

    $ mypy file_1.py foo/file_2.py file_3.pyi some/directory

本节描述了 mypy 如何将提供的路径映射到要进行类型检查的模块。

- Mypy 将检查所有与提供的文件对应的路径。

- Mypy 将递归发现并检查提供的目录路径中以 ``.py`` 或 ``.pyi`` 结尾的所有文件，考虑到 :option:`--exclude <mypy --exclude>`。

- 对于每个要检查的文件，mypy 将尝试将文件（例如 ``project/foo/bar/baz.py`` )与完全合格的模块名称（例如 ``foo.bar.baz`` )关联。包所在的目录( ``project`` )随后将添加到 mypy 的模块搜索路径中。

mypy 确定完全合格模块名称的方式取决于是否设置了选项 :option:`--no-namespace-packages <mypy --no-namespace-packages>` 和 :option:`--explicit-package-bases <mypy --explicit-package-bases>`。

1. 如果设置了 :option:`--no-namespace-packages <mypy --no-namespace-packages>`，mypy 将完全依赖 ``__init__.py[i]`` 文件的存在来确定完全合格的模块名称。也就是说，mypy 将向上遍历目录树，只要继续找到 ``__init__.py`` （或 ``__init__.pyi`` ）文件。

   例如，如果您的目录树包含 ``pkg/subpkg/mod.py``，mypy 将要求 ``pkg/__init__.py`` 和 ``pkg/subpkg/__init__.py`` 存在，以便正确将 ``mod.py`` 关联到 ``pkg.subpkg.mod``。

2. 默认情况。如果 :option:`--namespace-packages <mypy --no-namespace-packages>` 打开，但 :option:`--explicit-package-bases <mypy --explicit-package-bases>` 关闭，mypy 将允许没有 ``__init__.py[i]`` 的目录被视为包。具体而言，mypy 将查看文件的所有父目录，并使用目录树中最高的 ``__init__.py[i]`` 的位置来确定顶级包。

   例如，假设您的目录树仅包含 ``pkg/__init__.py`` 和 ``pkg/a/b/c/d/mod.py``。在确定 ``mod.py`` 的完全合格模块名称时，mypy 将查看 ``pkg/__init__.py`` 并得出关联的模块名称是 ``pkg.a.b.c.d.mod``。

3. 您会注意到上述情况仍然依赖于 ``__init__.py``。如果您无法在顶级包中放置 ``__init__.py`` ，但仍希望传递路径（而不是使用 ``-p`` 或 ``-m`` 标志的包或模块），:option:`--explicit-package-bases <mypy --explicit-package-bases>` 提供了解决方案。

   使用 :option:`--explicit-package-bases <mypy --explicit-package-bases>`，mypy 将定位到最近的父目录，该目录是 ``MYPYPATH`` 环境变量的成员、:confval:`mypy_path` 配置或当前工作目录。然后，mypy 将使用相对路径来确定完全合格的模块名称。

   例如，假设您的目录树仅包含 ``src/namespace_pkg/mod.py``。如果您运行以下命令，mypy 将正确地将 ``mod.py`` 关联到 ``namespace_pkg.mod``::

       $ MYPYPATH=src mypy --namespace-packages --explicit-package-bases .

如果您传递一个不以 ``.py[i]`` 结尾的文件，则假定的模块名称是 ``__main__`` （与 Python 解释器的行为相匹配），除非传递了 :option:`--scripts-are-modules <mypy --scripts-are-modules>`。

传递 :option:`-v <mypy -v>` 将显示 mypy 将检查的文件和关联的模块名称。


mypy 如何处理导入(handles imports)
************************************************

当 mypy 遇到 ``import`` 语句时，它将首先 :ref:`尝试定位 <finding-imports>` 文件系统中的该模块或该模块的类型存根。然后，mypy 将对导入的模块进行类型检查。这个过程有三种不同的结果：

1.  Mypy 无法跟踪导入：该模块要么不存在，要么是一个不使用类型提示的第三方库。

2.  Mypy 能够跟踪并进行类型检查，但您并不希望 mypy 检查该模块。

3.  Mypy 成功地跟踪并进行了类型检查，并且您希望 mypy 检查该模块。

第三种结果是 mypy 在理想情况下会执行的操作。接下来的部分将讨论在其他两种情况下该怎么做。

.. _ignore-missing-imports:
.. _fix-missing-imports:

缺失导入(Missing imports)
******************************

当您导入一个模块时，mypy 可能会报告它无法跟踪该导入。这可能导致以下类似的错误：

.. code-block:: text

    main.py:1: error: Skipping analyzing 'django': module is installed, but missing library stubs or py.typed marker
    main.py:2: error: Library stubs not installed for "requests"
    main.py:3: error: Cannot find implementation or library stub for module named "this_module_does_not_exist"

如果您在导入时遇到这些错误中的任何一个，mypy 将假设该模块的类型为 ``Any``，即动态类型。这意味着尝试访问该模块的任何属性将自动成功：

.. code-block:: python

    # Error: Cannot find implementation or library stub for module named 'does_not_exist'
    import does_not_exist

    # 但这会通过类型检查，x 将具有类型 'Any'
    x = does_not_exist.foobar()

这可能导致 mypy 未能警告您代码中的错误。由于对 ``Any`` 的操作结果仍为 ``Any``，这些动态类型可能在您的代码中传播，从而降低类型检查的有效性。有关更多信息，请参见 :ref:`dynamic-typing`。

接下来的部分将描述这些错误的含义及推荐的下一步措施；请滚动到与您的错误匹配的部分。


缺失包存根文件或py.typed标记(Missing library stubs)
----------------------------------------------------------

如果您收到 ``Skipping analyzing X: module is installed, but missing library stubs or py.typed marker`` 错误，这意味着 mypy 能够找到您正在导入的模块，但没有相应的类型提示。

Mypy 不会尝试推断您安装的任何第三方库的类型，除非它们已声明自己符合 :ref:`PEP 561 compliant stub package <installed-packages>` （例如，包含 ``py.typed`` 文件）或在 `typeshed <https://github.com/python/typeshed>`_ 上注册，该库是标准库和一些第三方库的类型存根。

如果您遇到此错误，请尝试为您使用的库获取类型提示：

1.  升级您使用的库的版本，以防较新版本开始包含类型提示。

2.  查找是否有与您第三方库对应的 :ref:`PEP 561 compliant stub package <installed-packages>`。存根包使您能够独立于库本身安装类型提示。

    例如，如果您想要 ``django`` 库的类型提示，可以安装 `django-stubs <https://pypi.org/project/django-stubs/>`_ 包。

3.  :ref:`编写自己的存根文件 <stub-files>`，其中包含库的类型提示。您可以通过命令行传递、使用 :confval:`files` 或 :confval:`mypy_path` 配置文件选项，或通过将位置添加到 ``MYPYPATH`` 环境变量来指向您的类型提示。

    这些存根文件不需要完整!一个好的策略是使用 :ref:`stubgen <stubgen>`，这是与 mypy 一起打包的程序，生成存根的初步草稿。然后，您可以仅在所需的库部分进行迭代。

    如果您想分享您的工作，可以尝试将您的存根贡献回库中——请参阅我们关于创建 :ref:`PEP 561 compliant packages <installed-packages>` 的文档。

如果您无法找到现有的类型提示，也没有时间编写自己的类型提示，您可以选择 *抑制(suppress)* 错误。

这只会使 mypy 停止在包含导入的行上报告错误：导入的模块将继续为类型 ``Any``，并且 mypy 可能不会捕获其使用中的错误。

1.  要抑制 *单个(single)* 缺失导入错误，请在包含导入的行末尾添加 ``# type: ignore``。

2.  要抑制来自单个库的 *所有* 缺失导入错误，请在您的 :ref:`mypy 配置文件 <config-file>` 中添加一个每模块部分，将 :confval:`ignore_missing_imports` 设置为 True。例如，假设您的代码库大量使用一个（未类型化的）库 ``foobar``。您可以通过在配置文件中添加以下部分来静默与该库相关的所有导入错误::

        [mypy-foobar.*]
        ignore_missing_imports = True

    注意：此选项等同于在您的代码库中对 ``foobar`` 的每个导入添加 ``# type: ignore``。有关更多信息，请参阅有关配置 :ref:`import discovery <config-file-import-discovery>` 的文档。``.*`` 在 ``foobar`` 后将忽略对 ``foobar`` 模块和子包的导入，除了 ``foobar`` 顶级包命名空间之外。

3.  要抑制代码库中 *所有(all)* 未类型化库的 *所有(all)* 缺失导入错误，请使用 :option:`--disable-error-code=import-untyped <mypy --ignore-missing-imports>`。有关此错误代码的更多详细信息，请参见 :ref:`code-import-untyped`。

    您还可以像这样设置 :confval:`disable_error_code`::

        [mypy]
        disable_error_code = import-untyped

    您还可以设置 :option:`--ignore-missing-imports <mypy --ignore-missing-imports>` 命令行标志，或在您的 mypy 配置文件的 *全局* 部分将 :confval:`ignore_missing_imports` 配置选项设置为 True。如果可能，我们建议避免使用 ``--ignore-missing-imports``：这等同于对您代码库中的所有未解析导入添加 ``# type: ignore``。


包存根文件未安装(not installed)
------------------------------------

如果 mypy 找不到第三方库的存根，但它知道该库的存根存在，您将收到如下消息：

.. code-block:: text

    main.py:1: error: Library stubs not installed for "yaml"
    main.py:1: note: Hint: "python3 -m pip install types-PyYAML"
    main.py:1: note: (or run "mypy --install-types" to install all missing stub packages)

您可以通过运行建议的 pip 命令来解决此问题。如果您在 CI 中运行 mypy，可以确保您需要的任何存根包的存在，方法与其他测试依赖项相同，例如，将它们添加到相应的 ``requirements.txt`` 文件中。

另外，您可以将 :option:`--install-types <mypy --install-types>` 添加到您的 mypy 命令中，以安装所有已知的缺失存根：

.. code-block:: text

    mypy --install-types

这比显式安装存根要慢，因为它实际上运行了两次 mypy——第一次用于查找缺失的存根，第二次在 mypy 安装了存根后正确地进行类型检查。它还可能使控制存根版本变得更加困难，从而导致类型检查的可重复性降低。

默认情况下，:option:`--install-types <mypy --install-types>` 会显示确认提示。使用 :option:`--non-interactive <mypy --non-interactive>` 可以在不要求确认的情况下安装所有建议的存根包，并对您的代码进行类型检查：

如果您已经在 mypy 运行的环境之外安装了相关的第三方库，可以使用 :option:`--python-executable <mypy --python-executable>` 标志指向该环境的 Python 可执行文件，mypy 将找到为该 Python 可执行文件安装的包。

如果您已安装相关的存根包，但仍然收到此错误，请参见下面的 :ref:`部分 <missing-type-hints-for-third-party-library>`。

.. _missing-type-hints-for-third-party-library:

无法找到实现或库存根(Cannot find)
------------------------------------------

如果您收到 ``Cannot find implementation or library stub for module`` 错误，这意味着 mypy 无法找到您尝试导入的模块，无论它是否附带类型提示。如果您遇到此错误，请尝试：

1.  确保您的导入没有拼写错误。

2.  如果该模块是第三方库，请确保 mypy 能够找到包含已安装库的解释器。

    例如，如果您在 virtualenv 中运行代码，请确保在 virtualenv 中安装和使用 mypy。或者，如果您想使用全局安装的 mypy，请将 :option:`--python-executable <mypy --python-executable>` 命令行标志设置为指向包含您已安装的第三方包的 Python 解释器。

    您可以通过像 ``python -m mypy ...`` 这样运行 mypy 来确认您是在预期的环境中运行。您可以通过运行 pip，如 ``python -m pip ...`` 来确认您在预期的环境中安装。

3.  阅读下面的 :ref:`finding-imports` 部分，以确保您理解 mypy 如何搜索和查找模块，并相应地修改您调用 mypy 的方式。

4.  通过使用 :confval:`mypy_path` 或 :confval:`files` 配置文件选项，或使用 ``MYPYPATH`` 环境变量，直接指定包含您要进行类型检查的模块的目录。

    注意：如果您尝试导入的模块实际上是某个包的 *子模块*，则应指定包含 *整个* 包的目录。例如，假设您尝试添加的模块是 ``foo.bar.baz``，它位于 ``~/foo-project/src/foo/bar/baz.py``。在这种情况下，您必须运行 ``mypy ~/foo-project/src`` (或将 ``MYPYPATH`` 设置为 ``~/foo-project/src`` )。

.. _finding-imports:

如何发现导入(found import)
******************************

当 mypy 遇到 ``import`` 语句或通过 :option:`--module <mypy --module>` 或 :option:`--package <mypy --package>` 标志从命令行接收模块名称时，mypy 尝试在文件系统上查找该模块，类似于 Python 查找模块的方式。然而，有一些不同之处。

首先，mypy 有自己的搜索路径。这是根据以下项目计算得出的：

- ``MYPYPATH`` 环境变量（在 UNIX 系统上为以冒号分隔的目录列表，在 Windows 上为以分号分隔）。
- :confval:`mypy_path` 配置文件选项。
- 命令行中给出的源代码所包含的目录（见 :ref:`Mapping file paths to modules <mapping-paths-to-modules>`）。
- 标记为安全进行类型检查的已安装包（见 :ref:`PEP 561 support <installed-packages>`）。
- `typeshed <https://github.com/python/typeshed>`_ 仓库的相关目录。

.. note::

    您不能通过 ``MYPYPATH`` 指向仅包含存根的包 (:pep:`561`)，它必须已安装（见 :ref:`PEP 561 support <installed-packages>`）。

其次，mypy 在查找常规 Python 文件和包时，还会搜索存根文件。查找模块 ``foo`` 的规则如下：

- 搜索会查看搜索路径中的每个目录（见上文），直到找到匹配项。
- 如果找到名为 ``foo`` 的包（即一个包含 ``__init__.py`` 或 ``__init__.pyi`` 文件的目录 ``foo`` )，那么这是一个匹配。
- 如果找到名为 ``foo.pyi`` 的存根文件，那么这是一个匹配。
- 如果找到名为 ``foo.py`` 的 Python 模块，那么这是一个匹配。

这些匹配项是按顺序尝试的，因此如果在搜索路径的同一目录中找到多个匹配项（例如，一个包和一个 Python 文件，或一个存根文件和一个 Python 文件），则列表中第一个的匹配将胜出。

特别是，如果在搜索路径的同一目录中同时存在一个 Python 文件和一个存根文件，则仅使用存根文件。（但是，如果文件位于不同的目录中，则使用在较早的目录中找到的文件。）

设置 :confval:`mypy_path`/``MYPYPATH`` 在您想要尝试对多组不同文件进行 mypy 检查且这些文件恰好共享一些公共依赖项的情况下特别有用。

例如，如果您有多个项目恰好使用同一组正在进行中的存根，直接将 ``MYPYPATH`` 指向包含存根的单一目录可能会更方便。

.. _follow-imports:

跟踪导入(Following imports)
**********************************

Mypy 旨在 :ref:`坚持跟踪所有导入 <finding-imports>`，即使导入的模块不是您明确希望 mypy 检查的文件。

例如，假设我们有两个模块 ``mycode.foo`` 和 ``mycode.bar``：前者有类型提示，后者没有。我们运行 :option:`mypy -m mycode.foo <mypy -m>`，mypy 发现 ``mycode.foo`` 导入了 ``mycode.bar``。

我们希望 mypy 如何检查 ``mycode.bar`` 的类型？这里 mypy 的行为是可配置的——尽管我们 **强烈推荐** 使用默认设置——通过使用 :option:`--follow-imports <mypy --follow-imports>` 标志。此标志接受四个字符串值之一：

-   ``normal`` （默认，推荐）正常跟踪所有导入并检查所有顶级代码的类型（以及所有具有至少一个类型注解的函数和方法的主体）。

-   ``silent`` 的行为与 ``normal`` 相同，但会额外 *抑制(suppress)* 任何错误消息。

-   ``skip`` *不(not)* 跟踪导入，而是会静默地将模块（及其 *任何导入的内容(anything imported from it)* ）替换为类型为 ``Any`` 的对象。

-   ``error`` 的行为与 ``skip`` 相同，但并不完全静默——它会将导入标记为错误，如下所示::

        main.py:1: note: Import of "mycode.bar" ignored
        main.py:1: note: (Using --follow-imports=error, module not passed on command line)

如果您正在启动一个新的代码库并计划从一开始就使用类型提示，我们建议您使用 :option:`--follow-imports=normal <mypy --follow-imports>` （默认）或 :option:`--follow-imports=error <mypy --follow-imports>` 。任一选项将帮助确保您不会意外跳过检查代码库的任何部分。

如果您计划在一个大型现有代码库中添加类型提示，我们建议您首先尝试使整个代码库（包括不使用类型提示的文件）在 :option:`--follow-imports=normal <mypy --follow-imports>` 下通过。这通常并不太难做到：mypy 设计时考虑了在查看未注解代码时报告尽可能少的错误消息。

仅当这样做不可行时，我们建议您只传递希望检查的文件，并使用 :option:`--follow-imports=silent <mypy --follow-imports>`。即使 mypy 无法完美地检查一个文件的类型，它仍然可以通过解析文件获取一些有用的信息（例如，理解某个对象具有的方法）。有关更多建议，请参见 :ref:`existing-code`。

我们不推荐使用 ``skip``，除非您知道自己在做什么：虽然此选项可能非常强大，但也可能导致许多难以调试的错误。

调整导入跟踪行为通常在限制于特定模块时最有用。这可以通过设置每个模块的 :confval:`follow_imports` 配置选项来实现。
