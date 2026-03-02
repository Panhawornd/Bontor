"""
Training Script for Random Forest Model
Run this to train the ML model before starting the service

Improvements:
- Per-major profiles (not per-category)
- Interaction features (STEM avg, language avg, ratios)
- StandardScaler for feature scaling
- Cross-validation metrics
- Per-class classification report
"""
import sys
from pathlib import Path
import numpy as np

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ml.train_rf import train_random_forest
from data.majors import MAJOR_DATABASE


def main():
    print("=" * 60)
    print("  NLP + ML Recommendation System - Model Training")
    print("=" * 60)
    print()
    print(f"Training with {len(MAJOR_DATABASE)} majors")
    print()
    
    # Train the model
    model, metrics = train_random_forest(
        majors_database=MAJOR_DATABASE,
        n_samples=50000,
        n_estimators=1000,
        max_depth=30,
        tune_hyperparams=True,
    )
    
    print()
    print("=" * 60)
    print("  Training Complete!")
    print("=" * 60)

    print(f"  Test Accuracy:   {metrics['test_accuracy']:.2%}")
    print(f"  Precision(w):    {metrics['test_precision_weighted']:.2%}")
    print(f"  Recall(w):       {metrics['test_recall_weighted']:.2%}")
    print(f"  Precision(m):    {metrics['test_precision_macro']:.2%}")
    print(f"  Recall(m):       {metrics['test_recall_macro']:.2%}")
    print(f"  CV Accuracy:     {metrics['cv_accuracy_mean']:.2%} "
          f"(+/- {metrics['cv_accuracy_std'] * 2:.2%})")
    if metrics.get("tuning_enabled"):
        print(f"  Tuning CV Best:  {metrics['tuning_best_cv_accuracy']:.2%}")
        print(f"  Best Params:     {metrics['tuning_best_params']}")
    print(f"  Features:        {metrics['n_features']}")
    print(f"  Classes:         {metrics['n_classes']}")

    print("\n  Confusion Matrix (rows=true, cols=pred):")
    print(np.array(metrics["confusion_matrix"]))
    print(f"\n  Total test samples (count): {metrics['test_total_samples']}")
    print("  Per-class test sample counts:")
    for major, count in metrics["test_samples_per_class"].items():
        print(f"    - {major}: {count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
