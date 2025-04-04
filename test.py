# import base64

# username = 'joseph'
# password = '12345s'
# role = 'admin'

# encoded_creds = base64.b64encode(f'{username}:{password}:{role}'.encode()).decode()
# print(f'Encoded credentials: {encoded_creds}')

from my_app_backend.context.context_hsm import ContextHSM

context = ContextHSM()
pass