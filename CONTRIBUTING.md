# 为 Mypy 贡献

[English](https://github.com/python/mypy/blob/main/CONTRIBUTING.md)

欢迎！Mypy 是一个社区项目，旨在为广泛的 Python 用户和代码库服务。如果你在自己的 Python 代码中尝试 mypy，你的经验和贡献对项目的成功至关重要。

## 行为准则

所有参与 Mypy 社区的人，特别是在我们的 issue 追踪器、拉取请求和聊天中，应该尊重他人，并遵循 [Python 社区行为准则](https://www.python.org/psf/codeofconduct/) 中阐明的指导方针。

## 开始开发

### 设置

#### (1) Fork mypy 仓库

在 GitHub 上，导航到 <https://github.com/python/mypy> 并 fork 该仓库。

#### (2) 克隆 mypy 仓库并进入

```bash
git clone git@github.com:<your_username>/mypy.git
cd mypy
```

#### (3) 创建并激活虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
# 对于 Windows 使用
python -m venv venv
. venv/Scripts/activate

# 更多细节，请参见 https://docs.python.org/3/library/venv.html#creating-virtual-environments
```

#### (4) 安装测试依赖和项目

```bash
python -m pip install -r test-requirements.txt
python -m pip install -e .
hash -r  # 这将重置 shell 的 PATH 缓存，Windows 上不需要
```

> **注意**
> 你需要 Python 3.8 或更高版本才能安装 `test-requirements.txt` 中列出的所有依赖。

### 运行测试

运行完整的测试套件可能需要一些时间，通常在准备 PR 时并不是必需的。一旦你提交了 PR，完整的测试套件将在 GitHub 上运行。你将能够看到任何测试失败，并对你的 PR 进行必要的更改。

然而，如果你希望这样做，可以像这样运行完整的测试套件：

```bash
python3 runtests.py
```

一些用于运行特定测试的有用命令包括：

```bash
# 使用 mypy 检查 mypy 自身的代码
python3 runtests.py self
# 或者等效命令：
python3 -m mypy --config-file mypy_self_check.ini -p mypy

# 从测试套件中运行单个测试
pytest -n0 -k 'test_name'

# 运行 "test-data/unit/check-dataclasses.test" 文件中的所有测试用例
pytest mypy/test/testcheck.py::TypeCheckSuite::check-dataclasses.test

# 运行格式化工具和代码检查工具
python runtests.py lint
```

有关运行和编写测试的详细指南，请参见 [test-data 目录中的 README](test-data/unit/README.md)。

#### 使用 `tox`

你也可以使用 [`tox`](https://tox.wiki/en/latest/) 来运行测试和其他命令。`tox` 会为你处理测试环境的设置。

```bash
# 运行测试
tox run -e py

# 使用特定的 Python 版本运行测试
tox run -e py311

# 运行特定命令
tox run -e lint

# 从测试套件中运行单个测试
tox run -e py -- -n0 -k 'test_name'

# 使用 Python 3.11 运行 "test-data/unit/check-dataclasses.test" 文件中的所有测试用例
tox run -e py311 -- mypy/test/testcheck.py::TypeCheckSuite::check-dataclasses.test

# 设置一个包含所有项目库的开发环境并运行命令
tox -e dev -- mypy --verbose test_case.py
tox -e dev --override testenv:dev.allowlist_externals+=env -- env  # 检查环境
```

如果你还没有安装 `tox`，可以使用上面描述的虚拟环境通过 `pip` 安装 `tox`（例如，``python3 -m pip install tox``）。

## 第一次贡献者

如果你想寻找可以帮助的任务，请浏览我们的 [问题追踪器](https://github.com/python/mypy/issues)！

特别关注：

- [适合新手的问题](https://github.com/python/mypy/labels/good-first-issue)
- [适合进一步贡献的问题](https://github.com/python/mypy/labels/good-second-issue)
- [文档问题](https://github.com/python/mypy/labels/documentation)

你无需请求许可即可处理这些问题。只需自行解决问题， [尝试添加单元测试](#running-tests) 并 [提交拉取请求](#submitting-changes)。

如果需要帮助修复特定问题，通常最好在问题本身上留言。如果你提供了你尝试过的内容和查找的方向，获得帮助的可能性会更大（维护者通常会帮助那些自助的人）。 [Gitter](https://gitter.im/python/typing) 也是一个寻求帮助的好地方。

像 `pdb` 和 `ipdb` 这样的交互式调试器对于入门 mypy 代码库非常有用。这是一个 [有用的教程](https://realpython.com/python-debugging-pdb/)。

同时，为我们的姐妹项目 [typeshed](https://github.com/python/typeshed/issues) 贡献也非常简单，该项目为库提供类型存根。这是熟悉类型语法的好方法。

## 提交更改

比起好的错误报告，更优秀的是一个错误的修复或一个急需新功能的实现。我们非常欢迎你的贡献。

我们使用常规的 GitHub 拉取请求流程，如果你曾在 GitHub 上为其他项目贡献过，可能会对它有所熟悉。有关具体操作，请参阅 [我们的 Git 和 GitHub 工作流程帮助页面](https://github.com/python/mypy/wiki/Using-Git-And-GitHub)，或 [GitHub 自己的文档](https://help.github.com/articles/using-pull-requests/)。

任何对 Mypy 感兴趣的人都可以审查你的代码。当 Mypy 的核心开发人员认为你的拉取请求准备就绪时，他们将合并它。

如果你的更改需要大量的工作，我们强烈建议你先打开一个问题，阐明你想要做的事情。这可以提前进行讨论，以防其他贡献者不同意你的想法或有帮助的建议。

最好的拉取请求是集中且清晰的，明确说明其目的和正确性，并包含对代码行为变化的测试。作为额外奖励，这些拉取请求也最容易让他人审查，从而帮助你快速合并！有关开源项目的优质拉取请求的标准建议适用；我们有 [自己的一篇说明](https://github.com/python/mypy/wiki/Good-Pull-Request) 供参考。

此外，在提交拉取请求后，请不要合并你的提交，因为这会在审查过程中抹去上下文。我们将在拉取请求合并时合并提交。

你可能还会发现 [Mypy 开发者指南](https://github.com/python/mypy/wiki/Developer-Guides) 中的其他页面对开发你的更改很有帮助。

## 核心开发者指南

核心开发者在处理拉取请求时应遵循以下规则：

- 合并 PR 之前，请始终等待测试通过。
- 使用 “[Squash and merge](https://github.com/blog/2141-squash-your-commits)” 来合并 PR。
- 删除已合并 PR 的分支（由核心开发者推送到主仓库）。
- 在合并前编辑最终提交信息，以符合以下风格（我们希望保持干净的 `git log` 输出）：
  - 合并多提交的 PR 时，确保提交信息不包含提交者的本地历史和 PR 的审查历史。编辑信息，仅描述 PR 的最终状态。
  - 确保提交信息末尾有一个 *单一* 换行符。这样在 `git log` 输出中，提交之间将有一个空行。
  - 根据需要拆分行，使提交信息的最大行长度不超过 80 个字符，包括主题行。
  - 主题和每段的首字母大写。
  - 确保提交信息的主题没有尾随的句点。
  - 在主题行中使用祈使语气（例如：“修复 README 中的拼写错误”）。
  - 如果 PR 修复了某个问题，请确保在信息主体中包含类似 “Fixes #xxx.” 的内容（而不是在主题中）。
  - 使用 Markdown 格式进行排版。
