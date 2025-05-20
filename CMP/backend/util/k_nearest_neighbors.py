
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

class KNearestNeighbors:
    def __init__(self) -> None:
        self.knn = NearestNeighbors(
            n_neighbors=10,
            metric="euclidean"
        )

    def fit_data(self, caregivers_data: list) -> dict:
        print(f"\nfit_data()")
        print(f"└── caregivers_data: {str(caregivers_data[0])[:40]}...")
        self.knn.fit(caregivers_data)

    def find_neighbors(self, careseeker_data: dict) -> tuple:
        print(f"\nfind_neighbors()")
        distances, indices = self.knn.kneighbors(careseeker_data)
        distances = distances[0]
        indices = indices[0]
        print(f"├── distances: {str(distances)[:40]}...")
        print(f"└── indices: {str(indices)[:40]}...")
        return {
            'distances': distances,
            'indices': indices
        }