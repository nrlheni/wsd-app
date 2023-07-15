import csv
import json
import unicodedata
from flask import Flask, render_template, request
from WSD import SimplifiedLesk
from evaluation import Evaluation
import pandas as pd
import excel2json

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/wsd", methods=["POST"])
def wsd():
    data = request.get_json()
    sentences = data['sentences']
    word = data['word']
    sense = []
    for sentence in sentences:
        wsd = SimplifiedLesk(sentence, word)
        predict_sense = wsd.predict_sense()
        sense.append(predict_sense)

    return sense


@app.route("/evaluate", methods=["POST"])
def eval():
    # Retrieve the selected data value
    number_rows = int(request.form.get('number_rows'))

    if number_rows == 100:
        range_end = 101
    elif number_rows == 200:
        range_end = 201
    elif number_rows == 300:
        range_end = 301
    else:
        range_end = 101

    # read in the data from the Excel file
    path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/asset/data/origin_dataset_v4.xlsx'
    df = pd.read_excel(path)

    actual_senses = df[1:range_end]['Actual Sense'].tolist()
    predicted_senses = df[1:range_end]['Predicted Sense'].tolist()
    wsd_evaluation = Evaluation(actual_senses, predicted_senses)

    if 'Label' not in df.columns:
        actual_labels, predicted_labels = wsd_evaluation.label_data()
        df['Label'] = predicted_labels
        df.to_excel(path, index=False)

    accuracy = wsd_evaluation.calculate_accuracy()

    count_predict_success = df[1:range_end]['Label'].value_counts().get(1, 1)
    count_predict_failed = df[1:range_end]['Label'].value_counts().get(0, 0)

    df['label'] = df.apply(
        lambda row: 'Tidak Sesuai' if row['Label'] == 0 else 'Sesuai', axis=1)
    data = df[1:range_end].to_dict(orient='records')

    evaluation_result = {
        'accuracy': '{:.2f}%'.format(accuracy),
        'number_of_predict_success': int(count_predict_success),
        'number_of_predict_failed': int(count_predict_failed),
        'data': data
    }

    return evaluation_result


if __name__ == "__main__":
    app.run(debug=True)
