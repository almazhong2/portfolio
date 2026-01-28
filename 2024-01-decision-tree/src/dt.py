import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import RandomOverSampler


DATA_PATH = "nkcore_ki_201903.csv"
FEATURE_COLS = [
    'KDPI', 'AGE', 'CREAT_DON', 'BMI_DON_CALC',
    'END_CPRA', 'DAYSWAIT_CHRON', 'HLAMIS', 'COLD_ISCH_KI'
]


def main(target_col, oversample):
    df = pd.read_csv(DATA_PATH, encoding='windows-1252')

    X = df[FEATURE_COLS]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

    if oversample:
        ros = RandomOverSampler(random_state=42)
        X_train, y_train = ros.fit_resample(X_train, y_train)
        print("random oversampling")

    clf = DecisionTreeClassifier(max_depth=4)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("\naccuracy:", accuracy_score(y_test, y_pred) * 100, "%")
    print(classification_report(y_test, y_pred), target_names = ["no cancer", "cancer"])

    # Plot tree
    plt.figure(figsize=(25, 20))
    plot_tree(
        clf,
        feature_name = FEATURE_COLS,
        class_names = True,
        filled = True,
        fontsize = 6
    )
    plt.title(f"Decision Tree for {target_col}")
    plt.show()

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens')
    plt.title(f'Confusion Matrix for {target_col}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="malig or GSTATUS_KI")
    parser.add_argument("--oversample", action="store_true")

    args = parser.parse_args()
    main(args.target, args.oversample)