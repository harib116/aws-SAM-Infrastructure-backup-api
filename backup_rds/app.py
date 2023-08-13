import json
from amazon_rds import create_snapshot_rds, PipelineResponseModel, PipelineErrorResponse

def ResponseModel(data, message="Success", status_code=200):
    return {
        "data": data,
        "message": message,
        "status_code": status_code
    }

def ErrorResponseModel(error, message="Failed", status_code=400):
    return {
        "error": error,
        "message": message,
        "status_code": status_code
    }

def lambda_handler(event, context):
    """CP event"""
    if event.get("CodePipeline.job"):
        print("codepipeline")
        jobId = event['CodePipeline.job']['id']
        try:
            userparams = event["CodePipeline.job"]["data"]["actionConfiguration"]["configuration"]["UserParameters"]
            userparams = json.loads(userparams)
            dump = create_snapshot_rds(userparams["cluster_name"], userparams["snapshot_prefix"])
        except Exception as E:
            print(repr(E))
            return PipelineErrorResponse(repr(E), jobId)
        return PipelineResponseModel({"output": str(dump)}, jobId)
    
    """Normal event"""
    # dump = create_snapshot_rds("micrologx-restaurant-infra-production-rdsdbcluster-dzeoaag5shsa", "lambda-")
    print(event)
    try:
        dump = create_snapshot_rds(event["cluster_name"], event["snapshot_prefix"])
    except Exception as E:
        print(repr(E))
        return ErrorResponseModel(repr(E))
    return ResponseModel(dump)

if __name__ == "__main__":
    r = lambda_handler({}, {})
    print(r)