import random
from kbbi import AutentikasiKBBI, KBBI
import json
import nltk
from nltk.corpus import wordnet as wn
from deep_translator import GoogleTranslator

# Get the synsets for the word
# synsets = wn.synsets('get up')
# synsets = wn.synsets(GoogleTranslator(
#     source='id', target='en').translate("dalam"))

# # Print the definition of the first synset in the list
# print(synsets)

# result = []
# for syn in synsets:
#     definition = GoogleTranslator(source='en', target='id').translate(
#         syn.definition())
#     example = GoogleTranslator(source='en', target='id').translate(
#         "; ".join(syn.examples()))

#     # print(definition)
#     # print(example)
#     # print(synset.pos())

#     result.append(definition)

# print(result)
# def translate(text, dest='en'):
#     translator = Translator()
#     return translator.translate(text, dest=dest).text

# def get_synonyms(word, pos):
#     synonyms = set()
#     for syn in wn.synsets(word, pos=pos):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms
from WSD import Preprocessing

file_path = "D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/article-segmentation.txt"
output_file_path = "D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/ambigous-word.txt"
auth = AutentikasiKBBI("nurulakhni12@gmail.com", "Gmna10112")

# sentence = "Pada era gempuran media sosial seperti saat ini fenomena ketidakamanan insecurity telah merambah pada hampir seluruh kalangan usia termasuk remaja"

# with open(file_path, "r") as input_file, open(output_file_path, "w") as output_file:
#     for line in input_file:
#         # Process each line here
#         sentence = line.strip()  # Remove leading/trailing whitespace
#         pre = Preprocessing()
#         tokens = pre.pipeline(sentence)
sentence = "Dalam penelitiannya yang berjudul Analisis Self love dalam Kumpulan Cerita Anak Majalah Bobo disimpulkan bahwa cerita anak dalam majalah Bobo mengandung aspek aspek cinta diri sendiri yang tersirat yang dapat mengembangkan sikap cinta diri sendiri pada anak melalui cara yang menyenangkan yakni berupa cerita"
pre = Preprocessing()
tokens = pre.pipeline(sentence)
print(tokens)


def has_multiple_entries(katajson):
    return len(katajson['entri']) > 1


def has_multiple_meanings(katajson):
    return len(katajson['entri'][0]['makna']) > 1


word = None
for random_word in tokens:
    try:
        kata = KBBI(random_word, auth)
        katajson = json.loads(json.dumps(kata.serialisasi(), indent=2))

        if has_multiple_entries(katajson):
            word = random_word
            break

    except Exception as e:
        continue

if not word:
    for random_word in tokens:
        try:
            kata = KBBI(random_word, auth)
            katajson = json.loads(json.dumps(kata.serialisasi(), indent=2))

            if has_multiple_meanings(katajson):
                word = random_word
                break

        except Exception as e:
            continue

print("ambiguous word:", word)

# Write the processed sentence to the output file
# output_file.write(word + "\n")

# pre = Preprocessing()
# tokens = pre.pipeline("aku membaca buku tentang sejarah di perpustakaan")
# random_index = random.randint(0, len(tokens) - 1)
# random_word = tokens[random_index]
# print(random_word)

# auth = AutentikasiKBBI("nurulakhni12@gmail.com", "Gmna10112")
# word = random_word
# kata = KBBI(word, auth)
# katajson = json.dumps(kata.serialisasi(), indent=2)
# print(katajson)
# katajson = json.loads(katajson)
# if len(katajson['entri']) == 1:
#     print(len(katajson['entri']))
# else:
#     print(len(katajson['entri']))
# result = []
# for entry in katajson['entri']:
#     # Loop over each 'makna' in this entry
#     print(", ".join(entry['gabungan_kata']))
#     for makna in entry['makna']:
#         # tag = []
#         # for kelas in makna['kelas']:
#         #     tag.append(kelas['kode'])
#         tag = makna['kelas'][0]['kode']
#         submakna = makna['submakna']
#         submakna = [d.replace("...", word) for d in submakna]
#         contoh = makna['contoh']
#         if bool(contoh):
#             contoh = [ex.replace("--", word) for ex in contoh]
#             print(contoh)

#         # Append the new dictionary to the result list
#         sense_example = {
#             'tag': tag,
#             'makna': ", ".join(submakna),
#             'contoh': contoh,
#         }
#         result.append(sense_example)

# result = {k: v for k, v in result.items() if v}
# print(result)
