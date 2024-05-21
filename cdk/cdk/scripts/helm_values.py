import json
import os
import boto3

def handler(event, context):
    try:
        # Fetch the environment value from SSM
        ssm_client = boto3.client('ssm')
        parameter_name = os.environ['PARAMETER_NAME']
        response = ssm_client.get_parameter(Name=parameter_name)
        env_value = response['Parameter']['Value']
        
        # Determine the replica count based on the environment
        if env_value == 'development':
            replica_count = 1
        elif env_value in ['staging', 'production']:
            replica_count = 2
        else:
            raise ValueError(f"Unexpected environment value: {env_value}")

        
        # Return the values for use in the CustomResource output
        return {
            'Status': 'SUCCESS',
            'PhysicalResourceId': context.log_stream_name,
            'Data': {'helm_values': replica_count}
        }
    except Exception as e:
        return {
            'Status': 'FAILED',
            'PhysicalResourceId': context.log_stream_name,
            'Data': {'Error': str(e)}
        }
# be sure this output can be consumed by the CustomResource in CRStack and notified to CloudFormation