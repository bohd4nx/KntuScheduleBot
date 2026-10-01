from aiogram.utils.text_decorations import html_decoration


def quote_html(text: str) -> str:
    """Екранує текст для безпечної вставки в HTML-повідомлення."""
    return html_decoration.quote(text)
