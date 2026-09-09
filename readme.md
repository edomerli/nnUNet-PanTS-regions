# nnUNet-PanTS

This repository contains the nnU-Net code used for our submission to the [PanTS leaderboard](https://github.com/MrGiovanni/PanTS).
The only changes are:
* defining pancreas subsegments and pancreas tumor labels as **regions** within the pancreas in `dataset.json` (see [here](https://huggingface.co/edomerli/nnUNet-PanTS-regions/blob/main/dataset.json))
* all foreground crops are applied on the pancreas

Trainer and evaluation code are [here](nnunetv2/custom_code).

## Installation

Clone and install following the standard nnU-Net directions: see the [installation and setup guide](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/getting-started/installation-and-setup.md).

## Setup

1. Make sure the PanTS dataset is in nnU-Net format.
2. Set the three standard nnU-Net environment variables (raw, preprocessed, results paths).
3. Set the custom trainer path used in this fork (`custom_code` folder contains the trainer):

```bash
export nnUNet_raw=/path/to/nnUNet_raw
export nnUNet_preprocessed=/path/to/nnUNet_preprocessed
export nnUNet_results=/path/to/nnUNet_results
export nnUNet_extTrainer=/path_to_this_repo/nnunetv2/custom_code
```

## Training

For completeness, I include below the training commands used (PanTS given Dataset ID 3):

```bash
nnUNetv2_plan_and_preprocess -d 3 -pl nnUNetPlannerResEncMIso1x1x1 -c 3d_fullres -np ${SLURM_CPUS_PER_TASK}
nnUNetv2_train 3 3d_fullres all -tr nnUNetTrainer_onlyMirror01_PanCrop -p nnUNetResEncUNetMPlansIso1x1x1 --c
```

`nnUNetPlannerResEncMIso1x1x1` class is included in the added file [residual_encoder_unet_iso_planners.py](nnunetv2/experiment_planning/experiment_planners/residual_unets/residual_encoder_unet_iso_planners.py).

## Model checkpoint

The trained model (nnU-Net style model folder, including `dataset.json`) is available on HuggingFace: [edomerli/nnUNet-PanTS-regions](https://huggingface.co/edomerli/nnUNet-PanTS-regions).

## Prediction and evaluation

After downloading the model checkpoint, fill in your own paths below (PanTS given Dataset ID 3):

```bash
# predict
nnUNetv2_predict_from_modelfolder -m /path/to/downloaded/hf/model/repo/ \
    -i /path/to/nnUNet_raw/Dataset003_PanTS_regions/imagesTs \
    -o /path/to/nnUNet_output/Dataset003_PanTS_regions/nnUNet_PanTS_submission \
    -f all -chk checkpoint_best.pth --disable_progress_bar

# evaluate
python /path_to_this_repo/nnunetv2/custom_code/evaluate_predictions_sens_spec.py \
    /path/to/nnUNet_raw/Dataset003_PanTS_regions/labelsTs \
    /path/to/nnUNet_output/Dataset003_PanTS_regions/nnUNet_PanTS_submission \
    -djfile /path/to/nnUNet_output/Dataset003_PanTS_regions/nnUNet_PanTS_submission/dataset.json \
    -pfile /path/to/nnUNet_output/Dataset003_PanTS_regions/nnUNet_PanTS_submission/plans.json \
    -np 8 \
    -o /path/to/nnUNet_output/Dataset003_PanTS_regions/nnUNet_PanTS_submission/summary_sens_spec.json
```

`/path/to/nnUNet_output` is any folder where you want to store the prediction output.

## Results (PanTS official in-distribution test set)

| Metric | Value |
|---|---|
| P-sensitivity @ 0.9 spec | 83.44% |
| P-specificity @ 0.9 spec | 90.13% |
| T-sensitivity | 76.16% |
| AUC | 0.902 |
| Pancreatic lesion DSC | 50.91% |

**Metric definitions:**
- **P-sensitivity / P-specificity @ volume threshold**: patient-wise metrics computed at varying prediction-volume thresholds. A patient is a ground-truth positive if any voxel carries the tumor label; a prediction is called positive if its predicted tumor voxel count exceeds the threshold. The reported values are taken at the threshold where specificity = 0.9.
- **AUC**: area under the sensitivity/specificity curve traced across all volume thresholds above.
- **T-sensitivity**: tumor-wise sensitivity; a predicted tumor counts as a true positive only if its DSC with the ground-truth tumor is ≥ 0.1 for that patient.