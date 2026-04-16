def calculate_quality_score(error_type, severity):

    base_score = 10

    penalty_map = {
        "Factual Error": 3,
        "Hallucination": 4,
        "Logical Error": 2,
        "Bias": 2,
        "Clarity Issue": 1
    }

    penalty = penalty_map.get(error_type, 1)

    score = base_score - (penalty * severity / 5)

    return round(score, 2)