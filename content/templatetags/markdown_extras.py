from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe
import markdown as md_lib

register = template.Library()

# 必要なら追加: "sane_lists", "smarty" など
_EXTENSIONS = [
    "fenced_code",
    "tables",
    "toc",
]

_EXTENSION_CONFIGS = {
    "toc": {
        "toc_depth": "2-3",   # h2〜h3だけ目次に
        "permalink": False,    # 見出しにリンク（不要なら False）
    }
}

def _render_md(text: str) -> tuple[str, str]:
    """
    Markdownを1回だけ変換して、(html, toc_html) を返す
    """
    md = md_lib.Markdown(
        extensions=_EXTENSIONS,
        extension_configs=_EXTENSION_CONFIGS,
        output_format="html5",
    )
    html = md.convert(text or "")
    toc_html = md.toc or ""
    return html, toc_html

@register.filter(name="md")
def md_filter(value: str) -> str:
    """
    本文HTML
    """
    html, _ = _render_md(value or "")
    return mark_safe(html)

@register.filter(name="md_toc")
def md_toc_filter(value: str) -> str:
    """
    目次HTML
    """
    _, toc = _render_md(value or "")
    return mark_safe(toc)
