from sklearn.preprocessing import MinMaxScaler
from scipy.stats.mstats import winsorize
import pandas as pd
import numpy as np

scaler = MinMaxScaler()

class PreprocessData:
    def __init__(self) -> any:
        self.transformation_values: dict = None

    def full_preprocessing(self, caregiver_data: list, initial_compute: bool = True):
        print(f"\nfull_preprocessing(initial_compute={initial_compute})")

        # Retrieve integer and boolean data.
        integer_data: list = [caregiver['integers'] for caregiver in caregiver_data]
        boolean_data: list = [caregiver['booleans'] for caregiver in caregiver_data]
        
        # Preprocess data.
        scaled_integer_data = self._normalize_integer_data(
            integer_data=integer_data,
            initial_compute=initial_compute
        )
        dampened_boolean_data: list = self._dampen_boolean_data(boolean_data)

        # Prepare final vectorized data.
        vectorized_data: list = self._concatenate_quantifiable_data(
            boolean_data=dampened_boolean_data,
            integer_data=scaled_integer_data
        )

        return vectorized_data

    def _normalize_integer_data(self, integer_data: list, initial_compute: bool = True) -> list:
        try:
            print(f"\nnormalize_integer_data()")

            # Will store feature space distribution of values for boolean adjustments.
            feature_space_percentiles: dict = {'q1': 0, 'q2': 0, 'q3': 0}

            # Remove outliers within n-lower/upper percentile.
            print(f"├── Pre-winsorization  | integer_data[0]: {integer_data[0]}")
            integer_data_df = pd.DataFrame(integer_data)
            number_of_rows: int = integer_data_df.shape[0]
            number_of_columns: int = integer_data_df.shape[1]
            for i in range(number_of_columns):
                column_data: list = integer_data_df.iloc[:, i]
                column_min: float = min(column_data)
                column_max: float = max(column_data)
                integer_data_df[i] = winsorize(column_data, limits=[0.01, 0.01])
                if initial_compute:
                    feature_space_percentiles['q1'] += (np.percentile(column_data, 25) - column_min) / (column_max - column_min)
                    feature_space_percentiles['q2'] += (np.percentile(column_data, 50) - column_min) / (column_max - column_min)
                    feature_space_percentiles['q3'] += (np.percentile(column_data, 75) - column_min) / (column_max - column_min)
            print(f"├── Post-winsorization | integer_data[0]: {integer_data[0]}")

            # Compute percentile averages. 
            if initial_compute and self.transformation_values == None:
                feature_space_percentiles = {
                    'q1': feature_space_percentiles['q1'] / number_of_rows,
                    'q2': feature_space_percentiles['q2'] / number_of_rows,
                    'q3': feature_space_percentiles['q3'] / number_of_rows,
                } 
                print(f"├── feature_space_percentiles | 'q1': {feature_space_percentiles['q1']:.10f}, 'q2': {feature_space_percentiles['q2']:.10f}, 'q3': {feature_space_percentiles['q3']:.10f}")
                self.transformation_values = feature_space_percentiles

            # Min-Max scaler to scale data within the ranges of 0-1, matching the booleans.
            scaled_integer_data: list = scaler.fit_transform(integer_data)
            print(f"└── scaled_integer_data[0]: {scaled_integer_data[0]}")
            return scaled_integer_data
        except Exception as e:
            print(f"ERROR .. {e}")

    def _dampen_boolean_data(self, boolean_data: list) -> list:
        print(f"\ndampen_boolean_data()")
        print(f"├── transformation_values: {str(self.transformation_values)[:40]}...")
        for i in range(len(boolean_data)):
            boolean_data[i] = list(boolean_data[i])
            for j in range(len(boolean_data[i])):
                boolean_data[i][j] = self.transformation_values['q1'] if boolean_data[i][j] == 0 else self.transformation_values['q3']
        print(f"└── boolean_data[0]: {str(boolean_data[0])[:40]}...")
        return boolean_data

    def _concatenate_quantifiable_data(self, boolean_data: list, integer_data: list) -> list:
        try:
            print(f"\nconcatenate_quantifiable_data()")
            if len(boolean_data) == 1 and len(integer_data) == 1:
                print(f"├── len(boolean_data): {len(boolean_data)}")
                print(f"├── len(integer_data): {len(integer_data)}")
                concatenated_quantifiables: list = [list(boolean_data[0]) + list(integer_data[0])]
                print(f"└── len(concatenated_quantifiables): {len(concatenated_quantifiables)} | len(concatenated_quantifiables[0]): {len((concatenated_quantifiables[0]))}")
                return concatenated_quantifiables
            else:
                print(f"├── len(boolean_data): {len(boolean_data)} | len(boolean_data[0]): {len(boolean_data[0]):}")
                print(f"├── len(integer_data): {len(integer_data)} | len(integer_data[0]): {len(integer_data[0]):}")
                if len(boolean_data) != len(integer_data):
                    print(f"Length of boolean_data and integer_data must be equal.")
                    return []
                concatenated_quantifiables: list = [list(boolean_data[i]) + list(integer_data[i]) for i in range(len(boolean_data))]
                print(f"└── len(concatenated_quantifiables): {len(concatenated_quantifiables)} | len(concatenated_quantifiables[0]): {len((concatenated_quantifiables[0]))}")
                return concatenated_quantifiables
        except Exception as e:
            print(f"ERROR .. {e}")