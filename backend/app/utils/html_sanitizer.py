import nh3
from typing import Optional

ALLOWED_TAGS = {
    "p", "br", "strong", "b", "em", "i", "s", "ul", "ol", "li",
    "a", "h1", "h2", "h3", "h4", "h5", "h6",
    "blockquote", "code", "pre",
    "table", "thead", "tbody", "tr", "th", "td"
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
}


def sanitize_html(html: Optional[str]) -> Optional[str]:
    """Sanitize user-provided HTML to prevent XSS. Returns None if input is None."""
    if not html:
        return html
    return nh3.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
