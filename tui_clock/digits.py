"""ASCII art digit definitions for the clock display."""

# Large ASCII art digits (7 lines tall, 6 characters wide each)
LARGE_DIGITS = {
    "0": [
        " ████ ",
        "██  ██",
        "██  ██",
        "██  ██",
        "██  ██",
        "██  ██",
        " ████ ",
    ],
    "1": [
        "  ██  ",
        " ███  ",
        "  ██  ",
        "  ██  ",
        "  ██  ",
        "  ██  ",
        " ████ ",
    ],
    "2": [
        " ████ ",
        "██  ██",
        "    ██",
        "  ██  ",
        " ██   ",
        "██    ",
        "██████",
    ],
    "3": [
        " ████ ",
        "██  ██",
        "    ██",
        "  ███ ",
        "    ██",
        "██  ██",
        " ████ ",
    ],
    "4": [
        "██  ██",
        "██  ██",
        "██  ██",
        "██████",
        "    ██",
        "    ██",
        "    ██",
    ],
    "5": [
        "██████",
        "██    ",
        "█████ ",
        "    ██",
        "    ██",
        "██  ██",
        " ████ ",
    ],
    "6": [
        " ████ ",
        "██    ",
        "█████ ",
        "██  ██",
        "██  ██",
        "██  ██",
        " ████ ",
    ],
    "7": [
        "██████",
        "    ██",
        "   ██ ",
        "  ██  ",
        "  ██  ",
        "  ██  ",
        "  ██  ",
    ],
    "8": [
        " ████ ",
        "██  ██",
        "██  ██",
        " ████ ",
        "██  ██",
        "██  ██",
        " ████ ",
    ],
    "9": [
        " ████ ",
        "██  ██",
        "██  ██",
        " █████",
        "    ██",
        "    ██",
        " ████ ",
    ],
    ":": [
        "      ",
        "  ██  ",
        "  ██  ",
        "      ",
        "  ██  ",
        "  ██  ",
        "      ",
    ],
}


def render_time_large(time_str: str) -> str:
    """Render a time string (e.g., '14:30') as large ASCII art.

    Args:
        time_str: Time string in format 'HH:MM'

    Returns:
        Multi-line string of ASCII art representation
    """
    lines = [""] * 7

    for char in time_str:
        if char in LARGE_DIGITS:
            digit_lines = LARGE_DIGITS[char]
            for i, digit_line in enumerate(digit_lines):
                lines[i] += digit_line + " "

    return "\n".join(lines)
