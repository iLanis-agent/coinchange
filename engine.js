// Change Math engine - change due, fewest pieces for an amount, and the number of ways to make it.
// Mirrored by oracle.py; keep the op order identical.
// Amounts are whole numbers of the smallest unit. Piece values are owner-entered whole numbers.

function _amt(x, label, max) {
  if (typeof x !== "number" || !isFinite(x) || Math.floor(x) !== x || x < 1 || x > max) {
    throw new Error(label + " must be a whole number from 1 to " + max);
  }
  return x;
}

function _pieces(list) {
  if (!Array.isArray(list) || list.length < 1) throw new Error("enter at least one piece value");
  if (list.length > 12) throw new Error("enter at most 12 piece values");
  var seen = {};
  for (var i = 0; i < list.length; i++) {
    _amt(list[i], "piece value", 100000);
    if (seen[list[i]]) throw new Error("piece values must not repeat");
    seen[list[i]] = true;
  }
  return list.slice().sort(function (a, b) { return b - a; });
}

function _join(d) { return d.join(", "); }
function _n(k) { return k + (k === 1 ? " piece" : " pieces"); }

// The due truth: what comes back from a payment.
function dueTruth(price, paid) {
  var q = _amt(price, "price", 10000000), p = _amt(paid, "amount paid", 10000000);
  if (p < q) return "Short by " + (q - p) + ": paid " + p + " against a price of " + q + ".";
  if (p === q) return "Paid exactly " + q + "; no change is due.";
  return "Change due is " + (p - q) + " (paid " + p + " against a price of " + q + ").";
}

function _greedy(a, d) {
  var k = 0, r = a;
  for (var i = 0; i < d.length; i++) {
    var t = Math.floor(r / d[i]);
    k += t; r -= t * d[i];
  }
  return { k: k, r: r };
}

// The fewest truth: the fewest pieces for an amount, against always taking the largest piece.
function fewTruth(amount, list) {
  var a = _amt(amount, "amount", 10000), d = _pieces(list);
  var INF = 1e9, best = [0], pick = [0];
  for (var v = 1; v <= a; v++) {
    var b = INF, c = 0;
    for (var i = 0; i < d.length; i++) {
      if (d[i] <= v && best[v - d[i]] + 1 < b) { b = best[v - d[i]] + 1; c = d[i]; }
    }
    best.push(b); pick.push(c);
  }
  if (best[a] >= INF) return a + " cannot be made exactly from " + _join(d) + ".";
  var counts = {}, r = a;
  while (r > 0) { counts[pick[r]] = (counts[pick[r]] || 0) + 1; r -= pick[r]; }
  var parts = [];
  for (var j = 0; j < d.length; j++) if (counts[d[j]]) parts.push(counts[d[j]] + " x " + d[j]);
  var out = "The fewest pieces for " + a + " from " + _join(d) + " is " + _n(best[a]) + ": " + parts.join(" + ") + ".";
  var g = _greedy(a, d);
  if (g.r !== 0) return out + " Taking the largest piece each time gets stuck with " + g.r + " left over.";
  if (g.k === best[a]) return out + " Taking the largest piece each time gives the same count.";
  return out + " Taking the largest piece each time needs " + _n(g.k) + ", " + (g.k - best[a]) + " more.";
}

// The ways truth: how many different mixes of pieces make an amount (order does not count).
function waysTruth(amount, list) {
  var a = _amt(amount, "amount", 10000), d = _pieces(list);
  var w = [1n];
  for (var v = 1; v <= a; v++) w.push(0n);
  for (var i = 0; i < d.length; i++) {
    for (var s = d[i]; s <= a; s++) w[s] += w[s - d[i]];
  }
  var n = w[a];
  if (n === 0n) return "There are no ways to make " + a + " exactly from " + _join(d) + ".";
  if (n === 1n) return "There is 1 way to make " + a + " from " + _join(d) + ", counting different orders as one way.";
  return "There are " + n.toString() + " ways to make " + a + " from " + _join(d) + ", counting different orders as one way.";
}
