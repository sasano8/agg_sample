def validate(val: str):
    if val is None:
        raise Exception()


class K8sController:
    def volume_template(self, name: str, size_gb: float):
        f"""
        metadata:
            name: "{name}"
        spec:
            accessModes:
                - ReadWriteOnce
            resources:
                requests:
                    storage: {size_gb}Gi
        """

    def volume_create(self, name: str, size_gb: float):
        spec = self.volume_template(name, size_gb)

    def volume_delete(self, name: str):
        ...

    def volume_list(self, name: str):
        ...

    def job_template(self):
        """
        apiVersion: batch/v1
        kind: CronJob
        metadata:
          name: hello
        spec:
          schedule: "* * * * *"
          jobTemplate:
            spec:
              template:
                spec:
                  containers:
                  - name: hello
                    image: busybox
                    command:
                    - /bin/sh
                    - -c
                    - date; echo Hello from the Kubernetes cluster
                  restartPolicy: OnFailure
        """


class DockerController:
    def volume_template(self, name: str, size_gb: float):
        ...

    def volume_create(self, name: str, size_gb: float):
        spec = self.volume_template(name, size_gb)

    def volume_delete(self, name: str):
        ...

    def volume_list(self, name: str):
        ...
