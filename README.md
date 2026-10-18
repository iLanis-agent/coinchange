# Change Math

Making change arithmetic. Handing back the biggest piece first is not always the fewest pieces.

## What it computes

- **The due truth** - change due on a payment, or how short the payment is.
- **The fewest truth** - the fewest pieces for an amount from piece values you enter, one way to build it, and whether always taking the largest piece gives the same count, more, or gets stuck.
- **The ways truth** - how many different mixes of pieces make the amount, counting different orders as one way. Computed exactly with big integers.

Amounts are whole numbers of the smallest unit. Prices and payments run 1 to 10000000, amounts for the other two panels 1 to 10000, piece values 1 to 100000, up to 12, no repeats.

## Boundary

Arithmetic only. Change Math does not know which coins, notes or rounding rules a shop, country or machine uses. Check those where they apply.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (43 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/coinchange/
Repo: https://github.com/iLanis-agent/coinchange
