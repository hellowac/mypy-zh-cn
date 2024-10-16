<img src="docs/source/mypy_light.svg" alt="mypy logo" width="300px"/>

[English](https://github.com/python/mypy)

Mypy: 用于 Python 的静态类型检查
=======================================

[![Stable Version](https://img.shields.io/pypi/v/mypy?color=blue)](https://pypi.org/project/mypy/)
[![Downloads](https://img.shields.io/pypi/dm/mypy)](https://pypistats.org/packages/mypy)
[![Build Status](https://github.com/python/mypy/actions/workflows/test.yml/badge.svg)](https://github.com/python/mypy/actions)
[![Documentation Status](https://readthedocs.org/projects/mypy/badge/?version=latest)](https://mypy.readthedocs.io/en/latest/?badge=latest)
[![Chat at https://gitter.im/python/typing](https://badges.gitter.im/python/typing.svg)](https://gitter.im/python/typing?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

有问题吗？
---------------

我们随时乐意回答问题！以下是一些提问的好地方：

- 对于你感兴趣的任何内容，可以尝试 [Gitter 聊天](https://gitter.im/python/typing)。
- 对于关于 Python 类型的常规问题，可以尝试 [类型讨论](https://github.com/python/typing/discussions)。

如果你刚刚开始，可以查看 [文档](https://mypy.readthedocs.io/en/stable/index.html) 和 [类型提示备忘单](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) 来帮助解答问题。

如果你认为发现了一个 bug：

- 检查我们的 [常见问题页面](https://mypy.readthedocs.io/en/stable/common_issues.html)。
- 在我们的 [问题追踪器](https://github.com/python/mypy/issues) 中搜索，看它是否已经被报告。
- 考虑在 [Gitter 聊天](https://gitter.im/python/typing) 中提问。

要报告 bug 或请求增强：

- 在 [我们的问题追踪器](https://github.com/python/mypy/issues) 中报告。
- 如果问题出在特定库或函数上，考虑在 [Typeshed 追踪器](https://github.com/python/typeshed/issues) 或该库的问题追踪器中报告。

要讨论新的类型系统特性：

- 在 [discuss.python.org](https://discuss.python.org/c/typing/32) 进行讨论。
- 历史讨论也可以在 [typing-sig 邮件列表](https://mail.python.org/archives/list/typing-sig@python.org/) 和 [python/typing 仓库](https://github.com/python/typing/issues) 中找到。

什么是 mypy？
-------------

Mypy 是一个用于 Python 的静态类型检查器。

类型检查器帮助确保你在代码中正确使用变量和函数。通过 mypy，可以为你的 Python 程序添加类型提示（[PEP 484](https://www.python.org/dev/peps/pep-0484/)），当你错误使用这些类型时，mypy 会发出警告。

Python 是一种动态语言，因此通常只有在运行代码时才会看到错误。Mypy 是一个 *静态* 检查器，它在不运行程序的情况下找到 bugs！

这里有一个小示例来激发你的兴趣：

```python
number = input("你最喜欢的数字是什么？")
print("它是", number + 1)  # 错误：不支持的操作数类型 for + ("str" 和 "int")
```

为 mypy 添加类型提示不会干扰程序的运行方式。可以把类型提示视为类似于注释！即使 mypy 报告错误，你仍然可以使用 Python 解释器运行你的代码。

Mypy 设计时考虑了渐进类型。这意味着你可以逐步为代码库添加类型提示，当静态类型不方便时，你可以随时回退到动态类型。

Mypy 具有强大且易于使用的类型系统，支持类型推断、泛型、可调用类型、元组类型、联合类型、结构子类型等特性。使用 mypy 可以使你的程序更容易理解、调试和维护。

有关更多示例和信息，请参见 [文档](https://mypy.readthedocs.io/en/stable/index.html)。

特别是，查看：

- [类型提示备忘单](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [入门指南](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [错误代码列表](https://mypy.readthedocs.io/en/stable/error_code_list.html)

快速开始
-----------

可以使用 pip 安装 mypy：

```bash
python3 -m pip install -U mypy
```

如果想运行最新版本的代码，可以直接从仓库安装：

```bash
python3 -m pip install -U git+https://github.com/python/mypy.git
# 或者如果你没有安装 'git'
python3 -m pip install -U https://github.com/python/mypy/zipball/master
```

现在，你可以这样进行程序的[类型检查]：

```bash
mypy PROGRAM
```

即使 mypy 报告类型错误，你仍然可以使用 Python 解释器运行你的静态类型程序：

```bash
python3 PROGRAM
```

你也可以在 [在线沙盒](https://mypy-play.net/) 中尝试 mypy（由宫崎佑介开发）。如果你在处理大型代码库，可以在 [守护进程模式] 下运行 mypy，这将提供更快（通常是毫秒级）的增量更新：

```bash
dmypy run -- PROGRAM
```

[类型检查]: https://mypy.readthedocs.io/en/latest/getting_started.html#function-signatures-and-dynamic-vs-static-typing  
[守护进程模式]: https://mypy.readthedocs.io/en/stable/mypy_daemon.html

[statically typed parts]: https://mypy.readthedocs.io/en/latest/getting_started.html#function-signatures-and-dynamic-vs-static-typing
[daemon mode]: https://mypy.readthedocs.io/en/stable/mypy_daemon.html

集成
------------

Mypy 可以集成到流行的 IDE 中：

- Vim：
  - 使用 [Syntastic](https://github.com/vim-syntastic/syntastic)：在 `~/.vimrc` 中添加
    `let g:syntastic_python_checkers=['mypy']`
  - 使用 [ALE](https://github.com/dense-analysis/ale)：安装 `mypy` 后默认启用，或通过在 `~/vim/ftplugin/python.vim` 中添加 `let b:ale_linters = ['mypy']` 显式启用。
- Emacs：使用 [Flycheck](https://github.com/flycheck/)
- Sublime Text：[SublimeLinter-contrib-mypy](https://github.com/fredcallaway/SublimeLinter-contrib-mypy)
- Atom：[linter-mypy](https://atom.io/packages/linter-mypy)
- PyCharm：[mypy 插件](https://github.com/dropbox/mypy-PyCharm-plugin)（PyCharm 集成了 [PEP 484](https://peps.python.org/pep-0484/) 的 [自有实现](https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html)）
- VS Code：提供与 mypy 的 [基本集成](https://code.visualstudio.com/docs/python/linting#_mypy)。
- pre-commit：使用 [pre-commit mirrors-mypy](https://github.com/pre-commit/mirrors-mypy)。

网站和文档
--------------------------

更多信息可在网站上找到：

  <https://www.mypy-lang.org/>

直接跳转到文档：

  <https://mypy.readthedocs.io/>

查看我们的更新日志：

  <https://mypy-lang.blogspot.com/>

贡献
------------

在测试、开发、文档和其他任务方面的帮助非常感谢，并对项目有用。所有经验水平的贡献者都有任务可以参与。

要开始开发 mypy，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果你需要帮助入门，请随时在 [Gitter](https://gitter.im/python/typing) 上询问。

Mypyc 和 mypy 的编译版本
----------------------------------

[Mypyc](https://github.com/mypyc/mypyc) 使用 Python 类型提示将 Python 模块编译为更快的 C 扩展。Mypy 本身就是使用 mypyc 编译的，这使得 mypy 的速度大约是解释版本的 4 倍！

要安装解释版本的 mypy，请使用：

```bash
python3 -m pip install --no-binary mypy -U mypy
```

要使用开发版本的 mypy 的编译版本，可以直接从 <https://github.com/mypyc/mypy_mypyc-wheels/releases/latest> 安装二进制文件。

要为 mypyc 项目贡献，请查看 <https://github.com/mypyc/mypyc>。
