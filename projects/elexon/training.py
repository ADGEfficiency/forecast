import pandas as pd
from sklearn.linear_model import Ridge


if __name__ == '__main__':

    names = [
        'x_train',
        'y_train',
        'x_test',
        'y_test'
    ]

    data = {name: pd.read_csv(
        './data/{}.csv'.format(name), index_col=0, parse_dates=True)
            for name in names}

    model = Ridge(alpha=100)
    model = model.fit(X=data['x_train'], y=data['y_train'])

    train_score = model.score(X=data['x_train'], y=data['y_train'])
    test_score = model.score(X=data['x_test'], y=data['y_test'])

    print(train_score, test_score)
