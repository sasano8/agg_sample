import docker
import time


def watch(namespace: str):
    # Dockerクライアントを作成します
    client = docker.from_env()

    # 監視するコンテナの名前を指定します
    container_name = "your-container-name"

    # コンテナの状態を監視し、完了または失敗した場合に情報を取得します
    while True:
        try:
            # コンテナの情報を取得します
            container = client.containers.get(container_name)

            # コンテナの状態を取得します
            container_status = container.status

            if container_status == "exited":
                print(f"Container {container_name} exited.")
                exit_code = container.attrs["State"]["ExitCode"]
                if exit_code == 0:
                    print(f"Container {container_name} succeeded.")
                else:
                    print(f"Container {container_name} failed with exit code {exit_code}.")
                break
            elif container_status == "running":
                print(f"Container {container_name} is still running.")
                time.sleep(5)
            else:
                print(f"Container {container_name} is in status: {container_status}.")
                time.sleep(5)

        except docker.errors.NotFound:
            print(f"Container {container_name} not found.")
            time.sleep(5)
            
def list_job(namespace: str):
    import docker

    # Dockerクライアントを作成します
    client = docker.from_env()

    # すべてのコンテナを取得します
    containers = client.containers.list(all=True)

    # コンテナの一覧を表示します
    for container in containers:
        print(f"Container ID: {container.id}, Name: {container.name}, Status: {container.status}")
        

def get_namespace_info(namespace: str):
    #dockerではnamespaceの機能はない。network機能で代替する。
    import docker

    # Dockerクライアントを作成します
    client = docker.from_env()

    # 新しいDockerネットワークを作成します
    # network = client.networks.create("your_network_name")

    # 作成したネットワークにコンテナを接続します
    container = client.containers.run("your_image_name", name="your_container_name", detach=True)
    network.connect(container)



# dockerでは実行時に任意のラベルを付与することができます
# docker run --label version=1.0 --label maintainer=your_name@example.com --label description="Sample Python application" -d your_image
# docker ps --filter "label=maintainer=your_name@example.com"
# docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Label \"maintainer\"}}"