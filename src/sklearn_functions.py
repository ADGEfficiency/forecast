from collections import defaultdict

import numpy as np
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.model_selection import TimeSeriesSplit 


def cross_validation(
        model,
        params,
        make_feature_pipeline,
        make_target_pipeline,
        pipeline_params,
        train_data,
        n_folds=5,
        verbose=False
):
    """
    Cross validates over a single set of model parameters

    args
    	model (sklearn estimator) uninitialized model
	params (dict)
	make_target_pipeline (function)
	make_target_pipeline (function)
	train_data (pd.DataFrame) fed into both the target and feature pipelines
	n_folds (int)
	verbose (bool)

    TODO ability to use different test_train_splits
    """
    results = defaultdict(list)

    print('running {} folds cross_validation over {}'.format(n_folds, params))
    ts_split = TimeSeriesSplit(n_splits=n_folds)

    for fold, (train_index, test_index) in enumerate(ts_split.split(train_data), 1):
        cv_train = train_data.iloc[train_index, :]
        cv_test = train_data.iloc[test_index, :]

        #  create a fresh feature generator and target generator for each fold of CV
        feature_generator = make_feature_pipeline(**pipeline_params)
        target_generator = make_target_pipeline(**pipeline_params)

        #  make the training and test data
        x_train = feature_generator.fit_transform(cv_train)
        x_test = feature_generator.transform(cv_test)

        y_train = target_generator.fit_transform(cv_train)
        y_test = target_generator.transform(cv_test)

        cv_model = model(**params)
        cv_model.fit(x_train, y_train.reshape(-1))
        train_score, test_score = 100 * cv_model.score(x_train, y_train), 100 * cv_model.score(x_test, y_test)

        results['train_scores'].append(train_score)
        results['test_scores'].append(test_score)
        results['models'].append(cv_model)
        results['feature_pipe'].append(feature_generator)
        results['target_pipe'].append(target_generator)

        if verbose:
            score_log = 'fold {:.0f} {:.1f} % train score {:.1f} % test score'.format(
                fold,
                train_score,
                test_score)

            print(score_log)

    results = dict(results)
    results['params'] = cv_model.get_params()
    results['train_score'] = np.mean(results['train_scores'])
    results['test_score'] = np.mean(results['test_scores'])

    print('CV done - train {} % test {} %'.format(
        results['train_score'], results['test_score'])
          )

    return results


def grid_search(model,
		model_params,
		make_feature_pipeline,
		make_target_pipeline,
		pipeline_params,
		train_data):
    """
    Grid search combined with cross validation

    args
        model (sklearn model)
        model_params (list) contains dictionaries of parameters
	make_feature_pipeline (function)
	make_target_pipeline (function)
	pipeline_params (dict)
	train_data (pd.DataFrame)

    Grid search over the different parameters in the model_params list

    Cross validation for each set of parameters
    """
    results = []

    for param in model_params:
        res = cross_validation(
            model,
            param,
            make_feature_pipeline,
            make_target_pipeline,
            pipeline_params,
            train_data)

        results.append(res)

        print('test score {:.1f} % params {}'.format(res['test_score'], param))

    return results


def train_dummy_classifiers(features, target):
    for strat in ['stratified', 'most_frequent', 'prior', 'uniform']:
        dc = DummyClassifier(strategy=strat)
        dc.fit(features, y=target.flatten())

        dummy_score = (100 * dc.score(features, target))
        print('{:.1f} % score for a dummy classifier using the {} stragety'.format(
	    dummy_score,
	    dc.get_params()['strategy']))


def train_dummy_regressors(features, target):
    for strat in ['mean', 'median']:
        dr = DummyRegressor(strategy=strat)
        dr.fit(features, y=target.flatten())

        dummy_score = (100 * dr.score(features, target))
        print('{:.1f} % score for a dummy regressor using the {} stragety'.format(
	    dummy_score,
	    dr.get_params()['strategy']))
