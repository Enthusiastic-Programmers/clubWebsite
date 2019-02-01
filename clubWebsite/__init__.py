from flask import Flask

app = Flask(__name__)
app.config.update({'SECRET_KEY':'ChangeMeInProduction!'})