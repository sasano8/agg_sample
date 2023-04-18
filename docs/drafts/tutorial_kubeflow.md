

- kubeflow: https://github.com/kubeflow/kubeflow/blob/master/components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/api/custom_resource.py
- tutorial: https://www.youtube.com/watch?v=6wWdNg0GMV4&t=477s
- tutorial: https://github.com/flopach/digits-recognizer-kubeflow


# トラブルシューティング


## jupyterでsudoできない

kubeflowではセキュリティ上の理由からsudoできません。


` kubectl get pod -n kubeflow-user-example-com test2-0 -o jsonpath='{.status.containerStatuses[?(@.name == "istio-proxy")].containerID}`
