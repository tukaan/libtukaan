from __future__ import annotations

import sys
from pathlib import Path

from tukaan._tcl import Tcl


class Xcursor:
    _loaded_cursors: dict[str, str] = {}
    _defined_cursors: dict[str, str] = {}

    @staticmethod
    def init() -> None:
        Tcl.load_dll(
            Path(__file__).parent
            / "unix"
            / f"libtkxcursor_{'x64' if sys.maxsize > 2**32 else 'x32'}{Tcl.dll_ext}",
            "Xcursor",
        )

    @classmethod
    def get_path_for_cursor(cls, cursor_id: str) -> str:
        return cls._loaded_cursors.get(cursor_id, "")

    @classmethod
    def load_cursor(cls, source: Path) -> str:
        source_str = Tcl.to(source)
        for cursor_id, path in cls._loaded_cursors.items():
            if path == source_str:
                return cursor_id

        if not source.exists():
            raise FileNotFoundError(source)

        cursor_id = Tcl.eval(str, f"Xcursor::load_cursor_file {source_str}")
        cls._loaded_cursors[cursor_id] = source_str
        return cursor_id

    @classmethod
    def set_cursor(cls, widget_name: str, cursor_id: str) -> None:
        Tcl.eval(None, f"Xcursor::set_cursor {widget_name} {cursor_id}")
        cls._defined_cursors[widget_name] = cursor_id

    @classmethod
    def undefine_cursors(cls, widget_names: set[str]) -> None:
        for widget_name in widget_names:
            Tcl.eval(None, f"Xcursor::undefine_cursor {widget_name}")
            cls._defined_cursors.pop(widget_name)

    @classmethod
    def cleanup_cursors(cls) -> None:
        for widget_name in cls._defined_cursors:
            Tcl.eval(None, f"Xcursor::undefine_cursor {widget_name}")
        for cursor_id in cls._loaded_cursors:
            Tcl.eval(None, f"Xcursor::free_cursor {cursor_id}")

        cls._loaded_cursors.clear()
        cls._defined_cursors.clear()
