from io import StringIO
import json
import numpy as np
import openpyxl
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from pycm import ConfusionMatrix


class Evaluation:
    def __init__(self, actual_sense, predicted_sense):
        self.actual_sense = actual_sense
        self.predicted_sense = predicted_sense

    def evaluate(self):
        cm = ConfusionMatrix(actual_vector=np.array(self.actual_sense),
                             predict_vector=np.array(self.predicted_sense))

        return cm


if __name__ == '__main__':
    # read in the data from the Excel file
    path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/dataset/origin_dataset.xlsx'
    df = pd.read_excel(path)

    # Extract the sentences, target words, ground truth senses, and predicted senses from the DataFrame

    # actual_sense = df['Actual Sense'].str.replace('\xa0', ' ').tolist()
    # predicted_senses = df['Predicted Sense'].str.replace('\xa0', ' ').tolist()

    # wsd_evaluation = Evaluation(actual_sense, predicted_senses)
    # result = wsd_evaluation.evaluate()
    # print(result.table)

    # print(result.save_stat(
    #     'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/overall_state.json', summary=True))
    # res = []
    # value = {
    #     'TP': result.TP,
    #     'FP': result.FP,
    #     'TN': result.TN,
    #     'FN': result.FN
    # }
    # res.append(value)
    # print(res)
    # with open('D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/overall_state.json', 'w') as file:
    #     json.dump(res, file)

    # Load the statistics from a JSON file
    with open('D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/overall_state_2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # for d in data:
    #     accuracy_dict = {}
    #     for key in d["TP"]:
    #         TP = d["TP"][key]
    #         TN = d["TN"][key]
    #         FP = d["FP"][key]
    #         FN = d["FN"][key]

    #         accuracy = round((TP + TN) / float(TP + TN + FP + FN), 2)

    #         if TP + FP == 0:
    #             precision = 0.00
    #         else:
    #             precision = round(TP / float(TP + FP), 2)

    #         if TP + FN == 0:
    #             recall = 0.00
    #         else:
    #             recall = round(TP / float(TP + FN), 2)

    #         if precision + recall == 0:
    #             f1score = 0.00
    #         else:
    #             f1score = round((2 * precision * recall) /
    #                             float(precision + recall), 2)

    #         d["Accuracy"][key] = accuracy
    #         d["Precision"][key] = precision
    #         d["Recall"][key] = recall
    #         d["F1_score"][key] = f1score

    # create a new list to store the transformed data
    # result = []

    # for d in data:
    #     for c in d['TP']:
    #         result.append({
    #             "class": c,
    #             "TP": d['TP'][c],
    #             "TN": d['TN'][c],
    #             "FP": d['FP'][c],
    #             "FN": d['FN'][c],
    #             "Accuracy": d['Accuracy'][c],
    #             "Precision": d['Precision'][c],
    #             "Recall": d['Recall'][c],
    #             "F1-score": d['F1_score'][c]
    #         })

    # print(result)

    classes = {}
    total_TP = 0
    total_TN = 0
    total_FP = 0
    total_FN = 0
    total_accuracy = 0
    total_precision = 0
    total_recall = 0
    total_f1score = 0

    for item in data:
        class_name = item['class']
        classes[class_name] = item
        TP = item['TP']
        FP = item['FP']
        FN = item['FN']
        TN = item['TN']
        TN = TN / (FP + TN)

        total_TP += TP
        total_TN += TN
        total_FP += FP
        total_FN += FN

    accuracy = round((total_TP + TN) / (total_TP + TN + FP + FN), 2)

    if total_TP + total_FP == 0:
        precision = 0.00
    else:
        precision = round(total_TP / (total_TP + total_FP), 2)

    if total_TP + total_FN == 0:
        recall = 0.00
    else:
        recall = round(total_TP / (total_TP + total_FN), 2)

    if precision + recall == 0:
        f1score = 0.00
    else:
        f1score = round(2 * precision * recall / (precision + recall), 2)

    overall_evaluation = {
        'TP': total_TP,
        'TN': total_TN,
        'FP': total_FP,
        'FN': total_FN,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1score': f1score
    }

    result = [{'Overall_evaluation': overall_evaluation,
               'Class_evaluation': list(classes.values())}]

    print(json.dumps(overall_evaluation, indent=4))
    # Write the updated dictionary back to the file
    # with open('D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/overall_state_3.json', 'w') as f:
    #     json.dump(result, f)
