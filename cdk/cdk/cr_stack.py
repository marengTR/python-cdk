from aws_cdk import (
    Stack,
    CustomResource,
    custom_resources as cr,
    CfnOutput
)
from constructs import Construct

class CRStack1(Stack):
    def __init__(self, scope: Construct, id: str, lambda_func_arn: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        #self.helm_att_CustomResource = CustomResource(self, 'CustomResource', service_token=lambda_func_arn)


        # add provider to the stack to get service token
        

        res_provider = cr.Provider(
            self,'crProvider',
            on_event_handler= lambda_func_arn
        )
            
        CustomResource(self, 'cust_res',service_token= res_provider.service_token)
        
        #self.helm_values = CustomResource(self, 'CustomResource', service_token=lambda_func_arn)
        # pass the attribute to EKSStack
        #helm_values = self.helm_att_CustomResource.get_att_string(attribute_name="helm_values")
        # helm_values = "1"
        # helm_values = self.helm_att_CustomResource.get_att_string(attribute_name="helm_values")
        # # Output the Helm values
        CfnOutput(self, "Output",
                   value=CustomResource.get_att_string(attribute_name="helm_values"))
        #self.helm_values_output = self.helm_values.get_att_string(attribute_name="helm_values")