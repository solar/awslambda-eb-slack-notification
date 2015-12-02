import slackweb

# slack incoming webhook endpoint
ENDPOINT = 'https://hooks.slack.com/services/xxxxxxxx/yyyyyyyy/zzzzzzzzzzzzzzzz';

DEFAULT_CHANNEL = '#default' # default channel name
CHANNELS = {
        # Environment name -> channel name
        'one': '#one',
        }

IGNORE_KEYS = ['RequestId', 'NotificationProcessId', 'Message']

# slack notification username
USERNAME = 'AWS SNS / Lambda'

def lambda_handler(event, context):
    raw = event['Records'][0]['Sns']['Message']
    data = dict([ parts for parts in
        [ parse(line) for line in raw.splitlines() if len(line) > 0 ]
        if len(parts) == 2 ])

    attachments = [{
        'fallback': data['Message'],
        'text': data['Message'],
        'fields': makefields(data)
        }]

    res = slackweb.Slack(ENDPOINT).notify(
            channel=getchannel(data),
            username=USERNAME,
            attachments=attachments)

    return res

def parse(line):
    parts = line.split(':', 1)
    if len(parts) == 2:
        key = parts[0]
        if len(key) > 0:
            return [key, parts[1].lstrip()]
    return []

def getchannel(data):
    env = data['Environment'] if 'Environment' in data else None
    channel = CHANNELS[data['Environment']] if env in CHANNELS else DEFAULT_CHANNEL

def makefields(data):
    fields = []
    for k, v in data.iteritems():
        if k not in IGNORE_KEYS:
            fields.append({
                'title': k,
                'value': v,
                'short': True
                })
    return fields
