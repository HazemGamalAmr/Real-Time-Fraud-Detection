from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
with DAG(
    'gcs_to_dataproc_to_bigquery_direct',
    default_args=default_args,
    description='Trigger PySpark on Dataproc from new data in GCS, PySpark handles loading into BigQuery',
    schedule_interval=None,
    catchup=False,
) as dag:

    # Task 1: Listen for new data in GCS bucket (Sensor)
    gcs_sensor_task = GCSObjectExistenceSensor(
        task_id='wait_for_new_gcs_data',
        bucket='iti-datalake',  # Replace with your GCS bucket
        object='streamingData/*.csv',  # Match new files (e.g., CSVs)
        timeout=600,  # Timeout in seconds
        poke_interval=10,  # Interval to check for new file
    )

    # Task 2: Pass the detected file path to the Spark job
    def get_file_path(**kwargs):
        bucket = kwargs['bucket']
        object = kwargs['object']
        return f"gs://{bucket}/{object}"

    get_gcs_file_task = PythonOperator(
        task_id='get_gcs_file_path',
        python_callable=get_file_path,
        provide_context=True,
        op_kwargs={
            'bucket': 'iti-datalake',  # Replace with your GCS bucket
            'object': 'streamingData/*.csv',
        },
    )

    # Task 3: Run PySpark Job on Dataproc to process data and load into BigQuery
    dataproc_spark_task = DataprocSubmitJobOperator(
        task_id='run_pyspark_job_on_dataproc',
        job={
            'reference': {'project_id': 'iti-graduation-project-434313'},  # Replace with your project ID
            'placement': {'cluster_name': 'cluster-368c'},  # Replace with Dataproc cluster
            'pyspark_job': {
                'main_python_file_uri': 'gs://GCS/Test_DAG.py',  # Replace with PySpark script in GCS
                'args': ['{{ ti.xcom_pull(task_ids="get_gcs_file_path") }}'],  # Pass the detected file path
            },
        },
        region='europe-west12',  # Replace with your Dataproc region
    )

    # Define the task dependencies
    gcs_sensor_task >> get_gcs_file_task >> dataproc_spark_task
