import math


# -------------------------
# 📐 MÉLYHÚZÁS SZÁMÍTÁS
# -------------------------
def calculate(d: float, h: float, f: float, k: float) -> dict:
    """
    Mélyhúzás teríték számítás

    Paraméterek:
    d - külső átmérő (mm)
    h - mélység (mm)
    f - lemezvastagság (mm)
    k - empirikus korrekciós faktor

    Visszatérés:
    dict → számítási eredmények
    """

    # --- alap validáció (biztonság)
    if d <= 0 or h <= 0 or f <= 0:
        raise ValueError("Invalid input values")

    # --- elméleti teríték
    D0 = math.sqrt(d**2 + 4 * d * (h + f))

    # --- korrigált teríték
    Dreal = D0 * (1 + k)

    # --- húzási arány
    draw_ratio = Dreal / d

    return {
        "D0": round(D0, 2),
        "Dreal": round(Dreal, 2),
        "draw_ratio": round(draw_ratio, 2)
    }