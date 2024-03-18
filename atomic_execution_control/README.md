# Testing AtomicExecutionControl


### Create the virtual environment

```bash
conda create -n "test_aec_env" python=3.10 ipython
```

To activate this environment, use

```bash
conda activate test_aec_env
```

optional, ensure your python path is correct 

```bash
export PATH="/Users/David/opt/anaconda3/envs/test_aec_env/bin:$PATH"
```

### Install requirements locally

```bash
rm -rf libs
mkdir -p libs/python/lib/python3.10/site-packages
pip3 install -r requirements.txt --target libs/python/lib/python3.10/site-packages
```

### Initialize DynamoDB 

Initialize the DynamoDB container using Docker Compose

```bash
docker-compose up
```

Check if the table exists

```bash
aws dynamodb list-tables --endpoint-url http://localhost:8000

```

If it is required, create the table with the file `create_dynamodb_table.json`

```bash
aws dynamodb create-table --cli-input-json file://create_dynamodb_table.json --endpoint-url http://localhost:8000

```

#### Delete DynamoDB table

```bash
aws dynamodb delete-table --table-name quality_score_survey_id_execution --endpoint-url http://localhost:8000
```
