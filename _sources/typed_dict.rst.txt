.. _typeddict:

TypedDict
*********

Python 程序经常使用字符串键的字典来表示对象。``TypedDict`` 让你可以为表示具有固定模式的字典提供精确的类型，例如 ``{'id': 1, 'items': ['x']}`` 。

这里是一个典型的例子：

.. code-block:: python

   movie = {'name': 'Blade Runner', 'year': 1982}

只期望一组固定的字符串键（上面的 ``'name'`` 和 ``'year'`` )，每个键都有独立的值类型（上面的 ``'name'`` 为 ``str``，而 ``'year'`` 为 ``int`` )。我们之前见过 ``dict[K, V]`` 类型，它让你声明统一的字典类型，其中每个值具有相同的类型，并且支持任意键。这显然不适合上面的 ``movie``。相反，你可以使用 ``TypedDict`` 为像 ``movie`` 这样的对象提供精确的类型，其中每个字典值的类型取决于键：

.. code-block:: python

   from typing import TypedDict

   Movie = TypedDict('Movie', {'name': str, 'year': int})

   movie: Movie = {'name': 'Blade Runner', 'year': 1982}

``Movie`` 是一个 ``TypedDict`` 类型，包含两个项目：``'name'`` (类型为 ``str`` )和 ``'year'`` (类型为 ``int`` )。注意我们为 ``movie`` 变量使用了显式类型注解。这个类型注解很重要——如果没有它，mypy 会尝试推断 ``movie`` 为一个常规的、统一的 :py:class:`dict` 类型，这不是我们想要的。

.. note::

   如果你将 ``TypedDict`` 对象作为参数传递给函数，通常不需要类型注解，因为 mypy 可以根据声明的参数类型推断所需的类型。此外，如果赋值目标之前已经定义，并且具有 ``TypedDict`` 类型，mypy 会将分配的值视为 ``TypedDict``，而不是 :py:class:`dict`。

现在 mypy 会将这些视为有效：

.. code-block:: python

   name = movie['name']  # 可以；name 的类型是 str
   year = movie['year']  # 可以；year 的类型是 int

Mypy 会将无效键检测为错误：

.. code-block:: python

   director = movie['director']  # 错误：'director' 不是有效的键

Mypy 还会拒绝将运行时计算的表达式作为键，因为它无法验证这是否是有效键。你只能使用字符串字面量作为 ``TypedDict`` 键。

``TypedDict`` 类型对象也可以作为构造函数。它在运行时返回一个普通的 :py:class:`dict` 对象——``TypedDict`` 不定义新的运行时类型：

.. code-block:: python

   toy_story = Movie(name='Toy Story', year=1995)

这等同于直接使用 ``{ ... }`` 或 ``dict(key=value, ...)`` 构造字典。构造函数的形式有时很方便，因为它可以在没有类型注解的情况下使用，并且还使对象的类型明确。

像所有类型一样，``TypedDict`` 可以用作构建任意复杂类型的组件。例如，你可以定义嵌套的 ``TypedDict`` 和包含 ``TypedDict`` 项的容器。与大多数其他类型不同，mypy 使用结构兼容性检查（或结构子类型）来处理 ``TypedDict``。具有额外项目的 ``TypedDict`` 对象与（子类型）更窄的 ``TypedDict`` 兼容，前提是项目类型兼容（*完整性* 也影响子类型，具体讨论如下）。

``TypedDict`` 对象不是常规 ``dict[...]`` 类型的子类型（反之亦然），因为 :py:class:`dict` 允许添加和删除任意键，而 ``TypedDict`` 则不然。然而，任何 ``TypedDict`` 对象都是 ``Mapping[str, object]`` 的子类型（即兼容），因为 :py:class:`~collections.abc.Mapping` 仅提供对字典项的只读访问：

.. code-block:: python

   def print_typed_dict(obj: Mapping[str, object]) -> None:
       for key, value in obj.items():
           print(f'{key}: {value}')

   print_typed_dict(Movie(name='Toy Story', year=1995))  # 可以

.. note::

   除非你使用的是 Python 3.8 或更高版本（在标准库 :py:mod:`typing` 模块中提供 ``TypedDict`` )，否则你需要使用 pip 安装 ``typing_extensions`` 来使用 ``TypedDict``：

   .. code-block:: text

      python3 -m pip install --upgrade typing-extensions

Totality
--------

By default mypy ensures that a ``TypedDict`` object has all the specified
keys. This will be flagged as an error:

.. code-block:: python

   # Error: 'year' missing
   toy_story: Movie = {'name': 'Toy Story'}

Sometimes you want to allow keys to be left out when creating a
``TypedDict`` object. You can provide the ``total=False`` argument to
``TypedDict(...)`` to achieve this:

.. code-block:: python

   GuiOptions = TypedDict(
       'GuiOptions', {'language': str, 'color': str}, total=False)
   options: GuiOptions = {}  # Okay
   options['language'] = 'en'

You may need to use :py:meth:`~dict.get` to access items of a partial (non-total)
``TypedDict``, since indexing using ``[]`` could fail at runtime.
However, mypy still lets use ``[]`` with a partial ``TypedDict`` -- you
just need to be careful with it, as it could result in a :py:exc:`KeyError`.
Requiring :py:meth:`~dict.get` everywhere would be too cumbersome. (Note that you
are free to use :py:meth:`~dict.get` with total ``TypedDict``\s as well.)

Keys that aren't required are shown with a ``?`` in error messages:

.. code-block:: python

   # Revealed type is "TypedDict('GuiOptions', {'language'?: builtins.str,
   #                                            'color'?: builtins.str})"
   reveal_type(options)

Totality also affects structural compatibility. You can't use a partial
``TypedDict`` when a total one is expected. Also, a total ``TypedDict`` is not
valid when a partial one is expected.

Supported operations
--------------------

``TypedDict`` objects support a subset of dictionary operations and methods.
You must use string literals as keys when calling most of the methods,
as otherwise mypy won't be able to check that the key is valid. List
of supported operations:

* Anything included in :py:class:`~collections.abc.Mapping`:

  * ``d[key]``
  * ``key in d``
  * ``len(d)``
  * ``for key in d`` (iteration)
  * :py:meth:`d.get(key[, default]) <dict.get>`
  * :py:meth:`d.keys() <dict.keys>`
  * :py:meth:`d.values() <dict.values>`
  * :py:meth:`d.items() <dict.items>`

* :py:meth:`d.copy() <dict.copy>`
* :py:meth:`d.setdefault(key, default) <dict.setdefault>`
* :py:meth:`d1.update(d2) <dict.update>`
* :py:meth:`d.pop(key[, default]) <dict.pop>` (partial ``TypedDict``\s only)
* ``del d[key]`` (partial ``TypedDict``\s only)

.. note::

   :py:meth:`~dict.clear` and :py:meth:`~dict.popitem` are not supported since they are unsafe
   -- they could delete required ``TypedDict`` items that are not visible to
   mypy because of structural subtyping.

完整性(Totality)
----------------

默认情况下，mypy 确保 ``TypedDict`` 对象具有所有指定的键。否则将被标记为错误：

.. code-block:: python

   # 错误：缺少 'year'
   toy_story: Movie = {'name': 'Toy Story'}

有时你希望在创建 ``TypedDict`` 对象时允许省略键。你可以向 ``TypedDict(...)`` 提供 ``total=False`` 参数来实现这一点：

.. code-block:: python

   GuiOptions = TypedDict(
       'GuiOptions', {'language': str, 'color': str}, total=False)
   options: GuiOptions = {}  # 可以
   options['language'] = 'en'

你可能需要使用 :py:meth:`~dict.get` 来访问部分（非总计）``TypedDict`` 的项，因为使用 ``[]`` 索引可能在运行时失败。然而，mypy 仍然允许在部分 ``TypedDict`` 上使用 ``[]``——你只需要小心，因为这可能导致 :py:exc:`KeyError` 。在任何地方都要求使用 :py:meth:`~dict.get` 会太繁琐。（请注意，你也可以在使用了 total 参数的 ``TypedDict`` 使用 :py:meth:`~dict.get`。）

在错误消息中，不是必需的键会用 ``?`` 显示：

.. code-block:: python

   # 显示的类型是 "TypedDict('GuiOptions', {'language'?: builtins.str,
   #                                            'color'?: builtins.str})"
   reveal_type(options)

完整性也会影响结构兼容性。当期望一个完整(total)的 ``TypedDict`` 时，你不能使用部分(partial)的 ``TypedDict``。同样，当期望一个部分(partial)的 ``TypedDict`` 时，完整(total)的 ``TypedDict`` 也是无效的。

支持的操作(Supported operations)
----------------------------------------

``TypedDict`` 对象支持一组字典操作和方法的子集。在调用大多数方法时，必须使用字符串字面量作为键，否则 mypy 将无法检查键是否有效。支持的操作列表：

* 包含在 :py:class:`~collections.abc.Mapping` 中的任何内容：

  * ``d[key]``
  * ``key in d``
  * ``len(d)``
  * ``for key in d`` （迭代）
  * :py:meth:`d.get(key[, default]) <dict.get>`
  * :py:meth:`d.keys() <dict.keys>`
  * :py:meth:`d.values() <dict.values>`
  * :py:meth:`d.items() <dict.items>`

* :py:meth:`d.copy() <dict.copy>`
* :py:meth:`d.setdefault(key, default) <dict.setdefault>`
* :py:meth:`d1.update(d2) <dict.update>`
* :py:meth:`d.pop(key[, default]) <dict.pop>`（仅适用于部分(partial) ``TypedDict`` )
* ``del d[key]`` (仅适用于部分(partial) ``TypedDict`` )

.. note::

   :py:meth:`~dict.clear` 和 :py:meth:`~dict.popitem` 不受支持，因为它们不安全——它们可能删除必需的 ``TypedDict`` 项，而这些项由于结构子类型(structural subtyping)从而对 mypy 不可见。

基于类的语法(Class-based)
------------------------------------

在 Python 3.6 及更高版本中，支持一种替代的基于类的语法来定义 ``TypedDict``：

.. code-block:: python

   from typing import TypedDict  # 在 Python 3.7 及更早版本中使用 "from typing_extensions"

   class Movie(TypedDict):
       name: str
       year: int

上述定义与原始的 ``Movie`` 定义等效。它实际上并不定义一个真实的类。此语法还支持一种继承形式——子类可以定义附加项。然而，这主要是一种符号快捷方式。由于 mypy 对 ``TypedDict`` 使用结构兼容性，因此兼容性不需要继承。以下是继承的示例：

.. code-block:: python

   class Movie(TypedDict):
       name: str
       year: int

   class BookBasedMovie(Movie):
       based_on: str

现在 ``BookBasedMovie`` 具有键 ``name``、``year`` 和 ``based_on``。

混合必须和非必须项(Mixing)
--------------------------------------

除了允许在 ``TypedDict`` 类型之间重用外，继承还允许你在单个 ``TypedDict`` 中混合必需项和非必需项（使用 ``total=False`` )。示例：

.. code-block:: python

   class MovieBase(TypedDict):
       name: str
       year: int

   class Movie(MovieBase, total=False):
       based_on: str

现在 ``Movie`` 具有必需键 ``name`` 和 ``year``, 而 ``based_on`` 在构造对象时可以省略。具有必需键和非必需键混合的 ``TypedDict`` (如上面的 ``Movie`` )仅在另一个 ``TypedDict`` 中所有必需键都是第一个 ``TypedDict`` 中的必需键，并且另一个 ``TypedDict`` 的所有非必需键也是第一个 ``TypedDict`` 的非必需键时，才会兼容。

只读项(Read-only)
------------------------------

你可以使用在 Python 3.13 中引入的 ``typing.ReadOnly`` 或 ``typing_extensions.ReadOnly`` 来标记 TypedDict 项为只读（:pep:`705`）：

.. code-block:: python

    from typing import TypedDict

    # 或在 Python 3.13+ 中使用 "from typing ..."
    from typing_extensions import ReadOnly

    class Movie(TypedDict):
        name: ReadOnly[str]
        num_watched: int

    m: Movie = {"name": "Jaws", "num_watched": 1}
    m["name"] = "The Godfather"  # 错误：“name”是只读的
    m["num_watched"] += 1  # 正确

具有可变项的 TypedDict 可以分配给具有相应只读项的 TypedDict ，并且项的类型可以 :ref:`协变 <variance-of-generics>`：

.. code-block:: python

    class Entry(TypedDict):
        name: ReadOnly[str | None]
        year: ReadOnly[int]

    class Movie(TypedDict):
        name: str
        year: int

    def process_entry(i: Entry) -> None: ...

    m: Movie = {"name": "Jaws", "year": 1975}
    process_entry(m)  # 正确

TypedDicts的联合(Unions)
----------------------------------------

由于在运行时，TypedDict 实际上只是常规字典，因此不能使用 ``isinstance`` 检查来区分 TypedDict 的不同变体，如同在常规对象中那样。

相反，你可以使用 :ref:`标记联合模式 <tagged_unions>`。文档中引用的部分提供了完整的描述和示例，但简而言之，你需要给每个 TypedDict 相同的键，其中每个值具有唯一的 :ref:`字面量类型 <literal_types>`。然后，检查该键以区分你的 TypedDicts。

内联TypedDict类型(Inline)
--------------------------------------------

.. note::

    这是一个实验性（非标准）功能。使用
    ``--enable-incomplete-feature=InlineTypedDict`` 来启用。

有时你可能想定义一个复杂的嵌套 JSON 架构，或为返回 TypedDict 的一次性函数进行注解。在这种情况下，使用内联 TypedDict 语法可能会很方便。例如：

.. code-block:: python

    def test_values() -> {"int": int, "str": str}:
        return {"int": 42, "str": "test"}

    class Response(TypedDict):
        status: int
        msg: str
        # 在这里使用内联语法可以避免定义两个额外的 TypedDict。
        content: {"items": list[{"key": str, "value": str}]}

内联 TypedDict 也可以作为类型别名的目标，但由于与常规变量的歧义，它仅允许用于（较新）显式类型别名形式：

.. code-block:: python

    from typing import TypeAlias

    X = {"a": int, "b": int}  # 创建一个类型为 dict[str, type[int]] 的变量
    Y: TypeAlias = {"a": int, "b": int}  # 创建一个类型别名
    type Z = {"a": int, "b": int}  # 同上（仅适用于 Python 3.12+）

此外，由于与运行时类型检查的不兼容，强烈建议在联合类型中 *不* 使用内联语法。
