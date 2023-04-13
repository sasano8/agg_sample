# https://huggingface.co/docs/hub/models-downloading
# https://huggingface.co/docs/hub/models-libraries
# https://huggingface.co/docs/hub/repositories-getting-started

from huggingface_hub import hf_hub_download
import joblib

REPO_ID = "YOUR_REPO_ID"
FILENAME = "sklearn_model.joblib"

model = joblib.load(hf_hub_download(repo_id=REPO_ID, filename=FILENAME))


# git を使用する場合

"""
git lfs install
git clone git@hf.co:<MODEL ID> # example: git clone git@hf.co:bigscience/bloom
"""
