# Timing Report — Week 2 Coding Assignment

Name: _______________________  Roll No.: _______________________

## Part 2: Empirical Timing vs. Predicted Growth

Compile and run `timing_harness.c` against your own `analysis.c`:

```
gcc -O2 -Wall -Wextra -o timing_harness timing_harness.c analysis.c
./timing_harness
```

Paste the three printed tables below exactly as produced.

### Table 1 — `linear_search` (predicted worst case: O(n))

```
(paste table here)
```

### Table 2 — `binary_search` (predicted worst case: O(log n))

```
(paste table here)
```

### Table 3 — `has_duplicate` (predicted worst case: O(n^2))

```
(paste table here)
```

## Questions (2-4 sentences each)

1. **Doubling `n` for `linear_search`.** Between two consecutive rows of
   Table 1 (n and 2n), what ratio would O(n) predict for the time? Is
   that roughly what you observed? If not, what do you think is going on
   (warm-up effects, measurement noise, cache behaviour)?

2. **Doubling `n` for `binary_search`.** What ratio would O(log n)
   predict when n doubles (hint: it is *not* close to 2)? Compare that
   prediction to Table 2.

3. **Doubling `n` for `has_duplicate`.** What ratio would O(n^2) predict
   when n doubles? Compare that prediction to Table 3, and contrast it
   with what you found for `linear_search` in Question 1 — this is the
   practical version of the lecture's "Numbers Side by Side" table.
