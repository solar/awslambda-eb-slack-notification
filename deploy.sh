#!/bin/bash

FUNCTION='function-name'
IAM_ROLE='arn:aws:iam::000000000000:role/lambda_basic_execution'

zip -r9 $FUNCTION.zip . -x '.direnv/*' -x '.envrc' -x 'deploy.sh' -x 'main.pyc' > /dev/null
aws lambda get-function --function-name $FUNCTION >/dev/null 2>&1

if [ $? != 0 ]; then
    echo 'Creating new lambda function'

    aws lambda create-function \
        --function-name $FUNCTION \
        --memory-size 128 \
        --timeout 20 \
        --role $IAM_ROLE \
        --handler main.lambda_handler \
        --runtime python2.7 \
        --zip-file fileb://$FUNCTION.zip
else
    echo 'Update existing function code'

    aws lambda update-function-code \
        --function-name $FUNCTION \
        --zip-file fileb://$FUNCTION.zip
fi
