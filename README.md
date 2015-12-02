# AWS lambda - eb slack notification 

## direnv .envrc
``` bash
layout python
export AWS_DEFAULT_PROFILE=xxx
```

## prepare
``` bash
% pip install -Ur requirements.txt
% pip install slackweb -t .
```

## test
``` bash
% python-lambda-local -f lambda_handler main.py event.json
```

## deploy
``` bash
% ./deploy.sh
```
