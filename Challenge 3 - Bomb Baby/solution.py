# 

# Your code goes here.

def multiplier(a, b):
    difference = a - b
    multiplier = (difference / b) + 1
    return multiplier

def solution(x, y):
    step, m, f = 0, int(x), int(y)
    while True:
        if m <= 0 or f <= 0:
            break
        if m > 100 or f > 100:
            if m > f:
                mul = multiplier(m, f)
                m -= f * mul
                step += mul
            elif f > m:
                mul = multiplier(f, m)
                f -= m * mul
                step += mul
            else:
                break
        else:
            if m > f:
                m -= f
            elif f > m:
                f -= m
            else:
                break
            step += 1
    
    if m == 1 and f == 1 and step >= 0:
        return str(step)
    return 'impossible'