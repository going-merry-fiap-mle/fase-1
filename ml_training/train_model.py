import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from app.infrastructure.session_manager import get_session
from app.infrastructure.models.book import Book


def load_data_from_database():
    print("Loading data from database...")

    with get_session() as session:
        books = session.query(Book).all()

        data = []
        for book in books:
            data.append({
                'id': str(book.id),
                'title': book.title,
                'price': float(book.price) if book.price else 0.0,
                'rating': book.rating if book.rating else None,
                'availability': book.availability,
                'category_name': book.category.name if book.category else 'Unknown'
            })

    df = pd.DataFrame(data)
    print(f"{len(df)} books loaded")
    print(f"Rating distribution:\n{df['rating'].value_counts().sort_index()}\n")

    return df


def feature_engineering(df):
    print("Performing feature engineering...")

    df_clean = df.dropna(subset=['rating']).copy()
    print(f"{len(df) - len(df_clean)} books removed due to missing rating")
    print(f"{len(df_clean)} valid books for training\n")

    if len(df_clean) < 10:
        raise ValueError("Insufficient data for training (minimum: 10 books with rating)")

    df_clean['high_rating'] = (df_clean['rating'] >= 4).astype(int)

    le_category = LabelEncoder()
    df_clean['category_encoded'] = le_category.fit_transform(df_clean['category_name'])

    le_availability = LabelEncoder()
    df_clean['availability_encoded'] = le_availability.fit_transform(df_clean['availability'])

    X = df_clean[['price', 'category_encoded', 'availability_encoded']]
    y = df_clean['high_rating']

    encoders = {
        'category': le_category,
        'availability': le_availability
    }

    print(f"Data shape: X={X.shape}, y={y.shape}")
    print(f"Target distribution:")
    print(f"   - High ratings (>=4): {sum(y)} ({sum(y)/len(y)*100:.1f}%)")
    print(f"   - Low ratings (<4): {len(y)-sum(y)} ({(len(y)-sum(y))/len(y)*100:.1f}%)\n")

    return X, y, encoders


def train_model(X, y):
    print("Training Random Forest model...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"   - Train: {len(X_train)} samples")
    print(f"   - Test: {len(X_test)} samples")

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    print("Model trained successfully!\n")

    return model, X_test, y_test


def evaluate_model(model, X_test, y_test):
    print("Evaluating model performance...")

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2%}\n")

    print("Classification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Low Rating (<4)', 'High Rating (>=4)']
    ))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print()

    feature_names = ['price', 'category', 'availability']
    importances = model.feature_importances_

    print("Feature Importance:")
    for name, importance in zip(feature_names, importances):
        print(f"   - {name}: {importance:.4f}")
    print()


def save_model(model, encoders):
    print("Saving model and encoders...")

    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "rating_classifier_v1.pkl"
    joblib.dump(model, model_path)
    print(f"   Model saved at: {model_path}")

    encoders_path = models_dir / "encoders_v1.pkl"
    joblib.dump(encoders, encoders_path)
    print(f"   Encoders saved at: {encoders_path}")

    metadata = {
        'model_version': 'v1.0.0',
        'algorithm': 'RandomForestClassifier',
        'features': ['price', 'category', 'availability'],
        'target': 'high_rating (1 if rating >= 4, else 0)',
        'classes': ['Low Rating (<4)', 'High Rating (>=4)']
    }

    metadata_path = models_dir / "model_metadata.pkl"
    joblib.dump(metadata, metadata_path)
    print(f"   Metadata saved at: {metadata_path}\n")


def main():
    print("=" * 60)
    print("ML MODEL TRAINING - BOOK RATING PREDICTION")
    print("=" * 60)
    print()

    try:
        df = load_data_from_database()
        X, y, encoders = feature_engineering(df)
        model, X_test, y_test = train_model(X, y)
        evaluate_model(model, X_test, y_test)
        save_model(model, encoders)

        print("=" * 60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("   1. Model saved at models/rating_classifier_v1.pkl")
        print("   2. Run Flask application to load the model")
        print("   3. Use POST /api/v1/ml/predict endpoint for predictions")
        print()

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
