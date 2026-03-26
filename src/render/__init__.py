from __future__ import annotations

import os
from tempfile import gettempdir

if "MPLCONFIGDIR" not in os.environ:
    os.environ["MPLCONFIGDIR"] = os.path.join(gettempdir(), "mplconfig")

if "XDG_CACHE_HOME" not in os.environ:
    os.environ["XDG_CACHE_HOME"] = gettempdir()

from src.render.report_builder import build_report_package

__all__ = ["build_report_package"]
