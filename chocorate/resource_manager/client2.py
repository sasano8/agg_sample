import yaml
from kubernetes import config, utils, watch
from kubernetes import client as kclient
import asyncio
from kubernetes.client.models.v1_job import V1Job
import orjson


def get_kind(obj: dict):
    items = {k.lower(): v for k, v in obj.items()}
    if "kind" not in items:
        return None, items
    else:
        return items["kind"].lower(), items


class K8sController:
    def __init__(self, client: kclient.ApiClient):
        self.client = client
        self.api = kclient.AppsV1Api(client)

    @staticmethod
    def make_from_file(file, **kwargs):
        with open(file, "r") as f:
            data = yaml.safe_load(f)
        obj = data.format(**kwargs)
        return obj

    @staticmethod
    def make_from_str(data: str, **kwargs):
        if not isinstance(data, str):
            raise Exception()
        obj = yaml.safe_load(data.format(**kwargs))
        return obj

    def create(self, body: dict, namespace: str = "default"):
        if not isinstance(body, dict):
            raise Exception()

        kind, body = get_kind(body)
        # if kind == "batch/v1":
        if kind == "job":
            c = kclient.BatchV1Api(self.client)
            ret: V1Job = c.create_namespaced_job(
                namespace=namespace, body=body, async_req=False
            )
            ret = ret.to_dict()
            # async_req=False と True で型が違う
            # async_req=True は使わないでよい（threadpoolで実行すればよい）
            # ret = thread.get()  # 実行は完了していないのでまだ結果を取得できない
        elif kind == "batch/????":
            raise NotImplementedError()
            c = kclient.AppsV1Api(self.client)
            ret = c.create_namespaced_deployment(namespace="default", body=body)
        else:
            raise Exception()
        return ret

    def apply(self, body: dict, namespace: str = "default"):
        ret = self.api.replace_namespaced_deployment(namespace="default", body=body)
        return ret

    def patch(self):
        raise NotImplementedError()
        # applyとpatchの違いが分からない
        api.patch_namespaced_deployment(namespace="default", body=body)

    def delete(self, body: dict, namespace: str = "default"):
        ret = self.api.delete_namespaced_deployment(namespace="default", body=body)
        return ret
    
    def watch(self, namespace: str = "default"):
        api_instance = kclient.BatchV1Api(self.client)
        w = watch.Watch()
        for event in w.stream(api_instance.list_namespaced_job, namespace):
            job = event['object']
            result = job.status
            print(result)

    @staticmethod
    def _sample_error():
        return {
            "kind": "Status",
            "apiVersion": "v1",
            "metadata": {},
            "status": "Failure",
            "message": 'jobs.batch "hello-world" already exists',
            "reason": "AlreadyExists",
            "details": {"name": "hello-world", "group": "batch", "kind": "jobs"},
            "code": 409,
        }

    @staticmethod
    def _sample_job():
        import datetime

        return {
            "api_version": "batch/v1",
            "kind": "Job",
            "metadata": {
                "annotations": None,
                "cluster_name": None,
                "creation_timestamp": datetime.datetime(
                    2023, 4, 15, 23, 21, 25, tzinfo=tzlocal()
                ),
                "deletion_grace_period_seconds": None,
                "deletion_timestamp": None,
                "finalizers": None,
                "generate_name": None,
                "generation": 1,
                "labels": {
                    "controller-uid": "ca7e647e-a00e-4681-a557-38d59fe417e0",
                    "job-name": "hello-world2",
                },
                "managed_fields": [
                    {
                        "api_version": "batch/v1",
                        "fields_type": "FieldsV1",
                        "fields_v1": {
                            "f:spec": {
                                "f:backoffLimit": {},
                                "f:completionMode": {},
                                "f:completions": {},
                                "f:parallelism": {},
                                "f:suspend": {},
                                "f:template": {
                                    "f:spec": {
                                        "f:containers": {
                                            'k:{"name":"pi"}': {
                                                ".": {},
                                                "f:image": {},
                                                "f:imagePullPolicy": {},
                                                "f:name": {},
                                                "f:resources": {},
                                                "f:terminationMessagePath": {},
                                                "f:terminationMessagePolicy": {},
                                            }
                                        },
                                        "f:dnsPolicy": {},
                                        "f:restartPolicy": {},
                                        "f:schedulerName": {},
                                        "f:securityContext": {},
                                        "f:terminationGracePeriodSeconds": {},
                                    }
                                },
                                "f:ttlSecondsAfterFinished": {},
                            }
                        },
                        "manager": "OpenAPI-Generator",
                        "operation": "Update",
                        "time": datetime.datetime(
                            2023, 4, 15, 23, 21, 25, tzinfo=tzlocal()
                        ),
                    }
                ],
                "name": "hello-world2",
                "namespace": "default",
                "owner_references": None,
                "resource_version": "414978",
                "self_link": None,
                "uid": "ca7e647e-a00e-4681-a557-38d59fe417e0",
            },
            "spec": {
                "active_deadline_seconds": None,
                "backoff_limit": 6,
                "completions": 1,
                "manual_selector": None,
                "parallelism": 1,
                "selector": {
                    "match_expressions": None,
                    "match_labels": {
                        "controller-uid": "ca7e647e-a00e-4681-a557-38d59fe417e0"
                    },
                },
                "template": {
                    "metadata": {
                        "annotations": None,
                        "cluster_name": None,
                        "creation_timestamp": None,
                        "deletion_grace_period_seconds": None,
                        "deletion_timestamp": None,
                        "finalizers": None,
                        "generate_name": None,
                        "generation": None,
                        "labels": {
                            "controller-uid": "ca7e647e-a00e-4681-a557-38d59fe417e0",
                            "job-name": "hello-world2",
                        },
                        "managed_fields": None,
                        "name": None,
                        "namespace": None,
                        "owner_references": None,
                        "resource_version": None,
                        "self_link": None,
                        "uid": None,
                    },
                    "spec": {
                        "active_deadline_seconds": None,
                        "affinity": None,
                        "automount_service_account_token": None,
                        "containers": [
                            {
                                "args": None,
                                "command": None,
                                "env": None,
                                "env_from": None,
                                "image": "hello-world",
                                "image_pull_policy": "Always",
                                "lifecycle": None,
                                "liveness_probe": None,
                                "name": "pi",
                                "ports": None,
                                "readiness_probe": None,
                                "resources": {"limits": None, "requests": None},
                                "security_context": None,
                                "startup_probe": None,
                                "stdin": None,
                                "stdin_once": None,
                                "termination_message_path": "/dev/termination-log",
                                "termination_message_policy": "File",
                                "tty": None,
                                "volume_devices": None,
                                "volume_mounts": None,
                                "working_dir": None,
                            }
                        ],
                        "dns_config": None,
                        "dns_policy": "ClusterFirst",
                        "enable_service_links": None,
                        "ephemeral_containers": None,
                        "host_aliases": None,
                        "host_ipc": None,
                        "host_network": None,
                        "host_pid": None,
                        "hostname": None,
                        "image_pull_secrets": None,
                        "init_containers": None,
                        "node_name": None,
                        "node_selector": None,
                        "overhead": None,
                        "preemption_policy": None,
                        "priority": None,
                        "priority_class_name": None,
                        "readiness_gates": None,
                        "restart_policy": "Never",
                        "runtime_class_name": None,
                        "scheduler_name": "default-scheduler",
                        "security_context": {
                            "fs_group": None,
                            "run_as_group": None,
                            "run_as_non_root": None,
                            "run_as_user": None,
                            "se_linux_options": None,
                            "supplemental_groups": None,
                            "sysctls": None,
                            "windows_options": None,
                        },
                        "service_account": None,
                        "service_account_name": None,
                        "share_process_namespace": None,
                        "subdomain": None,
                        "termination_grace_period_seconds": 30,
                        "tolerations": None,
                        "topology_spread_constraints": None,
                        "volumes": None,
                    },
                },
                "ttl_seconds_after_finished": 1000,
            },
            "status": {
                "active": None,
                "completion_time": None,
                "conditions": None,
                "failed": None,
                "start_time": None,
                "succeeded": None,
            },
        }


request = """
apiVersion: batch/v1
kind: Job
metadata:
  name: hello-world2
spec:
  ttlSecondsAfterFinished: 1000  # 保存期間
  template:
    spec:
      containers:
      - name: pi
        image: hello-world
        command: []
      restartPolicy: Never
"""


config.load_kube_config()
k8s_client = kclient.ApiClient()
obj = K8sController(k8s_client)

data = obj.make_from_str(request)
ret = obj.create(data)
obj.watch()
# print(orjson.dumps(ret))
# print(type(ret))
# print(ret["status"])
# print(ret["labels"]["job-name"])
# print(ret["metadata"]["creation_timestamp"])
# print(ret["api_version"])
# print(ret["kind"])

# status = {
#     "active": None,
#     "completion_time": None,
#     "conditions": None,
#     "failed": None,
#     "start_time": None,
#     "succeeded": None,
# }

