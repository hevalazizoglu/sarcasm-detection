import csv

from sklearn import svm

X = []
y = []

with open('tweet_features.csv', newline='') as csvfile:
    tweetfeaturereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for feature_list in tweetfeaturereader:
        X.append([float(x) for x in feature_list[:-2]] + [int(feature_list[-2])])
        y.append(int(feature_list[-1]))

clf = svm.SVC()
clf.fit(X[:2122], y[:2122])

predictions = clf.predict(X[2122:])

spam_matched = 0
total_spam_count = 0
nonspam_matched = 0
others_count = 0
matched_count = 0
for x in range(915):
    if y[2122+x] == 1:
        total_spam_count += 1
    else:
        others_count += 1
    if y[2122+x] == predictions[x]:
        matched_count += 1
        if predictions[x] == 1:
            spam_matched += 1
        else:
            nonspam_matched += 1

print("Match count: ", matched_count)
print("Accuracy: ", matched_count/915)
print("Spam found: ", spam_matched)
print("Total spam count: ", total_spam_count)
print("Nonspam found: ", nonspam_matched)
print("Others count: ", others_count)
print("Precision: ", spam_matched/915)
print("Recall: ", spam_matched/total_spam_count)
