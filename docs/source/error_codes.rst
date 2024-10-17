.. _error-codes:

错误代码(Error codes)
======================

Mypy 可以选择在每条错误消息后显示一个错误代码，例如 ``[attr-defined]``。错误代码有两个目的：

1. 可以使用 ``# type: ignore[code]`` 在某一行静默特定的错误代码。这样你就不会意外忽略其他潜在更严重的错误。

2. 错误代码可用于查找有关错误的文档。接下来的两个主题（:ref:`error-code-list` 和 :ref:`error-codes-optional`）记录了 mypy 可以报告的各种错误代码。

大多数错误代码在多个相关的错误消息之间共享。错误代码可能会在未来的 mypy 版本中更改。

.. _silence-error-codes:

基于错误代码静默错误(Silencing errors based on error codes)
--------------------------------------------------------------------------

你可以使用特殊的注释 ``# type: ignore[code, ...]`` 仅在特定行上忽略具有特定错误代码（或代码）的错误。这即使在你没有配置 mypy 显示错误代码的情况下也可以使用。

这个示例展示了如何忽略一个关于导入名称的错误，mypy 认为该名称未定义：

.. code-block:: python

   # 'foo' 在 'foolib' 中定义，即使 mypy 无法看到该定义。
   from foolib import foo  # type: ignore[attr-defined]

全局启用/禁用特定错误代码(Enabling/disabling specific error codes globally)
-------------------------------------------------------------------------------------

有命令行标志和配置文件设置，用于启用某些可选错误代码，例如 :option:`--disallow-untyped-defs <mypy --disallow-untyped-defs>`，这将启用 ``no-untyped-def`` 错误代码。

你可以使用 :option:`--enable-error-code <mypy --enable-error-code>` 和 :option:`--disable-error-code <mypy --disable-error-code>` 来启用或禁用没有专用命令行标志或配置文件设置的特定错误代码。

每个模块启用/禁用错误代码(Per-module enabling/disabling error codes)
------------------------------------------------------------------------------

你可以使用 :ref:`配置文件 <config-file>` 部分，仅在某些模块中启用或禁用特定错误代码。例如，这个 ``mypy.ini`` 配置将允许在测试中使用非注解的空容器，同时保持其他部分代码在严格模式下检查：

.. code-block:: ini

   [mypy]
   strict = True

   [mypy-tests.*]
   allow_untyped_defs = True
   allow_untyped_calls = True
   disable_error_code = var-annotated, has-type

请注意，每模块的启用/禁用将覆盖全局选项。因此，如果在全局配置部分中有错误代码列表，则无需为每个模块重复这些列表。例如：

.. code-block:: ini

   [mypy]
   enable_error_code = truthy-bool, ignore-without-code, unused-awaitable

   [mypy-extensions.*]
   disable_error_code = unused-awaitable

上述配置将允许扩展模块中的未使用的 awaitable，但仍会保持其他两个错误代码启用。整体逻辑如下：

* 命令行和/或配置主部分设置全局错误代码

* 各个配置部分按 glob/module *调整* 它们

* 行内 ``# mypy: disable-error-code="..."`` 和 ``# mypy: enable-error-code="..."`` 注释可以进一步 *调整* 它们以适应特定文件。例如：

.. code-block:: python

  # mypy: enable-error-code="truthy-bool, ignore-without-code"

因此，可以全局启用某些代码，在相应的配置部分中禁用所有测试中的代码，然后在某些特定测试中用行内注释重新启用它。

错误代码的子代码(Subcodes of error codes)
----------------------------------------------

在某些情况下，主要出于向后兼容性原因，一个错误代码可能也被另一个更广泛的错误代码覆盖。例如，代码为 ``[method-assign]`` 的错误可以通过 ``# type: ignore[assignment]`` 被忽略。类似的逻辑也适用于全局禁用错误代码。如果给定的错误代码是另一个错误代码的子代码，它将在文档中提及更狭窄的代码。这个层级不是嵌套的：不能有其他子代码的子代码。

强制要求错误代码(Requiring error codes)
--------------------------------------------

可以强制要求在 ``type: ignore`` 注释中指定错误代码。有关更多信息，请参见 :ref:`ignore-without-code <code-ignore-without-code>`。
