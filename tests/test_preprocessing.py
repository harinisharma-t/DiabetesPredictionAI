from src.prepare_data import load_and_prepare_data


def test_preprocessing():

    X_train, X_test, y_train, y_test = load_and_prepare_data()

    # Check that the dataset was split
    assert len(X_train) > 0
    assert len(X_test) > 0

    # Check that training and testing features have 8 columns
    assert X_train.shape[1] == 8
    assert X_test.shape[1] == 8

    # Check that target values exist
    assert len(y_train) > 0
    assert len(y_test) > 0