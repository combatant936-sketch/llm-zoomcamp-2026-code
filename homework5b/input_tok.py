import os, requests
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ['LOGFIRE_READ_TOKEN']
BASE_URL = 'https://logfire-us.pydantic.dev/v1/query'

query = '''
SELECT trace_id, span_name, message, attributes->>\'gen_ai.usage.input_tokens\' AS input_tokens
FROM records
WHERE otel_scope_name = \'pydantic-ai\'
ORDER BY start_timestamp DESC
'''

resp = requests.get(BASE_URL, params={'sql': query}, headers={'Authorization': f'Bearer {TOKEN}'})
resp.raise_for_status()
data = resp.json()
print(data)

