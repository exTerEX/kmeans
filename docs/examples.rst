Examples
========

.. ...existing code...

Image Color Quantization
------------------------

.. code-block:: python

   import numpy as np
   from PIL import Image
   from kmeans import KMeans

   # Load image
   img = Image.open('photo.jpg')
   img_array = np.array(img)
   
   # Reshape to (n_pixels, 3)
   pixels = img_array.reshape(-1, 3).astype(np.float64)
   
   # Cluster colors
   kmeans_model = KMeans(n_clusters=16)
   kmeans_model.fit(pixels)
   
   # Replace colors with centroids
   quantized = kmeans_model.centroids_[kmeans_model.labels_]
   quantized_img = quantized.reshape(img_array.shape).astype(np.uint8)
   
   # Save result
   Image.fromarray(quantized_img).save('quantized.jpg')

Customer Segmentation
---------------------

.. code-block:: python

   import pandas as pd
   from kmeans import KMeans

   # Load customer data
   df = pd.read_csv('customers.csv')
   features = df[['age', 'income', 'spending_score']].values
   
   # Normalize features
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   features_scaled = scaler.fit_transform(features)
   
   # Cluster customers
   model = KMeans(n_clusters=5)
   df['segment'] = model.fit_predict(features_scaled)
   
   # Analyze segments
   print(df.groupby('segment').mean())

Anomaly Detection
-----------------

.. code-block:: python

   from kmeans import KMeans
   import numpy as np

   # Cluster normal data
   normal_data = np.random.randn(1000, 5)
   model = KMeans(n_clusters=3)
   model.fit(normal_data)
   
   # Check new points
   test_data = np.random.randn(100, 5)
   labels = model.predict(test_data)
   
   # Calculate distances to nearest centroid
   distances = np.array([
       np.linalg.norm(test_data[i] - model.centroids_[labels[i]])
       for i in range(len(test_data))
   ])
   
   # Flag anomalies (far from any centroid)
   threshold = np.percentile(distances, 95)
   anomalies = test_data[distances > threshold]
   print(f"Found {len(anomalies)} anomalies")

Time Series Clustering
----------------------

.. code-block:: python

   from kmeans import KMeans

   # Assume time_series is shape (n_series, n_timepoints)
   time_series = np.random.randn(100, 50)
   
   # Cluster time series
   model = KMeans(n_clusters=5)
   labels = model.fit_predict(time_series)
   
   # Plot representative series from each cluster
   import matplotlib.pyplot as plt
   
   fig, axes = plt.subplots(1, 5, figsize=(20, 4))
   for i in range(5):
       cluster_series = time_series[labels == i]
       axes[i].plot(cluster_series.T, alpha=0.3)
       axes[i].plot(model.centroids_[i], 'r-', linewidth=2)
       axes[i].set_title(f'Cluster {i}')
   plt.show()