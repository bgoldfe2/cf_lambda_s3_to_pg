#!/bin/bash
set -ex

#----- Change these parameters to suit your environment -----#
AWS_PROFILE="default"
BUCKET_NAME="bruceg-testbucket-for-s3" # bucket must exist in the SAME region the deployment is taking place
SERVICE_NAME="serverless-s3-event-processor"
TEMPLATE_NAME="${SERVICE_NAME}.yaml"
STACK_NAME="${SERVICE_NAME}"
OUTPUT_DIR="./outputs/"
PACKAGED_OUTPUT_TEMPLATE="${OUTPUT_DIR}${STACK_NAME}-packaged-template.yaml"

#----- End of user parameters  -----#


# You can also change these parameters but it's not required
debugMODE="True"

# Package the code
function pack() {

    # Cleanup Output directory
    rm -rf "${OUTPUT_DIR}"*

    aws cloudformation package \
        --template-file "${TEMPLATE_NAME}" \
        --s3-bucket "${BUCKET_NAME}" \
        --output-template-file "${PACKAGED_OUTPUT_TEMPLATE}"
    
    exit
}
# Deploy the stack
function deploy() {
    echo "Stack Deployment Initiated"
    aws cloudformation deploy \
        --profile "${AWS_PROFILE}" \
        --template-file "${PACKAGED_OUTPUT_TEMPLATE}" \
        --stack-name "${STACK_NAME}" \
        --tags Service="${SERVICE_NAME}" \
        --capabilities CAPABILITY_IAM
        # --parameter-overrides \
            debugMODE="${debugMODE}" \
    exit
}

function nuke_stack() {
		# Deletes the stack
		aws cloudformation delete-stack --stack-name "${STACK_NAME}"
        exit
	}


# Check if we need to destroy the stack
if [ "$1" = "nuke" ]; then
 nuke_stack
  elif [ "$1" = "pack" ]; then
   pack
    elif [ "$1" = "deploy" ]; then
     deploy
fi
