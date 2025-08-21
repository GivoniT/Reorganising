# NBA Rating Package

This package restructures the original `Elo_Computation.py` script into a clean module.

## Usage

Run the full pipeline and generate artifacts:

```bash
python -m nbapack
```

This will create an `artifacts/` directory containing:

- `ratings_{engine}.csv` for each engine
- `{engine}_ratings_over_time.png` for each engine
- `results_with_predictions.csv`
- `engine_accuracy_summary.csv`
- `engine_score_summary.csv`

The data files are expected under `Datasets_Analysis/Datasets/`.
