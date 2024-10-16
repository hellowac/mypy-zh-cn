Mypy 文档
==================

这是什么？
------------

该目录包含 Mypy 文档的源代码（在 `source/` 下）和构建脚本。文档使用 Sphinx 和 reStructuredText，我们使用 `furo` 作为文档主题。

构建文档
--------------------------

安装 Sphinx 和文档所需的其他依赖项（即主题）。从 `docs` 目录使用 `pip`：

```
pip install -r requirements-docs.txt
```

像这样构建文档：

```
make html
```

构建的文档将放在 `docs/build` 目录中。打开 `docs/build/index.html` 查看文档。

有用的文档构建命令
------------------------------------

清理文档构建：

```
make clean
```

测试并检查文档中的链接：

```
make linkcheck
```

Read The Docs 上的文档
------------------------------

Mypy 文档托管在 Read The Docs 上，最新版本可在 https://mypy.readthedocs.io/en/latest 找到。