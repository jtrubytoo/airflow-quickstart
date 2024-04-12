# --------------- #
# PACKAGE IMPORTS #
# --------------- #

from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime

from airflow.providers.amazon.aws.operators.sqs import SqsPublishOperator

# -------------------- #
# Local module imports #
# -------------------- #

from include.global_variables import airflow_conf_variables as gv
from include.global_variables import constants as c

# -------- #
# Datasets #
# -------- #

start_dataset = Dataset("start")

# --- #
# DAG #
# --- #

@dag(
    start_date=datetime(2023, 1, 1),
    # this DAG runs as soon as the climate and weather data is ready in DuckDB
    schedule=[start_dataset],
    catchup=False,
    default_args=gv.default_args,
    description="Publishes a notification of completed run to SQS.",
    tags=["part_3"],
)
def publish_to_sqs():
        
    gv.task_log.info("I'm in the DAG")

    publish_to_queue_1 = SqsPublishOperator(
        task_id="publish_to_queue_1",
        aws_conn_id="aws_conn",
        sqs_queue="https://sqs.eu-west-2.amazonaws.com/383276468458/airflow-test-q",
        message_content="{{ task_instance }}-{{ logical_date }}",
        region_name="eu-west-2",
    )

publish_to_sqs()
