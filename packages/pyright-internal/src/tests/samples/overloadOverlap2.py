# This sample tests that overlapping-overload diagnostics for explicit self
# annotations are stable regardless of whether a related subclass stores its
# backing attribute under a public or a private name.
#
# Previously, private names (_f) caused variance to be inferred as covariant
# instead of invariant, which produced false-positive reportOverlappingOverload
# errors even though the overloads were semantically non-overlapping.
#
# The PEP 695 [T] syntax is required to trigger the bug because those TypeVars
# use auto-variance inference, unlike old-style TypeVar("T") which is always
# treated as invariant.

from __future__ import annotations

from typing import Any, Callable, overload


class ReactiveMixIn[T]:
    @property
    def value(self) -> T: ...

    @overload
    def __abs__(self: "ReactiveMixIn[complex]") -> "ReactiveMixIn[float]": ...

    @overload
    def __abs__(self: "ReactiveMixIn[bool]") -> "ReactiveMixIn[int]": ...

    @overload
    def __abs__(self) -> "ReactiveMixIn[T]": ...

    def __abs__(self) -> Any: ...

    @overload
    def __add__(self: "ReactiveMixIn[float]", other: float) -> "ReactiveMixIn[float]": ...

    @overload
    def __add__(self: "ReactiveMixIn[int]", other: float) -> "ReactiveMixIn[float]": ...

    @overload
    def __add__(self, other: Any) -> "ReactiveMixIn[Any]": ...

    def __add__(self, other: Any) -> Any: ...

    @overload
    def __rdivmod__(self: "ReactiveMixIn[int]", other: int) -> "ReactiveMixIn[tuple[int, int]]": ...

    @overload
    def __rdivmod__(self: "ReactiveMixIn[bool]", other: int) -> "ReactiveMixIn[tuple[int, int]]": ...

    @overload
    def __rdivmod__(self, other: Any) -> "ReactiveMixIn[Any]": ...

    def __rdivmod__(self, other: Any) -> Any: ...


# Public backing attribute: variance of T is inferred as invariant (always worked).
class ComputedPublic[T](ReactiveMixIn[T]):
    def __init__(self, f: Callable[[], T]) -> None:
        self.f = f

    @property
    def value(self) -> T:
        return self.f()


# Private backing attribute: previously caused variance to be inferred as
# covariant, which triggered false-positive reportOverlappingOverload errors.
class ComputedPrivate[T](ReactiveMixIn[T]):
    def __init__(self, f: Callable[[], T]) -> None:
        self._f = f

    @property
    def value(self) -> T:
        return self._f()
