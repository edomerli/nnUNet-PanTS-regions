from typing import Union, List, Tuple

import numpy as np
from nnunetv2.experiment_planning.experiment_planners.residual_unets.residual_encoder_unet_planners import \
    nnUNetPlannerResEncL, nnUNetPlannerResEncM
from nnunetv2.preprocessing.normalization.map_channel_name_to_normalization import get_normalization_scheme

class nnUNetPlannerResEncMIso1x1x1(nnUNetPlannerResEncM):
    def __init__(self, dataset_name_or_id: Union[str, int],
                 gpu_memory_target_in_gb: float = 8,
                 preprocessor_name: str = 'DefaultPreprocessor', plans_name: str = 'nnUNetResEncUNetMPlansIso1x1x1',
                 overwrite_target_spacing: Union[List[float], Tuple[float, ...]] = None,
                 suppress_transpose: bool = False):
        super().__init__(dataset_name_or_id, gpu_memory_target_in_gb, preprocessor_name, plans_name,
                         overwrite_target_spacing, suppress_transpose)

    def determine_fullres_target_spacing(self) -> np.ndarray:
        # detect 2D as having shape 1 in the first dimension for all cases
        shapes_after_crop = self.dataset_fingerprint['shapes_after_crop']
        if all([i[0] == 1 for i in shapes_after_crop]):
            return np.array([self.dataset_fingerprint['spacings'][0][0], 1., 1.])
        else:
            return np.array([1., 1., 1.])

    def generate_data_identifier(self, configuration_name: str) -> str:
        """Same as ExperimentPlanner method. Don't use ResEncUNetPlanner because you never want to reuse data (by having nnUNetPlans prefix) since it might have different spacing."""
        return self.plans_identifier + '_' + configuration_name


class nnUNetPlannerResEncLIso1x1x1(nnUNetPlannerResEncL):
    def __init__(self, dataset_name_or_id: Union[str, int],
                 gpu_memory_target_in_gb: float = 24,
                 preprocessor_name: str = 'DefaultPreprocessor', plans_name: str = 'nnUNetResEncUNetLPlansIso1x1x1',
                 overwrite_target_spacing: Union[List[float], Tuple[float, ...]] = None,
                 suppress_transpose: bool = False):
        super().__init__(dataset_name_or_id, gpu_memory_target_in_gb, preprocessor_name, plans_name,
                         overwrite_target_spacing, suppress_transpose)

    def determine_fullres_target_spacing(self) -> np.ndarray:
        # detect 2D as having shape 1 in the first dimension for all cases
        shapes_after_crop = self.dataset_fingerprint['shapes_after_crop']
        if all([i[0] == 1 for i in shapes_after_crop]):
            return np.array([self.dataset_fingerprint['spacings'][0][0], 1., 1.])
        else:
            return np.array([1., 1., 1.])

    def generate_data_identifier(self, configuration_name: str) -> str:
        """Same as ExperimentPlanner method. Don't use ResEncUNetPlanner because you never want to reuse data (by having nnUNetPlans prefix) since it might have different spacing."""
        return self.plans_identifier + '_' + configuration_name