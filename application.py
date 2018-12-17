from flask import Flask, url_for, render_template, request, make_response, json
import requests
from sklearn.externals import joblib
app = Flask(__name__)

dark_sky_api_key = "073ed950bcd367ad35e76ea60cf5511c"
ipstack_api_key = "55896dde6c19b26566166b446fe84094"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", prenom="Michel")
    elif request.method == "POST":
        response = make_response(render_template("project.html"))
        return response

@app.route("/project", methods=["GET", "POST"])
def project():
    current_location = requests.get("http://api.ipstack.com/check", params={"access_key": ipstack_api_key})
    current_location = current_location.json()
    latitude = current_location["latitude"]
    longitude = current_location["longitude"]
    ville = current_location["city"]
    weather = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(dark_sky_api_key, latitude, longitude))
    weather = weather.json()
    if request.method == "GET":
        return render_template("project.html", weather = weather, ville = ville)
    elif request.method == "POST":
        nom = request.form["nom_utilisateur"]
        email = request.form["email_utilisateur"]
        message = request.form["message_utilisateur"]
        response = make_response(render_template("project.html",ville=ville,weather = weather ,name = nom, email = email, message = message))
        response.set_cookie("Nom", nom)
        return response

@app.route("/urls", methods=["GET", "POST"])
def urls():
    nom = request.cookies.get("Nom")
    return render_template("url.html", nom = nom)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    regressor = joblib.load("./linear_regression_model.pkl")
    xp = [[float(request.form["regression"])]]
    y_pred = float(regressor.predict(xp))
    return render_template("predict.html", xp = xp[0][0], y_pred = y_pred)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        response = make_response(render_template("contact.html"))
        return response

if __name__ == "__main__":
    app.run(debug=True)
