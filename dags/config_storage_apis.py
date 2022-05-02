from airflow.kubernetes.secret import Secret
from kubernetes.client import models as k8s

def secret_file():
    """ 
    https://airflow.apache.org/docs/apache-airflow/1.10.1/_modules/airflow/contrib/kubernetes/secret.html
    spec:
        containers:
        - volumeMounts:
        - mountPath: /etc/sql_conn
            name: hoge
            readOnly: true
        voluems:
        - name: hoge
        secret:
            secretName: airflow-secrets
    """
    return Secret(
        deploy_type='volume', deploy_target='/etc/sql_conn',
        secret='airflow-secrets'
        )

def secret_env():
    """
    https://airflow.apache.org/docs/apache-airflow/1.10.1/_modules/airflow/contrib/kubernetes/secret.html
    spec:
    containers:
    - env:
        - name: SQL_CONN
            valueFrom:
            secretKeyRef:
                name: airflow-secrets
                key: sql_alchemy_conn
    """
    return Secret(
        deploy_type='env', deploy_target='SQL_CONN',
        secret='airflow-secrets', key='sql_alchemy_conn'
        )

def secret_all_keys():
    """
    https://airflow.apache.org/docs/apache-airflow/1.10.1/_modules/airflow/contrib/kubernetes/secret.html
    spec:
    containers:
        - envFrom:
          - secretRef:
              name: airflow-secrets-2
    """
    return Secret(
        deploy_type='env', deploy_target=None,
        secret='airflow-secrets-2'
        )

def volume_mount():
    """
    https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1VolumeMount.md
    spec:
      containers:
      - volumeMounts:
        - name: test-volume
          mountPath: /root/mount_file
    """
    return k8s.V1VolumeMount(
        mount_path='/root/mount_file', name='test-volume',
        read_only=True, sub_path=None, sub_path_expr=None,
        mount_propagation=None
        )

def volume():
    """
    https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Volume.md
    spec:
      volumes:
        - name: test-volume
          persistentVolumeClaim:
            claimName: my-pvc
    """
    return k8s.V1Volume(
        name='test-volume',
        persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
            claim_name='my-pvc'),
        )

def configmaps():
    """
    spec:
        containers:
        - envFrom:
          - configMapRef:
            name: test-configmap-1
          - configMapRef:
            name: test-configmap-2
    """
    return [
        k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='test-configmap-1')),
        k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='test-configmap-2')),
        ]
