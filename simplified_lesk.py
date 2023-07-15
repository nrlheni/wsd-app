import json
from deep_translator import GoogleTranslator
from kbbi import KBBI, AutentikasiKBBI
from nltk.corpus import wordnet as wn
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support


class simplifed_lesk:

    # def __init__(self):
    #     self.preprocess =

    def set_dictionary(self, word):
        dictionary = []

        # Get the sense for the word from kbbi
        auth = AutentikasiKBBI("nurulakhni12@gmail.com", "Gmna10112")
        kbbi_result = json.dumps(KBBI(word, auth).serialisasi(), indent=2)
        kbbi_result_json = json.loads(kbbi_result)

        for entry in kbbi_result_json['entri']:
            # Loop over each 'makna' in this entry
            for makna in entry['makna']:
                definition = makna['submakna']
                example = makna['contoh']

                # replace -- to target word in 'contoh' if exist
                if bool(example):
                    example = [ex.replace("--", word) for ex in example]

                # Append the new dictionary to the result list
                def_example = {
                    'makna': "; ".join(definition),
                    'contoh': "; ".join(example)
                }

                dictionary.append(def_example)

        # Get the sense for the word from wordnet
        # synsets = wn.synsets(GoogleTranslator(
        #     source='id', target='en').translate(word))
        # for syn in synsets:
        #     definition = GoogleTranslator(source='en', target='id').translate(
        #         syn.definition())
        #     example = GoogleTranslator(source='en', target='id').translate(
        #         "; ".join(syn.examples()))

        #     def_example = {
        #         'kelas': syn.pos(),
        #         'makna': definition,
        #         'contoh': example
        #     }
        #     dictionary.append(def_example)

        return dictionary

    def predicted_sense(self, dictionary, context, word):
        max_overlap = 0
        predicted_sense = None

        for sense in dictionary:
            filtered_definition = preprocess(sense['makna'])
            filtered_example = preprocess(sense['contoh'])
            dictionary = set(filtered_definition).union(filtered_example)

            intersection = dictionary.intersection(
                context).difference(set({word}))

            overlap = len(intersection)
            if overlap > max_overlap:
                max_overlap = overlap
                predicted_sense = sense['makna']

        if max_overlap == 0:
            predicted_sense = dictionary[0]['makna']

        return predicted_sense, max_overlap

    def evaluate(self, actual_senses, predicted_senses):

        # Compute the confusion matrix
        labels = np.unique(actual_senses + predicted_senses)
        confusion_mat = confusion_matrix(
            actual_senses, predicted_senses, labels=labels)

        # Compute the classification report
        classification_rep = classification_report(
            actual_senses, predicted_senses, labels=labels)

        # Compute the accuracy
        accuracy = np.sum(np.diag(confusion_mat)) / np.sum(confusion_mat) * 100

        # Compute the precision, recall, and F1-score
        precision, recall, f1_score, _ = precision_recall_fscore_support(
            actual_senses, predicted_senses, average='weighted', zero_division=1)

        tp = sum([confusion_mat[i][i] for i in range(len(labels))])
        fp = sum([sum(confusion_mat[:, i]) - confusion_mat[i][i]
                  for i in range(len(labels))])
        fn = sum([sum(confusion_mat[i, :]) - confusion_mat[i][i]
                  for i in range(len(labels))])
        tn = len(actual_senses) - tp - fp - fn

        # Format the metrics as percentages
        accuracy = '{:.2f}%'.format(accuracy)
        precision = '{:.2f}%'.format(precision * 100)
        recall = '{:.2f}%'.format(recall * 100)
        f1_score = '{:.2f}%'.format(f1_score * 100)

        return tp, fp, fn, tn, accuracy, precision, recall, f1_score, classification_rep
