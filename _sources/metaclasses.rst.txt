.. _metaclasses:

元类(Metaclasses)
======================

元类是描述其他类的构造和行为的类，类似于类描述对象的构造和行为。默认的元类是 `type`，但也可以使用其他元类。元类允许创建 “不同种类的类(a different kind of class)” ，例如 `~enum.Enum`、`~typing.NamedTuple` 和单例(singletons)。

Mypy 对 `~abc.ABCMeta` 和 `EnumMeta` 有一些特殊的理解。

.. _defining:

定义元类(Defining)
********************

.. code-block:: python

    class M(type):
        pass

    class A(metaclass=M):
        pass

.. _examples:

元类使用示例(example)
***********************

Mypy 支持在元类中查找属性：

.. code-block:: python

    from typing import ClassVar, Self

    class M(type):
        count: ClassVar[int] = 0

        def make(cls) -> Self:
            M.count += 1
            return cls()

    class A(metaclass=M):
        pass

    a: A = A.make()  # make() 在 M 中查找；结果是类型 A 的对象
    print(A.count)

    class B(A):
        pass

    b: B = B.make()  # 元类是继承的
    print(B.count + " objects were created")  # Error: 不支持的操作数类型用于 + ("int" 和 "str")

.. note::
    在 Python 3.10 及更早版本中，``Self`` 可以在 ``typing_extensions`` 中找到。

.. _limitations:

元类支持的陷阱和限制(Gotchas and limitations)
***************************************************

请注意，元类对继承结构有一些要求，因此最好不要将元类与类层次结构结合：

.. code-block:: python

    class M1(type): pass
    class M2(type): pass

    class A1(metaclass=M1): pass
    class A2(metaclass=M2): pass

    class B1(A1, metaclass=M2): pass  # Mypy 错误：元类冲突
    # 在运行时，上述定义引发异常
    # TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

    class B12(A1, A2): pass  # Mypy 错误：元类冲突

    # 这可以通过一个公共元类子类型来解决：
    class CorrectMeta(M1, M2): pass
    class B2(A1, A2, metaclass=CorrectMeta): pass  # OK，运行时也可以正常工作

* Mypy 不理解动态计算的元类，例如 ``class A(metaclass=f()): ...``
* Mypy 不理解也不能理解任意元类代码。
* Mypy 只识别 :py:class:`type` 的子类作为潜在的元类。