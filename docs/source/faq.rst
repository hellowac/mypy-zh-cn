常见问题解答(Frequently Asked Questions)
====================================================

为什么同时有动态和静态类型？(Why have both dynamic and static typing?)
********************************************************************************

动态类型可以灵活、强大、方便且易于使用。但这并不总是最佳的方法；许多开发者选择使用静态类型语言或为 Python 使用静态类型是有充分理由的。

以下是 mypy 风格静态类型的一些潜在好处：

- 静态类型可以使程序更易于理解和维护。类型声明可以作为机器检查的文档。这一点很重要，因为代码通常被阅读的频率远高于修改的频率，尤其是对于大型和复杂的程序。

- 静态类型可以帮助你更早、更少地进行测试和调试找到错误。特别是在大型和复杂的项目中，这可以节省大量时间。

- 静态类型可以帮助你在代码投入生产之前找到难以发现的错误。这可以提高可靠性并减少安全问题的数量。

- 静态类型使得构建非常有用的开发工具成为可能，这些工具可以提高编程生产力或软件质量，包括具有精确和可靠代码补全的 IDE、静态分析工具等。

- 你可以在单一语言中同时获得动态和静态类型的好处。动态类型可能非常适合小项目或编写程序的 UI。例如，随着程序的增长，你可以将复杂的应用逻辑调整为静态类型以帮助维护。

有关更多信息，请查看 mypy 网站的 `首页 <https://www.mypy-lang.org>`_。

我的项目会受益于静态类型吗？(Would my project benefit from static typing?)
****************************************************************************************

对于许多项目，动态类型完全可以接受（我们认为 Python 是一门很棒的语言）。但有时你的项目需要更强大的工具，这时 mypy 可能会派上用场。

如果你的项目符合以下一些条件，mypy（和静态类型）可能会很有用：

- 你的项目较大或较复杂。

- 你的代码库必须维护很长时间。

- 多位开发者在同一代码上工作。

- 运行测试需要耗费大量时间或工作（类型检查帮助你在开发早期快速找到错误，从而减少测试迭代次数）。

- 一些项目成员（开发人员或管理层）不喜欢动态类型，但其他人更喜欢动态类型和 Python 语法。Mypy 可能是一个大家都容易接受的解决方案。

- 你想为项目的未来做好准备，即使目前上述情况都不适用。越早开始，采用静态类型就越容易。

我可以使用 mypy 来检查我现有的 Python 代码吗？(Can I use mypy to type check my existing Python code?)
**********************************************************************************************************

Mypy 支持大多数 Python 特性和习惯用法，许多大型 Python 项目正在成功使用 mypy。使用复杂的 introspection 或元编程的代码可能难以进行类型检查，但在代码库中较少动态的其他部分使用静态类型仍然是可能的。

静态类型会使我的程序运行得更快吗？(Will static typing make my programs run faster)
**********************************************************************************************

Mypy 仅执行静态类型检查，并不提高性能。它对性能的影响很小。未来可能会有其他工具能够将静态类型的 mypy 代码编译为 C 模块或高效的 JVM 字节码，但这超出了 mypy 项目的范围。


mypy 是免费的吗？(Is mypy free?)
***************************************

是的。Mypy 是自由软件，也可以用于商业和专有项目。Mypy 在 MIT 许可证下提供。

我可以在 mypy 中使用鸭子类型吗？(Can I use duck typing with mypy?)
********************************************************************************************************

Mypy 同时支持 `名义子类型
<https://en.wikipedia.org/wiki/Nominative_type_system>`_ 和 `结构子类型
<https://en.wikipedia.org/wiki/Structural_type_system>`_。
结构子类型可以被视为“静态鸭子类型”。有人认为结构子类型更适合像 Python 这样的鸭子类型语言。然而，mypy 主要使用名义子类型，使结构子类型大多为可选（除了像 :py:class:`~collections.abc.Iterable` 这样的内置协议总是支持结构子类型）。原因如下：

1. 使用名义类型系统时，生成简短且有信息量的错误消息很容易。这在使用类型推断时尤为重要。

2. Python 提供了对名义 :py:func:`isinstance` 测试的内置支持，并且在程序中被广泛使用。仅提供有限的结构 :py:func:`isinstance` 支持，并且其类型安全性低于名义类型测试。

3. 许多程序员已经熟悉静态名义子类型，并且在 Java、C++ 和 C# 等语言中成功使用过。使用结构子类型的语言较少。

然而，结构子类型也可能很有用。例如，使用协议类型的“公共 API”可能更灵活。此外，使用协议类型消除了明确声明 ABC 实现的必要性。作为经验法则，我们建议在可能的情况下使用名义类，在必要时使用协议。有关协议类型和结构子类型的更多详细信息，请参见 :ref:`protocol-types` 和 :pep:`544`。

我喜欢 Python，但我不需要静态类型(I like Python and I have no need for static typing)
****************************************************************************************************************

Mypy 的目标不是说服每个人编写静态类型的 Python——静态类型完全是可选的，无论是现在还是将来。目标是为 Python 程序员提供更多选择，使 Python 成为大型项目中与其他静态类型语言更具竞争力的替代方案，提高程序员的生产力，并改善软件质量。

mypy 程序与普通 Python 程序有什么不同？(How are mypy programs different from normal Python?)
**************************************************************************************************************************

由于你使用标准的 Python 实现来运行 mypy 程序，mypy 程序也是 Python 程序。类型检查器可能会对一些有效的 Python 代码发出警告，但代码始终是可以运行的。此外，mypy 仍然不支持一些 Python 特性，但这在逐渐改善。

显而易见的区别是可用的静态类型检查。部分 :ref:`common_issues` 提到了一些可能需要的对 Python 代码的修改，以使代码能够无错误地进行类型检查。此外，你的代码必须显式声明定义的属性。

Mypy 支持模块化、高效的类型检查，这似乎排除了某些语言特性的类型检查，例如对方法的任意猴子补丁。

mypy 与 Cython 有什么不同？(How is mypy different from Cython?)
********************************************************************

:doc:`Cython <cython:index>` 是一种 Python 的变体，支持编译为 CPython C 模块。与 CPython 相比，它可以大大加快某些类型程序的速度，并提供静态类型（尽管这与 mypy 不同）。Mypy 在以下方面有所不同：

- Cython 更加关注性能，而 mypy 仅关注静态类型检查，提升性能不是直接目标。

- 对于静态类型代码，mypy 的语法可以说更简单、更“Pythonic”（没有 cdef/cpdef 等）。

- mypy 语法与 Python 兼容。Mypy 程序是可以使用任何 Python 实现运行的正常 Python 程序。Cython 对 Python 语法有许多不兼容的扩展，Cython 程序通常不能在不先将其编译为 CPython 扩展模块的情况下运行。Cython 还有一种纯 Python 模式，但似乎仅支持 Cython 功能的一个子集，且语法相当冗长。

- Mypy 拥有不同的类型系统特性。例如，mypy 具有泛型（参数多态）、函数类型和双向类型推断，而 Cython 不支持这些功能。（Cython 具有与 mypy 泛型不同但相关的融合类型。Mypy 也具有作为泛型扩展的类似特性。）

- Mypy 类型检查器了解许多 Python 标准库模块的静态类型，可以有效地对使用它们的代码进行类型检查。

- Cython 支持直接访问 C 函数，并且许多特性是通过将其转换为 C 或 C++ 定义的。Mypy 仅使用 Python 语义，并且不处理访问 C 库功能的问题。

它在 PyPy 上运行吗？(Does it run on PyPy?)
******************************************

在一定程度上。使用 PyPy 3.8，mypy 至少能够对自身进行类型检查。对于旧版本的 PyPy，mypy 依赖于 `typed-ast
<https://github.com/python/typed_ast>`_ ，该库使用了 PyPy 不支持的几个 API（包括一些内部 CPython API）。

mypy 是一个很棒的项目。我可以帮助吗？(Mypy is a cool project. Can I help?)
******************************************************************************************

任何帮助都非常感谢!如果你想贡献，可以 `联系
<https://www.mypy-lang.org/contact.html>`_ 开发者。与开发、设计、宣传、文档、测试、网站维护、融资等相关的任何帮助都是有益的。通过贡献你可以学到很多东西，任何人都可以帮助，即使是初学者!不过，如果你想参与 mypy 内部工作，掌握一些编译器和/或类型系统的知识是必不可少的。
