# Baseline Model Experiment

## Objective

Evaluate whether traditional machine learning algorithms can predict:

- Ticket Priority
- Customer Satisfaction Rating

using TF-IDF and structured features.

---

## Models Evaluated

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

---

## Dataset

Rows: 8469

Columns: 17

Target Classes

Ticket Priority

- Critical
- High
- Medium
- Low

Customer Satisfaction

- 1
- 2
- 3
- 4
- 5

---

## Results

| Model | Accuracy |
|--------|----------|
| Logistic Regression | 26.27% |
| Decision Tree | 25.86% |
| Random Forest | 25.27% |
| Gradient Boosting | 26.27% |

---

## Dataset Investigation

During qualitative inspection we observed:

- placeholder values
- repeated templates
- noisy text
- inconsistent relationship between ticket content and priority

---

## Conclusion

The baseline implementation is technically correct.

However,

the dataset does not provide sufficient signal for reliable priority prediction using traditional TF-IDF based models.

The baseline therefore serves as a benchmark rather than the final production model.

---

## Next Decision

Move to a modern NLP pipeline.

Potential improvements

- Better preprocessing
- Sentence embeddings
- Transformer models
- Cleaner dataset