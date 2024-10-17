.. _installed-packages:

使用已安装的包(Using installed packages)
================================================

通过 pip 安装的包可以声明它们支持类型检查。例如， `aiohttp <https://docs.aiohttp.org/en/stable/>`_ 包内置支持类型检查。

包也可以为库提供存根。例如， ``types-requests`` 是一个仅提供存根的包，它为 `requests <https://requests.readthedocs.io/en/master/>`_ 包提供存根。存根包通常从 `typeshed <https://github.com/python/typeshed>`_ 发布，这是一个共享的 Python 库存根仓库，存根包的命名格式通常为 ``types-<library>``。注意，许多存根包并非由原包的维护者维护。

以下部分解释了 mypy 如何使用这些包，以及如何创建此类包。

.. note::

   :pep:`561` 规定了一个包如何声明它支持类型检查。

.. note::

   新版本的存根包通常使用不被较旧甚至最近版本的 mypy 支持的类型系统功能。如果你将 mypy 固定为较旧版本（例如使用 ``requirements.txt``），建议你也将所有存根包依赖项的版本固定。

.. note::

   从 mypy 0.900 开始，大多数第三方包存根必须显式安装。这将 mypy 与存根版本进行解耦，使得存根可以独立更新而不需要更新 mypy。这也允许安装最初未包含在 mypy 中的存根。早期版本的 mypy 包含了一组固定的第三方包存根。

在 mypy 中使用已安装的包(PEP 561)
****************************************

通常，mypy 会自动找到并使用支持类型检查或提供存根的已安装包。这要求你在运行 mypy 的 Python 环境中安装这些包。由于许多包尚不支持类型检查，你可能还需要安装一个单独的存根包，通常命名为 ``types-<library>``。 （有关如何处理不支持类型检查且缺少存根的库，请参阅 :ref:`fix-missing-imports`）。

如果你在另一个 Python 安装或环境中安装了已键入的包，mypy 不会自动找到它们。一个选项是将这些包的副本安装在你安装了 mypy 的环境中。或者，你可以使用 :option:`--python-executable <mypy --python-executable>` 选项指向另一个环境的 Python 可执行文件，mypy 将找到为该 Python 可执行文件安装的包。

请注意，mypy 不支持一些更高级的导入功能，如 zip 导入和自定义导入钩子。

如果你不想使用任何提供类型信息的已安装包，可以使用 :option:`--no-site-packages <mypy --no-site-packages>` 选项禁用搜索已安装包。

注意，仅存根包不能与 ``MYPYPATH`` 一起使用。如果你希望 mypy 找到该包，则必须安装它。对于包 ``foo``，仅存根包的名称（``foo-stubs``）不是合法的包名称，因此 mypy 不会找到它，除非它已被安装（有关更多信息，请参阅 :pep:`PEP 561: Stub-only Packages <561#stub-only-packages>`）。

创建符合 PEP 561 的包(Creating PEP 561 compatible packages)
************************************************************************

.. note::

  除非你维护一个在 PyPI 上的包，或者想为现有的 PyPI 包发布类型信息，否则你通常可以忽略此部分。

:pep:`561` 描述了分发类型信息的三种主要方式：

1. 包在 Python 实现中包含内联类型注解。

2. 包随 Python 实现一起提供带有类型信息的 :ref:`存根文件 <stub-files>`。

3. 包将类型信息作为存根文件单独分发给另一个包（也称为“仅存根包”）。

如果你想为现有的库创建仅存根包，最简单的方法是向 `typeshed <https://github.com/python/typeshed>`_ 仓库贡献存根文件，存根包将自动上传到 PyPI。

如果你想将库包发布到包仓库（例如 PyPI）用于内部或外部类型检查，提供类型信息的包应在代码中的类型注释或类型标注旁边放置一个 ``py.typed`` 文件在包目录中。例如，下面是一个典型的目录结构：

.. code-block:: text

    setup.py
    package_a/
        __init__.py
        lib.py
        py.typed

``setup.py`` 文件可以是这样的：

.. code-block:: python

    from setuptools import setup

    setup(
        name="SuperPackageA",
        author="Me",
        version="0.1",
        package_data={"package_a": ["py.typed"]},
        packages=["package_a"]
    )

有些包包含存根文件和运行时文件的混合。这些包也需要一个 ``py.typed`` 文件。下面是一个示例：

.. code-block:: text

    setup.py
    package_b/
        __init__.py
        lib.py
        lib.pyi
        py.typed

``setup.py`` 文件可能是这样的：

.. code-block:: python

    from setuptools import setup

    setup(
        name="SuperPackageB",
        author="Me",
        version="0.1",
        package_data={"package_b": ["py.typed", "lib.pyi"]},
        packages=["package_b"]
    )

在这个示例中，``lib.py`` 和 ``lib.pyi`` 存根文件都存在。运行时，Python 解释器将使用 ``lib.py``，但 mypy 会使用 ``lib.pyi``。

如果包是仅存根包（运行时不导入），该包的前缀应为运行时包名，后缀为 ``-stubs`` 。仅存根包不需要 ``py.typed`` 文件。例如，如果我们有 ``package_c`` 的存根，我们可以这样做：

.. code-block:: text

    setup.py
    package_c-stubs/
        __init__.pyi
        lib.pyi

``setup.py`` 可能是这样的：

.. code-block:: python

    from setuptools import setup

    setup(
        name="SuperPackageC",
        author="Me",
        version="0.1",
        package_data={"package_c-stubs": ["__init__.pyi", "lib.pyi"]},
        packages=["package_c-stubs"]
    )

上述指令足以确保生成的 wheels 包含适当的文件。然而，为了确保包含在 ``sdist``（``.tar.gz`` 压缩包）中，你还可能需要修改 ``MANIFEST.in`` 中的包含规则：

.. code-block:: text

    global-include *.pyi
    global-include *.typed
