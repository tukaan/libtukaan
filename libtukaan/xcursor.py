from __future__ import annotations

import sys
from pathlib import Path

from tukaan._tcl import Tcl


class Xcursor:
    loaded_cursors: set[int] = set()
    defined_cursors: dict[str, int] = {}

    @staticmethod
    def init() -> None:
        Tcl.load_dll(
            Path(__file__).parent
            / "unix"
            / f"libtkxcursor_{'x64' if sys.maxsize > 2**32 else 'x32'}{Tcl.dll_ext}",
            "Xcursor",
        )

    @classmethod
    def load_cursor(cls, source: Path) -> int:
        if not source.exists():
            raise FileNotFoundError(source)

        cursor_id = Tcl.call(int, "Xcursor::load_cursor_file", source)
        cls.loaded_cursors.add(cursor_id)
        return cursor_id

    @classmethod
    def set_cursor(cls, widget_name: str, cursor_id: int) -> None:
        Tcl.call(None, "Xcursor::set_cursor", widget_name, cursor_id)
        cls.defined_cursors[widget_name] = cursor_id

    @classmethod
    def cleanup_cursors(cls) -> None:
        for widget_name in cls.defined_cursors:
            Tcl.call(None, "Xcursor::undefine_cursor", widget_name)
        for cursor_id in cls.loaded_cursors:
            Tcl.call(None, "Xcursor::free_cursor", cursor_id)

        cls.loaded_cursors.clear()
        cls.defined_cursors.clear()
