# from optimize import BeeColony
from graph import *
from utilities import *
# from reschedule import *
# from shutil import rmtree
from machine_learning import *

from reschedule import *
from data import *
data ="maintain"
title = "Maintain"
df = pd.read_csv(f"data/{data}.csv")

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

y_pred = model.predict(x)
# print(y_pred)
accuracy = accuracy_score(y_pred, y)
print(f"Accuracy: {accuracy}")
title = f"Confusion matrix in {data} \nAccuracy: {round(accuracy, 5)}"
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
