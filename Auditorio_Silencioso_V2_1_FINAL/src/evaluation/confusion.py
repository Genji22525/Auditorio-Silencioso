def confusion_counts(*, ground_truth_positive: bool, detected_positive: bool):
    # This primitive is intentionally generic. A complete FP/FN experiment
    # requires a declared benign/negative evidence population.
    if ground_truth_positive and detected_positive:
        return {"tp": 1, "fp": 0, "fn": 0, "tn": 0}
    if ground_truth_positive and not detected_positive:
        return {"tp": 0, "fp": 0, "fn": 1, "tn": 0}
    if not ground_truth_positive and detected_positive:
        return {"tp": 0, "fp": 1, "fn": 0, "tn": 0}
    return {"tp": 0, "fp": 0, "fn": 0, "tn": 1}
