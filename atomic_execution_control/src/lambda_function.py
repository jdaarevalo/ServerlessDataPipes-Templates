import os
from datetime import date
from time import sleep

from atomic_execution_control import AtomicExecutionControl

from aws_lambda_powertools import Logger

logger = Logger()

TABLE_NAME = "lambda_executions"
PRIMARY_KEY = "date_to_run"

# Initialize AtomicExecutionControl
aec = AtomicExecutionControl(
    table_name=TABLE_NAME,
    primary_key=PRIMARY_KEY,
    region_name="eu-west-1",
    endpoint_url="http://docker.for.mac.localhost:8000/" if os.environ.get("AWS_SAM_LOCAL") else None,
    logger=logger
)

def lambda_handler(event, context):
    

    # Attempt to write a lock key for today's date
    date_to_run = '2024-01-01'

    # delete items in Dynamo for old executions
    aec.delete_items_finished_or_old(keys=[date_to_run], item_execution_valid_for=1)

    # write in Dynamo the date_to_run and block other executions to the same key
    result = aec.write_atomically_a_key(key=date_to_run)

    if result:
        try:
            # If lock is acquired, perform your task
            print("Lock acquired, proceeding with task.")
            ## run_your_etl(date_to_run)
            sleep(10)
            # Remember to update the status to 'finished' after completing your task
            aec.update_status(key=date_to_run)
        except Exception as e:
            # If any error occurs, delete the item
            aec.delete_item(keys=[date_to_run])
            raise e
    else:
        # If lock couldn't be acquired, another instance is already processing the task
        print("Task already in progress by another instance.")
        # wait until other instances with the same key finish
        aec.wait_other_instances_finish(keys=[date_to_run])
    
    return {"statusCode": 200, "body": "ok"}  
