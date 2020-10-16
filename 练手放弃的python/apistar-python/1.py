from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star'}
    return {'message': 'Welcome to API star,%s' % name}

routs = [
    Route('/','GET', welcome),
    Include('/docs', docs_urls),
    Include('/static',static_urls)
]
app = App(routes=routs)

if __name__ == "__main__":
    app.main()