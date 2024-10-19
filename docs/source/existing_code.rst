.. _existing-code:

在现有代码库中使用 mypy
==========================

本节说明如何在一个现有的、类型注解较少或没有类型注解的代码库中开始使用 mypy。如果您是初学者，可以跳过本节。

从小处着手
-----------

如果您的代码库较大，选择其中一个子集（例如，5,000 到 50,000 行），首先让 mypy 成功运行该子集，而*不添加注释*。这在一两天内应该是可以做到的。尽早让 mypy 通过，您就能更早获益。

您可能需要修复一些 mypy 错误，或者通过插入 mypy 要求的注释或添加 ``# type: ignore`` 注释来静默您暂时不想修复的错误。

确保 mypy 一致运行并防止回归
-----------------------------------

确保您代码库中的所有开发人员以相同方式运行 mypy。确保这一点的一种方法是将 mypy 调用的小脚本添加到代码库中，或者将 mypy 调用添加到您用于运行测试的现有工具中，例如 ``tox``。

* 确保每个人都使用相同的选项运行 mypy。将 mypy :ref:`配置文件 <config-file>` 检查到代码库中是最简单的方法。

* 确保每个人检查相同的文件集。有关详细信息，请参见 :ref:`specifying-code-to-be-checked`。

* 确保每个人都使用相同版本的 mypy，例如，通过将 mypy 固定在其余开发要求中。

特别是，您要尽快确保在持续集成（CI）系统中运行 mypy。这将防止新的类型错误被引入到代码库中。

一个简单的 CI 脚本可能如下所示：

.. code-block:: text

    python3 -m pip install mypy==1.8
    # 运行您的标准化 mypy 调用，例如
    mypy my_project
    # 这也可以是 `scripts/run_mypy.sh`，`tox run -e mypy`，`make mypy` 等等。

忽略特定模块的错误
----------------------

默认情况下，mypy 会跟随您代码中的导入，并尝试检查所有内容。这意味着即使您只传递了几个文件给 mypy，它仍可能处理大量导入的文件。这可能导致您不想立即处理的许多错误。

解决此问题的一种方法是忽略尚未准备好进行类型检查的模块中的错误。:confval:`ignore_errors` 选项对此非常有用，例如，如果您尚未准备好处理 ``package_to_fix_later`` 的错误：

.. code-block:: text

   [mypy-package_to_fix_later.*]
   ignore_errors = True

您甚至可以反转这一点，在全局配置部分设置 ``ignore_errors = True``，并仅为您准备进行类型检查的模块启用错误报告，即设置 ``ignore_errors = False``。

mypy 的配置文件允许的每个模块配置可以极为有用。许多配置选项可以仅为特定模块启用或禁用。特别是，您还可以基于每个模块启用或禁用各种错误代码，参见 :ref:`error-codes`。

修复与导入相关的错误
----------------------

您可能会遇到的常见错误类型是 mypy 报告的无法找到模块、没有类型或没有存根文件的错误：

.. code-block:: text

    core/config.py:7: error: Cannot find implementation or library stub for module named 'frobnicate'
    core/model.py:9: error: Cannot find implementation or library stub for module named 'acme'
    ...

有时，这些可以通过在您运行 ``mypy`` 的环境中安装相关的软件包或存根库来修复。

有关这些错误的完整参考以及您可以修复它们的方式，请参见 :ref:`fix-missing-imports`。

您可能希望抑制来自某个没有类型的导入模块的所有错误。如果您只在一两个地方导入该模块，可以使用 ``# type: ignore`` 注释。例如，这里我们使用 ``# type: ignore`` 忽略了关于没有存根的第三方模块 ``frobnicate`` 的错误：

.. code-block:: python

   import frobnicate  # type: ignore
   ...
   frobnicate.initialize()  # OK (但未检查)

但如果您在许多地方导入该模块，这种做法会变得繁琐。在这种情况下，我们建议使用 :ref:`配置文件 <config-file>`。例如，要在代码库中的所有地方禁用导入 ``frobnicate`` 和 ``acme`` 的错误，可以使用如下配置：

.. code-block:: text

   [mypy-frobnicate.*]
   ignore_missing_imports = True

   [mypy-acme.*]
   ignore_missing_imports = True

如果您遇到大量错误，您可能希望忽略所有关于缺失导入的错误，例如通过设置 :option:`--disable-error-code=import-untyped <mypy --ignore-missing-imports>`，或者全局设置 :confval:`ignore_missing_imports` 为 true。这可能会隐藏后续的错误，因此我们建议尽可能避免这种做法。

最后，mypy 允许对特定导入跟踪行为进行精细控制。在处理这些时，很容易无意中造成问题，因此这应作为最后的手段。有关更多详细信息，请查看 :ref:`here <follow-imports>`。

优先为广泛导入的模块添加注释
----------------------------------

大多数项目都有一些广泛导入的模块，例如工具类或模型类。尽早为这些模块添加注释是个好主意，因为这能更有效地进行类型检查。

Mypy 支持渐进式类型检查，也就是说，您可以按照自己的节奏添加注释，因此可以暂时不为某些模块添加注释。注释越多，mypy 就越有用，但即使是少量的注释覆盖也很有帮助。

在编写代码时逐步添加注释
---------------------------

考虑在您的代码风格规范中加入以下建议：

1. 开发者应为任何新代码添加注释。
2. 在修改现有代码时，鼓励编写注释。

通过这种方式，您可以在不费太大力气的情况下逐步增加代码库中的注释覆盖率。

自动化旧代码的注释
------------------

可以使用一些工具基于简单的静态分析或在运行时收集的类型信息自动添加草拟注释。这些工具包括 :doc:`monkeytype:index` 、 `autotyping`_  和 `PyAnnotate`_ 。

一种简单的方法是从测试运行中收集类型信息。如果您的测试覆盖率良好（并且测试速度不太慢），这种方法可能效果很好。

另一种方法是为小比例的生产网络请求启用类型收集。这显然需要更加谨慎，因为类型收集可能会影响服务的可靠性或性能。

.. _getting-to-strict:

引入更严格的选项
--------------------------

Mypy 提供了高度可配置的选项。一旦开始使用静态类型，您可能希望探索 mypy 提供的各种严格性选项，以捕捉更多的错误。例如，您可以要求 mypy 对某些模块中的所有函数进行注释，以避免意外引入未进行类型检查的代码，使用 :confval:`disallow_untyped_defs` 。有关详细信息，请参考 :ref:`config-file`。

一个优秀的目标是确保您的代码库在运行 `mypy --strict` 时能够通过。这基本上确保您不会在没有明确规避的情况下遇到类型相关的错误（例如 `# type: ignore` 注释）。

以下配置等同于 `--strict` （截至 mypy 1.0）：

.. code-block:: text

   # 首先开启这些选项
   warn_unused_configs = True
   warn_redundant_casts = True
   warn_unused_ignores = True

   # 这些应该很容易通过
   strict_equality = True
   strict_concatenate = True

   # 尽快启用这个选项
   check_untyped_defs = True

   # 这些应该不会增加太多额外工作，但如果使用了很多未注释的库，可能会有些棘手
   disallow_subclassing_any = True
   disallow_untyped_decorators = True
   disallow_any_generics = True

   # 以下选项是强制使用类型注解的不同级别
   disallow_untyped_calls = True
   disallow_incomplete_defs = True
   disallow_untyped_defs = True

   # 这个不太难通过，但投资回报较低
   no_implicit_reexport = True

   # 如果使用了很多未注释的库，这个可能会很棘手
   warn_return_any = True


请注意，您也可以从 `--strict` 开始，并进行减法，例如：

.. code-block:: text

   strict = True
   warn_return_any = False

记住，许多这些选项可以在模块级别启用。例如，您可能希望对已完成注释的模块启用 `disallow_untyped_defs`，以防止新代码在没有注释的情况下被添加。

如果您愿意，也可以超越 `--strict`。Mypy 还有一些不属于 `--strict` 的附加检查，这些检查可能会很有用。请参阅完整的 :ref:`command-line` 参考和 :ref:`error-codes-optional`。

加快 mypy 运行速度
------------------

您可以使用 :ref:`mypy daemon <mypy_daemon>` 来实现更快的增量 mypy 运行。您的项目越大，这种效果就越明显。如果您的项目大约有 100,000 行代码或更多，您可能还想设置 :ref:`remote caching <remote-cache>` 以进一步加快速度。

.. _PyAnnotate: https://github.com/dropbox/pyannotate
.. _autotyping: https://github.com/JelleZijlstra/autotyping
