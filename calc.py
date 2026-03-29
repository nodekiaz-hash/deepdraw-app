def calculate(d, h, f, k):
    import math
    
    # elméleti teríték
    D0 = math.sqrt(d**2 + 4*d*(h+f))
    
    # korrigált teríték (empirikus)
    Dreal = D0 * (1 + k)
    
    # húzási arány
    m = Dreal / d

    return {
        "D0": round(D0, 2),
        "Dreal": round(Dreal, 2),
        "draw_ratio": round(m, 2)
    }