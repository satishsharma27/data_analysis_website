FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif"
BORDER = "rgba(255,255,255,0.08)"
TEXT = "#f0f0f0"
MUTED = "#888888"
BLUE = "#4f8ef7"
TEAL = "#2ec4a0"
CARD = "#151515"
AMBER = "#f0a500"
PINK = "#e8714a"
PURPLE = "#a78bfa"
GREEN = "#2ec4a0"

CATEGORY_COLORS = {
    "social": BLUE,
    "search": TEAL,
    "influencer": AMBER,
    "media": PINK,
}


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_number(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.0f}"
