def check_condition(area, slope):
    if area < 0.5 and slope > 0.001:
        return True
    else:
        return False