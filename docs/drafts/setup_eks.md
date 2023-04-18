<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">

# kubeflowのセットアップ

参考ドキュメントは次の通り。

- https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html#create-service-role
- https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/install-kubectl.html
- https://awslabs.github.io/kubeflow-manifests/docs/deployment/vanilla/guide/

### 要件

- Kubernetes クラスター構築用ホスト1台
- 開発用クラスター最小スペック
  - Kubernetes 1.8以降:
    - CPU 3つ？？？
    - クラスター内の最小 0.6 CPU (3 つの複製されたアンバサダー ポッド用に予約されており、必要に応じて追加の CPU を追加します)
    - ストレージが 10 GB 以上のノード (ML ライブラリとサードパーティ パッケージが Kubeflow Docker イメージにバンドルされているため)
  - メモリ: ??
- 本番用クラスター最小スペック
  - Kubernetes 1.8以降:
    - ???
    - ???
  - メモリ: ??

# Kubernetes 接続用ホスト / kubectl のセットアップ

## aws用

### Kubernetes クラスター構築用ホストの構築

開発用にはcloud9が簡単なのでオススメする。

### アーキテクチャの確認

アーキテクチャを確認します。

```shell
dpkg --print-architecture
ARCHITECTURE=amd64
```

### awscliのインストール

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### eksctlのインストール(amd64)

```shell
# curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.25.7/2023-03-17/bin/linux/${ARCHITECTURE}/kubectl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_${ARCHITECTURE}.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

### kubeflowに関するツールのインストール（kubectl等）

kubeflowセットアップに必要なツールをインストールする。

```shell
sudo apt update
sudo apt install git curl unzip tar make sudo vim wget -y
export KUBEFLOW_RELEASE_VERSION=v1.6.1
export AWS_RELEASE_VERSION=v1.6.1-aws-b1.0.2
git clone https://github.com/awslabs/kubeflow-manifests.git && cd kubeflow-manifests
git checkout ${AWS_RELEASE_VERSION}
git clone --branch ${KUBEFLOW_RELEASE_VERSION} https://github.com/kubeflow/manifests.git upstream

make install-tools
```

### aws configure

- 使用するユーザーにはEKSの権限が付与されていること（eksClusterRole というロールを作成するのが一般的）
- awsのIAMのユーザーコンソールからアクセスキー・シークレットキーが発行されていること

```shell
# AWS_PROFILE=default はcloud9によって予約されているので変更しないように
export AWS_PROFILE=kubeflow
aws configure --profile=$AWS_PROFILE
aws sts get-caller-identity  # 疎通確認
```

### eksクラスタの構築

所要時間は20分ほどです。

まず、クラスタの配置場所を決める。

```shell
export CLUSTER_NAME=kubeflow  # 任意の名前
export CLUSTER_REGION=ap-northeast-1
```

`CLUSTER_NAME`がすでに存在している場合は必要に応じて削除する。

```shell
eksctl get cluster --region ${CLUSTER_REGION}
eksctl delete cluster --region ${CLUSTER_REGION} --name ${CLUSTER_NAME} 
```

クラスタで使用するインスタンスを決める。
CPUは4以上使用できる必要あり。

- https://instances.vantage.sh
- t3.xlarge: $0.1043 hourly  	4cpu	16 GiB（インストール失敗）
- m5.large: $0.0960 hourly		2cpu	8 GiB
- p3.2xlarge: １時間あたり 3.06 USD	8cpu	61 GiB(多分GPU)

クラスタを作成する（以下は開発用の最小構成）。

```shell
export KUBE_VERSION=1.22
export NODE_TYPE=t3.xlarge
export NODES_MIN=1
export NODES_MAX=2

eksctl create cluster \
--name ${CLUSTER_NAME} \
--version ${KUBE_VERSION} \
--region ${CLUSTER_REGION} \
--nodegroup-name linux-nodes \
--node-type ${NODE_TYPE} \
--nodes ${NODES_MIN} \
--nodes-min ${NODES_MIN} \
--nodes-max ${NODES_MAX} \
--managed \
--with-oidc
```

以前に同じ名前でクラスタを作成していた場合、現在同名のクラスターが存在していなくても、`AlreadyExistsException`になることがあります（半日以上キャッシュが残る可能性あり）。

その場合、時間をおいて再試行するか、`CLUSTER_NAME`を変更して実行してください。

### eksクラスタの疎通確認

```shell
aws eks update-kubeconfig --region $CLUSTER_REGION --name $CLUSTER_NAME
kubectl get pods
```

### kubeflowの構築

所要時間は20分ほどです。

メトリックサーバをインストールする。
kubeflow 構築が終わらない場合、リソース不足の可能性があり、メトリックサーバで原因を解析する。
（代わりにPrometheusも使える？？）

```shell
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

```shell
kubectl top pods --all-namespaces --sum
```

kubeflowのpod群を展開する。

`vanilla`は簡易設定なので、本番での使用は控えること。

```shell
make deploy-kubeflow INSTALLATION_OPTION=kustomize DEPLOYMENT_OPTION=vanilla
```

kubeflowのpod群を削除する場合は次のように実行する。

```shell
make delete-kubeflow INSTALLATION_OPTION=kustomize DEPLOYMENT_OPTION=vanilla
```

### 疎通確認

エラーが生じていないか確認する。

```shell
kubectl get pods --all-namespaces
```

kubeflow UIをホスト上にポートフォワードする。

```shell
make port-forward
```

デフォルトでは次の認証情報でログイン可能。

- user@example.com
- 12341234

Cloud9上のブラウザ（Preview Running Applicationで起動。デフォルトで8080番のアプリケーションに繋がる）では上手く動作しないことがある。
Cloud9のブラウザを開いた後、`<i class="material-icons">`open_in_new `</i>` からローカルブラウザで確認する。


### .bashrcの保存

`~/.bashrc` で次の変数を設定するようにします。

```shell
export AWS_PROFILE=kubeflow
export CLUSTER_NAME=kubeflow
export CLUSTER_REGION=ap-northeast-1
export KUBE_VERSION=1.22
export NODE_TYPE=t3.xlarge
export NODES_MIN=1
export NODES_MAX=2
```
