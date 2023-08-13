import boto3
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# def create_snapshot_rds(cluster_name="micrologx-restaurant-infra-production-rdsdbcluster-dzeoaag5shsa", snapshot_prefix="lambda-"):
def create_snapshot_rds(cluster_name, snapshot_prefix="lambda-"):
    print("@create_snapshot_rds")
    print(cluster_name, snapshot_prefix)
    client = boto3.client('rds')
    resp = client.create_db_cluster_snapshot(
        DBClusterIdentifier=cluster_name,
        DBClusterSnapshotIdentifier=(snapshot_prefix + timestamp)
    )
    print(resp)
    return resp["DBClusterSnapshot"]["DBClusterSnapshotIdentifier"], resp["DBClusterSnapshot"]["DBClusterIdentifier"]


def PipelineResponseModel(data, job_id, message="Success"):
    pipeline = boto3.client('codepipeline')
    return pipeline.put_job_success_result(
        jobId=job_id,
        outputVariables=data
    )

def PipelineErrorResponse(error: str, job_id: str, execution_id="exec_id"):
    pipeline = boto3.client('codepipeline')
    return pipeline.put_job_failure_result(
        jobId=job_id,
        failureDetails={
            'type': "JobFailed",
            'message': error,
            'externalExecutionId': execution_id
        }
    )
