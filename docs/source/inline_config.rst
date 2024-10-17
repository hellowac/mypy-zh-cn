.. _inline-config:

内联配置(Inline configuration)
========================================

Mypy 支持在文件内部使用 ``# mypy:`` 注释设置每个文件的配置选项。例如：

.. code-block:: python

  # mypy: disallow-any-generics

内联配置注释优先于所有其他配置机制。

配置注释格式(Configuration comment format)
********************************************************

标志对应于 :ref:`配置文件标志 <config-file>`，但允许用连字符替代下划线。

值使用 ``=`` 指定，但 ``= True`` 可以省略：

.. code-block:: python

  # mypy: disallow-any-generics
  # mypy: always-true=FOO

多个标志可以用逗号分隔或放在单独的行上。要将逗号包含在选项的值中，请将值放在引号内：

.. code-block:: python

  # mypy: disallow-untyped-defs, always-false="FOO,BAR"

如同在配置文件中，接受布尔值的选项可以通过在其名称前加 ``no-`` 来反转，或者（在适用时）将前缀从 ``disallow`` 交换为 ``allow`` （反之亦然）：

.. code-block:: python

  # mypy: allow-untyped-defs, no-strict-optional