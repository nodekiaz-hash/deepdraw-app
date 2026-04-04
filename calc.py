import math


def process_calculation_logic(d: float, h: float, f: float, k: float) -> dict:
    """
    Deep drawing blank calculation

    Parameters:
        d: diameter
        h: height
        f: flange
        k: empirical correction factor

    Returns:
        dict with D0, Dreal, draw_ratio
    """

    # --- validation ---
    if d <= 0:
        raise ValueError("Diameter (d) must be > 0")

    # --- theoretical blank ---
    D0 = math.sqrt(d**2 + 4 * d * (h + f))

    # --- corrected blank ---
    Dreal = D0 * (1 + k)

    # --- draw ratio ---
    m = Dreal / d

    return {
        "D0": round(D0, 2),
        "Dreal": round(Dreal, 2),
        "draw_ratio": round(m, 2),
    }