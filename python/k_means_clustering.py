""""""
from ctypes import CDLL, c_size_t, c_int
import sys

library_path = f"build/kmeans_{sys.platform}.so"
try:
    kmeans_library = CDLL(library_path)
except:
    print(f"OS {sys.platform} not recognized")

k_means = kmeans_library.k_means
k_means.restype = None
