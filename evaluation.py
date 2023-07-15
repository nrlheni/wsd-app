import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json


class Evaluation:
    def __init__(self, actual_senses, predicted_senses):
        self.actual_senses = actual_senses
        self.predicted_senses = predicted_senses

    def label_data(self):
        actual_labels = []
        predicted_labels = []

        for actual_senses, predicted_sense in zip(self.actual_senses, self.predicted_senses):
            if actual_senses == predicted_sense:
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

        accuracy = (correct_predictions / total_instances) * 100
        return accuracy


if __name__ == '__main__':
    # read in the data from the Excel file
    path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/asset/data/origin_dataset_v4.xlsx'
    df = pd.read_excel(path)

    actual_senses = df['Actual Sense'].tolist()
    predicted_senses = df['Predicted Sense'].tolist()

    wsd_evaluation = Evaluation(actual_senses, predicted_senses)

    if 'Label' not in df.columns:
        actual_labels, predicted_labels = wsd_evaluation.label_data()
        df['Label'] = predicted_labels
        df.to_excel(path, index=False)

    accuracy = wsd_evaluation.calculate_accuracy()
    print(accuracy)

    evaluation_result = {
        'accuracy': '{:.2f}%'.format(accuracy)
    }

    print(json.dumps(evaluation_result, indent=2))
