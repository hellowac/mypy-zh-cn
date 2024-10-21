.. Mypy documentation master file, created by
   sphinx-quickstart on Sun Sep 14 19:50:35 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

欢迎来到 mypy 文档!
==============================

Mypy 是一个用于 Python 的静态类型检查器。

类型检查器帮助确保您在代码中正确使用变量和函数。通过 mypy，您可以为 Python 程序添加类型提示（:pep:`484`），当您不正确地使用这些类型时，mypy 将发出警告。

Python 是一种动态语言，因此通常只有在尝试运行代码时才能看到错误。Mypy 是一个 *静态* 检查器，因此它能够在不运行程序的情况下发现程序中的错误!

这里有一个小例子来激发您的兴趣：

.. code-block:: python

   number = input("你最喜欢的数字是什么？")
   print("它是", number + 1)  # 错误：不支持的操作数类型用于 + ("str" 和 "int")

为 mypy 添加类型提示不会干扰程序的运行方式。可以将类型提示视为类似于注释!即使 mypy 报告错误，您仍然可以使用 Python 解释器运行代码。

Mypy 的设计考虑到了渐进式类型。这意味着您可以逐步为代码库添加类型提示，并且在静态类型不方便时，您始终可以回退到动态类型。

Mypy 具有强大且易于使用的类型系统，支持类型推断、泛型、可调用类型、元组类型、联合类型、结构性子类型等功能。使用 mypy 将使您的程序更易于理解、调试和维护。

.. note::

   尽管 mypy 已经准备好用于生产，但偶尔可能会有更改导致向后兼容性中断。mypy 开发团队会尽量减少对用户代码的影响。如果出现重大向后不兼容的更改，mypy 的主要版本号将被提高。

内容
--------

.. toctree::
   :maxdepth: 2
   :caption: 第一步

   getting_started
   cheat_sheet_py3
   existing_code

.. _overview-type-system-reference:

.. toctree::
   :maxdepth: 2
   :caption: 类型系统参考

   builtin_types
   type_inference_and_annotations
   kinds_of_types
   class_basics
   runtime_troubles
   protocols
   dynamic_typing
   type_narrowing
   duck_type_compatibility
   stubs
   generics
   more_types
   literal_types
   typed_dict
   final_attrs
   metaclasses

.. toctree::
   :maxdepth: 2
   :caption: 配置和运行 mypy

   running_mypy
   command_line
   config_file
   inline_config
   mypy_daemon
   installed_packages
   extending_mypy
   stubgen
   stubtest

.. toctree::
   :maxdepth: 2
   :caption: 其他

   common_issues
   supported_python_features
   error_codes
   error_code_list
   error_code_list2
   additional_features
   faq
   changelog

.. toctree::
   :hidden:
   :caption: 项目链接

   GitHub <https://github.com/python/mypy>
   Website <https://mypy-lang.org/>

索引表
==================

* :ref:`genindex`
* :ref:`search`
