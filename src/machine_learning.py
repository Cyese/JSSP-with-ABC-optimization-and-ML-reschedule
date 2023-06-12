from data import Data
from utilities import plot, pd, np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

def run_DecisionTree():
    df = pd.read_csv("data/feature.csv")

    y = df['Rescheduling'].values.reshape(-1, 1)  # type: ignore
    x = df[['Week','Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time', 'Stage']]

    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.05)

    model = DecisionTreeClassifier(ccp_alpha=0.0, criterion='gini', max_depth=None,
                        max_features=None, max_leaf_nodes=None,
                        min_impurity_decrease=0.0,
                        min_samples_leaf= 1, min_samples_split= 2,
                        min_weight_fraction_leaf=0.0,
                        random_state=100, splitter='best')
    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)
    # print(y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
