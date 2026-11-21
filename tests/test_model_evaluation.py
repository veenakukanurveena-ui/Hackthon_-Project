from research.model_evaluation import ModelEvaluator


def test_evaluation_returns_metrics():
    evaluator = ModelEvaluator()

    actual = [0, 0, 1, 1, 0, 1]
    predicted = [0, 0, 1, 0, 0, 1]

    result = evaluator.evaluate(actual, predicted)

    assert "accuracy" in result
    assert "precision" in result
    assert "recall" in result
    assert "f1_score" in result
    assert "confusion_matrix" in result


def test_evaluation_returns_valid_accuracy():
    evaluator = ModelEvaluator()

    actual = [0, 0, 1, 1]
    predicted = [0, 1, 1, 1]

    result = evaluator.evaluate(actual, predicted)

    assert 0 <= result["accuracy"] <= 1
    