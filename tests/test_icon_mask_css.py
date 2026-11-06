"""The icon-mask colors are scoped so only the danger button changes between themes."""
from pathlib import Path

CSS = (Path(__file__).parent.parent / "src/static/css/main.css").read_text()


def test_bare_icon_mask_keeps_the_stock_color_in_both_themes():
    assert '[data-theme="dark"] .icon-mask' not in CSS
    block = CSS.split(".icon-mask {", 1)[1].split("}", 1)[0]
    assert "background-color: #f0a3a3" in block


def test_danger_button_icon_is_dark_red_in_light_and_pink_in_dark():
    assert ".icon-btn-danger .icon-mask { background-color: #7a1212; }" in CSS
    assert '[data-theme="dark"] .icon-btn-danger .icon-mask { background-color: #f0a3a3; }' in CSS


def test_neutral_icon_button_uses_the_text_color():
    assert ".icon-btn:not(.icon-btn-danger) .icon-mask { background-color: var(--color-text); }" in CSS
