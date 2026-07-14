from pathlib import Path

import joblib
import pandas as pd

from scipy.sparse import hstack


BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "artifacts"


model = joblib.load(MODELS_DIR / "random_forest.pkl")

tfidf = joblib.load(
    MODELS_DIR / "tfidf_vectorizer.pkl"
)

priority_encoder = joblib.load(
    MODELS_DIR / "priority_encoder.pkl"
)

metadata_feature_names = joblib.load(
    MODELS_DIR / "metadata_feature_names.pkl"
)


metadata_columns = [
    "type",
    "queue",
    "tag_1",
    "tag_2",
    "tag_3",
    "tag_4"
]


def predict_priority(ticket: dict) -> str:

    df = pd.DataFrame([ticket])

    metadata = pd.get_dummies(
        df[metadata_columns],
        dtype=int
    )

    metadata = metadata.reindex(
        columns=metadata_feature_names,
        fill_value=0
    )

    text_features = tfidf.transform(df["text"])

    X = hstack([
        text_features,
        metadata.values
    ])

    prediction = model.predict(X)

    return priority_encoder.inverse_transform(
        prediction
    )[0]