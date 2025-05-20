from backend.util.crud_functions import CrudFunctions
import random

# Translates KNN results to caregiver data.
def decode_knn_results(knn_results: dict, observed_caregivers: list) -> list:
    print(f"\n[START] decode_knn_results()")

    # Translate observed indices to caregiver UIDs.
    uid_list: list = []
    uid_to_knn_distance_map: dict = {}
    for i in range(len(knn_results['indices'])):
        knn_indices_at_i: int = knn_results['indices'][i]
        knn_distance_at_i: float = knn_results['distances'][i]
        current_index_uid: int = observed_caregivers[knn_indices_at_i]['uids']
        uid_list.append(current_index_uid)
        uid_to_knn_distance_map[current_index_uid] = knn_distance_at_i

    # Retrieve data for KNN-resulted caregivers.
    cf = CrudFunctions()
    matched_caregivers_data: list = cf.retrieve_user_profiles_from_list_of_uids(uid_list)
    del cf

    # Sort caregivers by KNN distance.
    for i in range(len(matched_caregivers_data)):
        current_index_uid = matched_caregivers_data[i][0]
        matched_caregivers_data[i] = list(matched_caregivers_data[i])
        matched_caregivers_data[i].append(uid_to_knn_distance_map[current_index_uid])
    matched_caregivers_data.sort(key=lambda x: x[-1])

    # Review caregivers.
    print(f"\nKNN Distance | Caregiver UID")
    for i in range(len(uid_list)):
        caregiver_profile: tuple = matched_caregivers_data[i]
        caregiver_uid: int = matched_caregivers_data[i][0]
        distance: float = uid_to_knn_distance_map[caregiver_uid]
        print(f"{distance:.2f}         | {caregiver_profile[0]}")

    print(f"\n[END] decode_knn_results()")
    return matched_caregivers_data