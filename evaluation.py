import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json
from pathlib import Path


class Evaluation:
    def __init__(self, actual_senses, predicted_senses):
        self.actual_senses = actual_senses
        self.predicted_senses = predicted_senses

    def label_data(self):
        actual_labels = []
        predicted_labels = []

        for actual_sense, predicted_sense in zip(self.actual_senses, self.predicted_senses):
            if actual_sense == predicted_sense:
                actual_labels.append(1)
                predicted_labels.append(1)
            else:
                actual_labels.append(1)
                predicted_labels.append(0)

        return actual_labels, predicted_labels

    def calculate_accuracy(self):
        actual_labels, predicted_labels = self.label_data()

        correct_predictions = sum(1 for actual, predicted in zip(
            actual_labels, predicted_labels) if actual == predicted)
        total_instances = len(actual_labels)
        failed_predictions = total_instances - correct_predictions
        accuracy = (correct_predictions / total_instances) * 100

        return accuracy, correct_predictions, failed_predictions


if __name__ == '__main__':
    # read in the data from the Excel file
    # path = Path('asset/data/origin_dataset_stemming.xlsx') # 57.67%
    # path = Path('asset/data/origin_dataset_stopword.xlsx')  # 54.67%
    path = Path('asset/data/origin_dataset_stemming_stopword.xlsx')  # 58%
    # path = Path('asset/data/origin_dataset_tanpa_stemming_stopword.xlsx')  # 57.33%

    df = pd.read_excel(path)

    actual_senses = df['Actual Sense'].tolist()
    predicted_senses = df['Predicted Sense'].tolist()

    wsd_evaluation = Evaluation(actual_senses, predicted_senses)

    if 'Label' not in df.columns:
        actual_labels, predicted_labels = wsd_evaluation.label_data()
        df['Label'] = predicted_labels
        df.to_excel(path, index=False)

    accuracy, correct, failed = wsd_evaluation.calculate_accuracy()
    print(accuracy)

    evaluation_result = {
        'accuracy': '{:.2f}%'.format(accuracy),
        'correct': correct,
        'failed': failed,
    }

    print(json.dumps(evaluation_result, indent=2))
