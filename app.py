import pygogo as gogo
from kubernetes import client, config
from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.models.v1_pod_status import V1PodStatus
from kubernetes.client.models.v1_container_status import V1ContainerStatus
import os
import time

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main():
    logger.info("Staring...")
    config.load_incluster_config()
    # kubectl get pods --label-selector={key=value} -n {namespace}
    k8s_client = client.CoreV1Api()
    while True:
        check_for_pods_crashlooping(k8s_client)
        logger.debug("Sleeping")
        time.sleep(60)


def check_for_pods_crashlooping(k8s_client):
    logger.debug("Checking for pods")
    pods = get_pods(k8s_client)  # type: [V1Pod]
    for pod in pods:
        status = pod.status  # type: V1PodStatus
        statuses = status.container_statuses  # type: [V1ContainerStatus]
        for status in statuses:
            if status.restart_count > int(get_config("KILL_AFTER_RESTARTS")):
                logger.info(f"Deleting {pod.metadata.name}")  # delete_pod(k8s_client, pod)
                delete_pod(k8s_client, pod)


def delete_pod(k8s_client, pod):
    logger.info(f"Deleting {pod.metadata.name}")
    api_response = k8s_client.delete_namespaced_pod(name=pod.metadata.name, namespace=get_config("NAMESPACE"))
    logger.info(f"Deleted {pod.metadata.name}, status='{api_response.status}'")


def get_pods(k8s_client):
    api_response = k8s_client.list_namespaced_pod(get_config("NAMESPACE"), label_selector=get_config("LABEL_SELECTOR"))
    pods = api_response.items
    return pods


def get_config(key):
    return os.environ.get(key)


if __name__ == '__main__':
    main()
