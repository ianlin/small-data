@outputSchema("score:INT")
def score_map(score):
    if not score:
        return 0
    score = int(score)
    if score == 1:
        return 100
    elif score == 2:
        return 90
    elif score == 3:
        return 80
    elif score == 4:
        return 70
    elif score == 5:
        return 60
    elif score <= 10:
        return 50
    elif score <= 20:
        return 40
    elif score <= 30:
        return 30
    elif score <= 40:
        return 20
    elif score <= 50:
        return 10
    elif score <= 100:
        return 5
    else:
        return 0
