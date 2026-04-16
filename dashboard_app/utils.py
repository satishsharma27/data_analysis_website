FONT = "Arial, Helvetica Neue, sans-serif"
BORDER = "#E8E6E0"
TEXT = "#2C2C2A"
MUTED = "#888780"
BLUE = "#378ADD"
TEAL = "#1D9E75"
CARD = "#FFFFFF"
AMBER = "#BA7517"
PINK = "#D4537E"
PURPLE = "#7F77DD"
GREEN = "#3B6D11"

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
