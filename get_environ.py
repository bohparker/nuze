import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

print('Environment Variables')
print('----------------------')
for k,v in os.environ.items():
    print(f'{k}:{v}')

print()

routes = []
print('URL Map')
print('==============')
for rule in app.url_map.iter_rules():
    routes.append(rule.endpoint)

print(routes)