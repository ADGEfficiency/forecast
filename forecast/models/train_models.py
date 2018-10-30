import numpy as np
import pandas as pd

from register import get_model

if __name__ == '__main__':

    model_config = {'model_id': 'random_forest',
                    'n_estimators': 1000,
                    'max_features': 'sqrt',
                    'verbose': 1}

    model = get_model(**model_config)

    print('training {}'.format(model_config['model_id']))
    model.fit(x_train, y_train)

    print('R2 on training data {}'.format(model.score(x_train, y_train)))
    print('R2 on test data {}'.format(model.score(x_test, y_test)))
