import re
import json
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from deep_translator import GoogleTranslator
from kbbi import KBBI, AutentikasiKBBI
from nltk.corpus import wordnet as wn
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score


class Preprocessing:
    def __init__(self):
        pass

    def tokenize(self, sentence):
        lower_sentence = sentence.lower()
        text = '' .join((t for t in lower_sentence if not t.isdigit()))
        token = re.findall(r'\b\w+\b', text)
        ordered_tokens = set()
        result = []
        for word in token:
            if word not in ordered_tokens:
                ordered_tokens.add(word)
                result.append(word)

        return result

    def stopword_removal(self, token):
        stopword = open("./asset/stopword/stopword.txt").read()
        filtered_tokens = [
            t for t in token if t not in stopword]

        return filtered_tokens

    def stem(self, filtered_tokens):
        stemmer = StemmerFactory().create_stemmer()
        stemmed_tokens = [stemmer.stem(
            token) for token in filtered_tokens]

        return stemmed_tokens

    def pipeline(self, sentence):
        token = self.tokenize(sentence)
        token = self.stopword_removal(token)
        token = self.stem(token)

        return token


class SimplifiedLesk:

    def __init__(self, sentence, word):
        self.sentence = sentence
        self.word = word.lower().join((w for w in self.word if not w.isdigit()))
        self.preprocess = Preprocessing()

    def _set_dictionary(self, word):
        dictionary = []

        # Get the sense for the word from kbbi
        auth = AutentikasiKBBI("nurulakhni12@gmail.com", "Gmna10112")
        kbbi_result = json.dumps(KBBI(word, auth).serialisasi(), indent=2)
        kbbi_result_json = json.loads(kbbi_result)

        for entry in kbbi_result_json['entri']:
            # Loop over each 'makna' in this entry
            for makna in entry['makna']:
                class_type = makna['kelas']
                if class_type:
                    class_type = makna['kelas'][0]['nama'].lower()
                definition = makna['submakna']
                definition = [d.replace("...", word) for d in definition]
                example = makna['contoh']

                # replace -- to target word in 'contoh' if exist
                if bool(example):
                    example = [ex.replace("--", word) for ex in example]

                # Append the new dictionary to the result list
                def_example = {
                    'kelas': class_type,
                    'makna': "; ".join(definition),
                    'contoh': "; ".join(example)
                }

                dictionary.append(def_example)

        return dictionary

    def _preprocess_dict(self, dictionary):
        preprocessed_dict = []
        filtered_example = []
        for sense in dictionary:
            filtered_definition = self.preprocess.pipeline(
                sense['makna'])
            if 'contoh' in sense and sense['contoh']:
                filtered_example = self.preprocess.pipeline(
                    sense['contoh'])
            result = {
                'makna': filtered_definition,
                'contoh': filtered_example
            }
            preprocessed_dict.append(result)

        return preprocessed_dict

    def _get_intersect(self, context, dictionary):
        if self.word in context:
            context.remove(self.word)
        context = set(context)
        word = set({self.word})
        dictionary = self._preprocess_dict(dictionary)
        overlap_scores = {}
        for i, sense in enumerate(dictionary):
            sense_dict = set(sense['makna'])
            if 'contoh' in sense and sense['contoh']:
                example_dict = set(sense['contoh'])
                sense_dict |= example_dict
            print('preprocess dict: ', sense_dict)
            intersection = sense_dict.intersection(
                context).difference(word)
            print('intersect-makna-'+str(i)+' : ', intersection)
            overlap_scores[i] = len(intersection)

        return overlap_scores

    def _calculate_overlap(self, overlap_score):
        max_overlap = max(overlap_score, key=overlap_score.get)

        return max_overlap

    def _get_sense_by_overlap_index(self, dictionary, max_overlap_index):
        sense = dictionary[max_overlap_index]['makna']
        class_type = dictionary[max_overlap_index]['kelas']

        return sense, class_type

    def predict_sense(self):
        context = self.preprocess.pipeline(self.sentence)
        dictionary = self._set_dictionary(self.word)
        overlap_scores = self._get_intersect(context, dictionary)
        max_overlap = self._calculate_overlap(overlap_scores)
        sense, class_type = self._get_sense_by_overlap_index(
            dictionary, max_overlap)
        predicted_sense = {
            'word': self.word,
            'sentence': self.sentence,
            'sense': sense,
            'type': class_type
        }

        return predicted_sense


if __name__ == '__main__':
    # read in the data from the Excel file
    path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/asset/data/origin_dataset_stemming_stopword.xlsx'
    # path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/asset/data/origin_dataset_tanpa_stemming_stopword.xlsx'
    # path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/asset/data/origin_dataset_stemming.xlsx'
    # path = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/asset/data/origin_dataset_stopword.xlsx'
    df = pd.read_excel(path)

    # loop through the pairs of values in columns A and B
    results = []
    for index, row in df.iterrows():
        sentence = row['Kalimat']
        word = row['Kata Ambigu']

        wsd = SimplifiedLesk(
            sentence, word)
        # Define the context sentence and the ambiguous word
        predict_sense = wsd.predict_sense()

        print(predict_sense)

        results.append(predict_sense['sense'])

    # Add the results to a new column in the DataFrame
    df['Predicted Sense'] = results

    # Write the updated DataFrame back to the Excel file
    df.to_excel(path, index=False)
