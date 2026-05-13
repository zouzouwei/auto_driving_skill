# Skill Benchmark: autonomous-driving-perception-code-reader

**Model**: claude-sonnet-4-6
**Date**: 2026-05-14T00:00:00Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 237.0s ± 57.3s | 164.6s ± 110.9s | +72.4s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes
- All expectations passed in both configurations, so these evals currently measure completeness more than skill-specific advantage.
- The with_skill runs were slower on camera and lane but faster on lidar; the single-run setup makes timing noisy.
- The strongest missing check is whether the reports correctly call out placeholder decode/loss behavior as incomplete implementation rather than real inference.
- The benchmark is useful as a documentation sanity check, but it is not yet a discriminative skill benchmark.
