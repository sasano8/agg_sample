import os
import profile
import boto3
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client.api_client import ApiClient

# AWSの認証情報を設定します。
os.environ["AWS_ACCESS_KEY_ID"] = "<your-access-key-id>"
os.environ["AWS_SECRET_ACCESS_KEY"] = "<your-secret-access-key>"
os.environ["AWS_DEFAULT_REGION"] = "<your-region>"

# Amazon EKSクラスターの名前を設定します。
cluster_name = "<your-eks-cluster-name>"

# EKSクラスターのkubeconfigを取得し、ローカルファイルに保存します。
eks = boto3.client("eks")
cluster_info = eks.describe_cluster(name=cluster_name)
kubeconfig = cluster_info["cluster"]["endpoint"]

with open("kubeconfig.yaml", "w") as f:
    f.write(kubeconfig)

# Kubernetes Pythonクライアントライブラリの設定をロードします。
config.load_kube_config(config_file="kubeconfig.yaml")

# Kubernetes APIクライアントを作成します。
kube_client = client.CoreV1Api()

# Kubernetesクラスターのすべてのノードをリストします。
try:
    nodes = kube_client.list_node()
    for node in nodes.items:
        print(f"Node Name: {node.metadata.name}")
except ApiException as e:
    print(f"Error: {e}")


# eksctl get cluster --name kubeflow -o json

# 全部手動で設定しようとするとロールやら色々設定しなければいけないので、面倒なので自動ロードにまかせる。
conf = {
    "type": "eks",
    # "CONFIG_PATH": None,
    "PROFILE_NAME": "kubeflow",
    "AWS_REGION": "ap-northeast-1",
    "CLUSTER_NAME": "kubeflow",
}

# 設定は自動で読み込まれる
# 最終的な優先順位は次のようになる
# コマンドラインオプション > 環境変数 > ~/.aws/credentials > ~/.aws/config

# config.load_kube_config(config_file=conf["CONFIG_PATH"])
# eks = boto3.client("eks", region_name=conf["AWS_REGION"], profile_name=conf["PROFILE_NAME"])

session = boto3.Session(
    region_name=conf["AWS_REGION"], profile_name=conf["PROFILE_NAME"]
)
eks = session.client("eks")
cluster_info = eks.describe_cluster(name=conf["CLUSTER_NAME"])
print(cluster_info)


# client = ApiClient(configuration=configuration)
# client.CoreV1Api()
