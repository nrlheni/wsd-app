# def evaluate(self, actual_sense, predicted_sense):

# Compute the confusion matrix
# labels = np.unique(actual_sense + predicted_sense)
# confusion_mat = confusion_matrix(
#     actual_sense, predicted_sense, labels=labels)

# # Compute the classification report
# classification_rep = classification_report(
#     actual_sense, predicted_sense, labels=labels)

# # Compute the accuracy
# accuracy = np.sum(np.diag(confusion_mat)) / np.sum(confusion_mat) * 100

# # Compute the precision, recall, and F1-score
# precision, recall, f1_score, _ = precision_recall_fscore_support(
#     actual_sense, predicted_sense, average='weighted')

# tp = sum([confusion_mat[i][i] for i in range(len(labels))])
# fp = sum([sum(confusion_mat[:, i]) - confusion_mat[i][i]
#           for i in range(len(labels))])
# fn = sum([sum(confusion_mat[i, :]) - confusion_mat[i][i]
#           for i in range(len(labels))])
# tn = len(actual_sense) - tp - fp - fn

# # Format the metrics as percentages
# accuracy = '{:.2f}%'.format(accuracy)
# precision = '{:.2f}%'.format(precision * 100)
# recall = '{:.2f}%'.format(recall * 100)
# f1_score = '{:.2f}%'.format(f1_score * 100)

# return tp, fp, fn, tn, accuracy, precision, recall, f1_score, classification_rep
