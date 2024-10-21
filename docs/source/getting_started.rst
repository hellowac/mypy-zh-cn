.. _getting-started:

入门
===============

本章介绍了 mypy 的一些核心概念，包括函数注解、`:py:mod:`typing` 模块、存根文件等。

如果您想快速入门，请参见
:ref:`mypy 备忘单 <cheat-sheet-py3>`。

如果您不熟悉静态和动态类型检查的概念，请仔细阅读本章，因为后续文档可能不会太容易理解。

安装和运行 mypy
***************************

Mypy 需要 Python 3.8 或更高版本才能运行。您可以使用 pip 安装 mypy：

.. code-block:: shell

    $ python3 -m pip install mypy

安装完成后，使用 ``mypy`` 工具运行它：

.. code-block:: shell

    $ mypy program.py

此命令将使 mypy 对您的 ``program.py`` 文件进行 *类型检查*，并打印出它发现的任何错误。Mypy 将对您的代码进行 *静态* 类型检查：这意味着它在检查错误时不会运行您的代码，类似于一个代码检查工具。

这也意味着，如果您愿意，可以随时忽略 mypy 报告的错误。即使 mypy 报告错误，您仍然可以使用 Python 解释器运行代码。

然而，如果您尝试直接在现有 Python 代码上运行 mypy，可能会报告几乎没有错误。这是一个特性!它使得逐步采用 mypy 变得容易。

为了从 mypy 获得有用的诊断信息，您必须在代码中添加 *类型注解*。请参阅下面的部分以获取详细信息。

.. _getting-started-dynamic-vs-static:

动态与静态类型
************************

没有类型注解的函数被 mypy 视为 *动态类型*：

.. code-block:: python

   def greeting(name):
       return 'Hello ' + name

默认情况下，mypy **不** 会对动态类型的函数进行类型检查。这意味着，除了少数例外，mypy 不会对常规未注解的 Python 报告任何错误。

即使您错误地使用该函数，也会如此!

.. code-block:: python

   def greeting(name):
       return 'Hello ' + name

   # 这些调用在程序运行时会失败，但 mypy 不会报告错误
   # 因为 "greeting" 没有类型注解。
   greeting(123)
   greeting(b"Alice")

我们可以通过添加 *类型注解*（也称为 *类型提示*）让 mypy 检测这些类型的错误。例如，您可以告诉 mypy ``greeting`` 函数既接受又返回一个字符串，如下所示：

.. code-block:: python

   # "name: str" 注解表示 "name" 参数应该是一个字符串
   # "-> str" 注解表示 "greeting" 将返回一个字符串
   def greeting(name: str) -> str:
       return 'Hello ' + name

这个函数现在是 *静态类型*：mypy 将使用提供的类型提示来检测对 ``greeting`` 函数的不正确使用以及在 ``greeting`` 函数内对变量的不正确使用。例如：

.. code-block:: python

   def greeting(name: str) -> str:
       return 'Hello ' + name

   greeting(3)         # 对 "greeting" 的第一个参数类型不兼容 "int"，预期 "str"
   greeting(b'Alice')  # 对 "greeting" 的第一个参数类型不兼容 "bytes"，预期 "str"
   greeting("World!")  # 没有错误

   def bad_greeting(name: str) -> str:
       return 'Hello ' * name  # 不支持的操作数类型用于 * ("str" 和 "str")

能够选择函数是动态类型还是静态类型是非常有帮助的。例如，如果您正在将现有的 Python 代码库迁移到使用静态类型，通常通过逐步添加类型提示而不是一次性添加所有提示会更容易。同样，当您在原型设计新功能时，最初使用动态类型实现代码可能更方便，等代码更加稳定后再添加类型提示。

一旦您完成了代码的迁移或原型设计，您可以使用 :option:`--disallow-untyped-defs <mypy --disallow-untyped-defs>` 标志来警告您是否错误地添加了动态函数。您还可以使用 :option:`--check-untyped-defs <mypy --check-untyped-defs>` 标志让 mypy 对动态类型的函数进行一些有限的检查。有关配置 mypy 的更多信息，请参见 :ref:`command-line`。

严格模式与配置
*****************************

Mypy 具有 *严格模式*，可以启用许多额外的检查，如 :option:`--disallow-untyped-defs <mypy --disallow-untyped-defs>`。

如果您使用 :option:`--strict <mypy --strict>` 标志运行 mypy，基本上在运行时不会出现与类型相关的错误而没有相应的 mypy 错误，除非您以某种方式明确规避 mypy。

然而，如果您试图为一个大型现有代码库添加静态类型，这个标志可能会过于严格。有关如何处理这种情况的建议，请参见 :ref:`existing-code`。

Mypy 的配置非常灵活，因此您可以先使用 ``--strict``，再逐个关闭特定的检查。例如，如果您使用了许多没有类型的第三方库， :option:`--ignore-missing-imports <mypy --ignore-missing-imports>` 可能会很有用。有关如何逐步达到 ``--strict`` 的信息，请参见 :ref:`getting-to-strict`。

有关配置选项的完整参考，请参见 :ref:`command-line` 和 :ref:`config-file`。

更复杂的类型
******************

到目前为止，我们添加的类型提示仅使用基本的具体类型，如 ``str`` 和 ``float``。如果我们想表达更复杂的类型，例如“字符串列表”或“整数的可迭代对象”怎么办？

例如，要指示某个函数可以接受字符串列表，可以使用 ``list[str]`` 类型（Python 3.9 及更高版本）：

.. code-block:: python

    def greet_all(names: list[str]) -> None:
        for name in names:
            print('Hello ' + name)

    names = ["Alice", "Bob", "Charlie"]
    ages = [10, 20, 30]

    greet_all(names)   # 没问题!
    greet_all(ages)    # 因为类型不兼容而出错


`:py:class:`list` 类型是被称为 *泛型类型* 的一个例子：它可以接受一个或多个 *类型参数*。在这种情况下，我们通过写 ``list[str]`` 对 :py:class:`list` 进行了 *参数化*。这让 mypy 知道 ``greet_all`` 接受特定包含字符串的列表，而不是包含整数或任何其他类型的列表。

在上面的例子中，类型签名可能有些过于严格。毕竟，这个函数不必 *特定* 接受一个列表——如果传入一个元组、集合或任何其他自定义可迭代对象，它也能正常运行。

您可以使用 :py:class:`collections.abc.Iterable` 来表达这个想法：

.. code-block:: python

    from collections.abc import Iterable  # 或者 "from typing import Iterable"

    def greet_all(names: Iterable[str]) -> None:
        for name in names:
            print('Hello ' + name)

这种行为实际上是 PEP 484 类型系统的一个基本方面：当我们用类型 ``T`` 注解某个变量时，我们实际上是在告诉 mypy 该变量可以赋值为 ``T`` 的实例，或者是 ``T`` 的 *子类型* 的实例。也就是说，``list[str]`` 是 ``Iterable[str]`` 的一个子类型。

这同样适用于继承，因此如果您有一个 ``Child`` 类继承自 ``Parent``，那么类型为 ``Child`` 的值可以赋值给类型为 ``Parent`` 的变量。例如，可以将 ``RuntimeError`` 实例传递给注解为接受 ``Exception`` 的函数。

作为另一个例子，假设您想编写一个可以接受 *整数* 或 *字符串* 的函数，但不接受其他类型。您可以使用联合类型来表达这一点。例如，``int`` 是 ``int | str`` 的一个子类型：

.. code-block:: python

  def normalize_id(user_id: int | str) -> str:
      if isinstance(user_id, int):
          return f'user-{100_000 + user_id}'
      else:
          return user_id

.. note::

   如果使用 Python 3.9 或更早版本，请使用 ``typing.Union[int, str]`` 而不是 ``int | str`` ，或者在文件顶部使用 ``from __future__ import annotations`` （参见 :ref:`runtime_troubles`）。

:py:mod:`typing` 模块包含许多其他有用的类型。

要快速浏览，可以查看 :ref:`mypy cheatsheet <cheat-sheet-py3>`。

要详细了解（包括如何创建自己的泛型类型或类型别名的信息），可以查看 :ref:`type system reference <overview-type-system-reference>`。

.. note::

   在添加类型时，约定是使用 ``from typing import <name>`` 形式导入类型（而不是仅仅 ``import typing`` 或 ``import typing as t``，或 ``from typing import *`` )。

   为了简洁，我们在代码示例中通常省略 :py:mod:`typing` 或 :py:mod:`collections.abc` 的导入，但如果您在未导入的情况下使用如 :py:class:`~collections.abc.Iterable` 这样的类型，mypy 会给出错误。

.. note::

   在一些示例中，我们使用了类型的首字母大写变体，如 ``List``，有时使用普通的 ``list``。它们是等价的，但前者在使用 Python 3.8 或更早版本时是必需的。

局部类型推断
********************

一旦您为函数添加了类型提示（即使其具有静态类型），mypy 会自动对该函数的主体进行类型检查。在此过程中，mypy 会尽可能多地尝试 *推断* 细节。

我们在上面的 ``normalize_id`` 函数中看到过这个例子——mypy 理解基本的 :py:func:`isinstance <isinstance>` 检查，因此可以推断在 if 分支中 ``user_id`` 变量的类型为 ``int``，而在 else 分支中为 ``str``。

另一个例子，考虑以下函数。Mypy 可以毫无问题地对该函数进行类型检查：它将利用可用的上下文推断 ``output`` 必须是 ``list[float]`` 类型，``num`` 必须是 ``float`` 类型：

.. code-block:: python

    def nums_below(numbers: Iterable[float], limit: float) -> list[float]:
        output = []
        for num in numbers:
            if num < limit:
                output.append(num)
        return output


有关更多细节，请参见 :ref:`type-inference-and-annotations`。

来自库的类型
********************

Mypy 还可以理解您使用的库中的类型。

例如，mypy 默认情况下对 Python 标准库有深入的了解。以下是一个使用 :doc:`pathlib 标准库模块 <python:library/pathlib>` 中 ``Path`` 对象的函数：

.. code-block:: python

    from pathlib import Path

    def load_template(template_path: Path, name: str) -> str:
        # Mypy 知道 `template_path` 有一个返回 str 的 `read_text` 方法
        template = template_path.read_text()
        # ...因此它理解这行代码的类型检查
        return template.replace('USERNAME', name)

如果您使用的第三方库 :ref:`声明支持类型检查 <installed-packages>`，mypy 将根据其包含的类型提示对您对该库的使用进行类型检查。

然而，如果第三方库没有类型提示，mypy 会抱怨缺少类型信息。

.. code-block:: text

  prog.py:1: error: Library stubs not installed for "yaml"
  prog.py:1: note: Hint: "python3 -m pip install types-PyYAML"
  prog.py:2: error: Library stubs not installed for "requests"
  prog.py:2: note: Hint: "python3 -m pip install types-requests"
  ...

在这种情况下，您可以为 mypy 提供其他类型信息来源，通过安装一个 *stub* 包。Stub 包是一个包含另一个库的类型提示但没有实际代码的包。

.. code-block:: shell

  $ python3 -m pip install types-PyYAML types-requests

分发的 stub 包通常命名为 ``types-<distribution>``。请注意，分发名称可能与您导入的包名称不同。例如，``types-PyYAML`` 包含 ``yaml`` 包的 stubs。

有关处理缺少类型信息的库错误的更多讨论，请参见 :ref:`fix-missing-imports` 。

有关 stubs 的更多信息，请参见 :ref:`stub-files` 。

下一步
**********

如果您急于开始，不想在阅读大量文档后再行动，这里有一些快速学习资源的指引：

* 阅读 :ref:`mypy cheatsheet <cheat-sheet-py3>`。

* 如果您有一个没有很多类型注解的现有大型代码库，请阅读 :ref:`existing-code`。

* 阅读关于 Zulip 项目采用 mypy 经验的 `博客文章 <https://blog.zulip.org/2016/10/13/static-types-in-python-oh-mypy/>`_。

* 如果您喜欢观看讲座而不是阅读，这里有一些推荐：

  * Carl Meyer: `在现实世界中的类型检查 Python <https://www.youtube.com/watch?v=pMgmKJyWKn8>`_ （PyCon 2018）

  * Greg Price: `大规模清晰代码：Zulip 和 Dropbox 的静态类型 <https://www.youtube.com/watch?v=0c46YHS3RY8>`_ （PyCon 2018）

* 如果您遇到问题，可以查看 :ref:`mypy 常见问题解决方案 <common_issues>`。

* 您可以在 `mypy 问题跟踪器 <https://github.com/python/mypy/issues>`_ 和 `typing Gitter 聊天 <https://gitter.im/python/typing>`_ 提问。

* 对于关于 Python 类型的常规问题，可以尝试在 `typing 讨论区 <https://github.com/python/typing/discussions>`_ 发布。

您也可以继续阅读本文档，跳过与您无关的部分。您不需要按顺序阅读各个部分。
