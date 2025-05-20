# Azure ML Model Deployment Pipeline

This repository contains an Azure DevOps pipeline for deploying the Llama-3.2-1B model to Azure Machine Learning and creating an endpoint.

## Prerequisites

1. Azure Subscription with the following services enabled:
   - Azure DevOps
   - Azure Machine Learning
   - Azure Container Registry (optional, for custom containers)

2. Required Azure DevOps permissions:
   - Create and manage pipelines
   - Create and manage service connections

3. Required Azure permissions:
   - Contributor access to Azure ML workspace
   - Ability to create and manage compute resources

## Setup Instructions

### 1. Azure ML Workspace Setup

1. Create an Azure ML workspace if you haven't already:
   ```bash
   az ml workspace create -n your-workspace-name -g your-resource-group
   ```

2. Register the Llama-3.2-1B model in your workspace:
   ```bash
   az ml model create --name llama-3.2-1b --path /path/to/model --type custom_model
   ```

### 2. Azure DevOps Pipeline Setup

1. Create a new pipeline in Azure DevOps:
   - Go to Pipelines > New Pipeline
   - Choose "Azure Repos Git" as your code location
   - Select your repository
   - Choose "Existing Azure Pipelines YAML file"
   - Select the `azure-pipelines.yml` file

2. Configure pipeline variables:
   - Go to the pipeline settings
   - Add the following variables:
     - `AZURE_ML_WORKSPACE`: Your Azure ML workspace name
     - `AZURE_ML_RESOURCE_GROUP`: Your Azure resource group name
     - `MODEL_NAME`: llama-3.2-1b
     - `ENDPOINT_NAME`: llama-endpoint

3. Create an Azure service connection:
   - Go to Project Settings > Service Connections
   - Create a new Azure Resource Manager service connection
   - Select your subscription and resource group
   - Grant access to all pipelines

### 3. Pipeline Configuration

The pipeline performs the following steps:
1. Sets up the Azure ML workspace
2. Creates a deployment configuration
3. Deploys the model to an online endpoint
4. Retrieves the scoring URI and primary key

### 4. Testing the Endpoint

After the pipeline runs successfully, you can test the endpoint using the following Python code:

```python
import requests
import json

# Get these values from the pipeline output
scoring_uri = "YOUR_SCORING_URI"
key = "YOUR_PRIMARY_KEY"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {key}'
}

data = {
    "input_data": {
        "input_string": "Your input text here"
    }
}

response = requests.post(scoring_uri, headers=headers, json=data)
print(response.json())
```

## Monitoring and Management

1. Monitor the endpoint in Azure ML Studio:
   - Go to Endpoints > Online endpoints
   - Select your endpoint
   - View metrics, logs, and deployment status

2. Scale the endpoint:
   - Adjust the `instance_count` in the deployment configuration
   - Update the `instance_type` if needed

## Troubleshooting

1. If the pipeline fails:
   - Check the pipeline logs for detailed error messages
   - Verify all prerequisites are met
   - Ensure service connections are properly configured

2. If the endpoint is not responding:
   - Check the endpoint status in Azure ML Studio
   - Review the deployment logs
   - Verify the model is properly registered

## Security Considerations

1. Store sensitive information in Azure DevOps pipeline variables
2. Use managed identities where possible
3. Implement proper access controls for the endpoint
4. Monitor endpoint usage and implement rate limiting if needed

## Cost Optimization

1. Use appropriate instance types for your workload
2. Implement auto-scaling based on demand
3. Monitor resource usage and adjust accordingly
4. Consider using Azure Spot instances for non-critical workloads 