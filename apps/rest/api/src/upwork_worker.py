import upwork
from upwork.routers.jobs import search
client = upwork.Client(config)
params = {'q': 'python', 'title': 'Web developer'}
search.Api(client).find(params)
