"""The shared modal backdrop must stack above page content.

Without a z-index, a fixed backdrop paints in DOM order among z-index:auto/0 layers, so cards
with z-index overlays and the opacity-faded footer drew on top of open dialogs.
"""

import re
from pathlib import Path

CSS = Path(__file__).parent.parent / "src" / "static" / "css"


def _z_index(css: str, selector: str) -> int:
    block = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css).group(1)
    return int(re.search(r"z-index:\s*(\d+)", block).group(1))


def test_dialog_backdrop_stacks_above_tooltips_and_card_overlays():
    main = (CSS / "main.css").read_text()
    assert _z_index(main, ".dialog-backdrop") > _z_index(main, ".tooltip")


def test_dialog_backdrop_stacks_above_feedback_trigger():
    main = (CSS / "main.css").read_text()
    feedback = (CSS / "feedback-widget.css").read_text()
    assert _z_index(main, ".dialog-backdrop") > _z_index(feedback, ".feedback-trigger")
