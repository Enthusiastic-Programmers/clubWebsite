from clubWebsite import create_instance, add_context
from clubWebsite.config import BaseConfig

app = create_instance(BaseConfig)
app = add_context(app)

if __name__ == '__main__':

    app.run('localhost', port=8080, debug=True)