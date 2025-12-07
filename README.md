# KMeans

A fast k-means clustering algorithm implemented in C with Python bindings.

## Installation

### Using UV (recommended)

```bash
uv pip install .
```

### Using pip

```bash
pip install .
```

### Development installation

```bash
uv pip install -e ".[dev]"
```

## Quick Start

```python
import numpy as np
from kmeans import KMeans, kmeans

# Generate sample data
np.random.seed(42)
data = np.vstack([
    np.random.randn(100, 2) + [0, 0],
    np.random.randn(100, 2) + [5, 5],
    np.random.randn(100, 2) + [10, 0],
])

# Using the functional API
centroids, labels = kmeans(data, k=3)

# Using the class-based API
model = KMeans(n_clusters=3)
model.fit(data)
predictions = model.predict(data)
```

## Features

* Fast k-means clustering with C implementation
* K-means++ initialization
* NumPy integration
* Scikit-learn compatible API
* Support for arbitrary dimensions

## License

MIT
