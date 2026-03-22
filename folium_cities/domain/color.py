def color_for_user(user_id: int, palette: tuple[str, ...]) -> str:
    if not palette:
        raise ValueError("Color palette cannot be empty.")

    # Use modulo to keep a stable color assignment without index overflows.
    return palette[(user_id - 1) % len(palette)]

