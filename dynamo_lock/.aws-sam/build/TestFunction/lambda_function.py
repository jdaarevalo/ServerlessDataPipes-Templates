import os
from datetime import date
#from lambda_dynamo_lock import LambdaDynamoLock

from aws_lambda_powertools import Logger

logger = Logger()

TABLE_NAME = "answers_options_execution"
PRIMARY_KEY = "date_to_run"


def lambda_handler(event, context):
    print("#"*100)
    # Initialize LambdaDynamoLock
    ldl = LambdaDynamoLock(
        table_name=TABLE_NAME,
        primary_key=PRIMARY_KEY,
        region_name="eu-west-1",
        endpoint_url="http://docker.for.mac.localhost:8000/" if os.environ.get("AWS_SAM_LOCAL") else None,
        logger=logger
    )

    # Attempt to write a lock key for today's date
    date_to_run = '2023-01-01'
    print("#"*100)
    # delete items in Dynamo for old executions
    ldl.delete_items_finished_or_old(keys=[date_to_run], item_execution_valid_for=1)

    # write in Dynamo the date_to_run and block other executions to the same key
    result = ldl.write_atomically_a_key(key=date_to_run)

    if result:
        # If lock is acquired, perform your task
        print("Lock acquired, proceeding with task.")
        ## run_your_etl(date_to_run)
        # Remember to update the status to 'finished' after completing your task
        ldl.update_status(key=date_to_run)
    else:
        # If lock couldn't be acquired, another instance is already processing the task
        print("Task already in progress by another instance.")
        # wait until other instances with the same key finish
        ldl.wait_other_instances_finish(keys=[date_to_run])
    return "OK"
