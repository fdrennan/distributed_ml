# source activate distributed
# conda env export > distributed.yml
from sklearn import linear_model
from sklearn.externals import joblib

reg = linear_model.LinearRegression()
reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])

reg.coef_

joblib.dump(reg, 'regression.joblib')

clf = joblib.load('regression.joblib')

clf.coef_