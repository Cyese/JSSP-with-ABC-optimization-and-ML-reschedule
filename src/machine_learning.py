from data import DataProduct
from utilities import plot, pd, np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn import tree
from sklearn.feature_selection import r_regression
from imblearn.over_sampling import SMOTE
# from collections import Counter

def run_DecisionTree(data: str):
    fill = "New Order" if data == 'order' else "Product"
    df = pd.read_csv(f"data/feature_{data}.csv")

    y = df['Rescheduling'].values.reshape(-1, 1)  # type: ignore
    x = df[['Week','Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time']]

    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2)

    model = DecisionTreeClassifier(ccp_alpha=0.0, criterion='gini', max_depth=None,
                        max_features=None, max_leaf_nodes=None,
                        min_impurity_decrease=0.0,
                        min_samples_leaf= 1, min_samples_split= 2,
                        min_weight_fraction_leaf=0.0,
                        random_state=100, splitter='best')
    model.fit(X_train, y_train)


    y_pred = model.predict(x)
    # print(y_pred)
    accuracy = accuracy_score(y_pred, y)
    print(f"Accuracy: {accuracy}")
    title = f"Confusion matrix in {fill} \nAccuracy: {round(accuracy, 5)}"
    classes = ["Rechedule", "Non-Reschedule"]

    cm = confusion_matrix(y, y_pred)
    plot.imshow(cm, interpolation='nearest', cmap="Blues")
    plot.colorbar()
    plot.title(title)
    tick_marks = np.arange(len(classes))
    plot.xticks(tick_marks, classes, rotation=45)
    plot.yticks(tick_marks, classes)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    # Add text annotations to each cell
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plot.text(j, i, format(cm[i, j], 'd'),
                horizontalalignment="center",
                color="white" if cm_norm[i, j] > thresh else "black")

    # plot.xlabel('Predicted value')
    # plot.ylabel('True value')
    plot.tight_layout()
    plot.savefig(f"misc/confusion_matrix_{data}")
    plot.show()


def balance_data(data: str):
    fill = "New Order" if data == 'order' else "Product"
    df = pd.read_csv(f"data/feature_{data}.csv")

    y = df['Rescheduling'].values.reshape(-1, 1)  # type: ignore
    x = df[['Week','Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time']]
    # print(f'Original dataset shape {len(y)}')
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(x, y) # type: ignore
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, random_state=42, test_size=0.20)
    __x = pd.DataFrame(X_res)
    __y = pd.Series(y_res)
    new_data = pd.merge(__x, __y.rename("Rescheduling"), left_index=True, right_index=True)
    new_data.to_csv(f"data/balanced_feature_{data}.csv")

    model = DecisionTreeClassifier(ccp_alpha=0.0, criterion='gini', max_depth=None,
                        max_features=None, max_leaf_nodes=None,
                        min_impurity_decrease=0.0,
                        min_samples_leaf= 1, min_samples_split= 2,
                        min_weight_fraction_leaf=0.0,
                        random_state=100, splitter='best')
    clf = model.fit(X_train, y_train)
    y_pred = model.predict(X_res)
    # print(y_pred)
    accuracy = accuracy_score(y_pred, y_res)
    print(f"Accuracy: {accuracy}")
    title = f"Balanced confusion matrix in {fill} \nAccuracy: {round(accuracy, 5)}"
    classes = ["Rechedule", "Non-Reschedule"]
    cm = confusion_matrix(y_res, y_pred)
    plot.imshow(cm, interpolation='nearest', cmap="Blues")
    plot.colorbar()
    plot.title(title)
    tick_marks = np.arange(len(classes))
    plot.xticks(tick_marks, classes, rotation=45)
    plot.yticks(tick_marks, classes)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    # Add text annotations to each cell
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plot.text(j, i, format(cm[i, j], 'd'),
                horizontalalignment="center",
                color="white" if cm_norm[i, j] > thresh else "black")

    # plot.xlabel('Predicted value')
    # plot.ylabel('True value')
    plot.tight_layout()
    plot.savefig(f"misc/balanced_confusion_matrix_{data}")

    plot.show()


def plot_decesion_tree(data: str):
    fill = "New Order" if data == 'order' else "Product"
    df = pd.read_csv(f"data/balanced_feature_{data}.csv")

    y = df['Rescheduling'].values.reshape(-1, 1)  # type: ignore
    x = df[['Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time']]
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2, train_size= 0.8)


    model = DecisionTreeClassifier(ccp_alpha=0.0, criterion='gini', max_depth=None,
                        max_features=None, max_leaf_nodes=None,
                        min_impurity_decrease=0.0,
                        min_samples_leaf= 1, min_samples_split= 2,
                        min_weight_fraction_leaf=0.0,
                        random_state=100, splitter='best')
    clf = model.fit(X_train, y_train)
    fig, ax = plot.subplots(figsize=(20, 15))  # Adjust figure size as per your preference
    colors = ['skyblue', 'lightgreen']
    tree.plot_tree(clf, fontsize=10, feature_names=x.columns, rounded=True, proportion=True, impurity=False, node_ids=True, ax=ax, max_depth=3) # type: ignore
    plot.savefig(f'misc/DecesionTree_{data}')
    text = tree.export_text(clf, feature_names=['Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time'], max_depth=3) # type: ignore
    with open(f'misc/text_tree_{data}.txt', "w+") as file:
        file.write(text)

def split_sample_test(data: str, sample: int):
    fill = "NewOrder" if data == 'order' else "Product"
    df = pd.read_csv(f"data/balanced_feature_{data}.csv")

    # y = df['Rescheduling'].values.reshape(-1, 1)  # type: ignore
    # x = df[['Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time']]
    kf = KFold(n_splits=7, shuffle=True)
    model = DecisionTreeClassifier(ccp_alpha=0.0, criterion='gini', max_depth=None,
                    max_features=None, max_leaf_nodes=None,
                    min_impurity_decrease=0.0,
                    min_samples_leaf= 1, min_samples_split= 2,
                    min_weight_fraction_leaf=0.0,
                    random_state=100, splitter='best')
    with open(f"misc/kfold_{fill}_{sample}.txt", "w+") as file:
        for index, (train_index, test_index) in enumerate(kf.split(df)) :
            file.write(f"Test fold index: {index}\n")
            # print(train_index)
            df_train = df.iloc[train_index]
            file.write(f"\tTrain: {round(len(train_index)/len(df), 4)*100}%\n")
            file.write(f"\tTest:  {round(len(test_index)/len(df), 4)*100}%\n")
            y_train = df_train['Rescheduling'].values.reshape(-1, 1)  # type: ignore
            x_train = df_train[['Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time']]

            x_test = df[['Timestep', 'MU', 'RBM', 'RSDU', 'Total extended time']]
            y_test = df['Rescheduling'].values.reshape(-1, 1)  # type: ignore

            clf = model.fit(x_train, y_train)
            y_predict= clf.predict(x_test)
            accuracy = accuracy_score(y_predict, y_test)
            file.write(f"\tAccuracy: {accuracy}\n")
    