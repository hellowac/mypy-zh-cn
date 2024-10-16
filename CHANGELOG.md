# Mypy 版本说明

## 下一个版本

## Mypy 1.12

我们刚刚将 mypy 1.12 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 的静态类型检查器。此版本包括新功能、性能改进和错误修复。你可以按照以下方式安装：

```bash
python3 -m pip install -U mypy
```

你可以在 [Read the Docs](http://mypy.readthedocs.io) 阅读此版本的完整文档。

### 支持 Python 3.12 的泛型语法（PEP 695）

现在默认启用对 Python 3.12 中引入的新类型参数语法的支持，已记录在案，不再是实验性功能。在 mypy 1.11 中通过功能标志提供的实验性功能。

以下示例演示了新语法：

```python
# 泛型函数
def f[T](x: T) -> T: ...

reveal_type(f(1))  # 显示的类型是 'int'

# 泛型类
class C[T]:
    def __init__(self, x: T) -> None:
       self.x = x

c = C('a')
reveal_type(c.x)  # 显示的类型是 'str'

# 类型别名
type A[T] = C[list[T]]
```

有关更多信息，请参阅 [文档](https://mypy.readthedocs.io/en/latest/generics.html)。

包括以下改进：

* 记录 Python 3.12 类型参数语法（Jukka Lehtosalo，PR [17816](https://github.com/python/mypy/pull/17816)）
* 进一步更新文档（Jukka Lehtosalo，PR [17826](https://github.com/python/mypy/pull/17826)）
* 允许自我返回类型与逆变（Jukka Lehtosalo，PR [17786](https://github.com/python/mypy/pull/17786)）
* 默认启用新类型参数语法（Jukka Lehtosalo，PR [17798](https://github.com/python/mypy/pull/17798)）
* 如果新样式类型别名用作基类，则生成错误（Jukka Lehtosalo，PR [17789](https://github.com/python/mypy/pull/17789)）
* 如果基类具有显式方差，则继承方差（Jukka Lehtosalo，PR [17787](https://github.com/python/mypy/pull/17787)）
* 修复无效类型变量引用时的崩溃（Jukka Lehtosalo，PR [17788](https://github.com/python/mypy/pull/17788)）
* 修复冻结数据类的协变（Jukka Lehtosalo，PR [17783](https://github.com/python/mypy/pull/17783)）
* 允许以“`_`”命名前缀的属性的协变（Jukka Lehtosalo，PR [17782](https://github.com/python/mypy/pull/17782)）
* 在新样式类型别名中支持 `Annotated[...]`（Jukka Lehtosalo，PR [17777](https://github.com/python/mypy/pull/17777)）
* 修复嵌套的泛型类（Jukka Lehtosalo，PR [17776](https://github.com/python/mypy/pull/17776)）
* 增加对类型参数和类型别名作用域内不正确表达式使用的检测和错误报告（Kirill Podoprigora，PR [17560](https://github.com/python/mypy/pull/17560)）

### 对 Python 3.13 的基本支持

此版本增加了对 Python 3.13 特性的部分支持，并提供了 Python 3.13 的编译二进制文件。Mypyc 现在也支持 Python 3.13。

特别地，支持以下特性：
* 各种新的标准库特性和变更（通过 typeshed 存根改进）
* `typing.ReadOnly`（详见下文）
* `typing.TypeIs`（在 mypy 1.10 中添加，[PEP 742](https://peps.python.org/pep-0742/)）
* 使用遗留语法时的类型参数默认值（[PEP 696](https://peps.python.org/pep-0696/)）

尚不支持以下特性：
* `warnings.deprecated`（[PEP 702](https://peps.python.org/pep-0702/)）
* 使用 Python 3.12 类型参数语法时的类型参数默认值

### Mypyc 对 Python 3.13 的支持

Mypyc 现在支持 Python 3.13。这是由 Marc Mueller 提供的，并由 Jukka Lehtosalo 进行了额外修复。尚不支持自由线程的 Python 3.13 构建。

更改列表：

* 为 Python 3.13 添加额外包含（Marc Mueller，PR [17506](https://github.com/python/mypy/pull/17506)）
* 为 Python 3.13 添加另一个包含（Marc Mueller，PR [17509](https://github.com/python/mypy/pull/17509)）
* 修复 Python 3.13 的 ManagedDict 函数（Marc Mueller，PR [17507](https://github.com/python/mypy/pull/17507)）
* 更新 Python 3.13 的 mypyc 测试输出（Marc Mueller，PR [17508](https://github.com/python/mypy/pull/17508)）
* 修复 Python 3.13 的 `PyUnicode` 函数（Marc Mueller，PR [17504](https://github.com/python/mypy/pull/17504)）
* 修复 Python 3.13 的 `_PyObject_LookupAttrId`（Marc Mueller，PR [17505](https://github.com/python/mypy/pull/17505)）
* 修复 Python 3.13 的 `_PyList_Extend`（Marc Mueller，PR [17503](https://github.com/python/mypy/pull/17503)）
* 修复 Python 3.13 的 `gen_is_coroutine`（Marc Mueller，PR [17501](https://github.com/python/mypy/pull/17501)）
* 修复 Python 3.13 的 `_PyObject_FastCall`（Marc Mueller，PR [17502](https://github.com/python/mypy/pull/17502)）
* 避免在 3.13 上使用 `_PyObject_CallMethodOneArg`（Jukka Lehtosalo，PR [17526](https://github.com/python/mypy/pull/17526)）
* 不再依赖 3.13 上的 `_PyType_CalculateMetaclass`（Jukka Lehtosalo，PR [17525](https://github.com/python/mypy/pull/17525)）
* 不在 3.13 上使用 `_PyUnicode_FastCopyCharacters`（Jukka Lehtosalo，PR [17524](https://github.com/python/mypy/pull/17524)）
* 不在 3.13 上使用 `_PyUnicode_EQ`，因为它不再导出（Jukka Lehtosalo，PR [17523](https://github.com/python/mypy/pull/17523)）

### 推断条件表达式的联合类型

Mypy 现在总是尝试推断条件表达式的联合类型，如果左右操作数类型不同。这导致推断类型更加精确，并使 mypy 能够检测到更多问题。例如：

```python
s = "foo" if cond() else 1
# "s" 的类型现在是 "str | int"（之前是 "object"）
```

值得注意的是，如果其中一个操作数的类型是 `Any`，则条件表达式的类型现在是 `<type> | Any`。以前推断的类型只是 `Any`。新类型基本上表示该值可以是 `<type>` 类型，也可能是某种（未知）类型。对结果进行的大多数操作也必须对 `<type>` 有效。相关示例：

```python
from typing import Any

def func(a: Any, b: bool) -> None:
    x = a if b else None
    # x 的类型是 "Any | None"
    print(x.y)  # 错误：None 没有属性 "y"
```

此功能由 Ivan Levkivskyi 提供（PR [17427](https://github.com/python/mypy/pull/17427)）。

### 对 TypedDict 的 ReadOnly 支持 (PEP 705)

现在可以使用 `typing.ReadOnly` 将 TypedDict 项目指定为只读 ([PEP 705](https://peps.python.org/pep-0705))：

```python
from typing import TypedDict

# 或在 Python 3.13 上使用 "from typing ..."
from typing_extensions import ReadOnly

class TD(TypedDict):
    a: int
    b: ReadOnly[int]

d: TD = {"a": 1, "b": 2}
d["a"] = 3  # 正确
d["b"] = 5  # 错误：“b”是只读的
```

此功能由 Nikita Sobolev 提供（PR [17644](https://github.com/python/mypy/pull/17644)）。

### Python 3.8 结束支持在即

我们计划在下一个 mypy 功能发布或随后的版本中放弃对 Python 3.8 的支持。Python 3.8 将于 2024 年 10 月结束支持。

### 默认设置的计划更改

我们计划在 mypy 2.0 中默认启用 `--local-partial-types`。这通常需要至少进行小幅代码更改。该选项在 mypy 守护进程中隐式启用，从而使守护进程和非守护进程模式的行为一致。

我们建议 mypy 用户尽快开始使用本地部分类型（或明确禁用它们）以为这一变化做好准备。

这也可以在 mypy 配置文件中进行配置：

```
local_partial_types = True
```

有关更多信息，请参阅 [文档](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-local-partial-types)。

### 文档更新

Mypy 文档现在在许多示例中使用现代语法变体和导入。一些示例在 Python 3.8 上不再有效，这是 mypy 支持的最早 Python 版本。

值得注意的是，`Iterable` 和其他协议/抽象基类从 `collections.abc` 导入，而不是 `typing`：
```python
from collections.abc import Iterable, Callable
```

示例还避免使用内置类型的大写别名：使用 `list[str]` 代替 `List[str]`。在 Python 3.10 中引入的 `X | Y` 联合类型语法现在也很普遍。

文档更新列表：

* 记录 `--output=json` CLI 选项（Edgar Ramírez Mondragón，PR [17611](https://github.com/python/mypy/pull/17611)）
* 更新文档中对弃用类型别名的各种引用（Jukka Lehtosalo，PR [17829](https://github.com/python/mypy/pull/17829)）
* 在文档中强调 "X | Y" 联合语法（Jukka Lehtosalo，PR [17835](https://github.com/python/mypy/pull/17835)）
* 在文档中讨论自类型之前的上限（Jukka Lehtosalo，PR [17827](https://github.com/python/mypy/pull/17827)）
* 在 mypy 文档中显示变更日志（quinn-sasha，PR [17742](https://github.com/python/mypy/pull/17742)）
* 列出 `--enable-incomplete-feature` 文档中的所有不完整特性（sobolevn，PR [17633](https://github.com/python/mypy/pull/17633)）
* 移除对 pygments 主题的显式设置（Pradyun Gedam，PR [17571](https://github.com/python/mypy/pull/17571)）
* 使用 TypedDict 文档化 ReadOnly（Jukka Lehtosalo，PR [17905](https://github.com/python/mypy/pull/17905)）
* 文档化 TypeIs（Chelsea Durazo，PR [17821](https://github.com/python/mypy/pull/17821)）

### 实验性内联 TypedDict 语法

Mypy 现在支持一种非标准的实验性语法，用于定义匿名 TypedDict。示例：

```python
def func(n: str, y: int) -> {"name": str, "year": int}:
    return {"name": n, "year": y}
```

该功能默认禁用。使用 `--enable-incomplete-feature=InlineTypedDict` 来启用它。*我们可能在未来的版本中移除此功能。*

该功能由 Ivan Levkivskyi 提供（PR [17457](https://github.com/python/mypy/pull/17457)）。

### Stubgen 改进

* 修复了在字面量类级关键字上的崩溃（sobolevn，PR [17663](https://github.com/python/mypy/pull/17663)）
* Stubgen 添加 `--version` 选项（sobolevn，PR [17662](https://github.com/python/mypy/pull/17662)）
* 修复 `stubgen --no-analysis/--parse-only` 文档（sobolevn，PR [17632](https://github.com/python/mypy/pull/17632)）
* 在 stubgenc 中生成签名时包含关键字参数（Eric Mark Martin，PR [17448](https://github.com/python/mypy/pull/17448)）
* 添加支持从文档字符串提取类型时检测 `Literal` 类型（Michael Carlstrom，PR [17441](https://github.com/python/mypy/pull/17441)）
* 使用 `Generator` 类型变量的默认值（Sebastian Rittau，PR [17670](https://github.com/python/mypy/pull/17670)）

### Stubtest 改进

* 添加对 `cached_property` 的支持（Ali Hamdan，PR [17626](https://github.com/python/mypy/pull/17626)）
* 向 `stubtest` 添加 `enable_incomplete_feature` 验证（sobolevn，PR [17635](https://github.com/python/mypy/pull/17635)）
* 修复 `stubtest` 在使用 `--mypy-config-file` 时的错误代码处理（sobolevn，PR [17629](https://github.com/python/mypy/pull/17629)）

### 其他显著修复和改进

* 使用不支持的类型参数默认值时报告错误（Jukka Lehtosalo，PR [17876](https://github.com/python/mypy/pull/17876)）
* 修复当节点类型变化时，mypy 守护进程重新处理交叉引用的问题（Ivan Levkivskyi，PR [17883](https://github.com/python/mypy/pull/17883)）
* 不要在值为 IntEnum/StrEnum 时使用相等性来缩小类型（Jukka Lehtosalo，PR [17866](https://github.com/python/mypy/pull/17866)）
* 不将 None 与 IntEnum 的比较视为模糊（Jukka Lehtosalo，PR [17877](https://github.com/python/mypy/pull/17877)）
* 修复 IntEnum 和 StrEnum 类型的缩小（Jukka Lehtosalo，PR [17874](https://github.com/python/mypy/pull/17874)）
* 在类型推断过程中根据自类型过滤重载项（Jukka Lehtosalo，PR [17873](https://github.com/python/mypy/pull/17873)）
* 启用联合 TypeVar 上限的负缩小（Brian Schubert，PR [17850](https://github.com/python/mypy/pull/17850)）
* 修复成员表达式格式化的问题（Brian Schubert，PR [17848](https://github.com/python/mypy/pull/17848)）
* 避免在扩展类型时类型大小爆炸（Jukka Lehtosalo，PR [17842](https://github.com/python/mypy/pull/17842)）
* 修复在匹配语句中元组的负缩小问题（Brian Schubert，PR [17817](https://github.com/python/mypy/pull/17817)）
* 将假值的 str/bytes/int 缩小为字面量类型（Brian Schubert，PR [17818](https://github.com/python/mypy/pull/17818)）
* 针对最新的 Python 3.13 进行测试，使得 3.14 的测试变得简单（Shantanu，PR [17812](https://github.com/python/mypy/pull/17812)）
* 拒绝参数规格类型的可调用对象调用中参数不足的情况（Stanislav Terliakov，PR [17323](https://github.com/python/mypy/pull/17323)）
* 修复在向接受单个 ParamSpec 的泛型基类传递过多类型参数时的崩溃（Brian Schubert，PR [17770](https://github.com/python/mypy/pull/17770)）
* 修复 TypeVar 上限有时未显示在漂亮可调用对象中的问题（Brian Schubert，PR [17802](https://github.com/python/mypy/pull/17802)）
* 为重叠函数签名添加错误代码（Katrina Connors，PR [17597](https://github.com/python/mypy/pull/17597)）
* 检查 `not ...` 一元表达式中的 `truthy-bool`（sobolevn，PR [17773](https://github.com/python/mypy/pull/17773)）
* 添加缺失的 lines-covered 和 lines-valid 属性（Soubhik Kumar Mitra，PR [17738](https://github.com/python/mypy/pull/17738)）
* 修复递归元组类型的另一个崩溃场景（Ivan Levkivskyi，PR [17708](https://github.com/python/mypy/pull/17708)）
* 在 `functools.partial` 中解析 TypeVar 上限（Shantanu，PR [17660](https://github.com/python/mypy/pull/17660)）
* 在检查延迟节点时始终重置绑定器（Ivan Levkivskyi，PR [17643](https://github.com/python/mypy/pull/17643)）
* 修复在单个解包时调用属性导致的崩溃（Ivan Levkivskyi，PR [17641](https://github.com/python/mypy/pull/17641)）
* 修复检查器插件 API 与实现之间的签名不匹配（bzoracler，PR [17343](https://github.com/python/mypy/pull/17343)）
* 索引类型也会生成 GenericAlias（Shantanu，PR [17546](https://github.com/python/mypy/pull/17546)）
* 修复可调用协议中的自类型崩溃（Ivan Levkivskyi，PR [17499](https://github.com/python/mypy/pull/17499)）
* 修复带方法的 NamedTuple 和函数中的错误（Ivan Levkivskyi，PR [17498](https://github.com/python/mypy/pull/17498)）
* 在 3.13 中为数据类添加 `__replace__`（Max Muoto，PR [17469](https://github.com/python/mypy/pull/17469)）
* 修复 `--no-namespace-packages` 的帮助信息（Raphael Krupinski，PR [17472](https://github.com/python/mypy/pull/17472)）
* 修复异步生成器的类型检查（Danny Yang，PR [17452](https://github.com/python/mypy/pull/17452)）
* 修复 attrs 插件中的严格可选处理（Ivan Levkivskyi，PR [17451](https://github.com/python/mypy/pull/17451)）
* 允许在泛型中混合 ParamSpec 和 TypeVarTuple（Ivan Levkivskyi，PR [17450](https://github.com/python/mypy/pull/17450)）
* 改进类型的 `functools.partial`（Shantanu，PR [17898](https://github.com/python/mypy/pull/17898)）
* 使 ReadOnly TypedDict 项目具有协变性（Jukka Lehtosalo，PR [17904](https://github.com/python/mypy/pull/17904)）
* 修复与 `functools.partial` 相关的联合可调用对象（Jukka Lehtosalo，PR [17903](https://github.com/python/mypy/pull/17903)）
* 改进与 `functools.partial` 相关的泛型函数处理（Ivan Levkivskyi，PR [17925](https://github.com/python/mypy/pull/17925)）

### 类型仓库更新

请查看 [git log](https://github.com/python/typeshed/commits/main?after=91a58b07cdd807b1d965e04ba85af2adab8bf924+0&branch=main&path=stdlib) 以获取标准库类型仓库 stub 变化的完整列表。

### 致谢

感谢所有为本次发布做出贡献的 mypy 贡献者：

- Ali Hamdan
- Anders Kaseorg
- Bénédikt Tran
- Brian Schubert
- bzoracler
- Chelsea Durazo
- Danny Yang
- Edgar Ramírez Mondragón
- Eric Mark Martin
- InSync
- Ivan Levkivskyi
- Jordandev678
- Katrina Connors
- Kirill Podoprigora
- Marc Mueller
- Max Muoto
- Max Murin
- Michael Carlstrom
- Michael I Chen
- Pradyun Gedam
- quinn-sasha
- Raphael Krupinski
- Sebastian Rittau
- Shantanu
- sobolevn
- Soubhik Kumar Mitra
- Stanislav Terliakov
- wyattscarpenter

我还想感谢我的雇主，Dropbox，支持 mypy 的开发。


## Mypy 1.11

我们刚刚将 mypy 1.11 上传到 Python 包索引 ([PyPI](https://pypi.org/project/mypy/))。Mypy 是一个 Python 的静态类型检查器。本次发布包含新功能、性能改进和错误修复。您可以通过以下方式安装：

    python3 -m pip install -U mypy

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读本次发布的完整文档。

### 支持 Python 3.12 的泛型语法（PEP 695）

Mypy 现在支持 Python 3.12 中引入的新类型参数语法 ([PEP 695](https://peps.python.org/pep-0695/))。此功能仍为实验性，必须通过 `--enable-incomplete-feature=NewGenericSyntax` 标志启用，或在 mypy 配置文件中设置 `enable_incomplete_feature = NewGenericSyntax`。我们计划在下一个 mypy 功能发布中默认启用此功能。

以下示例演示了新语法：

```python
# 泛型函数
def f[T](x: T) -> T: ...

reveal_type(f(1))  # 显示的类型为 'int'

# 泛型类
class C[T]:
    def __init__(self, x: T) -> None:
       self.x = x

c = C('a')
reveal_type(c.x)  # 显示的类型为 'str'

# 类型别名
type A[T] = C[list[T]]
```

该功能由 Jukka Lehtosalo 贡献。

### 支持 `functools.partial`

Mypy 现在对 `functools.partial` 的使用进行类型检查。之前 mypy 会接受任意参数。

以下示例现在会产生错误：

```python
from functools import partial

def f(a: int, b: str) -> None: ...

g = partial(f, 1)

# 参数的类型不兼容 "int"; 预期为 "str"
g(11)
```

该功能由 Shantanu 贡献（PR [16939](https://github.com/python/mypy/pull/16939)）。


### 对未类型化重写的更严格检查

过去的 mypy 版本没有检查未类型化方法与重写方法的兼容性，这可能导致错误的否定。现在，当使用 `--check-untyped-defs` 时，mypy 会执行这些检查。

例如，使用 `--check-untyped-defs` 时，以下代码会生成错误：

```python
class Base:
    def f(self, x: int = 0) -> None: ...

class Derived(Base):
    # 签名与 "Base" 不兼容
    def f(self): ...
```

该功能由 Steven Troxler 贡献（PR [17276](https://github.com/python/mypy/pull/17276)）。

### 类型推断的改进

在 mypy 1.5 中引入的新多态推断算法现在在更多场景中使用，特别是涉及泛型高阶函数时，改进了类型推断。

该功能由 Ivan Levkivskyi 贡献（PR [17348](https://github.com/python/mypy/pull/17348)）。

Mypy 现在在某些上下文中使用元组项类型的联合，以启用更精确的推断类型。例如：

```python
for x in (1, 'x'):
    # 之前推断为 'object'
    reveal_type(x)  # 显示的类型为 'int | str'
```

此功能同样由 Ivan Levkivskyi 贡献（PR [17408](https://github.com/python/mypy/pull/17408)）。

### 重载重叠检测的改进

mypy 检查两个 `@overload` 签名是否不安全重叠的细节经过彻底重构。这不仅修复了一些误报，还允许 mypy 检测到额外的不安全签名。

该功能由 Ivan Levkivskyi 贡献（PR [17392](https://github.com/python/mypy/pull/17392)）。


### 更好的表达式中的类型提示支持

Mypy 现在允许更多在所有表达式上下文中评估为有效类型注释的表达式。这些表达式的推断类型有时也更精确，之前通常为 `object`。

以下示例使用包含可调用类型的联合类型作为表达式，现在不再生成错误：

```python
from typing import Callable

print(Callable[[], int] | None)  # 无错误
```

该功能由 Jukka Lehtosalo 贡献（PR [17404](https://github.com/python/mypy/pull/17404)）。

### Mypyc 改进

Mypyc 现在支持在 Python 3.12 中引入的新泛型语法（见上文）。另一个显著的改进是对 `int` 值的基本操作显著加快。

- 支持 Python 3.12 泛型函数和类的语法（Jukka Lehtosalo, PR [17357](https://github.com/python/mypy/pull/17357)）
- 支持 Python 3.12 类型别名语法（Jukka Lehtosalo, PR [17384](https://github.com/python/mypy/pull/17384)）
- 修复 ParamSpec（Shantanu, PR [17309](https://github.com/python/mypy/pull/17309)）
- 内联整数解包操作的快速路径（Jukka Lehtosalo, PR [17266](https://github.com/python/mypy/pull/17266)）
- 内联标记整数的算术和位操作（Jukka Lehtosalo, PR [17265](https://github.com/python/mypy/pull/17265)）
- 允许将原始类型指定为纯（Jukka Lehtosalo, PR [17263](https://github.com/python/mypy/pull/17263)）

### Stubtest 的更改
- 忽略 `_ios_support`（Alex Waygood, PR [17270](https://github.com/python/mypy/pull/17270)）
- 改进对 Python 3.13 的支持（Shantanu, PR [17261](https://github.com/python/mypy/pull/17261)）

### Stubgen 的更改
- 优雅处理无效的 `Optional` 并识别 PEP 604 联合的别名（Ali Hamdan, PR [17386](https://github.com/python/mypy/pull/17386)）
- 修复 Python 3.13（Jelle Zijlstra, PR [17290](https://github.com/python/mypy/pull/17290)）
- 保留枚举值初始化器（Shantanu, PR [17125](https://github.com/python/mypy/pull/17125)）

### 杂项新功能
- 通过 `--output json` 添加错误格式支持和 JSON 输出选项（Tushar Sadhwani, PR [11396](https://github.com/python/mypy/pull/11396)）
- 支持 Python 3.11+ 中的 `enum.member`（Nikita Sobolev, PR [17382](https://github.com/python/mypy/pull/17382)）
- 支持 Python 3.11+ 中的 `enum.nonmember`（Nikita Sobolev, PR [17376](https://github.com/python/mypy/pull/17376)）
- 支持 Python 3.13 中的 `namedtuple.__replace__`（Shantanu, PR [17259](https://github.com/python/mypy/pull/17259)）
- 支持 `collections.namedtuple` 中的 `rename=True`（Jelle Zijlstra, PR [17247](https://github.com/python/mypy/pull/17247)）
- 添加对 `__spec__` 的支持（Shantanu, PR [14739](https://github.com/python/mypy/pull/14739)）


### 错误报告的更改
- 在消息中提及 `--enable-incomplete-feature=NewGenericSyntax`（Shantanu, PR [17462](https://github.com/python/mypy/pull/17462)）
- 不报告插件生成的方法与 `explicit-override`（sobolevn, PR [17433](https://github.com/python/mypy/pull/17433)）
- 对函数类型变量使用和显示命名空间（Ivan Levkivskyi, PR [17311](https://github.com/python/mypy/pull/17311)）
- 修复协议中对 Final 本地作用域变量的误报（GiorgosPapoutsakis, PR [17308](https://github.com/python/mypy/pull/17308)）
- 在更多消息中使用 Never，并在连接时使用 ambiguous（Shantanu, PR [17304](https://github.com/python/mypy/pull/17304)）
- 在详细输出中记录配置文件的完整路径（dexterkennedy, PR [17180](https://github.com/python/mypy/pull/17180)）
- 为不支持的属性装饰器添加 `[prop-decorator]` 代码（Christopher Barber, PR [16571](https://github.com/python/mypy/pull/16571)）
- 对使用 `:=` 和 `[truthy-bool]` 的第二个错误消息进行抑制（Nikita Sobolev, PR [15941](https://github.com/python/mypy/pull/15941)）
- 为将功能 Enum 分配给不同名称的变量生成错误（Shantanu, PR [16805](https://github.com/python/mypy/pull/16805)）
- 修复第三方库卸载后的缓存运行错误报告（Shantanu, PR [17420](https://github.com/python/mypy/pull/17420)）

### 崩溃修复
- 修复 TypedDict 中无效类型的守护进程崩溃（Ivan Levkivskyi, PR [17495](https://github.com/python/mypy/pull/17495)）
- 修复与 `partial()` 相关的崩溃和错误（Ivan Levkivskyi, PR [17423](https://github.com/python/mypy/pull/17423)）
- 修复解包 TypedDict 时的崩溃（Ivan Levkivskyi, PR [17359](https://github.com/python/mypy/pull/17359)）
- 修复 ParamSpec 解包 TypedDict 时的崩溃（Ivan Levkivskyi, PR [17358](https://github.com/python/mypy/pull/17358)）
- 修复涉及元组的递归联合时的崩溃（Ivan Levkivskyi, PR [17353](https://github.com/python/mypy/pull/17353)）
- 修复无效可调用属性重写时的崩溃（Ivan Levkivskyi, PR [17352](https://github.com/python/mypy/pull/17352)）
- 修复在 NamedTuple 中解包 self 时的崩溃（Ivan Levkivskyi, PR [17351](https://github.com/python/mypy/pull/17351)）
- 修复带有可选类型的递归别名崩溃（Ivan Levkivskyi, PR [17350](https://github.com/python/mypy/pull/17350)）
- 修复在泛型定义内的类型注释崩溃（Bénédikt Tran, PR [16849](https://github.com/python/mypy/pull/16849)）

### 文档更改
- 在文档中对可选错误代码使用内联配置（Shantanu, PR [17374](https://github.com/python/mypy/pull/17374)）
- 在文档中使用小写泛型（Seo Sanghyeon, PR [17176](https://github.com/python/mypy/pull/17176)）
- 添加 show-error-code-links 的文档（GiorgosPapoutsakis, PR [17144](https://github.com/python/mypy/pull/17144)）
- 更新 CONTRIBUTING.md 以包含 Windows 命令（GiorgosPapoutsakis, PR [17142](https://github.com/python/mypy/pull/17142)）


### 其他显著改进和修复
- 修复对 TypeVarTuple 的 ParamSpec 推断（Ivan Levkivskyi, PR [17431](https://github.com/python/mypy/pull/17431)）
- 修复 `partial` 的显式类型（Ivan Levkivskyi, PR [17424](https://github.com/python/mypy/pull/17424)）
- 始终允许 lambda 调用（Ivan Levkivskyi, PR [17430](https://github.com/python/mypy/pull/17430)）
- 修复包含 None 的 PEP 604 联合类型的 isinstance 检查（Shantanu, PR [17415](https://github.com/python/mypy/pull/17415)）
- 修复新样式类型变量中的自引用上限（Ivan Levkivskyi, PR [17407](https://github.com/python/mypy/pull/17407)）
- 考虑实例与可调用对象之间的重叠（Ivan Levkivskyi, PR [17389](https://github.com/python/mypy/pull/17389)）
- 允许在类方法中使用新样式的 self 类型（Ivan Levkivskyi, PR [17381](https://github.com/python/mypy/pull/17381)）
- 修复对 PEP 604 联合类型的类型别名进行 isinstance 检查（Shantanu, PR [17371](https://github.com/python/mypy/pull/17371)）
- 在重叠检查中正确处理解包（Ivan Levkivskyi, PR [17356](https://github.com/python/mypy/pull/17356)）
- 修复具有泛型构造函数的类的类型应用（Ivan Levkivskyi, PR [17354](https://github.com/python/mypy/pull/17354)）
- 更新 `typing_extensions` 至 >=4.6.0 以修复 Python 3.12 错误（Ben Brown, PR [17312](https://github.com/python/mypy/pull/17312)）
- 避免在 lambda 中出现 "does not return" 错误（Shantanu, PR [17294](https://github.com/python/mypy/pull/17294)）
- 修复在非严格可选模式下与描述符相关的错误（Max Murin, PR [17293](https://github.com/python/mypy/pull/17293)）
- 不要将 lambda 体内的不可达性泄露到周围作用域（Anders Kaseorg, PR [17287](https://github.com/python/mypy/pull/17287)）
- 修复 Windows 上非 ASCII 字符的问题（Alexander Leopold Shon, PR [17275](https://github.com/python/mypy/pull/17275)）
- 修复负整数字面量的类型缩小问题（gilesgc, PR [17256](https://github.com/python/mypy/pull/17256)）
- 修复 mypy 守护进程中 .py 和 .pyi 文件之间的混淆（Valentin Stanciu, PR [17245](https://github.com/python/mypy/pull/17245)）
- 修复 `tuple[X, Y]` 表达式的类型（urnest, PR [17235](https://github.com/python/mypy/pull/17235)）
- 不要忘记在发生 `name-defined` 错误后，`TypedDict` 被包裹在 `Unpack` 中（Christoph Tyralla, PR [17226](https://github.com/python/mypy/pull/17226)）
- 将注解参数标记为具有显式类型，而非推断类型（bzoracler, PR [17217](https://github.com/python/mypy/pull/17217)）
- 不要将 Enum 私有属性视为枚举成员（Ali Hamdan, PR [17182](https://github.com/python/mypy/pull/17182)）
- 修复包含管道字符的字面量字符串（Jelle Zijlstra, PR [17148](https://github.com/python/mypy/pull/17148)）


### Typeshed 更新

请查看 [git log](https://github.com/python/typeshed/commits/main?after=6dda799d8ad1d89e0f8aad7ac41d2d34bd838ace+0&branch=main&path=stdlib) 获取标准库 typeshed 存根更改的完整列表。

### Mypy 1.11.1
- 修复 `RawExpressionType.accept` 在 `--cache-fine-grained` 下崩溃（Anders Kaseorg, PR [17588](https://github.com/python/mypy/pull/17588)）
- 修复 PEP 604 的 isinstance 缓存（Shantanu, PR [17563](https://github.com/python/mypy/pull/17563)）
- 修复在 Python < 3.12 上未定义的 `typing.TypeAliasType`（Nikita Sobolev, PR [17558](https://github.com/python/mypy/pull/17558)）
- 修复 `types.GenericAlias` 查找崩溃（Shantanu, PR [17543](https://github.com/python/mypy/pull/17543)）

### Mypy 1.11.2
- 联合类型字面量字符串的替代修复（Ivan Levkivskyi, PR [17639](https://github.com/python/mypy/pull/17639)）
- 存储前解包 `TypedDict` 项类型（Ivan Levkivskyi, PR [17640](https://github.com/python/mypy/pull/17640)）

### 致谢
感谢所有为此版本贡献的 mypy 开发者：

- Alex Waygood
- Alexander Leopold Shon
- Ali Hamdan
- Anders Kaseorg
- Ben Brown
- Bénédikt Tran
- bzoracler
- Christoph Tyralla
- Christopher Barber
- dexterkennedy
- gilesgc
- GiorgosPapoutsakis
- Ivan Levkivskyi
- Jelle Zijlstra
- Jukka Lehtosalo
- Marc Mueller
- Matthieu Devlin
- Michael R. Crusoe
- Nikita Sobolev
- Seo Sanghyeon
- Shantanu
- sobolevn
- Steven Troxler
- Tadeu Manoel
- Tamir Duberstein
- Tushar Sadhwani
- urnest
- Valentin Stanciu

同时也感谢我的雇主 Dropbox 对 mypy 开发的支持。


## Mypy 1.10

我们刚刚将 mypy 1.10 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是 Python 的静态类型检查器。本次发布包含新特性、性能改进和错误修复。您可以通过以下命令安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读此版本的完整文档。

### 支持 TypeIs (PEP 742)

Mypy 现在支持 `TypeIs`（[PEP 742](https://peps.python.org/pep-0742/)），允许函数缩小值的类型，类似于 `isinstance()`。与 `TypeGuard` 不同，`TypeIs` 可以在 if 语句的 `if` 和 `else` 分支中缩小类型：

```python
from typing_extensions import TypeIs

def is_str(s: object) -> TypeIs[str]:
    return isinstance(s, str)

def f(o: str | int) -> None:
    if is_str(o):
        # o 的类型是 'str'
        ...
    else:
        # o 的类型是 'int'
        ...
```

`TypeIs` 将在 Python 3.13 的 `typing` 模块中添加，但可以通过从 `typing_extensions` 导入在早期 Python 版本中使用。

此功能由 Jelle Zijlstra 贡献（PR [16898](https://github.com/python/mypy/pull/16898)）。

### 支持 TypeVar 默认值 (PEP 696)

[PEP 696](https://peps.python.org/pep-0696/) 添加了对类型参数默认值的支持。例如：

```python
from typing import Generic
from typing_extensions import TypeVar

T = TypeVar("T", default=int)

class C(Generic[T]):
   ...

x: C = ...
y: C[str] = ...
reveal_type(x)  # C[int], 因为有默认值
reveal_type(y)  # C[str]
```

TypeVar 默认值将被添加到 Python 3.13 的 `typing` 模块中，但可以通过从 `typing_extensions` 导入在早期 Python 版本中使用。

此功能由 Marc Mueller 贡献（PR [16878](https://github.com/python/mypy/pull/16878) 和 PR [16925](https://github.com/python/mypy/pull/16925)）。

### 支持 TypeAliasType (PEP 695)

作为实现 [PEP 695](https://peps.python.org/pep-0695/) 的初步步骤，mypy 现在支持 `TypeAliasType`。`TypeAliasType` 提供了 Python 3.12 中新 `type` 语句的回溯支持。

```python
type ListOrSet[T] = list[T] | set[T]
```

等价于：

```python
T = TypeVar("T")
ListOrSet = TypeAliasType("ListOrSet", list[T] | set[T], type_params=(T,))
```

在 mypy 中使用的示例：

```python
from typing_extensions import TypeAliasType, TypeVar

NewUnionType = TypeAliasType("NewUnionType", int | str)
x: NewUnionType = 42
y: NewUnionType = 'a'
z: NewUnionType = object()  # 错误：赋值中类型不兼容（表达式的类型是 "object"，变量的类型是 "int | str"）[assignment]

T = TypeVar("T")
ListOrSet = TypeAliasType("ListOrSet", list[T] | set[T], type_params=(T,))
a: ListOrSet[int] = [1, 2]
b: ListOrSet[str] = {'a', 'b'}
c: ListOrSet[str] = 'test'  # 错误：赋值中类型不兼容（表达式的类型是 "str"，变量的类型是 "list[str] | set[str]"）[assignment]
```

`TypeAliasType` 已在 Python 3.12 的 `typing` 模块中添加，但可以通过从 `typing_extensions` 导入在早期 Python 版本中使用。

此功能由 Ali Hamdan 贡献（PR [16926](https://github.com/python/mypy/pull/16926)、PR [17038](https://github.com/python/mypy/pull/17038) 和 PR [17053](https://github.com/python/mypy/pull/17053)）。

### 检测额外的 unsafe super() 使用

当目标具有简单（空）主体时，mypy 将更一致地拒绝 unsafe 使用 `super()`。示例：

```python
class Proto(Protocol):
    def method(self) -> int: ...

class Sub(Proto):
    def method(self) -> int:
        return super().meth()  # 错误（不安全）
```

此功能由 Shantanu 贡献（PR [16756](https://github.com/python/mypy/pull/16756)）。

### Stubgen 改进
- 保留空元组注释（Ali Hamdan, PR [16907](https://github.com/python/mypy/pull/16907)）
- 添加对 PEP 570 位置参数的支持（Ali Hamdan, PR [16904](https://github.com/python/mypy/pull/16904)）
- 用内置容器替换过时的类型别名（Ali Hamdan, PR [16780](https://github.com/python/mypy/pull/16780)）
- 修复生成的数据类 `__init__` 签名（Ali Hamdan, PR [16906](https://github.com/python/mypy/pull/16906)）

### Mypyc 改进
- 提供更简单的 IR 到 IR 转换定义方式（Jukka Lehtosalo, PR [16998](https://github.com/python/mypy/pull/16998)）
- 实现整数（不）相等的降低过程和添加原语（Jukka Lehtosalo, PR [17027](https://github.com/python/mypy/pull/17027)）
- 实现剩余标记整数比较的降低（Jukka Lehtosalo, PR [17040](https://github.com/python/mypy/pull/17040)）
- 优化一些布尔/比特寄存器（Jukka Lehtosalo, PR [17022](https://github.com/python/mypy/pull/17022)）
- 重新标记由 async with 产生的重定义名称（Richard Si, PR [16408](https://github.com/python/mypy/pull/16408)）
- 优化运行时的 TYPE_CHECKING 为 False（Srinivas Lade, PR [16263](https://github.com/python/mypy/pull/16263)）
- 修复不可达推导的编译（Richard Si, PR [15721](https://github.com/python/mypy/pull/15721)）
- 不在不可内联的最终局部读取时崩溃（Richard Si, PR [15719](https://github.com/python/mypy/pull/15719)）

### 文档改进
- 从 `typing` 导入 `TypedDict` 而不是 `typing_extensions`（Riccardo Di Maio, PR [16958](https://github.com/python/mypy/pull/16958)）
- 在章节标题中添加缺失的 `mutable-override`（James Braza, PR [16886](https://github.com/python/mypy/pull/16886)）

### 错误报告改进
- 在错误消息中更一致地使用小写泛型（Jukka Lehtosalo, PR [17035](https://github.com/python/mypy/pull/17035)）

### 其他显著变化和修复
- 修复访问联合类型上的描述符时的错误推断类型（Matthieu Devlin, PR [16604](https://github.com/python/mypy/pull/16604)）
- 修复在 `Callable` 别名中展开无效 `Unpack` 时崩溃（Ali Hamdan, PR [17028](https://github.com/python/mypy/pull/17028)）
- 修复字符串格式化与字符串枚举时的误报（roberfi, PR [16555](https://github.com/python/mypy/pull/16555)）
- 匹配元组与序列模式时缩小单个项目（Loïc Simon, PR [16905](https://github.com/python/mypy/pull/16905)）
- 修复 TypeGuard 或 TypeIs 中类型变量的误报（Evgeniy Slobodkin, PR [17071](https://github.com/python/mypy/pull/17071)）
- 改进生成器的 `yield from` 推断（Shantanu, PR [16717](https://github.com/python/mypy/pull/16717)）
- 修复在 `attrs` 类中模拟哈希方法逻辑（Hashem, PR [17016](https://github.com/python/mypy/pull/17016)）
- 添加使用 `ParamSpec` 的 typeshed 回滚提交（Tamir Duberstein, PR [16942](https://github.com/python/mypy/pull/16942)）
- 修复 `types.EllipsisType` 的类型缩小（Shantanu, PR [17003](https://github.com/python/mypy/pull/17003)）
- 修复单项目枚举匹配类型耗尽（Oskari Lehto, PR [16966](https://github.com/python/mypy/pull/16966)）
- 改进空集合的类型推断（Marc Mueller, PR [16994](https://github.com/python/mypy/pull/16994)）
- 修复装饰属性的覆盖检查（Shantanu, PR [16856](https://github.com/python/mypy/pull/16856)）
- 修复与函数主题的匹配缩小（Edward Paget, PR [16503](https://github.com/python/mypy/pull/16503)）
- 允许在 `Literal[...]` 中使用 `+N`（Spencer Brown, PR [16910](https://github.com/python/mypy/pull/16910)）
- 实验性：在 `type[...]` 中支持 TypedDict（Marc Mueller, PR [16963](https://github.com/python/mypy/pull/16963)）
- 实验性：修复 `type[...]` 中具有可选键的 TypedDict 的问题（Marc Mueller, PR [17068](https://github.com/python/mypy/pull/17068)）

### Typeshed 更新

有关标准库 typeshed 存根更改的完整列表，请参阅 [git log](https://github.com/python/typeshed/commits/main?after=6dda799d8ad1d89e0f8aad7ac41d2d34bd838ace+0&branch=main&path=stdlib)。

### Mypy 1.10.1

- 修复卸载第三方库后缓存运行时的错误报告（Shantanu, PR [17420](https://github.com/python/mypy/pull/17420)）

### 感谢名单
感谢所有为本次发布做出贡献的 mypy 贡献者：

- Alex Waygood
- Ali Hamdan
- Edward Paget
- Evgeniy Slobodkin
- Hashem
- hesam
- Hugo van Kemenade
- Ihor
- James Braza
- Jelle Zijlstra
- jhance
- Jukka Lehtosalo
- Loïc Simon
- Marc Mueller
- Matthieu Devlin
- Michael R. Crusoe
- Nikita Sobolev
- Oskari Lehto
- Riccardo Di Maio
- Richard Si
- roberfi
- Roman Solomatin
- Sam Xifaras
- Shantanu
- Spencer Brown
- Srinivas Lade
- Tamir Duberstein
- youkaichao

我还想感谢我的雇主 Dropbox 对 mypy 开发的支持。

## Mypy 1.9

我们刚刚将 mypy 1.9 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 的静态类型检查器。本次发布包括新特性、性能改进和错误修复。你可以按如下方式安装：

    python3 -m pip install -U mypy

你可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读本次发布的完整文档。

### 破坏性变更

由于我们在 mypy 1.9 中使用的 typeshed 版本不支持 Python 3.7，因此 mypy 1.9 也不再支持该版本（Jared Hance, PR [16883](https://github.com/python/mypy/pull/16883)）。

我们计划在今年晚些时候默认启用 [局部部分类型](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-local-partial-types)（通过 `--local-partial-types` 标志启用）。这个变化多年前就已宣布，现在终于要实施。这是一个重大不兼容的变更，因此我们可能会将其作为即将发布的 mypy 2.0 的一部分。这使得守护进程和非守护进程的 mypy 运行在默认情况下具有相同的行为。

局部部分类型也可以在 mypy 配置文件中启用：
```
local_partial_types = True
```

我们正在考虑提供一个工具，以便更容易地迁移项目使用 `--local-partial-types`，但目前尚不清楚这是否可行。迁移通常涉及为模块级和类级变量添加一些显式的类型注解。

### 对类型参数默认值的基本支持（PEP 696）

本次发布包含对类型参数默认值的新实验性支持（[PEP 696](https://peps.python.org/pep-0696)）。请尝试一下！这个特性由 Marc Mueller 贡献。

由于此特性将在下一个 Python 特性版本（3.13）中正式引入，因此目前需要从 `typing_extensions` 导入 `TypeVar`、`ParamSpec` 或 `TypeVarTuple` 来使用默认值。

下面是根据 PEP 修改的示例，定义了 `BotT` 的默认值：
```python
from typing import Generic
from typing_extensions import TypeVar

class Bot: ...

BotT = TypeVar("BotT", bound=Bot, default=Bot)

class Context(Generic[BotT]):
    bot: BotT

class MyBot(Bot): ...

# 类型是 Bot（默认值）
reveal_type(Context().bot)
# 类型是 MyBot
reveal_type(Context[MyBot]().bot)
```

### 类型检查改进
- 修复重载缺失类型存储的问题（Marc Mueller, PR [16803](https://github.com/python/mypy/pull/16803)）。
- 修复 `'WriteToConn' object has no attribute 'flush'` 错误（Charlie Denton, PR [16801](https://github.com/python/mypy/pull/16801)）。
- 改进 TypeAlias 错误消息（Marc Mueller, PR [16831](https://github.com/python/mypy/pull/16831)）。
- 支持收窄包含 `type[None]` 的联合类型（Christoph Tyralla, PR [16315](https://github.com/python/mypy/pull/16315)）。
- 支持将 TypedDict 作为类基类型的函数语法（anniel-stripe, PR [16703](https://github.com/python/mypy/pull/16703)）。
- 接受多行引号注解（Shantanu, PR [16765](https://github.com/python/mypy/pull/16765)）。
- 在 `Literal` 中允许一元加号（Jelle Zijlstra, PR [16729](https://github.com/python/mypy/pull/16729)）。
- 替换静态方法返回类型中的类型变量（Kouroche Bouchiat, PR [16670](https://github.com/python/mypy/pull/16670)）。
- 将 TypeVarTuple 视为不变（Marc Mueller, PR [16759](https://github.com/python/mypy/pull/16759)）。
- 为 `attrs` 插件中的 `field()` 添加 `alias` 支持（Nikita Sobolev, PR [16610](https://github.com/python/mypy/pull/16610)）。
- 改进 attrs 哈希检测（Tin Tvrtković, PR [16556](https://github.com/python/mypy/pull/16556)）。

### 性能改进
- 加速查找函数类型变量（Jukka Lehtosalo, PR [16562](https://github.com/python/mypy/pull/16562)）。

### 文档更新
- 在 "mypy --help" 中记录 `--enable-incomplete-feature` 的支持值（Froger David, PR [16661](https://github.com/python/mypy/pull/16661)）。
- 更新新类型系统讨论链接（thomaswhaley, PR [16841](https://github.com/python/mypy/pull/16841)）。
- 在备忘单中添加缺失的类实例化（Aleksi Tarvainen, PR [16817](https://github.com/python/mypy/pull/16817)）。
- 记录 `--no-strict-optional` 的潜在问题（Shantanu, PR [16731](https://github.com/python/mypy/pull/16731)）。
- 改进 mypy 守护进程文档中关于局部部分类型的说明（Makonnen Makonnen, PR [16782](https://github.com/python/mypy/pull/16782)）。
- 修正编号错误（Stefanie Molin, PR [16838](https://github.com/python/mypy/pull/16838)）。
- 各种文档改进（Shantanu, PR [16836](https://github.com/python/mypy/pull/16836)）。

### Stubtest 改进
- 忽略缺失的私有函数/方法参数（私有参数名称以单下划线开头且具有默认值）（PR [16507](https://github.com/python/mypy/pull/16507)）。
- 忽略新的协议 dunder（Alex Waygood, PR [16895](https://github.com/python/mypy/pull/16895)）。
- 可以省略私有参数（Sebastian Rittau, PR [16507](https://github.com/python/mypy/pull/16507)）。
- 添加将枚举成员设置为 "..." 的支持（Jelle Zijlstra, PR [16807](https://github.com/python/mypy/pull/16807)）。
- 调整符号表逻辑（Shantanu, PR [16823](https://github.com/python/mypy/pull/16823)）。
- 修复重载解析中的位置参数处理（Shantanu, PR [16750](https://github.com/python/mypy/pull/16750)）。

### Stubgen 改进
- 修复 TypeVarTuple 的星号解包崩溃（Ali Hamdan, PR [16869](https://github.com/python/mypy/pull/16869)）。
- 在所有地方使用 PEP 604 联合（Ali Hamdan, PR [16519](https://github.com/python/mypy/pull/16519)）。
- 不忽略属性删除器（Ali Hamdan, PR [16781](https://github.com/python/mypy/pull/16781)）。
- 支持为 `staticmethod` 生成类型存根（WeilerMarcel, PR [14934](https://github.com/python/mypy/pull/14934)）。

### 感谢致辞

感谢所有为此版本贡献的 mypy 开发者：

- Aleksi Tarvainen
- Alex Waygood
- Ali Hamdan
- anniel-stripe
- Charlie Denton
- Christoph Tyralla
- Dheeraj
- Fabian Keller
- Fabian Lewis
- Froger David
- Ihor
- Jared Hance
- Jelle Zijlstra
- Jukka Lehtosalo
- Kouroche Bouchiat
- Lukas Geiger
- Maarten Huijsmans
- Makonnen Makonnen
- Marc Mueller
- Nikita Sobolev
- Sebastian Rittau
- Shantanu
- Stefanie Molin
- Stephen Morton
- thomaswhaley
- Tin Tvrtković
- WeilerMarcel
- Wesley Collin Wright
- zipperer

也感谢我的雇主 Dropbox 对 mypy 开发的支持。

## Mypy 1.8

我们刚刚将 mypy 1.8 上传到 Python 包索引 ([PyPI](https://pypi.org/project/mypy/))。mypy 是 Python 的静态类型检查器。此版本包含新功能、性能改进和错误修复。您可以通过以下方式安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读此版本的完整文档。

### 类型检查改进
- 在 `isinstance` 检查中，如果至少一个类型是 final，则不进行类型交集（Christoph Tyralla, PR [16330](https://github.com/python/mypy/pull/16330)）。
- 检测到没有 `__bool__` 的 `@final` 类不能有假值实例（Ilya Priven, PR [16566](https://github.com/python/mypy/pull/16566)）。
- 不允许具有额外关键字的 `TypedDict` 类（Nikita Sobolev, PR [16438](https://github.com/python/mypy/pull/16438)）。
- 不允许 `NamedTuple` 的类级关键字（Nikita Sobolev, PR [16526](https://github.com/python/mypy/pull/16526)）。
- 使不精确约束处理更健壮（Ivan Levkivskyi, PR [16502](https://github.com/python/mypy/pull/16502)）。
- 修复扩展泛型 `TypedDict` 中的严格可选性（Ivan Levkivskyi, PR [16398](https://github.com/python/mypy/pull/16398)）。
- 允许对 PEP 695 构造的类型忽略（Shantanu, PR [16608](https://github.com/python/mypy/pull/16608)）。
- 为 `TypedDict` 和 `NamedTuple` 启用 `type_check_only` 支持（Nikita Sobolev, PR [16469](https://github.com/python/mypy/pull/16469)）。

### 性能改进
- 增加分析特殊形式赋值的快速路径（Jukka Lehtosalo, PR [16561](https://github.com/python/mypy/pull/16561)）。

### 错误报告改进
- 不显示插件错误代码的文档链接（Ivan Levkivskyi, PR [16383](https://github.com/python/mypy/pull/16383)）。
- 改进 `super` 检查的错误消息并添加更多测试（Nikita Sobolev, PR [16393](https://github.com/python/mypy/pull/16393)）。
- 为可变协变重写添加错误代码（Ivan Levkivskyi, PR [16399](https://github.com/python/mypy/pull/16399)）。

### Stubgen 改进
- 在函数签名中保留简单默认值（Ali Hamdan, PR [15355](https://github.com/python/mypy/pull/15355)）。
- 在输出中包含 `__all__`（Jelle Zijlstra, PR [16356](https://github.com/python/mypy/pull/16356)）。
- 修复与 pybind11 和 mypy 1.7 的 stubgen 回归（Chad Dombrova, PR [16504](https://github.com/python/mypy/pull/16504)）。

### Stubtest 改进
- 改进不可表示默认值的处理（Jelle Zijlstra, PR [16433](https://github.com/python/mypy/pull/16433)）。
- 如果缺少函数，打印更有帮助的错误信息（Alex Waygood, PR [16517](https://github.com/python/mypy/pull/16517)）。
- 支持 `@type_check_only` 装饰器（Nikita Sobolev, PR [16422](https://github.com/python/mypy/pull/16422)）。
- 警告缺少 `__del__`（Shantanu, PR [16456](https://github.com/python/mypy/pull/16456)）。
- 修复某些使用 `final` 和 `deprecated` 的崩溃（Shantanu, PR [16457](https://github.com/python/mypy/pull/16457)）。

### 崩溃修复
- 修复对 `Callable[[Unpack[Tuple[Any, ...]]], Any]` 的类型别名导致的崩溃（Alex Waygood, PR [16541](https://github.com/python/mypy/pull/16541)）。
- 修复在 `__call__` 中的 TypeGuard 导致的崩溃（Ivan Levkivskyi, PR [16516](https://github.com/python/mypy/pull/16516)）。
- 修复方法中的无效枚举导致的崩溃（Ivan Levkivskyi, PR [16511](https://github.com/python/mypy/pull/16511)）。
- 修复 TypedDict 中未导入 Any 导致的崩溃（Ivan Levkivskyi, PR [16510](https://github.com/python/mypy/pull/16510)）。

### 文档更新
- 将软错误限制的默认值更新为 -1（Sveinung Gundersen, PR [16542](https://github.com/python/mypy/pull/16542)）。
- 支持 Sphinx 7.x（Michael R. Crusoe, PR [16460](https://github.com/python/mypy/pull/16460)）。

### 其他显著变化和修复
- 允许 mypy 输出包含每个文件结果的 junit 文件（Matthew Wright, PR [16388](https://github.com/python/mypy/pull/16388)）。

### Typeshed 更新

请参阅 [git log](https://github.com/python/typeshed/commits/main?after=4a854366e03dee700109f8e758a08b2457ea2f51+0&branch=main&path=stdlib) 查看标准库 typeshed stub 的完整更改列表。

### 感谢致辞

感谢所有为此版本贡献的 mypy 开发者：

- Alex Waygood
- Ali Hamdan
- Chad Dombrova
- Christoph Tyralla
- Ilya Priven
- Ivan Levkivskyi
- Jelle Zijlstra
- Jukka Lehtosalo
- Marcel Telka
- Matthew Wright
- Michael R. Crusoe
- Nikita Sobolev
- Ole Peder Brandtzæg
- robjhornby
- Shantanu
- Sveinung Gundersen
- Valentin Stanciu

也感谢我的雇主 Dropbox 对 mypy 开发的支持。

发布者：Wesley Collin Wright

## Mypy 1.7

我们刚刚将 mypy 1.7 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 的静态类型检查器。此版本包含新功能、性能改进和错误修复。您可以通过以下命令安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 阅读此版本的完整文档。

### 使用 TypedDict 进行 `**kwargs` 类型注解

Mypy 现在支持将 `Unpack[...]` 与 TypedDict 类型结合使用，以注解 `**kwargs` 参数，默认启用。示例：

```python
# 或 'from typing_extensions import ...'
from typing import TypedDict, Unpack

class Person(TypedDict):
    name: str
    age: int

def foo(**kwargs: Unpack[Person]) -> None:
    ...

foo(name="x", age=1)  # 正确
foo(name=1)  # 错误
```

上述 `foo` 的定义等同于以下带有仅限关键字参数 `name` 和 `age` 的定义：

```python
def foo(*, name: str, age: int) -> None:
    ...
```

有关更多信息，请参见 [PEP 692](https://peps.python.org/pep-0692/)。请注意，与 PEP 当前版本不同，mypy 总是将带有 `Unpack[SomeTypedDict]` 的签名视为其扩展形式的等价，且对 TypedDict 参数没有特别的类型检查规则。

此功能由 Ivan Levkivskyi 于 2022 年贡献（PR [13471](https://github.com/python/mypy/pull/13471)）。

### TypeVarTuple 支持已启用（实验性）

Mypy 现在默认启用对变参泛型（TypeVarTuple）的支持，作为实验性功能。有关详细信息，请参见 [PEP 646](https://peps.python.org/pep-0646/)。

TypeVarTuple 的实现由 Jared Hance 和 Ivan Levkivskyi 在多个 mypy 版本中完成，并得到了 Jukka Lehtosalo 的帮助。

本次发布包含的更改：

- 修复处理带有 unpack 的元组类型上下文（Ivan Levkivskyi，PR [16444](https://github.com/python/mypy/pull/16444)）
- 在检查重载约束时处理 TypeVarTuple（robjhornby，PR [16428](https://github.com/python/mypy/pull/16428)）
- 启用 Unpack/TypeVarTuple 支持（Ivan Levkivskyi，PR [16354](https://github.com/python/mypy/pull/16354)）
- 修复 unpack 调用特殊情况导致的崩溃（Ivan Levkivskyi，PR [16381](https://github.com/python/mypy/pull/16381)）
- 对变参类型支持进行最后的调整（Ivan Levkivskyi，PR [16334](https://github.com/python/mypy/pull/16334)）
- 在同一可调用对象中支持 PEP-646 和 PEP-692（Ivan Levkivskyi，PR [16294](https://github.com/python/mypy/pull/16294)）
- 支持变参类型的新 `*` 语法（Ivan Levkivskyi，PR [16242](https://github.com/python/mypy/pull/16242)）
- 正确处理带有空参数的变参实例（Ivan Levkivskyi，PR [16238](https://github.com/python/mypy/pull/16238)）
- 正确处理变参类型的运行时类型应用（Ivan Levkivskyi，PR [16240](https://github.com/python/mypy/pull/16240)）
- 支持变参元组的打包/解包（Ivan Levkivskyi，PR [16205](https://github.com/python/mypy/pull/16205)）
- 更好地支持变参调用和索引（Ivan Levkivskyi，PR [16131](https://github.com/python/mypy/pull/16131)）
- 用户定义的变参类型的子类型和推断（Ivan Levkivskyi，PR [16076](https://github.com/python/mypy/pull/16076)）
- 完成对变参类型的类型分析（Ivan Levkivskyi，PR [15991](https://github.com/python/mypy/pull/15991)）

### 安装 Mypyc 依赖的新方式

如果您想安装 mypyc 所需的包依赖（不仅仅是 mypy），现在应该安装 `mypy[mypyc]` 而不是仅仅安装 `mypy`：

```bash
python3 -m pip install -U 'mypy[mypyc]'
```

Mypy 的用户比 mypyc 多，因此始终安装 mypyc 依赖项往往会引入不必要的依赖。

此更改由 Shantanu 提供（PR [16229](https://github.com/python/mypy/pull/16229)）。

### 重新导出的新规则

Mypy 不再将 `import a.b as b` 视为显式重新导出。旧行为可能被认为是不一致和令人惊讶的。这可能会影响一些存根包，例如旧版本的 `types-six`。如果将该导入视为重新导出是有意为之，您可以将导入更改为 `from a import b as b`。

此更改由 Anders Kaseorg 提供（PR [14086](https://github.com/python/mypy/pull/14086)）。

### 改进的类型推断

最近引入到 mypy 的新类型推断算法（但默认未启用）现在默认启用。它特别改善了对通用可调用对象的调用的类型推断，尤其是在参数也是通用可调用对象的情况下。您可以使用 `--old-type-inference` 来禁用新行为。

新的算法（在少数情况下）可能会产生不同的错误消息、不同的错误代码，或在不同的行上报告错误。在不正确使用通用类型的情况下，这种情况更为常见。

新类型推断算法由 Ivan Levkivskyi 提供，PR [16345](https://github.com/python/mypy/pull/16345) 使其默认启用。

### 使用 len() 缩小元组类型

Mypy 现在可以通过 `len()` 检查缩小元组类型。例如：

```python
def f(t: tuple[int, int] | tuple[int, int, int]) -> None:
    if len(t) == 2:
        a, b = t   # Ok
    ...
```

此功能由 Ivan Levkivskyi 提供（PR [16237](https://github.com/python/mypy/pull/16237)）。

### 更精确的元组长度（实验性）

Mypy 通过 `--enable-incomplete-feature=PreciseTupleTypes` 支持对元组类型长度的实验性更精确检查。有关更多信息，请参阅 [文档](https://mypy.readthedocs.io/en/latest/command_line.html#enabling-incomplete-experimental-features)。

一般来说，我们计划使用 `--enable-incomplete-feature` 来引入需要社区反馈的实验性功能。

此功能由 Ivan Levkivskyi 提供（PR [16237](https://github.com/python/mypy/pull/16237)）。

### Mypy 更新日志

我们现在在 mypy Git 存储库中维护一个 [更新日志](https://github.com/python/mypy/blob/master/CHANGELOG.md)。它反映了 [mypy 发布博客帖子](https://mypy-lang.blogspot.com/) 的内容。我们将继续发布发布博客帖子。在未来，发布博客帖子将在发布日期附近基于更新日志创建。

此更改由 Shantanu 提供（PR [16280](https://github.com/python/mypy/pull/16280)）。

### Mypy 守护进程改进

* 修复因删除子模块而导致的守护进程崩溃（Jukka Lehtosalo, PR [16370](https://github.com/python/mypy/pull/16370)）
* 修复 dmypy 中使用 `--export-types` 时的文件重载问题（Ivan Levkivskyi, PR [16359](https://github.com/python/mypy/pull/16359)）
* 修复 Windows 上的 dmypy inspect（Ivan Levkivskyi, PR [16355](https://github.com/python/mypy/pull/16355)）
* 修复命名空间包的 dmypy inspect（Ivan Levkivskyi, PR [16357](https://github.com/python/mypy/pull/16357)）
* 修复通用函数中返回类型变为可选的问题（Jukka Lehtosalo, PR [16342](https://github.com/python/mypy/pull/16342)）
* 修复与模块级 `__getattr__` 相关的守护进程误报（Jukka Lehtosalo, PR [16292](https://github.com/python/mypy/pull/16292)）
* 修复与 ABCs 相关的守护进程崩溃（Jukka Lehtosalo, PR [16275](https://github.com/python/mypy/pull/16275)）
* 流式输出 dmypy 而不是在最后一次性输出（Valentin Stanciu, PR [16252](https://github.com/python/mypy/pull/16252)）
* 确保显示所有 dmypy 错误（Valentin Stanciu, PR [16250](https://github.com/python/mypy/pull/16250)）

### Mypyc 改进

* 在重复的函数定义上生成错误（Jukka Lehtosalo, PR [16309](https://github.com/python/mypy/pull/16309)）
* 不会因不可达语句而崩溃（Jukka Lehtosalo, PR [16311](https://github.com/python/mypy/pull/16311)）
* 避免嵌套函数中的循环引用（Jukka Lehtosalo, PR [16268](https://github.com/python/mypy/pull/16268)）
* 修复新 Python 中对内函数直接访问 `__dict__` 的问题（Shantanu, PR [16084](https://github.com/python/mypy/pull/16084)）
* 使元组的打包和解包更加高效（Jukka Lehtosalo, PR [16022](https://github.com/python/mypy/pull/16022)）

### 错误报告改进

* 更新星号表达式错误消息以匹配 CPython（Cibin Mathew, PR [16304](https://github.com/python/mypy/pull/16304)）
* 修复“也许您忘记使用 await”的错误代码说明（Jelle Zijlstra, PR [16203](https://github.com/python/mypy/pull/16203)）
* 对于不安全的重载，使用错误代码 `[unsafe-overload]`，而不是 `[misc]`（Randolf Scholz, PR [16061](https://github.com/python/mypy/pull/16061)）
* 修改与 void 函数相关的错误消息（Albert Tugushev, PR [15876](https://github.com/python/mypy/pull/15876)）
* 在消息中将底层类型表示为 Never（Shantanu, PR [15996](https://github.com/python/mypy/pull/15996)）
* 为不兼容的 AsyncIterator 返回类型添加提示（Ilya Priven, PR [15883](https://github.com/python/mypy/pull/15883)）
* 不建议使用运行时包现在附带类型的存根包（Alex Waygood, PR [16226](https://github.com/python/mypy/pull/16226)）

### 性能改进

* 加快类型参数检查（Jukka Lehtosalo, PR [16353](https://github.com/python/mypy/pull/16353)）
* 增加自类型检查的快速路径（Jukka Lehtosalo, PR [16352](https://github.com/python/mypy/pull/16352)）
* 缓存关于文件是否为 typeshed 文件的信息（Jukka Lehtosalo, PR [16351](https://github.com/python/mypy/pull/16351)）
* 在日志调用中跳过不必要的昂贵 `repr()`（Jukka Lehtosalo, PR [16350](https://github.com/python/mypy/pull/16350)）

### Attrs 和数据类改进

* `dataclass.replace`: 允许转换类（Ilya Priven, PR [15915](https://github.com/python/mypy/pull/15915)）
* `dataclass.replace`: 回退到 typeshed 签名（Ilya Priven, PR [15962](https://github.com/python/mypy/pull/15962)）
* 文档化 `dataclass_transform` 行为（Ilya Priven, PR [16017](https://github.com/python/mypy/pull/16017)）
* `attrs`: 移除字段类型检查（Ilya Priven, PR [15983](https://github.com/python/mypy/pull/15983)）
* `attrs`, `dataclasses`: 当基类不强制使用插槽时，不强制执行（Ilya Priven, PR [15976](https://github.com/python/mypy/pull/15976)）
* 修复数据类字段/属性冲突崩溃（Nikita Sobolev, PR [16147](https://github.com/python/mypy/pull/16147)）

### Stubgen 改进

* 以 utf-8 编码写入存根（Jørgen Lind, PR [16329](https://github.com/python/mypy/pull/16329)）
* 修复语义分析模式中缺少的属性设置器（Ali Hamdan, PR [16303](https://github.com/python/mypy/pull/16303)）
* 统一 C 扩展和纯 Python 存根生成器，采用面向对象设计（Chad Dombrova, PR [15770](https://github.com/python/mypy/pull/15770)）
* 修复生成导入的多个问题（Ali Hamdan, PR [15624](https://github.com/python/mypy/pull/15624)）
* 生成有效的数据类存根（Ali Hamdan, PR [15625](https://github.com/python/mypy/pull/15625)）

### 崩溃修复

* 修复方法中 TypedDict 的增量模式崩溃（Ivan Levkivskyi, PR [16364](https://github.com/python/mypy/pull/16364)）
* 修复 TypedDict 中的星号解包崩溃（Ivan Levkivskyi, PR [16116](https://github.com/python/mypy/pull/16116)）
* 修复增量模式下格式错误的 TypedDict 导致的崩溃（Ivan Levkivskyi, PR [16115](https://github.com/python/mypy/pull/16115)）
* 修复命名空间包的报告生成崩溃（Shantanu, PR [16019](https://github.com/python/mypy/pull/16019)）
* 修复解析错误代码配置时的拼写错误导致的崩溃（Shantanu, PR [16005](https://github.com/python/mypy/pull/16005)）
* 修复 `__post_init__()` 内部错误（Ilya Priven, PR [16080](https://github.com/python/mypy/pull/16080)）

### 文档更新

* 使从 README 中复制命令更容易（Hamir Mahal, PR [16133](https://github.com/python/mypy/pull/16133)）
* 文档和重命名 `[overload-overlap]` 错误代码（Shantanu, PR [16074](https://github.com/python/mypy/pull/16074)）
* 文档 `--force-uppercase-builtins` 和 `--force-union-syntax`（Nikita Sobolev, PR [16049](https://github.com/python/mypy/pull/16049)）
* 文档 `force_union_syntax` 和 `force_uppercase_builtins`（Nikita Sobolev, PR [16048](https://github.com/python/mypy/pull/16048)）
* 说明我们不跟踪符号之间的关系（Ilya Priven, PR [16018](https://github.com/python/mypy/pull/16018)）

### 其他显著变化和修复

* 将缩小的类型传播到 lambda 表达式（Ivan Levkivskyi, PR [16407](https://github.com/python/mypy/pull/16407)）
* 避免从 `setuptools._distutils` 导入（Shantanu, PR [16348](https://github.com/python/mypy/pull/16348)）
* 删除递归别名标志（Ivan Levkivskyi, PR [16346](https://github.com/python/mypy/pull/16346)）
* 正确使用调用的适当子类型（Ivan Levkivskyi, PR [16343](https://github.com/python/mypy/pull/16343)）
* 更一致地使用上界作为推断回退（Ivan Levkivskyi, PR [16344](https://github.com/python/mypy/pull/16344)）
* 添加 `[unimported-reveal]` 错误代码（Nikita Sobolev, PR [16271](https://github.com/python/mypy/pull/16271)）
* 为 `TypedDict` 添加 `|=` 和 `|` 运算符支持（Nikita Sobolev, PR [16249](https://github.com/python/mypy/pull/16249)）
* 澄清参数的方差约定（Ivan Levkivskyi, PR [16302](https://github.com/python/mypy/pull/16302)）
* 正确识别 `typing_extensions.NewType`（Ganden Schaffner, PR [16298](https://github.com/python/mypy/pull/16298)）
* 修复缺少类型映射的部分定义（Shantanu, PR [15995](https://github.com/python/mypy/pull/15995)）
* 使用 SPDX 许可证标识符（Nikita Sobolev, PR [16230](https://github.com/python/mypy/pull/16230)）
* 使 `__qualname__` 和 `__module__` 在类体中可用（Anthony Sottile, PR [16215](https://github.com/python/mypy/pull/16215)）
* stubtest: 提示存根中的参数需要为关键字参数（Alex Waygood, PR [16210](https://github.com/python/mypy/pull/16210)）
* 元组切片不应传播回退（Thomas Grainger, PR [16154](https://github.com/python/mypy/pull/16154)）
* 修复重载情况下的类型对象处理（Shantanu, PR [16168](https://github.com/python/mypy/pull/16168)）
* 修复海象运算符与空集合的交互（Ivan Levkivskyi, PR [16197](https://github.com/python/mypy/pull/16197)）
* 在推断中使用类型变量界限（Ivan Levkivskyi, PR [16178](https://github.com/python/mypy/pull/16178)）
* 使用上界作为推断的回退方案（Ivan Levkivskyi, PR [16184](https://github.com/python/mypy/pull/16184)）
* 特殊处理空集合的类型推断（Ivan Levkivskyi, PR [16122](https://github.com/python/mypy/pull/16122)）
* 允许在可调用类型中解包 `TypedDict`（Ivan Levkivskyi, PR [16083](https://github.com/python/mypy/pull/16083)）
* 修复具有通用 self 的重载 `__call__` 的推断（Shantanu, PR [16053](https://github.com/python/mypy/pull/16053)）
* 在泛型类上调用动态类钩子（Petter Friberg, PR [16052](https://github.com/python/mypy/pull/16052)）
* 通过属性访问保留隐式导出的类型（Shantanu, PR [16129](https://github.com/python/mypy/pull/16129)）
* 修复 stubtest bug（Alex Waygood）
* 修复 `tuple[Any, ...]` 子类型问题（Shantanu, PR [16108](https://github.com/python/mypy/pull/16108)）
* 对简单可调用后缀进行宽容处理（Ivan Levkivskyi, PR [15913](https://github.com/python/mypy/pull/15913)）
* 为插件添加 `add_overloaded_method_to_class` 辅助函数（Nikita Sobolev, PR [16038](https://github.com/python/mypy/pull/16038)）
* 将 `misc/proper_plugin.py` 打包为 `mypy` 的一部分（Nikita Sobolev, PR [16036](https://github.com/python/mypy/pull/16036)）
* 修复匹配语句中的 `case Any()`（DS/Charlie, PR [14479](https://github.com/python/mypy/pull/14479)）
* 使可迭代逻辑更一致（Shantanu, PR [16006](https://github.com/python/mypy/pull/16006)）
* 修复具有 `__call__` 的属性的推断（Shantanu, PR [15926](https://github.com/python/mypy/pull/15926)）

### Typeshed 更新

请查看 [git log](https://github.com/python/typeshed/commits/main?after=4a854366e03dee700109f8e758a08b2457ea2f51+0&branch=main&path=stdlib) 获取标准库 typeshed 存根更改的完整列表。

### 致谢

感谢所有为此版本贡献的 mypy 贡献者：

* Albert Tugushev
* Alex Waygood
* Ali Hamdan
* Anders Kaseorg
* Anthony Sottile
* Chad Dombrova
* Cibin Mathew
* dinaldoap
* DS/Charlie
* Eli Schwartz
* Ganden Schaffner
* Hamir Mahal
* Ihor
* Ikko Eltociear Ashimine
* Ilya Priven
* Ivan Levkivskyi
* Jelle Zijlstra
* Jukka Lehtosalo
* Jørgen Lind
* KotlinIsland
* Matt Bogosian
* Nikita Sobolev
* Petter Friberg
* Randolf Scholz
* Shantanu
* Thomas Grainger
* Valentin Stanciu

同时感谢我的雇主 Dropbox 对 mypy 开发的支持。

发布者：Jukka Lehtosalo

## Mypy 1.6

[2023年10月10日](https://mypy-lang.blogspot.com/2023/10/mypy-16-released.html)

我们刚刚将 mypy 1.6 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是 Python 的静态类型检查器。此版本包括新功能、性能改进和错误修复。您可以通过以下方式安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读此版本的完整文档。

### 引入导入错误的错误子代码

当导入目标是一个不支持静态类型检查的已安装库，并且没有可用的存根文件时，mypy 现在使用错误代码 `import-untyped`。其他无效导入产生 `import-not-found` 错误代码。它们都是导入错误代码的子代码，该代码以前用于所有类型的导入相关错误。

使用 `--disable-error-code=import-untyped` 可以仅忽略没有存根的已安装库的导入错误。这样，mypy 仍会报告例如导入语句中的拼写错误。

如果您使用 `--warn-unused-ignore` 或 `--strict`，mypy 会警告您使用 `# type: ignore[import]` 来忽略导入错误。您应该使用更具体的错误代码。否则，忽略导入错误代码仍会静默处理这两种错误。

此功能由 Shantanu 贡献（PR [15840](https://github.com/python/mypy/pull/15840)，PR [14740](https://github.com/python/mypy/pull/14740)）。

### 删除对 Python 3.6 及更早版本的支持

不再支持使用 `--python-version 3.6` 运行 mypy。Python 3.6 已经有一段时间没有被 mypy 正确支持，此次更新使其变得明确。此改动由 Nikita Sobolev 贡献（PR [15668](https://github.com/python/mypy/pull/15668)）。

### 选择性过滤 `--disallow-untyped-calls` 目标

使用 `--disallow-untyped-calls` 可能会在使用缺失类型信息的库时产生很多错误。现在，您可以使用 `--untyped-calls-exclude=acme` 等参数来禁用关于调用 acme 包中定义的函数的错误。有关更多信息，请参阅 [文档](https://mypy.readthedocs.io/en/latest/command_line.html#cmdoption-mypy-untyped-calls-exclude)。

此功能由 Ivan Levkivskyi 贡献（PR [15845](https://github.com/python/mypy/pull/15845)）。

### 改进的可调用类型之间的类型推断

Mypy 现在在可调用类型的参数中更好地推断类型变量。例如，以下代码片段现在可以正确类型检查：

```python
def f(c: Callable[[T, S], None]) -> Callable[[str, T, S], None]: ...
def g(*x: int) -> None: ...

reveal_type(f(g))  # Callable[[str, int, int], None]
```

此功能由 Ivan Levkivskyi 贡献（PR [15910](https://github.com/python/mypy/pull/15910)）。

### 不再将 None 和 TypeVar 视为重载中的重叠

Mypy 现在不再将参数类型为 None 的重载项与类型变量视为重叠：

```python
@overload
def f(x: None) -> None: ..
@overload
def f(x: T) -> Foo[T]: ...
```

之前，mypy 会对此定义产生错误。这在 T 的上界为 object 的情况下略显不安全，因为类型变量的值可能为 None。我们放宽了一些规则，以解决常见问题。

此功能由 Ivan Levkivskyi 贡献（PR [15846](https://github.com/python/mypy/pull/15846)）。

### 对 `--new-type-inference` 的改进

实验性的类型推断新算法（多态推断）作为 mypy 1.5 中的选择性功能推出，现在进行了多项改进：

* 改进约束求解中的传递闭包计算（Ivan Levkivskyi，PR [15754](https://github.com/python/mypy/pull/15754)）
* 在 `--new-type-inference` 下支持上界和取值（Ivan Levkivskyi，PR [15813](https://github.com/python/mypy/pull/15813)）
* 对变元类型的基本支持（Ivan Levkivskyi，PR [15879](https://github.com/python/mypy/pull/15879)）
* 多态推断：支持参数规范和 lambda 表达式（Ivan Levkivskyi，PR [15837](https://github.com/python/mypy/pull/15837)）
* 添加 `--new-type-inference` 时失效缓存（Marc Mueller，PR [16059](https://github.com/python/mypy/pull/16059)）

**注意：** 我们计划在 mypy 1.7 中默认启用 `--new-type-inference`。请尝试并告知我们您是否遇到任何问题。

### ParamSpec 的改进

* 支持包含 ParamSpec 的 self-types（Ivan Levkivskyi，PR [15903](https://github.com/python/mypy/pull/15903)）
* 允许在 Concatenate 中使用 “…” 并清理 ParamSpec 字面量（Ivan Levkivskyi，PR [15905](https://github.com/python/mypy/pull/15905)）
* 修复回调协议中的 ParamSpec 推断（Ivan Levkivskyi，PR [15986](https://github.com/python/mypy/pull/15986)）
* 从参数推断 ParamSpec 约束（Ivan Levkivskyi，PR [15896](https://github.com/python/mypy/pull/15896)）
* 修复 ParamSpec 的无效类型变量导致的崩溃（Ivan Levkivskyi，PR [15953](https://github.com/python/mypy/pull/15953)）
* 修复 ParamSpecs 之间的子类型关系（Ivan Levkivskyi，PR [15892](https://github.com/python/mypy/pull/15892)）

### Stubgen 的改进

* 添加选项以在 stubgen 中包含文档字符串（chylek，PR [13284](https://github.com/python/mypy/pull/13284)）
* 为具有默认值的 NamedTuple 字段添加所需的 `...` 初始化器（Nikita Sobolev，PR [15680](https://github.com/python/mypy/pull/15680)）

### Stubtest 的改进

* 修复 `__mypy-replace` 误报（Alex Waygood，PR [15689](https://github.com/python/mypy/pull/15689)）
* 修复字节枚举子类的边缘案例（Alex Waygood，PR [15943](https://github.com/python/mypy/pull/15943)）
* 如果 typeshed 缺少标准库模块，则生成错误（Alex Waygood，PR [15729](https://github.com/python/mypy/pull/15729)）
* 修复缺失标准库模块的新检查（Alex Waygood，PR [15960](https://github.com/python/mypy/pull/15960)）
* 修复 stubtest 中的 enum.Flag 边缘案例（Alex Waygood，PR [15933](https://github.com/python/mypy/pull/15933)）

### 文档的改进

* 不再建议创建自己的 `assert_never` 辅助函数（Nikita Sobolev，PR [15947](https://github.com/python/mypy/pull/15947)）
* 修复文档中所有缺失的引用（Albert Tugushev，PR [15875](https://github.com/python/mypy/pull/15875)）
* 记录 `await-not-async` 错误代码（Shantanu，PR [15858](https://github.com/python/mypy/pull/15858)）
* 改进禁用错误代码的文档（Shantanu，PR [15841](https://github.com/python/mypy/pull/15841)）

### 其他显著变化和修复

* 对不支持的 PEP 695 特性（引入于 Python 3.12）提供合理的错误消息（Shantanu，PR [16013](https://github.com/python/mypy/pull/16013)）
* 移除 `--py2` 命令行参数（Marc Mueller，PR [15670](https://github.com/python/mypy/pull/15670)）
* 将错误消息中的空元组从 `tuple[]` 更改为 `tuple[()]`（Nikita Sobolev，PR [15783](https://github.com/python/mypy/pull/15783)）
* 修复某些节点延迟时的 `assert_type` 失败（Nikita Sobolev，PR [15920](https://github.com/python/mypy/pull/15920)）
* 在未绑定的 TypeVar 有值时生成错误（Nikita Sobolev，PR [15732](https://github.com/python/mypy/pull/15732)）
* 修复对 `types-google-cloud-ndb` 的过度建议（Shantanu，PR [15347](https://github.com/python/mypy/pull/15347)）
* 修复对 `== None` 和 `in (None,)` 条件的类型缩小（Marti Raudsepp，PR [15760](https://github.com/python/mypy/pull/15760)）
* 修复 `attrs.fields` 的推断（Shantanu，PR [15688](https://github.com/python/mypy/pull/15688)）
* 将“在非异步函数中等待”设为非阻塞错误并给予错误代码（Gregory Santosa，PR [15384](https://github.com/python/mypy/pull/15384)）
* 添加对装饰重载的基本支持（Ivan Levkivskyi，PR [15898](https://github.com/python/mypy/pull/15898)）
* 修复与 self types 相关的 TypeVar 回归（Ivan Levkivskyi，PR [15945](https://github.com/python/mypy/pull/15945)）
* 为没有字段的 dataclass 添加 `__match_args__`（Ali Hamdan，PR [15749](https://github.com/python/mypy/pull/15749)）
* 在 dmypy 的详细输出中包含 stdout 和 stderr（Valentin Stanciu，PR [15881](https://github.com/python/mypy/pull/15881)）
* 改进匹配缩小和可达性分析（Shantanu，PR [15882](https://github.com/python/mypy/pull/15882)）
* 支持 `__bool__` 与 `Literal` 在 `--warn-unreachable` 中（Jannic Warken，PR [15645](https://github.com/python/mypy/pull/15645)）
* 修复从通用 @frozen attrs 类继承的问题（Ilya Priven，PR [15700](https://github.com/python/mypy/pull/15700)）
* 正确缩小 `tuple[type[X], ...]` 的类型（Nikita Sobolev，PR [15691](https://github.com/python/mypy/pull/15691)）
* 不将故意空的生成器标记为不可达（Ilya Priven，PR [15722](https://github.com/python/mypy/pull/15722)）
* 在 mypy sdist 中添加 tox.ini（Marcel Telka，PR [15853](https://github.com/python/mypy/pull/15853)）
* 修复 mypyc 在 pretty 中的回归（Shantanu，PR [16124](https://github.com/python/mypy/pull/16124)）

### Typeshed 更新

Typeshed 现在是模块化的，除了标准库存根外，其他所有内容都作为独立的 PyPI 包分发。有关 typeshed 变更的完整列表，请参见 [git log](https://github.com/python/typeshed/commits/main?after=6a8d653a671925b0a3af61729ff8cf3f90c9c662+0&branch=main&path=stdlib)。

### 致谢

感谢 Max Murin，他为本次发布做了大部分的发布管理工作（我只是进行了最后的步骤）。

感谢所有对本次发布做出贡献的 mypy 贡献者：

* Albert Tugushev
* Alex Waygood
* Ali Hamdan
* chylek
* EXPLOSION
* Gregory Santosa
* Ilya Priven
* Ivan Levkivskyi
* Jannic Warken
* KotlinIsland
* Marc Mueller
* Marcel Johannesmann
* Marcel Telka
* Mark Byrne
* Marti Raudsepp
* Max Murin
* Nikita Sobolev
* Shantanu
* Valentin Stanciu

由 Jukka Lehtosalo 发布。


### Mypy 1.5

[2023年8月10日](https://mypy-lang.blogspot.com/2023/08/mypy-15-released.html)

我们刚刚将 mypy 1.5 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是 Python 的静态类型检查器。此版本包含新特性、弃用项和 bug 修复。您可以通过以下方式安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 阅读本次发布的完整文档。

### 删除对 Python 3.7 的支持

Mypy 不再支持运行在 Python 3.7 上，因为该版本已达到生命周期结束。这项更改由 Shantanu 提供（PR [15566](https://github.com/python/mypy/pull/15566)）。

### 可选检查以强制要求显式 @override

如果启用 `explicit-override` 错误代码，mypy 将生成错误，如果方法重写没有使用 `@typing.override` 装饰器（如 [PEP 698](https://peps.python.org/pep-0698/#strict-enforcement-per-project）中讨论的那样）。这样，mypy 可以检测到意外引入的重写。例如：

```python
# mypy: enable-error-code="explicit-override"

from typing_extensions import override

class C:
    def foo(self) -> None: pass
    def bar(self) -> None: pass

class D(C):
    # 错误：方法 "foo" 未使用 @override，但正在重写
    def foo(self) -> None:
        ...

    @override
    def bar(self) -> None:  # 正确
        ...
```

您可以通过 `--enable-error-code=explicit-override` 在 mypy 命令行中启用此错误代码，或在 mypy 配置文件中设置 `enable_error_code = explicit-override`。

该装饰器将在 Python 3.12 的 `typing` 中可用，但您也可以在所有支持的 Python 版本中使用最近版本的 `typing_extensions` 的回溯版本。

此功能由 Marc Mueller 提供（PR [15512](https://github.com/python/mypy/pull/15512)）。

### 更灵活的 TypedDict 创建和更新

之前，Mypy 在类型检查 TypedDict 的创建和更新操作时过于严格。尽管这些检查在技术上通常是正确的，但有时会对看似有效的代码触发错误。现在，默认情况下，这些检查已经放宽。您可以通过使用新的 `--extra-checks` 标志启用更严格的检查。

使用 `**` 语法进行构造现在更加灵活：

```python
from typing import TypedDict

class A(TypedDict):
    foo: int
    bar: int

class B(TypedDict):
    foo: int

a: A = {"foo": 1, "bar": 2}
b: B = {"foo": 3}
a2: A = { **a, **b}  # OK（之前会报错）
```

您也可以使用包含更新的 TypedDict 子集的 TypedDict 参数调用 `update()`：

```python
a.update(b)  # OK（之前会报错）
```

此功能由 Ivan Levkivskyi 提供（PR [15425](https://github.com/python/mypy/pull/15425)）。

### 弃用标志：`--strict-concatenate`

`--strict-concatenate` 的行为现在已包含在新的 `--extra-checks` 标志中，旧标志被弃用。

### 可选显示错误代码文档链接

如果您使用 `--show-error-code-links`，mypy 将为（许多）报告的错误添加文档链接。对于足够明显的错误消息，将不会显示链接，每个错误代码只显示一次。

示例输出：
```
a.py:1: error: Need type annotation for "foo" (hint: "x: List[<type>] = ...")  [var-annotated]
a.py:1: note: See https://mypy.rtfd.io/en/stable/_refs.html#code-var-annotated for more info
```
此功能由 Ivan Levkivskyi 提供（PR [15449](https://github.com/python/mypy/pull/15449)）。

### 一致地避免对不可达代码进行类型检查

如果模块顶层有不可达代码，mypy 将不会对不可达语句进行类型检查。这与函数的行为一致。`--warn-unreachable` 的行为现在也更为一致。

此功能由 Ilya Priven 提供（PR [15386](https://github.com/python/mypy/pull/15386)）。

### 实验性改进的泛型函数类型推断

您可以使用 `--new-type-inference` 选择加入一个实验性的新类型推断算法。它特别修复了在调用参数也是泛型函数的泛型函数时出现的问题。当前的实现仍然不完整，但我们鼓励您尝试并报告任何回归问题。我们计划在未来的 mypy 版本中默认启用这个新算法。

此功能由 Ivan Levkivskyi 提供（PR [15287](https://github.com/python/mypy/pull/15287)）。

### 对 Python 3.12 的部分支持

Mypy 和 mypyc 现在支持在最近的 Python 3.12 开发版本上运行。并非所有新特性都被支持，目前还没有为 Python 3.12 提供编译的 wheel 文件。

- 修复 Python 3.12 的 AST 警告（Nikita Sobolev, PR [15558](https://github.com/python/mypy/pull/15558)）
- mypyc：修复 Python 3.12 上协议的多重继承（Jukka Lehtosalo, PR [15572](https://github.com/python/mypy/pull/15572)）
- mypyc：修复 Python 3.12 上的自编译（Jukka Lehtosalo, PR [15582](https://github.com/python/mypy/pull/15582)）
- mypyc：修复 Python 3.12 上带有 `__dict__` 的实例的序列化问题（Jukka Lehtosalo, PR [15574](https://github.com/python/mypy/pull/15574)）
- mypyc：修复 Python 3.12 上的 i16 问题（Jukka Lehtosalo, PR [15510](https://github.com/python/mypy/pull/15510)）
- mypyc：修复 Python 3.12 上的整数运算（Jukka Lehtosalo, PR [15470](https://github.com/python/mypy/pull/15470)）
- mypyc：修复 Python 3.12 上的生成器问题（Jukka Lehtosalo, PR [15472](https://github.com/python/mypy/pull/15472)）
- mypyc：修复 Python 3.12 上带有 `__dict__` 的类的问题（Jukka Lehtosalo, PR [15471](https://github.com/python/mypy/pull/15471)）
- mypyc：修复 Python 3.12 上的协程问题（Jukka Lehtosalo, PR [15469](https://github.com/python/mypy/pull/15469)）
- mypyc：在 Python 3.12 上不再使用 `PyErr_ChainExceptions`，因为它已被弃用（Jukka Lehtosalo, PR [15468](https://github.com/python/mypy/pull/15468)）
- mypyc：添加 Python 3.12 特性宏（Jukka Lehtosalo, PR [15465](https://github.com/python/mypy/pull/15465)）

### 数据类改进

- 改进 `dataclasses.replace` 的签名（Ilya Priven, PR [14849](https://github.com/python/mypy/pull/14849)）
- 修复数据类与协议结合时的崩溃问题（Ilya Priven, PR [15629](https://github.com/python/mypy/pull/15629)）
- 修复数据类中的严格可选项处理（Ivan Levkivskyi, PR [15571](https://github.com/python/mypy/pull/15571)）
- 支持自定义数据类描述符的可选类型（Marc Mueller, PR [15628](https://github.com/python/mypy/pull/15628)）
- 为数据类添加 `__slots__` 属性（Nikita Sobolev, PR [15649](https://github.com/python/mypy/pull/15649)）
- 支持更好的 `__post_init__` 方法签名（Nikita Sobolev, PR [15503](https://github.com/python/mypy/pull/15503)）

### Mypyc 改进

- 支持无符号 8 位原生整数类型：`mypy_extensions.u8`（Jukka Lehtosalo, PR [15564](https://github.com/python/mypy/pull/15564)）
- 支持有符号 16 位原生整数类型：`mypy_extensions.i16`（Jukka Lehtosalo, PR [15464](https://github.com/python/mypy/pull/15464)）
- 在存根中定义 `mypy_extensions.i16`（Jukka Lehtosalo, PR [15562](https://github.com/python/mypy/pull/15562)）
- 记录更多不支持的特性并更新支持的特性（Richard Si, PR [15524](https://github.com/python/mypy/pull/15524)）
- 修复最终命名元组类（Richard Si, PR [15513](https://github.com/python/mypy/pull/15513)）
- 使用 C99 复合字面量处理未定义的元组值（Jukka Lehtosalo, PR [15453](https://github.com/python/mypy/pull/15453)）
- 在设置函数中不显式分配 NULL 值（Logan Hunt, PR [15379](https://github.com/python/mypy/pull/15379)）

### Stubgen 改进

- 教授 stubgen 处理复杂和一元表达式（Nikita Sobolev, PR [15661](https://github.com/python/mypy/pull/15661)）
- 支持 `ParamSpec` 和 `TypeVarTuple`（Ali Hamdan, PR [15626](https://github.com/python/mypy/pull/15626)）
- 修复非字符串文档字符串导致的崩溃（Ali Hamdan, PR [15623](https://github.com/python/mypy/pull/15623)）

### 文档更新

- 添加额外错误代码的文档（Ivan Levkivskyi, PR [15539](https://github.com/python/mypy/pull/15539)）
- 改进类型缩减的文档（Ilya Priven, PR [15652](https://github.com/python/mypy/pull/15652)）
- 对协议文档进行小幅改进（Shantanu, PR [15460](https://github.com/python/mypy/pull/15460)）
- 在速查表中移除令人困惑的实例变量示例（Adel Atallah, PR [15441](https://github.com/python/mypy/pull/15441)）

### 其他显著修复和改进

* 常量折叠额外的单元和二元表达式（Richard Si, PR [15202](https://github.com/python/mypy/pull/15202)）
* 从 Protocol 中排除与 CPython 相同的特殊属性（Kyle Benesch, PR [15490](https://github.com/python/mypy/pull/15490)）
* 将 attrs.define 的 slots 参数的默认值更改为 True，以匹配运行时行为（Ilya Priven, PR [15642](https://github.com/python/mypy/pull/15642)）
* 修复如果属性在类和元类中都定义时的类属性类型（Alex Waygood, PR [14988](https://github.com/python/mypy/pull/14988)）
* 在类方法的第一个参数中将 type 处理为 typing.Type（Erik Kemperman, PR [15297](https://github.com/python/mypy/pull/15297)）
* 修复 --find-occurrences 标志（Shantanu, PR [15528](https://github.com/python/mypy/pull/15528)）
* 修复类模式的错误位置（Nikita Sobolev, PR [15506](https://github.com/python/mypy/pull/15506)）
* 修复在 mypy 守护进程中重新添加带有错误的文件（Ivan Levkivskyi, PR [15440](https://github.com/python/mypy/pull/15440)）
* 修复 Windows 上的 dmypy 运行（Ivan Levkivskyi, PR [15429](https://github.com/python/mypy/pull/15429)）
* 修复属性删除器的抽象和非抽象变体错误（Shantanu, PR [15395](https://github.com/python/mypy/pull/15395)）
* 从错误消息中移除“cannot”的特殊处理（Ilya Priven, PR [15428](https://github.com/python/mypy/pull/15428)）
* 为 attrs 类添加运行时 `__slots__` 属性（Nikita Sobolev, PR [15651](https://github.com/python/mypy/pull/15651)）
* 将 get_expression_type 添加到 CheckerPluginInterface（Ilya Priven, PR [15369](https://github.com/python/mypy/pull/15369)）
* 从 NamedTuple._make() 中移除不再存在的参数（Alex Waygood, PR [15578](https://github.com/python/mypy/pull/15578)）
* 允许在使用显式 @staticmethod 装饰器时在 `__all__` 中使用 typing.Self（Erik Kemperman, PR [15353](https://github.com/python/mypy/pull/15353)）
* 修复没有 Self 注解的子类方法中的自引用类型（Ivan Levkivskyi, PR [15541](https://github.com/python/mypy/pull/15541)）
* 在元组中检查抽象类对象（Nikita Sobolev, PR [15366](https://github.com/python/mypy/pull/15366)）

### Typeshed 更新

Typeshed 现在是模块化的，并作为单独的 PyPI 包分发，除了标准库存根之外。请参见 [git log](https://github.com/python/typeshed/commits/main?after=fc7d4722eaa54803926cee5730e1f784979c0531+0&branch=main&path=stdlib) 了解 Typeshed 变化的完整列表。

### 致谢

感谢所有为本次发布贡献的 mypy 贡献者：

* Adel Atallah
* Alex Waygood
* Ali Hamdan
* Erik Kemperman
* Federico Padua
* Ilya Priven
* Ivan Levkivskyi
* Jelle Zijlstra
* Jared Hance
* Jukka Lehtosalo
* Kyle Benesch
* Logan Hunt
* Marc Mueller
* Nikita Sobolev
* Richard Si
* Shantanu
* Stavros Ntentos
* Valentin Stanciu

由 Valentin Stanciu 发布


## Mypy 1.4

[2023年6月20日](https://mypy-lang.blogspot.com/2023/06/mypy-140-released.html)

我们刚刚将 mypy 1.4 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 的静态类型检查器。此版本包含新特性、性能改进和 bug 修复。您可以通过以下方式安装它：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读此版本的完整文档。

### 重写装饰器

Mypy 现在可以确保在重命名方法时，重写的方法也被重命名。您可以通过使用 `@typing.override` 装饰器（[PEP 698](https://peps.python.org/pep-0698/)）显式标记一个方法为重写基类方法。如果方法在基类中被重命名，而重写的方法没有，mypy 将生成错误。此装饰器将在 Python 3.12 的 typing 中提供，但您也可以在所有受支持的 Python 版本中使用最近版本的 `typing_extensions` 中的回溯版本。

该功能由 Thomas M Kehrenberg 贡献（PR [14609](https://github.com/python/mypy/pull/14609)）。

### 向嵌套函数传播类型收窄

之前，类型收窄不会传播到嵌套函数，因为如果收窄的变量在嵌套函数的定义和调用之间发生变化，则这将不合理。Mypy 现在将在变量在嵌套函数定义后未被赋值的情况下传播收窄的类型：

```python
def outer(x: str | None = None) -> None:
    if x is None:
        x = calculate_default()
    reveal_type(x)  # "str" (收窄)

    def nested() -> None:
        reveal_type(x)  # 现在是 "str"（之前是 "str | None"）

    nested()
```

这可能会生成一些新错误，因为之前必要的断言可能变得是平凡的或无操作的。

该功能由 Jukka Lehtosalo 贡献（PR [15133](https://github.com/python/mypy/pull/15133)）。

### 使用“==”收窄枚举值

Mypy 现在允许使用 `==` 操作符来收窄枚举类型。之前，仅支持使用 `is` 操作符。这使得对枚举类型的穷尽性检查更加可用，因为仅使用 `is` 操作符的要求并不直观。在以下示例中，mypy 可以检测到开发者忘记处理值 `MyEnum.C` 的情况：

```python
from enum import Enum

class MyEnum(Enum):
    A = 0
    B = 1
    C = 2

def example(e: MyEnum) -> str:  # 错误：缺少返回语句
    if e == MyEnum.A:
        return 'x'
    elif e == MyEnum.B:
        return 'y'
```

添加一个额外的 `elif` 分支可以解决该错误：

```python
def example(e: MyEnum) -> str:  # 无错误 -- 所有值均已覆盖
    if e == MyEnum.A:
        return 'x'
    elif e == MyEnum.B:
        return 'y'
    elif e == MyEnum.C:
        return 'z'
```

这一变化可能会导致在使用 `--strict-equality` 时出现测试用例中的误报，比如在断言语句 `assert o.x == SomeEnum.X` 中。例如：

```python
# mypy: strict-equality

from enum import Enum

class MyEnum(Enum):
    A = 0
    B = 1

class C:
    x: MyEnum
    ...

def test_something() -> None:
    c = C(...)
    assert c.x == MyEnum.A
    c.do_something_that_changes_x()
    assert c.x == MyEnum.B  # 错误：非重叠的相等检查
```

可以使用 `# type: ignore[comparison-overlap]` 来忽略这些错误，或者使用临时变量作为解决方法进行断言：

```python
def test_something() -> None:
    ...
    x = c.x
    assert x == MyEnum.A  # 不收窄 c.x
    c.do_something_that_changes_x()
    x = c.x
    assert x == MyEnum.B  # OK
```

该功能由 Shantanu 贡献（PR [11521](https://github.com/python/mypy/pull/11521)）。

### 性能改进

*   加快大联合类型的简化，同时修复递归元组崩溃（Shantanu，PR [15128](https://github.com/python/mypy/pull/15128)）。
*   加快联合子类型的检查（Shantanu，PR [15104](https://github.com/python/mypy/pull/15104)）。
*   在类型检查第三方库代码时，或在忽略错误时不检查大多数函数体（Jukka Lehtosalo，PR [14150](https://github.com/python/mypy/pull/14150)）。

### 插件改进

*   `attrs.evolve`: 支持泛型和联合类型（Ilya Konstantinov，PR [15050](https://github.com/python/mypy/pull/15050)）。
*   修复 ctypes 插件（Alex Waygood）。

### 崩溃修复

*   修复当函数范围递归别名作为上界时的崩溃（Ivan Levkivskyi，PR [15159](https://github.com/python/mypy/pull/15159)）。
*   修复在 `follow_imports_for_stubs` 中的崩溃（Ivan Levkivskyi，PR [15407](https://github.com/python/mypy/pull/15407)）。
*   修复在显式初始化子类中的 `stubtest` 崩溃（Shantanu，PR [15399](https://github.com/python/mypy/pull/15399)）。
*   修复在使用空键索引 `TypedDict` 时的崩溃（Shantanu，PR [15392](https://github.com/python/mypy/pull/15392)）。
*   修复作为属性的 `NamedTuple` 崩溃（Ivan Levkivskyi，PR [15404](https://github.com/python/mypy/pull/15404)）。
*   正确跟踪嵌套函数/类的循环深度（Ivan Levkivskyi，PR [15403](https://github.com/python/mypy/pull/15403)）。
*   修复递归元组连接时的崩溃（Ivan Levkivskyi，PR [15402](https://github.com/python/mypy/pull/15402)）。
*   修复自定义 `ErrorCode` 子类的崩溃（Marc Mueller，PR [15327](https://github.com/python/mypy/pull/15327)）。
*   修复在数据类协议中赋值给 `self` 属性时的崩溃（Ivan Levkivskyi，PR [15157](https://github.com/python/mypy/pull/15157)）。
*   修复在泛型上下文中使用泛型方法体内的 lambda 时的崩溃（Ivan Levkivskyi，PR [15155](https://github.com/python/mypy/pull/15155)）。
*   修复在 `make_simplified_union` 中的递归类型别名崩溃（Ivan Levkivskyi，PR [15216](https://github.com/python/mypy/pull/15216)）。

### 错误消息改进

*   在错误消息中使用小写的内置集合类型，如 `list[...]`，而不是 `List[...]`，当目标是 Python 3.9+ 时（Max Murin，PR [15070](https://github.com/python/mypy/pull/15070)）。
*   当目标是 Python 3.10+ 时，在错误消息中使用 `X | Y` 联合语法（Omar Silva，PR [15102](https://github.com/python/mypy/pull/15102)）。
*   当目标是 Python 3.9+ 时，在错误消息中使用 `type` 而不是 `Type`（Rohit Sanjay，PR [15139](https://github.com/python/mypy/pull/15139)）。
*   在不可达代码中不显示未使用的忽略错误，并使其成为真实错误代码（Ivan Levkivskyi，PR [15164](https://github.com/python/mypy/pull/15164)）。
*   默认不限制显示的错误数量（Rohit Sanjay，PR [15138](https://github.com/python/mypy/pull/15138)）。
*   改进对真实函数的消息（madt2709，PR [15193](https://github.com/python/mypy/pull/15193)）。
*   当类型名称模糊时，输出不同的类型（teresa0605，PR [15184](https://github.com/python/mypy/pull/15184)）。
*   更新关于 `try` 中无效异常类型的消息（AJ Rasmussen，PR [15131](https://github.com/python/mypy/pull/15131)）。
*   如果参数类型因不支持的数字类型而不兼容，添加解释（Jukka Lehtosalo，PR [15137](https://github.com/python/mypy/pull/15137)）。
*   为非可调用类型的“与超类型不兼容的签名”消息添加更多细节（Ilya Priven，PR [15263](https://github.com/python/mypy/pull/15263)）。

### 文档更新

*   在 `dmypy` 文档中添加 `--local-partial-types` 注释（Alan Du，PR [15259](https://github.com/python/mypy/pull/15259)）。
*   更新 Windows 的 `mypy` 开始文档（Valentin Stanciu，PR [15233](https://github.com/python/mypy/pull/15233)）。
*   澄清文档中关于可调用对象的类型对象使用（Viicos，PR [15079](https://github.com/python/mypy/pull/15079)）。
*   澄清 `disallow_untyped_defs` 和 `disallow_incomplete_defs` 之间的区别（Ilya Priven，PR [15247](https://github.com/python/mypy/pull/15247)）。
*   在文档和测试中使用 `attrs` 和 `@attrs.define`（Ilya Priven，PR [15152](https://github.com/python/mypy/pull/15152)）。

### Mypyc 改进

*   修复某些变量在推断可选类型时出现的意外 `TypeError`（Richard Si，PR [15206](https://github.com/python/mypy/pull/15206)）。
*   内联数学字面量（Logan Hunt，PR [15324](https://github.com/python/mypy/pull/15324)）。
*   支持在字典显示中解包映射（Richard Si，PR [15203](https://github.com/python/mypy/pull/15203)）。

### Stubgen 变更

*   不从基类中移除 `Generic`（Ali Hamdan，PR [15316](https://github.com/python/mypy/pull/15316)）。
*   支持 `yield from` 语句（Ali Hamdan，PR [15271](https://github.com/python/mypy/pull/15271)）。
*   修复缺失的 `total` 在 `TypedDict` 类中（Ali Hamdan，PR [15208](https://github.com/python/mypy/pull/15208)）。
*   修复基于调用的 `namedtuple` 被省略在类基中（Ali Hamdan，PR [14680](https://github.com/python/mypy/pull/14680)）。
*   支持 `TypedDict` 替代语法（Ali Hamdan，PR [14682](https://github.com/python/mypy/pull/14682)）。
*   使 `stubgen` 尊重 `MYPY_CACHE_DIR`（Henrik Bäärnhielm，PR [14722](https://github.com/python/mypy/pull/14722)）。
*   修复和简化（Ali Hamdan，PR [15232](https://github.com/python/mypy/pull/15232)）。

### 其他显著修复和改进

*   修复使用 `TypeVar` 值限制时嵌套异步函数的问题（Jukka Lehtosalo，PR [14705](https://github.com/python/mypy/pull/14705)）。
*   始终允许从 lambda 返回 `Any`（Ivan Levkivskyi，PR [15413](https://github.com/python/mypy/pull/15413)）。
*   为 `TypeVar` 默认值添加基础（PEP 696）（Marc Mueller，PR [14872](https://github.com/python/mypy/pull/14872)）。
*   更新语义分析器以支持 `TypeVar` 默认值（PEP 696）（Marc Mueller，PR [14873](https://github.com/python/mypy/pull/14873)）。
*   使字典表达式推断更一致（Ivan Levkivskyi，PR [15174](https://github.com/python/mypy/pull/15174)）。
*   不阻止重复基类（Nikita Sobolev，PR [15367](https://github.com/python/mypy/pull/15367)）。
*   当同时使用 `staticmethod` 和 `classmethod` 装饰器时生成错误（Juhi Chandalia，PR [15118](https://github.com/python/mypy/pull/15118)）。
*   修复字面量的 `assert_type` 行为（Carl Karsten，PR [15123](https://github.com/python/mypy/pull/15123)）。
*   修复匹配主题忽略重新定义的问题（Vincent Vanlaer，PR [15306](https://github.com/python/mypy/pull/15306)）。
*   支持 `__all__.remove`（Shantanu，PR [15279](https://github.com/python/mypy/pull/15279)）。

### Typeshed 更新

Typeshed 现在是模块化的，并作为独立的 PyPI 包进行分发，除了标准库存根。有关 typeshed 变更的完整列表，请参见 [git log](https://github.com/python/typeshed/commits/main?after=877e06ad1cfd9fd9967c0b0340a86d0c23ea89ce+0&branch=main&path=stdlib)。

### 致谢

感谢所有为此次发布贡献的 mypy 贡献者：

*   Adrian Garcia Badaracco
*   AJ Rasmussen
*   Alan Du
*   Alex Waygood
*   Ali Hamdan
*   Carl Karsten
*   dosisod
*   Ethan Smith
*   Gregory Santosa
*   Heather White
*   Henrik Bäärnhielm
*   Ilya Konstantinov
*   Ilya Priven
*   Ivan Levkivskyi
*   Juhi Chandalia
*   Jukka Lehtosalo
*   Logan Hunt
*   madt2709
*   Marc Mueller
*   Max Murin
*   Nikita Sobolev
*   Omar Silva
*   Özgür
*   Richard Si
*   Rohit Sanjay
*   Shantanu
*   teresa0605
*   Thomas M Kehrenberg
*   Tin Tvrtković
*   Tushar Sadhwani
*   Valentin Stanciu
*   Viicos
*   Vincent Vanlaer
*   Wesley Collin Wright
*   William Santosa
*   yaegassy

还要感谢我的雇主 Dropbox 对 mypy 开发的支持。

发布者：Jared Hance


### Mypy 1.3

[2023年5月10日](https://mypy-lang.blogspot.com/2023/05/mypy-13-released.html)

我们刚刚将 mypy 1.3 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 的静态类型检查器。本次发布包括新特性、性能改进和错误修复。您可以通过以下方式安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读此版本的完整文档。

### 性能改进

*   改进联合子类型的性能（Shantanu，PR [15104](https://github.com/python/mypy/pull/15104)）。
*   添加负子类型缓存（Ivan Levkivskyi，PR [14884](https://github.com/python/mypy/pull/14884)）。

### Stub 工具改进

*   Stubtest：检查如果运行时是抽象的，则存根也是抽象的，即使存根是重载的方法（Alex Waygood，PR [14955](https://github.com/python/mypy/pull/14955)）。
*   Stubtest：验证存根方法或属性在运行时是否被 @final 装饰（Alex Waygood，PR [14951](https://github.com/python/mypy/pull/14951)）。
*   Stubtest：修复运行时与 TypedDict 相关的假阳性（Alex Waygood，PR [14984](https://github.com/python/mypy/pull/14984)）。
*   Stubgen：支持 @functools.cached_property（Nikita Sobolev，PR [14981](https://github.com/python/mypy/pull/14981)）。
*   对 stubgenc 的改进（Chad Dombrova，PR [14564](https://github.com/python/mypy/pull/14564)）。

### attrs 改进

*   为泛型 attrs 类添加对 TypeVars 转换器的支持（Chad Dombrova，PR [14908](https://github.com/python/mypy/pull/14908)）。
*   修复在绑定的 TypeVar 上的 attrs.evolve（Ilya Konstantinov，PR [15022](https://github.com/python/mypy/pull/15022)）。

### 文档更新

*   改进异步文档（Shantanu，PR [14973](https://github.com/python/mypy/pull/14973)）。
*   对备忘单进行改进（Shantanu，PR [14972](https://github.com/python/mypy/pull/14972)）。
*   添加字节格式错误代码的文档（Shantanu，PR [14971](https://github.com/python/mypy/pull/14971)）。
*   将不安全链接转换为 HTTPS（Marti Raudsepp，PR [14974](https://github.com/python/mypy/pull/14974)）。
*   在异步迭代器文档中也提到重载（Shantanu，PR [14998](https://github.com/python/mypy/pull/14998)）。
*   stubtest：改善允许列表文档（Shantanu，PR [15008](https://github.com/python/mypy/pull/15008)）。
*   澄清“使用类型...但不在运行时”（Jon Shea，PR [15029](https://github.com/python/mypy/pull/15029)）。
*   修复备忘单示例的对齐（Ondřej Cvacho，PR [15039](https://github.com/python/mypy/pull/15039)）。
*   修复回调协议与可调用类型对象匹配的错误（Shantanu，PR [15042](https://github.com/python/mypy/pull/15042)）。

### 错误报告改进

*   改进字节格式错误（Shantanu，PR [14959](https://github.com/python/mypy/pull/14959)）。

### Mypyc 改进

*   修复布尔值和整数的联合（Tomer Chachamu，PR [15066](https://github.com/python/mypy/pull/15066)）。

### 其他修复和改进

*   修复使用 isinstance 时的 Self 包含的联合类型缩小（Christoph Tyralla，PR [14923](https://github.com/python/mypy/pull/14923)）。
*   允许匹配 SupportsKeysAndGetItem 的对象被解包（Bryan Forbes，PR [14990](https://github.com/python/mypy/pull/14990)）。
*   检查静态方法的类型保护有效性（EXPLOSION，PR [14953](https://github.com/python/mypy/pull/14953)）。
*   修复使用 emscripten 交叉编译时的 sys.platform（Ethan Smith，PR [14888](https://github.com/python/mypy/pull/14888)）。

### Typeshed 更新

Typeshed 现在是模块化的，并作为独立的 PyPI 包进行分发，除了标准库存根。有关 typeshed 变更的完整列表，请参见 [git log](https://github.com/python/typeshed/commits/main?after=b0ed50e9392a23e52445b630a808153e0e256976+0&branch=main&path=stdlib)。

### 感谢名单

感谢所有为本次发布做出贡献的 mypy 贡献者：

*   Alex Waygood
*   Amin Alaee
*   Bryan Forbes
*   Chad Dombrova
*   Charlie Denton
*   Christoph Tyralla
*   dosisod
*   Ethan Smith
*   EXPLOSION
*   Ilya Konstantinov
*   Ivan Levkivskyi
*   Jon Shea
*   Jukka Lehtosalo
*   KotlinIsland
*   Marti Raudsepp
*   Nikita Sobolev
*   Ondřej Cvacho
*   Shantanu
*   sobolevn
*   Tomer Chachamu
*   Yaroslav Halchenko

发布者：Wesley Collin Wright。

---

## Mypy 1.2

[2023年4月6日](https://mypy-lang.blogspot.com/2023/04/mypy-12-released.html)

我们刚刚将 mypy 1.2 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 的静态类型检查器。本次发布包括新特性、性能改进和错误修复。您可以通过以下方式安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读此版本的完整文档。

### 数据类转换的改进

*   支持字段说明符中“init”参数的隐式默认值（Wesley Collin Wright 和 Jukka Lehtosalo，PR [15010](https://github.com/python/mypy/pull/15010)）。
*   支持数据类转换中的描述符（Jukka Lehtosalo，PR [15006](https://github.com/python/mypy/pull/15006)）。
*   修复增量模式中的 frozen_default（Wesley Collin Wright）。
*   修复具有直接元类的基类的冻结行为（Wesley Collin Wright，PR [14878](https://github.com/python/mypy/pull/14878)）。

### Mypyc：原生浮点数

Mypyc 现在为 float 类型的值使用原生、未包装的表示。以前，这些值是堆分配的 Python 对象。原生浮点数速度更快且占用更少的内存。使用浮点运算的代码在使用原生浮点数时可以快几倍。

各种浮点操作和数学函数现在也有优化的实现。有关完整列表，请参阅 [文档](https://mypyc.readthedocs.io/en/latest/float_operations.html)。

这可能会改变现有使用 float 子类的代码的行为。当将 float 子类的实例赋值给 float 类型的变量时，它会在编译时隐式转换为 float 实例：

```python
from lib import MyFloat  # MyFloat 是 float 的子类

def example() -> None:
    x = MyFloat(1.5)
    y: float = x  # 从 MyFloat 到 float 的隐式转换
    print(type(y))  # float，而不是 MyFloat
```

以前，隐式转换适用于 int 子类，但不适用于 float 子类。

此外，int 值不能再赋值给 float 类型的变量，因为这些类型现在具有不兼容的表示。需要显式转换：

```python
def example(n: int) -> None:
    a: float = 1  # 错误：不能将 "int" 赋值给 "float"
    b: float = 1.0  # 正确
    c: float = n  # 错误
    d: float = float(n)  # 正确
```

此限制仅适用于赋值，因为否则它们可能会将变量的类型从 float 缩小到 int。int 值在作为期望 float 值的函数的参数传递时仍可以隐式转换为 float。

请注意，mypy 仍然不支持未包装浮点值的数组。使用 list\[float\] 涉及堆分配的浮点对象，因为列表只能存储包装值。对高效浮点数组的支持是下一个主要计划的 mypyc 特性之一。

相关更改：

*   使用原生未包装的表示法来表示浮点数（Jukka Lehtosalo，PR [14880](https://github.com/python/mypy/pull/14880)）。
*   文档中关于原生浮点数和整数的说明（Jukka Lehtosalo，PR [14927](https://github.com/python/mypy/pull/14927)）。
*   修复浮点数到整数的转换（Jukka Lehtosalo，PR [14936](https://github.com/python/mypy/pull/14936)）。

### Mypyc：原生整数

Mypyc 现在支持带符号的 32 位和 64 位整数类型，除了任意精度的 int 类型。您可以使用 mypy_extensions.i32 和 mypy_extensions.i64 来加速大量使用整数运算的代码。

简单示例：
```python
from mypy_extensions import i64

def inc(x: i64) -> i64:
    return x + 1
```
有关更多信息，请参考 [文档](https://mypyc.readthedocs.io/en/latest/using_type_annotations.html#native-integer-types)。此功能由 Jukka Lehtosalo 提供。

### 其他 Mypyc 修复和改进

*   支持对 TypedDict 进行迭代（Richard Si，PR [14747](https://github.com/python/mypy/pull/14747)）
*   不同元组类型之间的更快强制转换（Jukka Lehtosalo，PR [14899](https://github.com/python/mypy/pull/14899)）
*   通过类型别名进行更快调用（Jukka Lehtosalo，PR [14784](https://github.com/python/mypy/pull/14784)）
*   通过 cls 进行更快的类方法调用（Jukka Lehtosalo，PR [14789](https://github.com/python/mypy/pull/14789)）

### 崩溃修复

*   修复协议定义中的类级导入崩溃（Ivan Levkivskyi，PR [14926](https://github.com/python/mypy/pull/14926)）
*   修复单项联合别名的崩溃（Ivan Levkivskyi，PR [14876](https://github.com/python/mypy/pull/14876)）
*   修复增量模式下的 ParamSpec 崩溃（Ivan Levkivskyi，PR [14885](https://github.com/python/mypy/pull/14885)）

### 文档更新

*   更新 1.0 版本的 --strict 文档（Shantanu，PR [14865](https://github.com/python/mypy/pull/14865)）
*   一些小的文档调整（Jukka Lehtosalo，PR [14847](https://github.com/python/mypy/pull/14847)）
*   改善 mypy 顶层的 disable-error-code 注释文档（Nikita Sobolev，PR [14810](https://github.com/python/mypy/pull/14810)）

### 错误报告改进

*   向 `typing_extensions` 建议添加错误代码（Shantanu，PR [14881](https://github.com/python/mypy/pull/14881)）
*   为顶级 await 添加单独的错误代码（Nikita Sobolev，PR [14801](https://github.com/python/mypy/pull/14801)）
*   不建议两个过时的存根包（Jelle Zijlstra，PR [14842](https://github.com/python/mypy/pull/14842)）
*   为 pandas-stubs 和 lxml-stubs 添加建议（Shantanu，PR [14737](https://github.com/python/mypy/pull/14737)）

### 其他修复和改进

*   多重继承将可调用对象视为函数的子类型（Christoph Tyralla，PR [14855](https://github.com/python/mypy/pull/14855)）
*   stubtest：尊重 @final 运行时装饰器并在存根中强制执行（Nikita Sobolev，PR [14922](https://github.com/python/mypy/pull/14922)）
*   修复与 type\[<type-var>\] 相关的误报（sterliakov，PR [14756](https://github.com/python/mypy/pull/14756)）
*   修复 ParamSpec 前缀的重复，并正确替换 ParamSpecs（EXPLOSION，PR [14677](https://github.com/python/mypy/pull/14677)）
*   修复 `__iter__` 错误报告为缺失的行号（Jukka Lehtosalo，PR [14893](https://github.com/python/mypy/pull/14893)）
*   修复重载泛型的不可兼容重写（Shantanu，PR [14882](https://github.com/python/mypy/pull/14882)）
*   允许在切片表达式中使用 SupportsIndex（Shantanu，PR [14738](https://github.com/python/mypy/pull/14738)）
*   支持在使用 dataclass_transform 的数据类和类的主体中使用 if 语句（Jacek Chałupka，PR [14854](https://github.com/python/mypy/pull/14854)）
*   允许可迭代类对象被解包（包括枚举）（Alex Waygood，PR [14827](https://github.com/python/mypy/pull/14827)）
*   修复在 match 语句中使用海象表达式的缩小（Shantanu，PR [14844](https://github.com/python/mypy/pull/14844)）
*   为 attr.evolve 添加签名（Ilya Konstantinov，PR [14526](https://github.com/python/mypy/pull/14526)）
*   修复解包迭代器时的 Any 推断（Alex Waygood，PR [14821](https://github.com/python/mypy/pull/14821)）
*   修复重载 `__iter__` 方法的解包（Nikita Sobolev，PR [14817](https://github.com/python/mypy/pull/14817)）
*   减小 mypy 缓存中的 JSON 数据大小（dosisod，PR [14808](https://github.com/python/mypy/pull/14808)）
*   改进本地定义与全局定义同名时的“在定义之前使用”检查（Stas Ilinskiy，PR [14517](https://github.com/python/mypy/pull/14517)）
*   尊重 NoReturn 作为 __setitem__ 返回类型以标记不可达代码（sterliakov，PR [12572](https://github.com/python/mypy/pull/12572)）

### Typeshed 更新

Typeshed 现在是模块化的，除了标准库存根外，其余部分作为单独的 PyPI 包分发。有关 Typeshed 更改的完整列表，请参见 [git log](https://github.com/python/typeshed/commits/main?after=a544b75320e97424d2d927605316383c755cdac0+0&branch=main&path=stdlib)。

### 感谢名单

感谢所有为本次发布做出贡献的 mypy 贡献者：

*   Alex Waygood
*   Avasam
*   Christoph Tyralla
*   dosisod
*   EXPLOSION
*   Ilya Konstantinov
*   Ivan Levkivskyi
*   Jacek Chałupka
*   Jelle Zijlstra
*   Jukka Lehtosalo
*   Marc Mueller
*   Max Murin
*   Nikita Sobolev
*   Richard Si
*   Shantanu
*   Stas Ilinskiy
*   sterliakov
*   Wesley Collin Wright

发布者：Jukka Lehtosalo。


## Mypy 1.1.1

[2023年3月6日](https://mypy-lang.blogspot.com/2023/03/mypy-111-released.html)

我们刚刚将 mypy 1.1.1 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 静态类型检查器。本次发布包含新特性、性能改进和错误修复。您可以使用以下命令安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读本次发布的完整文档。

### 对 `dataclass_transform` 的支持

此次发布新增对在 [PEP 681](https://peps.python.org/pep-0681/#decorator-function-example) 中定义的 `dataclass_transform` 装饰器的全面支持。该功能允许生成 `__init__` 方法或其他方法的装饰器、基类和 metaclasses 基于类的属性（类似于数据类），以便 mypy 能够识别这些方法。此功能由 Wesley Collin Wright 提供。

### 方法分配的专用错误代码

由于 mypy 无法安全检查所有对方法的分配（即猴子补丁），因此默认情况下 mypy 会生成错误。为了更容易忽略该错误，mypy 现在使用新错误代码 `method-assign`。通过在文件中或全局禁用此错误代码，如果签名兼容，mypy 将不再对方法的分配发出警告。mypy 还支持旧的错误代码 `assignment`，以防止向后兼容性中断。此功能由 Ivan Levkivskyi 提供（PR [14570](https://github.com/python/mypy/pull/14570)）。

### 崩溃修复

*   修复类作用域中 comprehension 的海象运算符崩溃（Ivan Levkivskyi，PR [14556](https://github.com/python/mypy/pull/14556)）
*   修复与值约束 TypeVar 相关的崩溃（Shantanu，PR [14642](https://github.com/python/mypy/pull/14642)）

### 缓存损坏修复

*   修复泛型 TypedDict/NamedTuple 缓存（Ivan Levkivskyi，PR [14675](https://github.com/python/mypy/pull/14675)）

### Mypyc 修复和改进

*   减少“非特征基类必须优先…”错误的频率（Richard Si，PR [14468](https://github.com/python/mypy/pull/14468)）
*   为布尔比较和算术生成更快的代码（Jukka Lehtosalo，PR [14489](https://github.com/python/mypy/pull/14489)）
*   优化原生类的 `__enter__/__exit__`（Jared Hance，PR [14530](https://github.com/python/mypy/pull/14530)）
*   检测属性定义是否与基类/特征冲突（Jukka Lehtosalo，PR [14535](https://github.com/python/mypy/pull/14535)）
*   支持 `__divmod__` 和 `__rdivmod__` 魔法方法（Richard Si，PR [14613](https://github.com/python/mypy/pull/14613)）
*   支持 `__pow__`, `__rpow__`, 和 `__ipow__` 魔法方法（Richard Si，PR [14616](https://github.com/python/mypy/pull/14616)）
*   修复解包到下划线的崩溃（Ivan Levkivskyi，PR [14624](https://github.com/python/mypy/pull/14624)）
*   修复对字典联合的迭代（Richard Si，PR [14713](https://github.com/python/mypy/pull/14713)）

### 修复检测未定义名称（使用前定义）

*   正确处理海象运算符（Stas Ilinskiy，PR [14646](https://github.com/python/mypy/pull/14646)）
*   正确处理匹配主体中的海象声明（Stas Ilinskiy，PR [14665](https://github.com/python/mypy/pull/14665)）

### Stubgen 改进

Stubgen 是一个用于自动生成库草稿存根的工具。

*   允许在顶层以下使用别名（Chad Dombrova，PR [14388](https://github.com/python/mypy/pull/14388)）
*   修复 PEP 604 联合中的崩溃（Shantanu，PR [14557](https://github.com/python/mypy/pull/14557)）
*   在生成的 .pyi 文件中保留 PEP 604 联合（hamdanal，PR [14601](https://github.com/python/mypy/pull/14601)）

### Stubtest 改进

Stubtest 是一个用于测试存根是否符合实现的工具。

*   更新消息格式，使其更易于定位错误位置（Avasam，PR [14437](https://github.com/python/mypy/pull/14437)）
*   更好地处理名称改编边缘情况（Alex Waygood，PR [14596](https://github.com/python/mypy/pull/14596)）

### 错误报告和消息的变化

*   添加新的 TypedDict 错误代码 `typeddict-unknown-key`（JoaquimEsteves，PR [14225](https://github.com/python/mypy/pull/14225)）
*   在错误消息中为参数提供更合理的位置（Max Murin，PR [14562](https://github.com/python/mypy/pull/14562)）
*   在错误消息中，仅引用模块的名称（Ilya Konstantinov，PR [14567](https://github.com/python/mypy/pull/14567)）
*   改善关于 `Enum()` 的误导性消息（Rodrigo Silva，PR [14590](https://github.com/python/mypy/pull/14590)）
*   如果定义不在 typing 中，建议从 `typing_extensions` 导入（Shantanu，PR [14591](https://github.com/python/mypy/pull/14591)）
*   一致使用 type-abstract 错误代码（Ivan Levkivskyi，PR [14619](https://github.com/python/mypy/pull/14619)）
*   一致使用 TypedDict 的 literal-required 错误代码（Ivan Levkivskyi，PR [14621](https://github.com/python/mypy/pull/14621)）
*   调整不一致的数据类插件错误消息（Wesley Collin Wright，PR [14637](https://github.com/python/mypy/pull/14637)）
*   整合布尔字面值参数的错误消息（Wesley Collin Wright，PR [14693](https://github.com/python/mypy/pull/14693)）

### 其他修复和改进

*   检查类型保护是否接受位置参数（EXPLOSION，PR [14238](https://github.com/python/mypy/pull/14238)）
*   修复在 Container 和 Iterable 的联合上使用 in 运算符的错误（Max Murin，PR [14384](https://github.com/python/mypy/pull/14384)）
*   通过 metaclass 支持类型\[T\] 的协议推断（Ivan Levkivskyi，PR [14554](https://github.com/python/mypy/pull/14554)）
*   允许对字节类类型进行重叠比较（Shantanu，PR [14658](https://github.com/python/mypy/pull/14658)）
*   修复 README 中的 mypy 守护进程文档链接（Ivan Levkivskyi，PR [14644](https://github.com/python/mypy/pull/14644)）

### Typeshed 更新

Typeshed 现在是模块化的，并作为单独的 PyPI 包分发，除了标准库存根。请查看 [git log](https://github.com/python/typeshed/commits/main?after=5ebf892d0710a6e87925b8d138dfa597e7bb11cc+0&branch=main&path=stdlib) 获取 Typeshed 更改的完整列表。

### 鸣谢

感谢所有为本次发布贡献的 mypy 开发者：

*   Alex Waygood
*   Avasam
*   Chad Dombrova
*   dosisod
*   EXPLOSION
*   hamdanal
*   Ilya Konstantinov
*   Ivan Levkivskyi
*   Jared Hance
*   JoaquimEsteves
*   Jukka Lehtosalo
*   Marc Mueller
*   Max Murin
*   Michael Lee
*   Michael R. Crusoe
*   Richard Si
*   Rodrigo Silva
*   Shantanu
*   Stas Ilinskiy
*   Wesley Collin Wright
*   Yilei "Dolee" Yang
*   Yurii Karabas

我们还要感谢我们的雇主 Dropbox，为 mypy 核心团队提供资金支持。

发布者：Max Murin

---

## Mypy 1.0

[2023年2月6日](https://mypy-lang.blogspot.com/2023/02/mypy-10-released.html)

我们刚刚将 mypy 1.0 上传到 Python 包索引（[PyPI](https://pypi.org/project/mypy/)）。Mypy 是一个 Python 静态类型检查器。本次发布包含新特性、性能改进和错误修复。您可以使用以下命令安装：

```bash
python3 -m pip install -U mypy
```

您可以在 [Read the Docs](http://mypy.readthedocs.io) 上阅读本次发布的完整文档。

### 新的发布版本方案

现在 mypy 达到 1.0，我们将切换到新的版本方案。Mypy 的版本号将采用 x.y.z 形式。

规则：

*   如果特性发布包含显著的向后不兼容更改，且影响大量用户，则主版本号（x）递增。
*   每个特性发布都递增次版本号（y）。次版本发布包括来自 Typeshed 的标准库存根更新。
*   仅在有修复时递增点版本号（z）。

Mypy 不使用 SemVer，因为大多数次版本发布至少具有 Typeshed 中的轻微向后不兼容更改。此外，许多类型检查特性会在代码中发现新的合法问题。这些不会被视为向后不兼容的更改，除非新错误的数量非常高。

任何显著的向后不兼容更改必须在前一次特性发布的博客文章中宣布，才能进行更改。前一个版本还必须提供一个标志以显式启用或禁用新行为（在可行的情况下），以便用户能够为更改做准备并报告问题。我们应在切换默认设置后至少保留该特性标志几个版本。

有关版本方案的详细信息和最新版本，请参见 [mypy wiki 中的“发布过程”](https://github.com/python/mypy/wiki/Release-Process)。

### 性能改进

Mypy 1.0 比 mypy 0.991 在 Dropbox 内部代码库的类型检查速度提高了多达 40%。我们还建立了一个每日作业来测量最新开发版本的性能，方便跟踪性能变化。

许多优化推动了这一改进：

*   提高在具有多个属性的类上的错误性能（Shantanu，PR [14379](https://github.com/python/mypy/pull/14379)）
*   加速 make\_simplified\_union（Jukka Lehtosalo，PR [14370](https://github.com/python/mypy/pull/14370)）
*   微优化 get\_proper\_type(s)（Jukka Lehtosalo，PR [14369](https://github.com/python/mypy/pull/14369)）
*   微优化 flatten\_nested\_unions（Jukka Lehtosalo，PR [14368](https://github.com/python/mypy/pull/14368)）
*   一些语义分析器的微优化（Jukka Lehtosalo，PR [14367](https://github.com/python/mypy/pull/14367)）
*   其他微优化（Jukka Lehtosalo，PR [14366](https://github.com/python/mypy/pull/14366)）
*   优化：避免语义分析器中对上下文管理器的几次使用（Jukka Lehtosalo，PR [14360](https://github.com/python/mypy/pull/14360)）
*   优化：在类型子类中启用始终定义的属性（Jukka Lehtosalo，PR [14356](https://github.com/python/mypy/pull/14356)）
*   优化：移除类型分析器中的昂贵上下文管理器（Jukka Lehtosalo，PR [14357](https://github.com/python/mypy/pull/14357)）
*   子类型：Union/Union 子类型检查的快速路径（Hugues，PR [14277](https://github.com/python/mypy/pull/14277)）
*   微优化：避免导致不必要装箱的 Bogus\[int\] 类型（Jukka Lehtosalo，PR [14354](https://github.com/python/mypy/pull/14354)）
*   避免在未向用户显示错误时执行缓慢的错误消息逻辑（Jukka Lehtosalo，PR [14336](https://github.com/python/mypy/pull/14336)）
*   加速 hasattr() 检查的实现（Jukka Lehtosalo，PR [14333](https://github.com/python/mypy/pull/14333)）
*   避免在热代码路径中使用上下文管理器（Jukka Lehtosalo，PR [14331](https://github.com/python/mypy/pull/14331)）
*   将各种类型查询更改为更快的布尔类型查询（Jukka Lehtosalo，PR [14330](https://github.com/python/mypy/pull/14330)）
*   加速递归类型检查（Jukka Lehtosalo，PR [14326](https://github.com/python/mypy/pull/14326)）
*   通过避免嵌套函数优化子类型检查（Jukka Lehtosalo，PR [14325](https://github.com/python/mypy/pull/14325)）
*   优化子类型检查中的类型参数检查（Jukka Lehtosalo，PR [14324](https://github.com/python/mypy/pull/14324)）
*   加速刷新类型变量（Jukka Lehtosalo，PR [14323](https://github.com/python/mypy/pull/14323)）
*   为 \*\*kwds 优化 TypedDict 类型的实现（Jukka Lehtosalo，PR [14316](https://github.com/python/mypy/pull/14316)）

### 提醒使用未定义的变量

如果在定义之前使用变量，Mypy 现在将生成错误。此功能默认启用。例如：

```python
y = x  # E: Name "x" is used before definition [used-before-def]
x = 0
```

此功能由 Stas Ilinskiy 贡献。

### 检测可能未定义的变量（实验性）

现在提供一个新的实验性可能未定义错误代码，可以检测可能未定义的变量：

```python
if b:
    x = 0
print(x)  # Error: Name "x" may be undefined [possibly-undefined]
```

该错误代码默认禁用，因为它可能产生误报。此功能由 Stas Ilinskiy 贡献。

### 支持 “Self” 类型

现在有一种更简单的语法来声明 [泛型自类型](https://mypy.readthedocs.io/en/stable/generics.html#generic-methods-and-generic-self)，该类型在 [PEP 673](https://peps.python.org/pep-0673/) 中引入。您不再需要定义类型变量来使用“自类型”，并且可以将其与属性一起使用。以下是 mypy 文档中的示例：

```python
from typing import Self

class Friend:
    other: Self | None = None

    @classmethod
    def make_pair(cls) -> tuple[Self, Self]:
        a, b = cls(), cls()
        a.other = b
        b.other = a
        return a, b

class SuperFriend(Friend):
    pass

# a 和 b 的推断类型为 "SuperFriend"，而不是 "Friend"
a, b = SuperFriend.make_pair()
```

此功能在 Python 3.11 中引入。在早期的 Python 版本中，可以在 `typing_extensions` 中使用 Self 的回溯版本。

此功能由 Ivan Levkivskyi 贡献（PR [14041](https://github.com/python/mypy/pull/14041)）。

### 支持在类型别名中使用 ParamSpec

现在可以在类型别名中使用 ParamSpec 和 Concatenate。示例：
```python
from typing import ParamSpec, Callable

P = ParamSpec("P")
A = Callable[P, None]

def f(c: A[int, str]) -> None:
    c(1, "x")
```
此功能由 Ivan Levkivskyi 贡献（PR [14159](https://github.com/python/mypy/pull/14159)）。

### ParamSpec 和泛型自类型不再是实验性

对 ParamSpec（[PEP 612](https://www.python.org/dev/peps/pep-0612/)）和泛型自类型的支持不再被视为实验性。

### 其他新功能

*   数据类转换的最小部分实现（[PEP 681](https://peps.python.org/pep-0681/)）（Wesley Collin Wright，PR [14523](https://github.com/python/mypy/pull/14523)）
*   添加对 `typing_extensions.TypeVar` 的基本支持（Marc Mueller，PR [14313](https://github.com/python/mypy/pull/14313)）
*   添加 `--debug-serialize` 选项（Marc Mueller，PR [14155](https://github.com/python/mypy/pull/14155)）
*   常量折叠最终变量的初始化（Jukka Lehtosalo，PR [14283](https://github.com/python/mypy/pull/14283)）
*   启用 attrs 的 Final 实例属性（Tin Tvrtković，PR [14232](https://github.com/python/mypy/pull/14232)）
*   允许函数参数作为基类（Ivan Levkivskyi，PR [14135](https://github.com/python/mypy/pull/14135)）
*   允许与混合协议一起使用 super()（Ivan Levkivskyi，PR [14082](https://github.com/python/mypy/pull/14082)）
*   添加 dict.keys 会员的类型推断（Matthew Hughes，PR [13372](https://github.com/python/mypy/pull/13372)）
*   如果属性使用 `__slots__` 定义，则为类属性访问生成错误（Harrison McCarty，PR [14125](https://github.com/python/mypy/pull/14125)）
*   支持回调协议中的其他属性（Ivan Levkivskyi，PR [14084](https://github.com/python/mypy/pull/14084)）

### 修复崩溃问题

*   修复使用前向引用的前缀 ParamSpec 崩溃（Ivan Levkivskyi，PR [14569](https://github.com/python/mypy/pull/14569)）
*   修复在解析相同的部分类型两次时的内部崩溃（Shantanu，PR [14552](https://github.com/python/mypy/pull/14552)）
*   修复在新导入循环中的守护进程模式崩溃（Ivan Levkivskyi，PR [14508](https://github.com/python/mypy/pull/14508)）
*   修复 mypy 守护进程崩溃（Ivan Levkivskyi，PR [14497](https://github.com/python/mypy/pull/14497)）
*   修复增量模式下 Any 元类的崩溃（Ivan Levkivskyi，PR [14495](https://github.com/python/mypy/pull/14495)）
*   修复在函数外的推导中使用 await 的崩溃（Ivan Levkivskyi，PR [14486](https://github.com/python/mypy/pull/14486)）
*   修复在上界的前向引用中使用 Self 类型的崩溃（Ivan Levkivskyi，PR [14206](https://github.com/python/mypy/pull/14206)）
*   修复在方法外使用不正确的 super() 时的崩溃（Ivan Levkivskyi，PR [14208](https://github.com/python/mypy/pull/14208)）
*   修复使用冻结 attrs 时的覆盖崩溃（Ivan Levkivskyi，PR [14186](https://github.com/python/mypy/pull/14186)）
*   修复在嵌套位置出现泛型函数时的增量模式崩溃（Ivan Levkivskyi，PR [14148](https://github.com/python/mypy/pull/14148)）
*   修复格式错误的 NamedTuple 导致的守护进程崩溃（Ivan Levkivskyi，PR [14119](https://github.com/python/mypy/pull/14119)）
*   修复 ParamSpec 推导中的崩溃（Ivan Levkivskyi，PR [14118](https://github.com/python/mypy/pull/14118)）
*   修复嵌套泛型可调用对象的崩溃（Ivan Levkivskyi，PR [14093](https://github.com/python/mypy/pull/14093)）
*   修复解包语法错误引发的崩溃（Shantanu，PR [11499](https://github.com/python/mypy/pull/11499)）
*   修复在 lambda 内部进行部分类型推导时的崩溃（Ivan Levkivskyi，PR [14087](https://github.com/python/mypy/pull/14087)）
*   修复与枚举的崩溃（Michael Lee，PR [14021](https://github.com/python/mypy/pull/14021)）
*   修复格式错误的 TypedDict 和 disallow-any-expr 的崩溃（Michael Lee，PR [13963](https://github.com/python/mypy/pull/13963)）

### 错误报告改进

*   对缺少 self 的错误提供更有帮助的信息（Shantanu，PR [14386](https://github.com/python/mypy/pull/14386)）
*   添加错误代码 truthy-iterable（Marc Mueller，PR [13762](https://github.com/python/mypy/pull/13762)）
*   修复错误消息中的复数形式（KotlinIsland，PR [14411](https://github.com/python/mypy/pull/14411)）

### Mypyc：支持 match 语句

Mypyc 现在可以编译 Python 3.10 的 match 语句。

此功能由 dosisod 贡献（PR [13953](https://github.com/python/mypy/pull/13953)）。

### 其他 Mypyc 修复和改进

*   优化原生类实例的 int(x)/float(x)/complex(x)（Richard Si，PR [14450](https://github.com/python/mypy/pull/14450)）
*   始终发出警告（Richard Si，PR [14451](https://github.com/python/mypy/pull/14451)）
*   更快的布尔和整数转换（Jukka Lehtosalo，PR [14422](https://github.com/python/mypy/pull/14422)）
*   支持覆盖属性的属性（Jukka Lehtosalo，PR [14377](https://github.com/python/mypy/pull/14377)）
*   预计算“in”操作和迭代的集合字面量（Richard Si，PR [14409](https://github.com/python/mypy/pull/14409)）
*   设置非扩展类的 `__all__` 时不加载带前向引用的目标（Richard Si，PR [14401](https://github.com/python/mypy/pull/14401)）
*   编译去除 NewType 类型调用（Richard Si，PR [14398](https://github.com/python/mypy/pull/14398)）
*   改进多重继承的错误消息（Joshua Bronson，PR [14344](https://github.com/python/mypy/pull/14344)）
*   简化联合类型（Jukka Lehtosalo，PR [14363](https://github.com/python/mypy/pull/14363)）
*   修复联合简化的相关问题（Jukka Lehtosalo，PR [14364](https://github.com/python/mypy/pull/14364)）
*   针对 typeshed 对 Collection 的更改的修复（Shantanu，PR [13994](https://github.com/python/mypy/pull/13994)）
*   允许使用 enum.Enum（Shantanu，PR [13995](https://github.com/python/mypy/pull/13995)）
*   修复在 Arch Linux 上的编译问题（dosisod，PR [13978](https://github.com/python/mypy/pull/13978)）

### 文档改进

*   各种文档和错误消息调整（Jukka Lehtosalo，PR [14574](https://github.com/python/mypy/pull/14574)）
*   改进泛型文档（Shantanu，PR [14587](https://github.com/python/mypy/pull/14587)）
*   改进协议文档（Shantanu，PR [14577](https://github.com/python/mypy/pull/14577)）
*   改进动态类型文档（Shantanu，PR [14576](https://github.com/python/mypy/pull/14576)）
*   改进常见问题页面（Shantanu，PR [14581](https://github.com/python/mypy/pull/14581)）
*   添加顶级 TypedDict 页面（Shantanu，PR [14584](https://github.com/python/mypy/pull/14584)）
*   改进入门文档（Shantanu，PR [14572](https://github.com/python/mypy/pull/14572)）
*   将 truthy-function 文档从“可选检查”移至“默认启用”（Anders Kaseorg，PR [14380](https://github.com/python/mypy/pull/14380)）
*   避免在装饰器工厂文档中使用隐式可选（Tom Schraitle，PR [14156](https://github.com/python/mypy/pull/14156)）
*   澄清有关 install-types 的文档（Shantanu，PR [14003](https://github.com/python/mypy/pull/14003)）
*   改善模块级类型忽略错误的可搜索性（Shantanu，PR [14342](https://github.com/python/mypy/pull/14342)）
*   在 README 中宣传 mypy 守护进程（Ivan Levkivskyi，PR [14248](https://github.com/python/mypy/pull/14248)）
*   在 README 中添加错误代码的链接（Ivan Levkivskyi，PR [14249](https://github.com/python/mypy/pull/14249)）
*   文档说明报告生成会禁用缓存（Ilya Konstantinov，PR [14402](https://github.com/python/mypy/pull/14402)）
*   停止称 mypy 为测试软件（Ivan Levkivskyi，PR [14251](https://github.com/python/mypy/pull/14251)）
*   Flycheck-mypy 被弃用，因为其功能已合并到 Flycheck（Ivan Levkivskyi，PR [14247](https://github.com/python/mypy/pull/14247)）
*   更新“声明装饰器”中的代码示例（ChristianWitzler，PR [14131](https://github.com/python/mypy/pull/14131)）

### Stubtest 改进

Stubtest 是一个用于测试存根是否符合实现的工具。

*   改进与 `__all__` 相关错误的错误消息（Alex Waygood，PR [14362](https://github.com/python/mypy/pull/14362)）
*   改进确定全局命名空间名称是否被导入的启发式（Alex Waygood，PR [14270](https://github.com/python/mypy/pull/14270)）
*   捕获模块导入时的 BaseException（Shantanu，PR [14284](https://github.com/python/mypy/pull/14284)）
*   将导出符号错误与 `__all__` 对象路径关联（Nikita Sobolev，PR [14217](https://github.com/python/mypy/pull/14217)）
*   将 `__warningregistry__` 添加到忽略的模块 dunder 列表（Nikita Sobolev，PR [14218](https://github.com/python/mypy/pull/14218)）
*   如果存根中存在默认值，则检查其正确性（Jelle Zijlstra，PR [14085](https://github.com/python/mypy/pull/14085)）

### Stubgen 改进

Stubgen 是一个用于自动生成库草稿存根的工具。

*   将 dll 视为 C 模块（Shantanu，PR [14503](https://github.com/python/mypy/pull/14503)）

### 其他显著修复和改进

*   根据最近的 typeshed 更改更新存根建议（Alex Waygood，PR [14265](https://github.com/python/mypy/pull/14265)）
*   修复带缓存的 attrs 协议检查（Marc Mueller，PR [14558](https://github.com/python/mypy/pull/14558)）
*   修复操作数项类型具有自定义 `__eq__` 的严格相等检查（Jukka Lehtosalo，PR [14513](https://github.com/python/mypy/pull/14513)）
*   不要认为对象总是为真（Jukka Lehtosalo，PR [14510](https://github.com/python/mypy/pull/14510)）
*   正确支持 TypedDict 的联合作为字典字面量上下文（Ivan Levkivskyi，PR [14505](https://github.com/python/mypy/pull/14505)）
*   正确扩展使用 Self 和 TypeVar 的泛型类中的类型（Ivan Levkivskyi，PR [14491](https://github.com/python/mypy/pull/14491)）
*   修复使用调用语法定义的递归 TypedDicts/NamedTuples（Ivan Levkivskyi，PR [14488](https://github.com/python/mypy/pull/14488)）
*   修复类继承 Any 时的类型推断问题（Shantanu，PR [14404](https://github.com/python/mypy/pull/14404)）
*   修复涉及六个的泛型基类的误报（Ivan Levkivskyi，PR [14478](https://github.com/python/mypy/pull/14478)）
*   在命名空间模式下，不要将没有扩展名的脚本视为模块（Tim Geypens，PR [14335](https://github.com/python/mypy/pull/14335)）
*   修复联合中的受限类型变量的推断（Christoph Tyralla，PR [14396](https://github.com/python/mypy/pull/14396)）
*   修复从 typing 导入的 Unpack（Marc Mueller，PR [14378](https://github.com/python/mypy/pull/14378)）
*   允许多行值的 ini 配置中使用尾随逗号（Nikita Sobolev，PR [14240](https://github.com/python/mypy/pull/14240)）
*   修复涉及 Unions 和生成器或协程的假阴性（Shantanu，PR [14224](https://github.com/python/mypy/pull/14224)）
*   修复可调用的类型参数约束（Vincent Vanlaer，PR [14153](https://github.com/python/mypy/pull/14153)）
*   修复具有固定长度元组的类型别名（Jukka Lehtosalo，PR [14184](https://github.com/python/mypy/pull/14184)）
*   修复类型别名和新样式联合的相关问题（Jukka Lehtosalo，PR [14181](https://github.com/python/mypy/pull/14181)）
*   简化联合的方式不再过于激进（Ivan Levkivskyi，PR [14178](https://github.com/python/mypy/pull/14178)）
*   简化可调用重叠逻辑（Ivan Levkivskyi，PR [14174](https://github.com/python/mypy/pull/14174)）
*   在将值赋给联合类型变量时尝试空上下文（Ivan Levkivskyi，PR [14151](https://github.com/python/mypy/pull/14151)）
*   改进递归类型处理（Ivan Levkivskyi，PR [14147](https://github.com/python/mypy/pull/14147)）
*   使非数字非空的 FORCE_COLOR 变量为真（Shantanu，PR [14140](https://github.com/python/mypy/pull/14140)）
*   修复递归类型别名的问题（Ivan Levkivskyi，PR [14136](https://github.com/python/mypy/pull/14136)）
*   正确处理 Python 3.11 上的 Enum 名称（Ivan Levkivskyi，PR [14133](https://github.com/python/mypy/pull/14133)）
*   修复类对象回退到元类的回调协议（Ivan Levkivskyi，PR [14121](https://github.com/python/mypy/pull/14121)）
*   正确支持可调用的 ClassVar 中的 self 类型（Ivan Levkivskyi，PR [14115](https://github.com/python/mypy/pull/14115)）
*   修复嵌套位置和属性中的类型变量冲突（Ivan Levkivskyi，PR [14095](https://github.com/python/mypy/pull/14095)）
*   允许类变量作为只读属性的实现（Ivan Levkivskyi，PR [14081](https://github.com/python/mypy/pull/14081)）
*   防止警告导致 dmypy 失败（Andrzej Bartosiński，PR [14102](https://github.com/python/mypy/pull/14102)）
*   正确处理 mypy 守护进程中的嵌套定义（Ivan Levkivskyi，PR [14104](https://github.com/python/mypy/pull/14104)）
*   如果可能存在提升，不要认为分支是不可达的（Ivan Levkivskyi，PR [14077](https://github.com/python/mypy/pull/14077)）
*   修复具体子类中重载方法的不兼容重写（Shantanu，PR [14017](https://github.com/python/mypy/pull/14017)）
*   修复类型别名中的新样式联合语法（Jukka Lehtosalo，PR [14008](https://github.com/python/mypy/pull/14008)）
*   修复和优化重载兼容性检查（Shantanu，PR [14018](https://github.com/python/mypy/pull/14018)）
*   改进通过导入处理重定义的方式（Shantanu，PR [13969](https://github.com/python/mypy/pull/13969)）
*   保留（某些）隐式导出的类型（Shantanu，PR [13967](https://github.com/python/mypy/pull/13967)）

### Typeshed 更新

Typeshed 现在是模块化的，除了标准库存根之外的所有内容都以单独的 PyPI 包分发。请参阅 [git log](https://github.com/python/typeshed/commits/main?after=ea0ae2155e8a04c9837903c3aff8dd5ad5f36ebc+0&branch=main&path=stdlib) 获取 typeshed 更改的完整列表。

### 致谢

感谢所有为此版本做出贡献的 mypy 贡献者：

*   Alessio Izzo
*   Alex Waygood
*   Anders Kaseorg
*   Andrzej Bartosiński
*   Avasam
*   ChristianWitzler
*   Christoph Tyralla
*   dosisod
*   Harrison McCarty
*   Hugo van Kemenade
*   Hugues
*   Ilya Konstantinov
*   Ivan Levkivskyi
*   Jelle Zijlstra
*   jhance
*   johnthagen
*   Jonathan Daniel
*   Joshua Bronson
*   Jukka Lehtosalo
*   KotlinIsland
*   Lakshay Bisht
*   Lefteris Karapetsas
*   Marc Mueller
*   Matthew Hughes
*   Michael Lee
*   Nick Drozd
*   Nikita Sobolev
*   Richard Si
*   Shantanu
*   Stas Ilinskiy
*   Tim Geypens
*   Tin Tvrtković
*   Tom Schraitle
*   Valentin Stanciu
*   Vincent Vanlaer

我们还要感谢我们的雇主 Dropbox，资助了 mypy 核心团队的工作。

由 Stas Ilinskiy 发布

## 以前的版本

有关以前版本的信息，请参阅 [此处](https://mypy-lang.blogspot.com/)。
