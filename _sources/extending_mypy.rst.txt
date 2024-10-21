.. _extending-mypy:

扩展和集成 mypy(Extending and integrating mypy)
============================================================

.. _integrating-mypy:

将 mypy 集成到另一个 Python 应用中(Integrating mypy into another Python application)
************************************************************************************************

可以通过导入 ``mypy.api`` 并调用 ``run`` 函数将 mypy 集成到另一个 Python 3 应用中。该函数接受一个 ``list[str]`` 类型的参数，其中包含通常传递给 mypy 的命令行参数。

函数 ``run`` 返回一个 ``tuple[str, str, int]``，即 ``(<normal_report>, <error_report>, <exit_status>)``，其中 ``<normal_report>`` 是 mypy 通常写入 :py:data:`sys.stdout` 的内容，``<error_report>`` 是 mypy 通常写入 :py:data:`sys.stderr` 的内容，``exit_status`` 是 mypy 通常返回给操作系统的退出状态。

使用该 API 的一个简单示例如下：

.. code-block:: python

    import sys
    from mypy import api

    result = api.run(sys.argv[1:])

    if result[0]:
        print('\nType checking report:\n')
        print(result[0])  # stdout

    if result[1]:
        print('\nError report:\n')
        print(result[1])  # stderr

    print('\nExit status:', result[2])


.. _extending-mypy-using-plugins:

使用插件扩展 mypy(Extending mypy using plugins)
********************************************************

Python 是一种高度动态的语言，具有广泛的元编程能力。许多流行的库利用这些能力创建更加灵活和/或自然的 API，但使用静态类型很难表达这些 API。将 :pep:`484` 类型系统扩展以适应所有现有的动态模式既不切实际，有时甚至是不可能的。

Mypy 支持一个插件系统，使你能够自定义 mypy 的类型检查方式。如果你希望扩展 mypy 以检查使用了难以通过 :pep:`484` 类型表达的库的代码，这会非常有用。

插件系统的重点是提高 mypy 对第三方框架 *语义(semantics)* 的理解。目前还没有办法定义新的第一类类型。

.. note::

   插件系统是实验性的，易于变化。如果你想编写 mypy 插件，建议你先通过 `gitter <https://gitter.im/python/typing>`_ 联系 mypy 核心开发人员。特别是，不保证向后兼容性。

   向后不兼容的更改可能会在没有弃用期的情况下进行，但我们会在 `插件 API 更改公告问题 <https://github.com/python/mypy/issues/6617>`_ 中宣布这些更改。

配置 mypy 使用插件(Configuring mypy to use plugins)
**************************************************************

插件是 Python 文件，可以通过 mypy 的 :confval:`plugins` 选项在 :ref:`配置文件 <config-file>` 中指定，支持两种格式：插件文件的相对或绝对路径，或者模块名称（如果插件是通过 ``pip install`` 安装在与 mypy 运行相同的虚拟环境中）。这两种格式可以混合使用，例如：

.. code-block:: ini

    [mypy]
    plugins = /one/plugin.py, other.plugin

Mypy 将尝试导入这些插件，并寻找一个名为 ``plugin`` 的入口函数。如果插件的入口函数有不同的名称，可以在其后通过冒号指定：

.. code-block:: ini

    [mypy]
    plugins = custom_plugin:custom_entry_point

在接下来的章节中，我们会介绍插件系统的基础知识并附带一些示例。有关技术细节，请参阅 mypy 源代码中的 `mypy/plugin.py <https://github.com/python/mypy/blob/master/mypy/plugin.py>`_ 中的文档字符串。你还可以在捆绑的插件中找到一些好的示例，这些插件位于 `mypy/plugins <https://github.com/python/mypy/tree/master/mypy/plugins>`_。

高级概览(High-level overview)
**************************************

每个入口函数都应该接受一个字符串参数，该参数是完整的 mypy 版本号，并返回 ``mypy.plugin.Plugin`` 的子类：

.. code-block:: python

   from mypy.plugin import Plugin

   class CustomPlugin(Plugin):
       def get_type_analyze_hook(self, fullname: str):
           # 请参阅下面的解释
           ...

   def plugin(version: str):
       # 如果插件适用于所有 mypy 版本，可以忽略版本参数。
       return CustomPlugin

在代码分析的不同阶段（首先是语义分析，然后是类型检查），mypy 会在用户插件上调用诸如 ``get_type_analyze_hook()`` 的方法。例如，这个方法可以返回一个回调，mypy 会使用它来分析具有给定全名的未绑定类型。请参阅 :ref:`下方 <plugin_hooks>` 的完整插件钩子方法列表。

Mypy 维护一个从配置文件获取的插件列表，加上始终启用的默认（内置）插件。对于列表中的每个插件，mypy 会调用一次方法，直到某个方法返回非 ``None`` 值为止。然后这个回调将用于自定义分析/检查当前抽象语法树节点的相应方面。

``get_xxx`` 方法返回的回调将获得当前详细的上下文以及用于创建新节点、新类型、发出错误消息等的 API，结果将用于进一步处理。

插件开发者应确保其插件在增量和守护进程模式下能够良好运行。特别是，插件不应由于缓存插件钩子的结果而持有全局状态。

.. _plugin_hooks:

当前的插件钩子列表(Current list of plugin hooks)
********************************************************

**get_type_analyze_hook()** 用于自定义类型分析器的行为。例如，:pep:`484` 不支持定义变长泛型类型：

.. code-block:: python

   from lib import Vector

   a: Vector[int, int]
   b: Vector[int, int, int]

在分析这段代码时，mypy 会调用 ``get_type_analyze_hook("lib.Vector")``，因此插件可以为每个变量返回某个有效类型。

**get_function_hook()** 用于调整函数调用的返回类型。这个钩子也会在类实例化时调用。如果返回类型过于复杂，无法通过常规的 Python 类型系统表达，这是一个不错的选择。

**get_function_signature_hook()** 用于调整函数的签名。

**get_method_hook()** 与 ``get_function_hook()`` 类似，但用于方法，而不是模块级别的函数。

**get_method_signature_hook()** 用于调整方法的签名。这包括除 :py:meth:`~object.__init__` 和 :py:meth:`~object.__new__` 之外的特殊 Python 方法。例如，在以下代码中：

.. code-block:: python

   from ctypes import Array, c_int

   x: Array[c_int]
   x[0] = 42

mypy 会调用 ``get_method_signature_hook("ctypes.Array.__setitem__")``，这样插件可以模仿 :py:mod:`ctypes` 的自动转换行为。

**get_attribute_hook()** 用于重写实例成员字段查找和属性访问（不包括方法调用）。该钩子只针对类中已经存在的字段调用。*例外情况：* 如果类上有 :py:meth:`__getattr__ <object.__getattr__>` 或 :py:meth:`__getattribute__ <object.__getattribute__>` 方法，该钩子将为所有不涉及方法的字段调用。

**get_class_attribute_hook()** 类似于上面的钩子，但用于类上的属性而不是实例属性。与上面的不同，这不针对 :py:meth:`__getattr__ <object.__getattr__>` 或 :py:meth:`__getattribute__ <object.__getattribute__>` 进行特殊处理。

**get_class_decorator_hook()** 可用于更新具有类装饰器的类定义。例如，你可以为类添加一些属性，以匹配运行时行为：

.. code-block:: python

   from dataclasses import dataclass

   @dataclass  # 内置插件在这里添加 `__init__` 方法
   class User:
       name: str

   user = User(name='example')  # mypy 可以通过插件理解这一点

**get_metaclass_hook()** 类似于上面的钩子，但用于元类。

**get_base_class_hook()** 类似于上面的钩子，但用于基类。

**get_dynamic_class_hook()** 可用于允许 mypy 中的动态类定义。每次为一个简单名称赋值且右侧是函数调用时，都会调用该插件钩子：

.. code-block:: python

   from lib import dynamic_class

   X = dynamic_class('X', [])

对于这样的定义，mypy 会调用 ``get_dynamic_class_hook("lib.dynamic_class")``。插件应创建相应的 ``mypy.nodes.TypeInfo`` 对象，并将其放入相关的符号表中。（这个类的实例表示 mypy 中的类，并持有诸如限定名称、方法解析顺序等重要信息。）

**get_customize_class_mro_hook()** 可用于在类主体分析之前修改类的 MRO（例如在其中插入一些条目）。

**get_additional_deps()** 可用于为模块添加新的依赖项。它会在语义分析之前调用。例如，如果一个库有根据配置信息动态加载的依赖项，可以使用此钩子。

**report_config_data()** 可用于当插件有某种每模块的配置影响类型检查时。当模块的配置发生变化时，我们希望使 mypy 的缓存失效，从而重新检查模块。此钩子应报告给 mypy 任何相关的配置信息，以便当配置更改时，mypy 知道要重新检查模块。钩子应返回可编码为 JSON 的数据。

实用工具(Useful tools)
************************

Mypy 附带了 ``mypy.plugins.proper_plugin`` 插件，对于插件作者非常有用，因为它可以找到遗漏的 ``get_proper_type()`` 调用，这是一个常见错误。

建议将其作为插件 CI 的一部分启用。
