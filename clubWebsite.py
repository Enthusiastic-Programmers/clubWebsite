import os
from flask import Flask, render_template, send_from_directory

# By default flask looks for html templates in the "templates" directory 
# relative to source. Overriding this to use the CWD, in order to avoid
# restructuring the repo's layout.
cwd = os.path.abspath('.')

#--------------------------------------------------------------------------------------------------
# Application instance
#--------------------------------------------------------------------------------------------------
app = Flask(__name__, template_folder=cwd)
app.logger.info("Using template dir %s", cwd)

#--------------------------------------------------------------------------------------------------
# Route functions
# Ideally the hyperlinks in each page would just point to "/about" or "/contact", but the full
# filename including extension is also added as a route endpoint
#--------------------------------------------------------------------------------------------------

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/faq")
@app.route("/faq.html")
def faq():
    return render_template("faq.html")

@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/about")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/join")
@app.route("/join.html")
def join():
    return render_template("join.html")


#--------------------------------------------------------------------------------------------------
# Workaround to securely serve static files via flask. 
# The proper way to do this is to put static content under the /static folder relative to the CWD
#--------------------------------------------------------------------------------------------------
@app.route('/images/<filename>')
def static_image(filename):
    return send_from_directory(cwd + "/images", filename)

@app.route('/stylesheets/<filename>')
def static_stylesheet(filename):
    return send_from_directory(cwd + "/stylesheets", filename)