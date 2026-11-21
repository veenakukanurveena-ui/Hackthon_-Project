from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


class ModelEvaluator:

    def evaluate(self, actual, predicted):

        if len(actual) != len(predicted):
            raise ValueError(
                "Actual and predicted labels must have equal length."
            )

        if len(actual) == 0:
            raise ValueError("Evaluation data cannot be empty.")

        # Labels: 0 = Normal, 1 = Anomaly
        accuracy = accuracy_score(actual, predicted)

        precision = precision_score(
            actual, predicted, zero_division=0
        )

        recall = recall_score(
            actual, predicted, zero_division=0
        )

        f1 = f1_score(
            actual, predicted, zero_division=0
        )

        matrix = confusion_matrix(
            actual, predicted, labels=[0, 1]
        )

        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": matrix.tolist(),
            "classification_report": classification_report(
                actual,
                predicted,
                labels=[0, 1],
                target_names=["Normal", "Anomaly"],
                zero_division=0
            )
        }


if __name__ == "__main__":

    # Example ground-truth labels
    actual = [0, 0, 1, 1, 0, 1, 0, 1]

    # Example model predictions
    predicted = [0, 0, 1, 1, 0, 0, 0, 1]

    evaluator = ModelEvaluator()

    results = evaluator.evaluate(actual, predicted)

    print("\nAI Model Evaluation Results:")

    for key, value in results.items():
        print(f"\n{key}:")
        print(value)
        