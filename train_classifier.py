#sorts the data into right vs left classes for the motor to move

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# Load recorded EEG data
X = np.load("eeg_data.npy")
y = np.load("labels.npy")

# Preprocessing: Simple feature extraction (mean per channel)
X = np.mean(X, axis=1)

# Organize data into left and right classes
X_left = X[y == 0]  # Assuming 0 is left
X_right = X[y == 1]  # Assuming 1 is right

y_left = y[y == 0]
y_right = y[y == 1]

# Ensure that both classes have sufficient data (optional check)
print(f"Left class data: {X_left.shape}, Right class data: {X_right.shape}")

# Train-test split (combine left and right data)
X_combined = np.concatenate((X_left, X_right), axis=0)
y_combined = np.concatenate((y_left, y_right), axis=0)

X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)

# Train an SVM classifier
clf = SVC(kernel='linear')
clf.fit(X_train, y_train)

# Evaluate model accuracy
y_pred = clf.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save trained model
joblib.dump(clf, "motor_classifier.pkl")
print("Classifier saved as motor_classifier.pkl")
