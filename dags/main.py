from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.operators.python_operator import PythonOperator
from kubernetes_pod_operator_work.dags import config_storage_apis
from kubernetes.client import models as k8s

default_args = {
    'owner': '467s',
    'depends_on_past': False,
    'start_date': days_ago(2),
}

c1 = k8s.V1Container(
    name="containe1",
    image="busybox",
)
c2 = k8s.V1Container(
    name="container2",
    image="busybox",
)

p = k8s.V1Pod(
    api_version="v1",
    kind="Pod",
    metadata=k8s.V1ObjectMeta(
        namespace="default",
        name="share-pod"
    ),
    spec=k8s.V1PodSpec(
        restart_policy='Never',
        containers=[c1, c2],
    )
)

pod_template_file = """
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: share-pod
  name: share-pod
spec:
  containers:
  - image: busybox
    name: container1
  - image: busybox
    name: container2
  restartPolicy: Always
"""


with DAG(
    'test_kubernetes_pod_operator_work',
    default_args=default_args,
    description='KubernetesPodOperatorを試す',
    tags=["work"],
) as dag:
    dag.doc_md = """
    KubernetesPodOperatorを試す
    """
    k = KubernetesPodOperator(
        namespace='default',
        name="hello-dry-run-work",
        image="debian",
        cmds=["sh", "-c", "mkdir -p /airflow/xcom/;echo '[1,2,3,4]' > /airflow/xcom/return.json"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        secrets=[
            config_storage_apis.secret_file(),
            config_storage_apis.secret_env(),
            config_storage_apis.secret_all_keys()],
        volumes=[config_storage_apis.volume()],
        volume_mounts=[config_storage_apis.volume_mount()],
        env_from=config_storage_apis.configmaps(),
        do_xcom_push=False,
        in_cluster=False,
    )
    k2 = KubernetesPodOperator(
        full_pod_spec=p,
        task_id="dry_run_demo2",
        do_xcom_push=False,
        in_cluster=False,
    )

    k3 = KubernetesPodOperator(
        namespace='default',
        pod_template_file=pod_template_file,
        task_id="dry_run_demo3",
        do_xcom_push=False,
        in_cluster=False,
    )

    def print_dry_run(*kwargs):
        print(k3.dry_run())
    
    o = PythonOperator(
        task_id='print_dry_run',
        python_callable=print_dry_run,
        dag=dag,
    )
        
    k >> [k3, o]
