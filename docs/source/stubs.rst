.. _stub-files:

存根文件(Stub)
================

*存根文件* 是包含 Python 模块公共接口框架的文件，包括类、变量、函数——最重要的是它们的类型。

Mypy 使用存储在 `typeshed <https://github.com/python/typeshed>`_ 仓库中的存根文件来确定标准库和第三方库的函数、类及其他定义的类型。您也可以创建自己的存根，以用于类型检查您的代码。

创建存根文件
***************

以下是创建存根文件的概述：

* 为库（或任意模块）编写存根文件，并将其存储为 ``.pyi`` 文件，放在库模块的同一目录中。
* 或者，将您的存根（ ``.pyi`` 文件）放在专门用于存根的目录中（例如：:file:`myproject/stubs` ）。在这种情况下，您需要将环境变量 ``MYPYPATH`` 设置为指向该目录。例如::

    $ export MYPYPATH=~/work/myproject/stubs

使用普通的 Python 文件命名约定来命名模块，例如： :file:`csv.pyi` 对于模块 ``csv``。对于包，使用子目录和 :file:`__init__.pyi` 文件。请注意，:pep:`561` 存根-only 包必须已安装，并且不能通过 ``MYPYPATH`` 指向（见 :ref:`PEP 561 support <installed-packages>` ）。

如果一个目录同时包含 ``.py`` 和 ``.pyi`` 文件，则 ``.pyi`` 文件优先。这种方式可以让您轻松地为模块添加注释，即使您不想修改源代码。例如，如果您在程序中使用第三方开源库（而 typeshed 中尚未有存根），这将非常有用。

就这样！

现在您可以在 mypy 程序中访问该模块，并对使用该库的代码进行类型检查。如果您为某个库模块编写了存根，考虑将其贡献回 typeshed 仓库，以便其他使用 mypy 的程序员也能使用。

Mypy 还附带了两个工具，以便更轻松地创建和维护存根：:ref:`stubgen` 和 :ref:`stubtest`。

以下部分将解释您可以在程序和存根文件中使用的类型注解种类。

.. note::

   您可能会想将 ``MYPYPATH`` 指向标准库或安装了第三方包的 :file:`site-packages` 目录。这几乎总是个坏主意——您很可能会收到大量关于您未编写的代码的错误消息，而 mypy 对这些代码的分析效果并不好。在最坏的情况下，mypy 可能由于某个第三方包中意外的构造而崩溃。

存根文件语法(syntax)
*********************

存根文件采用正常的 Python 语法编写，但通常省略运行时逻辑，如变量初始化、函数体和默认参数。

如果无法完全省略某些运行时逻辑，建议使用省略号表达式（ ``...`` ）进行替代或省略。每个省略号在存根文件中字面上写作三个点：

.. code-block:: python

    # 带注解的变量不需要赋值。
    # 因此，按照惯例，我们在存根文件中省略它们。
    x: int

    # 函数体不能完全删除。按照惯例，
    # 我们用 `...` 替代 `pass` 语句。
    def func_1(code: str) -> int: ...

    # 默认参数也可以这样处理。
    def func_2(a: int, b: int = ...) -> int: ...

.. note::

    省略号 ``...`` 在 :ref:`可调用类型 <callable-types>` 和 :ref:`元组类型 <tuple-types>` 中也有不同的含义。

在运行时使用存根文件语法(runtime)
*********************************

您可能偶尔需要在常规 Python 代码中省略实际逻辑，例如，在编写 :ref:`重载变体 <function-overloading>` 或 :ref:`自定义协议 <protocol-types>` 的方法时。

推荐的风格是使用省略号来实现这一点，和存根文件中的用法一样。对于可能意外调用没有实际逻辑的函数的代码用户，抛出 :py:exc:`NotImplementedError` 也是被认为在风格上可接受的做法。

只要函数体中没有运行时逻辑，您也可以省略默认参数: 函数体只包含一个省略号、pass 语句或 ``raise NotImplementedError()`` 。函数体包含文档字符串也是可以接受的。例如：

.. code-block:: python

    from typing import Protocol

    class Resource(Protocol):
        def ok_1(self, foo: list[str] = ...) -> None: ...

        def ok_2(self, foo: list[str] = ...) -> None:
            raise NotImplementedError()

        def ok_3(self, foo: list[str] = ...) -> None:
            """一些文档字符串"""
            pass

        # 错误：参数 "foo" 的默认值不兼容（默认值类型为 "ellipsis"，参数类型为 "list[str]"）
        def not_ok(self, foo: list[str] = ...) -> None:
            print(foo)
