import numpy as np
import pytest
from kmeans import KMeans, kmeans


@pytest.fixture
def sample_data():
    """Generate sample clustered data."""
    np.random.seed(42)
    return np.vstack(
        [
            np.random.randn(50, 2) + [0, 0],
            np.random.randn(50, 2) + [10, 10],
        ]
    )


def test_kmeans_function(sample_data):
    """Test the functional kmeans API."""
    centroids, labels = kmeans(sample_data, k=2)

    assert centroids.shape == (2, 2)
    assert labels.shape == (100,)
    assert set(labels) == {0, 1}


def test_kmeans_class(sample_data):
    """Test the KMeans class."""
    model = KMeans(n_clusters=2)
    model.fit(sample_data)

    assert model.centroids_.shape == (2, 2)  # type: ignore
    assert model.labels_.shape == (100,)  # type: ignore


def test_kmeans_predict(sample_data):
    """Test prediction on new data."""
    model = KMeans(n_clusters=2)
    model.fit(sample_data)

    new_data = np.array([[0.0, 0.0], [10.0, 10.0]])
    predictions = model.predict(new_data)

    assert len(predictions) == 2
    assert predictions[0] != predictions[1]


def test_kmeans_fit_predict(sample_data):
    """Test fit_predict method."""
    model = KMeans(n_clusters=2)
    labels = model.fit_predict(sample_data)

    assert labels.shape == (100,)  # type: ignore
    np.testing.assert_array_equal(labels, model.labels_)


def test_invalid_k():
    """Test that invalid k raises an error."""
    data = np.random.randn(10, 2)

    with pytest.raises(ValueError):
        kmeans(data, k=0)

    with pytest.raises(ValueError):
        kmeans(data, k=20)
