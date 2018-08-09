from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from .lstm import ManyOneLSTM


models = {
    'random_forest': RandomForestRegressor,
    'linear': LinearRegression,
    'lstm': ManyOneLSTM
}


def make_model(model_id, **kwargs):
    print('making {}'.format(model_id))
    model = models[model_id]
    return model(**kwargs)
