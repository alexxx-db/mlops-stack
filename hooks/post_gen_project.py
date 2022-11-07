import os
import shutil


def remove_filepath(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


project_name = "{{cookiecutter.project_name}}"
current_cloud = "{{cookiecutter.cloud}}"
cicd_platform = "{{cookiecutter.cicd_platform}}"
include_feature_store = {{cookiecutter.include_feature_store}}

mlp_paths = [
    os.path.join("profiles"),
    os.path.join("notebooks", "Train.py"),
    os.path.join("pipeline.yaml")
]

cloud_specific_paths = {
    "azure": [
        os.path.join(".github", "workflows", "scripts", "generate-aad-token.sh"),
        os.path.join(".mlops-setup-scripts", "cicd", "main-azure.tf"),
        os.path.join(".mlops-setup-scripts", "terraform", "main-azure.tf"),
        os.path.join(".mlops-setup-scripts", "terraform", "variables.tf"),
    ],
    "aws": [
        os.path.join(".mlops-setup-scripts", "cicd", "main-aws.tf"),
        os.path.join(".mlops-setup-scripts", "terraform", "main-aws.tf"),
    ],
}

for cloud, paths in cloud_specific_paths.items():
    if cloud != current_cloud:
        for path in paths:
            remove_filepath(path)


cicd_specific_paths = {
    "gitHub": [
        os.path.join(".github"),
    ],
    "azureDevOpsServices": [
        os.path.join(".azure"),
        os.path.join(".mlops-setup-scripts", "cicd", "azure-devops.tf"),
    ],
}

for cicd, paths in cicd_specific_paths.items():
    if cicd != cicd_platform:
        for path in paths:
            remove_filepath(path)

# Remove test files
test_paths = ["_params_testing_only.txt"]
if project_name != "27896cf3-bb3e-476e-8129-96df0406d5c7":
    for path in test_paths:
        os.remove(path)

# Remove MLP code in cases of Feature Store (they are not used).
if include_feature_store:
    for path in mlp_paths:
        os.remove(path)

readme_path = os.path.join(os.getcwd(), "README.md")
print(
    f"Finished generating ML project. See the generated README at {readme_path} for next steps!"
)
