# Custom class imports.
from backend.util.k_nearest_neighbors import KNearestNeighbors
from backend.tests.generate_test_data import GenerateTestData
from backend.util.preprocess_data import PreprocessData
from backend.util.crud_functions import CrudFunctions

# Custom method imports.
from backend.util.process_knn_results import decode_knn_results

class RecommendationSystem:
    def __init__(self) -> None:
        # Initialize utility class instances for the recommendation system.
        self.cf = CrudFunctions()
        self.gtd = GenerateTestData()
        self.knn = KNearestNeighbors()
        self.pre = PreprocessData()

    # ABOUT: Recommendation initialization.
    # WHERE: Called by main app script.
    def initialize_recommendation_system(self, mode: str="test") -> None:
        print(f"initialize_recommendation_system()")

        # Initialization mode toggle.
        if mode == "test":
            self._run_test_recommendation_system()
        elif mode == "prod":
            self._run_production_recommendation_system()
        else:
            print(f"Please enter an initialization mode. (e.g., mode='test' or 'prod')")

        return

    # ABOUT: Runs recommendation system tests.
    # WHERE: Should only be called by initialize_recommendation_system().
    def _run_test_recommendation_system(self) -> None:
        # [0] Data generation.
        self.gtd.generate_n_test_users(number_of_test_users=10e4)

        # [1] Simulate test users.
        careseeker_data: list = self.cf.retrieve_all_data_from_random_caregiver()
        caregivers_data: list = self.cf.retrieve_all_caregivers_for_preprocessing()

        # [2] Preprocess simulated data.
        vectorized_caregivers_data: list = self.pre.full_preprocessing(caregivers_data)
        vectorized_careseeker_data: list = self.pre.full_preprocessing(careseeker_data, initial_compute=False)

        # [3] Fit vectorized data to knn data structure.
        self.knn.fit_data(vectorized_caregivers_data)

        # [4] Test knn.
        knn_results: dict = self.knn.find_neighbors(vectorized_careseeker_data)
        
        # [5] Decode knn results.
        matched_caregivers_data: list = decode_knn_results(knn_results, observed_caregivers=caregivers_data)
        
        # [6] Review results.
        careseeker_requirements: list = self.cf.retrieve_user_profile_from_uid(careseeker_data[0]['uids'])
        print(careseeker_requirements)

        return

    # ABOUT: Runs production recommendation system.
    # WHERE: Should only be called by initialize_recommendation_system().
    def _run_production_recommendation_system(self) -> None:
        # Retrieve all caregiver quantifiables.
        caregivers_data: list = self.cf.retrieve_all_caregivers_for_preprocessing()

        # Preprocess caregivers data.
        vectorized_caregivers_data: list = self.pre.full_preprocessing(caregivers_data)

        # Fit vectorized data to knn data structure.
        self.knn.fit_data(vectorized_caregivers_data)
    
    # ABOUT: Retrieves recommended caregivers.
    # WHERE: Should be called by an API endpoint's method.
    def recommend_caregivers(self, caregivers_data) -> list:
        # Retrieve careseeker quantifiables.
        careseeker_data: list = self.cf.retrieve_all_data_from_random_caregiver()

        # Preprocess careseeker quantifiables.
        vectorized_careseeker_data: list = self.pre.full_preprocessing(careseeker_data, initial_compute=False)
        
        # Similarity search against current knn-fitted vectors.
        knn_results: dict = self.knn.find_neighbors(vectorized_careseeker_data)

        # Decode knn results.
        decoded_caregivers_data: list = decode_knn_results(knn_results, observed_caregivers=caregivers_data)

        # Postprocess decoded caregivers data.
        matched_caregivers_data: list = self.post.filter_by_requirements(decoded_caregivers_data)

        return matched_caregivers_data