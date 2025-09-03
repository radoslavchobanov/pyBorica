"""Utility functions used across the BORICA CQES wrapper."""

from __future__ import annotations

import time
from typing import Callable, Literal, Tuple, Any


def poll(
    fn: Callable[[], Tuple[Literal["done", "in_progress"], dict[str, Any]]],
    *,
    interval_s: float = 2.0,
    timeout_s: float = 180.0,
) -> dict[str, Any]:
    """Generic polling helper.

    Calls ``fn`` repeatedly every ``interval_s`` seconds until it returns a
    tuple ``("done", payload)`` or until ``timeout_s`` seconds have elapsed.

    Parameters
    ----------
    fn:
        A function with no arguments that returns a pair ``(state, payload)``.
        ``state`` must be ``"done"`` or ``"in_progress"``.
    interval_s:
        How long to wait between invocations of ``fn``.
    timeout_s:
        Maximum time to continue polling. When expired, a ``TimeoutError`` is raised.

    Returns
    -------
    dict
        The payload returned by ``fn`` when ``state`` equals ``"done"``.

    Raises
    ------
    TimeoutError
        If the timeout is reached before ``fn`` returns ``"done"``.
    """
    deadline = time.time() + timeout_s
    while True:
        state, payload = fn()
        if state == "done":
            return payload
        if time.time() >= deadline:
            raise TimeoutError("Polling timed out.")
        time.sleep(interval_s)