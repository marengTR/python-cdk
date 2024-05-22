import json
import os
import pytest
from unittest import mock
from helm_values import handler

# Mock context object
class MockContext:
    log_stream_name = "mock_log_stream"

@pytest.fixture
def ssm_client_mock():
    with mock.patch('boto3.client') as mock_boto_client:
        yield mock_boto_client

@pytest.fixture
def env_vars():
    original_env = os.environ.copy()
    os.environ['PARAMETER_NAME'] = '/platform/account/env'
    yield
    os.environ = original_env

def test_handler_development(env_vars, ssm_client_mock):
    # Mock SSM response
    ssm_client_mock().get_parameter.return_value = {'Parameter': {'Value': 'development'}}
    
    event = {}
    context = MockContext()
    response = handler(event, context)
    
    expected_helm_values = {
        "controller": {
            "replicaCount": 1
        }
    }
    
    assert response['Status'] == 'SUCCESS'
    assert json.loads(response['Data']['helm_values']) == expected_helm_values

def test_handler_staging(env_vars, ssm_client_mock):
    # Mock SSM response
    ssm_client_mock().get_parameter.return_value = {'Parameter': {'Value': 'staging'}}
    
    event = {}
    context = MockContext()
    response = handler(event, context)
    
    expected_helm_values = {
        "controller": {
            "replicaCount": 2
        }
    }
    
    assert response['Status'] == 'SUCCESS'
    assert json.loads(response['Data']['helm_values']) == expected_helm_values

def test_handler_production(env_vars, ssm_client_mock):
    # Mock SSM response
    ssm_client_mock().get_parameter.return_value = {'Parameter': {'Value': 'production'}}
    
    event = {}
    context = MockContext()
    response = handler(event, context)
    
    expected_helm_values = {
        "controller": {
            "replicaCount": 2
        }
    }
    
    assert response['Status'] == 'SUCCESS'
    assert json.loads(response['Data']['helm_values']) == expected_helm_values

def test_handler_unexpected_environment(env_vars, ssm_client_mock):
    # Mock SSM response
    ssm_client_mock().get_parameter.return_value = {'Parameter': {'Value': 'unexpected_env'}}
    
    event = {}
    context = MockContext()
    response = handler(event, context)
    
    assert response['Status'] == 'FAILED'
    assert 'Unexpected environment value' in response['Data']['Error']

