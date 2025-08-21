"""Configuration defaults for nbapack engines and outputs."""

K_FACTOR = 32.0
INIT_RATING = 1500.0

TRUESKILL_MU = 25.0
TRUESKILL_SIGMA = 25.0/3.0
TRUESKILL_BETA = 25.0/6.0
TRUESKILL_TAU = 25.0/300.0
TRUESKILL_DRAW_PROB = 0.0

# Output filenames
OUT_RATINGS_PATTERN = "ratings_{engine}.csv"
OUT_RESULTS_WITH_PRED = "results_with_predictions.csv"
OUT_ACCURACY_SUMMARY = "engine_accuracy_summary.csv"
OUT_SCORE_SUMMARY = "engine_score_summary.csv"
