"""
Quick Training Script for Random Forest Model
Run this to train the ML model before starting the service
"""
import sys
from pathlib import Path

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
        n_samples=20000,
        n_estimators=800,
        max_depth=20,
        save_model=True
    )
    
    print()
    print("=" * 60)
    print("  Training Complete!")
    print("=" * 60)

    print(f"  Test Accuracy:  {metrics['test_accuracy']:.2%}")
    print(f"  Features:       {metrics['n_features']}")
    print(f"  Classes:        {metrics['n_classes']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
