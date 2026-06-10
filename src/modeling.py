from sklearn.dummy import DummyClassifier


def baseline_classifier(X, y):
    clf = DummyClassifier(strategy="most_frequent")
    clf.fit(X, y)
    return clf
