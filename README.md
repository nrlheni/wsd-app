# Word Sense Disambiguation App for Indonesian Sentences using Simplified Lesk Algorithm

## Overview
This repository hosts a Word Sense Disambiguation (WSD) application for Indonesian sentences, employing the Simplified Lesk Algorithm. Developed as a thesis research project for a Bachelor's degree, this app aims to disambiguate the meanings of words in Indonesian based on the context of the sentence.

## Technology Stack
- **Backend**: Flask, Python 3.9.7
- **Frontend**: HTML, CSS, JavaScript

## Corpus Used
The application utilizes the [KBBI (Kamus Besar Bahasa Indonesia)](https://kbbi.kemdikbud.go.id/) library as the corpus for word sense disambiguation. KBBI is a comprehensive dictionary of the Indonesian language, which provides a rich dataset for this purpose.

## Features
- **Word Sense Disambiguation**: Given a sentence in Indonesian, the app determines the correct meaning of ambiguous words using the Simplified Lesk Algorithm.
- **Evaluation**: The application includes functionality to evaluate the accuracy and performance of the disambiguation process, providing insights into its effectiveness.
- **User Interface**: A user-friendly interface allows users to input sentences and view the disambiguated results.

## Evaluation Data
Evaluation data is available within the repository or can be generated using provided scripts. This data helps in assessing the accuracy and effectiveness of the WSD algorithm.

For demonstration purposes, you can also use data from the evaluation table included in the repository.

The evaluation includes 4 sets of metrics:
- Data with stemming preprocessed
- Data with stemming and stopword removal preprocessed
- Data with only stopword removal preprocessed
- Data without both stemming and stopword removal

Each evaluation set shows the number of correct and incorrect predictions, along with the accuracy of the word sense disambiguation algorithm.

## Visual

![image](https://github.com/nrlheni/wsd-app/assets/86219910/ec8ca787-7346-441f-ba1d-a48a9b0dbb9a)

![image](https://github.com/nrlheni/wsd-app/assets/86219910/ae943559-4716-446b-8a98-08c189bae275)

## Author
[Nurul Akhni]

