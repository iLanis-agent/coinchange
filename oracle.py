#!/usr/bin/env python3
# Change Math oracle - mirrors engine.js.
import json, math

def _amt(x, label, mx):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or math.floor(x) != x or x < 1 or x > mx:
        raise ValueError(f"{label} must be a whole number from 1 to {mx}")
    return int(x)

def _pieces(lst):
    if not isinstance(lst, list) or len(lst) < 1:
        raise ValueError("enter at least one piece value")
    if len(lst) > 12:
        raise ValueError("enter at most 12 piece values")
    seen = set()
    for x in lst:
        _amt(x, "piece value", 100000)
        if x in seen:
            raise ValueError("piece values must not repeat")
        seen.add(x)
    return sorted((int(x) for x in lst), reverse=True)

def _join(d): return ", ".join(str(x) for x in d)
def _n(k): return f"{k} piece" if k == 1 else f"{k} pieces"

def due_truth(price, paid):
    q = _amt(price, "price", 10000000); p = _amt(paid, "amount paid", 10000000)
    if p < q:
        return f"Short by {q - p}: paid {p} against a price of {q}."
    if p == q:
        return f"Paid exactly {q}; no change is due."
    return f"Change due is {p - q} (paid {p} against a price of {q})."

def few_truth(amount, lst):
    a = _amt(amount, "amount", 10000); d = _pieces(lst)
    INF = 10**9
    best = [0]; pick = [0]
    for v in range(1, a + 1):
        b = INF; c = 0
        for x in d:
            if x <= v and best[v - x] + 1 < b:
                b = best[v - x] + 1; c = x
        best.append(b); pick.append(c)
    if best[a] >= INF:
        return f"{a} cannot be made exactly from {_join(d)}."
    counts = {}; r = a
    while r > 0:
        counts[pick[r]] = counts.get(pick[r], 0) + 1; r -= pick[r]
    parts = [f"{counts[x]} x {x}" for x in d if counts.get(x)]
    out = f"The fewest pieces for {a} from {_join(d)} is {_n(best[a])}: {' + '.join(parts)}."
    k = 0; r = a
    for x in d:
        t = r // x; k += t; r -= t * x
    if r != 0:
        return out + f" Taking the largest piece each time gets stuck with {r} left over."
    if k == best[a]:
        return out + " Taking the largest piece each time gives the same count."
    return out + f" Taking the largest piece each time needs {_n(k)}, {k - best[a]} more."

def ways_truth(amount, lst):
    a = _amt(amount, "amount", 10000); d = _pieces(lst)
    w = [1] + [0] * a
    for x in d:
        for s in range(x, a + 1):
            w[s] += w[s - x]
    n = w[a]
    if n == 0:
        return f"There are no ways to make {a} exactly from {_join(d)}."
    if n == 1:
        return f"There is 1 way to make {a} from {_join(d)}, counting different orders as one way."
    return f"There are {n} ways to make {a} from {_join(d)}, counting different orders as one way."

FNS = {"dueTruth": due_truth, "fewTruth": few_truth, "waysTruth": ways_truth}
US = [100, 50, 25, 10, 5, 1]
CASES = [
    ("dueTruth", [925, 1000]), ("dueTruth", [1000, 1000]), ("dueTruth", [1000, 925]), ("dueTruth", [1, 10000000]),
    ("dueTruth", [10000000, 1]), ("dueTruth", [1, 2]), ("dueTruth", [0, 5]), ("dueTruth", [5, 0]), ("dueTruth", [10000001, 5]), ("dueTruth", [5, 2.5]), ("dueTruth", [-5, 5]),
    ("fewTruth", [6, [1, 3, 4]]), ("fewTruth", [41, [25, 10, 5, 1]]), ("fewTruth", [99, US]), ("fewTruth", [3, [5, 2]]),
    ("fewTruth", [7, [5, 2]]), ("fewTruth", [1, [1]]), ("fewTruth", [10000, [1]]), ("fewTruth", [30, [25, 10, 1]]),
    ("fewTruth", [3, [5, 4]]), ("fewTruth", [12, [6, 4, 1]]), ("fewTruth", [8, [4]]), ("fewTruth", [10000, [100, 50, 25, 10, 5, 1]]),
    ("fewTruth", [0, [1, 2]]), ("fewTruth", [10001, [1]]), ("fewTruth", [5, []]), ("fewTruth", [5, [1, 1]]), ("fewTruth", [5, [0, 1]]),
    ("fewTruth", [5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]), ("fewTruth", [5, [1.5]]), ("fewTruth", [5, 3]),
    ("waysTruth", [100, US]), ("waysTruth", [10, [1, 5, 10]]), ("waysTruth", [4, [1, 2, 3]]), ("waysTruth", [3, [2]]),
    ("waysTruth", [8, [4]]), ("waysTruth", [1, [1]]), ("waysTruth", [10000, US]), ("waysTruth", [200, [200, 100, 50, 20, 10, 5, 2, 1]]),
    ("waysTruth", [0, [1]]), ("waysTruth", [10001, [1]]), ("waysTruth", [5, []]), ("waysTruth", [5, [2, 2]]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
