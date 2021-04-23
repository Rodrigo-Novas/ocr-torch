from flask import Flask, render_template, redirect, url_for, jsonify, send_file, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect
import redis
import utils as u
import os
from pathlib import Path

app = Flask(__name__)

cache = redis.Redis(host="redis", port=6379)

csrf = CSRFProtect(app)

app.secret_key="SQLOULAKK"

IMAGE_EXTENSIONS = {'jpg', 'png'}
PDF_EXTENSIONS = {'pdf'}

BASE_DIR = Path(__file__).resolve().parent.parent
            
def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS and filename.rsplit('.', 1)[1].lower() != ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in PDF_EXTENSIONS and filename.rsplit('.', 1)[1].lower() != ""

@app.route("/ping")
def pong():
    return "pong"

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/image-to-text", methods=["GET", "POST"])
def image_to_text():
    if request.method == "POST":
        app.logger.info("Post")
        if 'archivo' not in request.files:
            app.logger.info("No se subio file")
            return redirect(request.url)
        else:
            file = request.files['archivo']
            app.logger.info(f"Se subio archivo {file.filename}")
            if file and allowed_image(file.filename):
                app.logger.info(f"Se subio archivo {file.filename}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_DIR, filename))
                texto = u.ocr_text(os.path.join(BASE_DIR, filename))
                return jsonify({"Convertido": "exito", "Texto": texto})
            else:
                return jsonify({"Respuesta": "Fallo, la extension no es permitida"})
    return render_template("image-to-text.html")

@app.route("/pdf-to-text", methods=["GET", "POST"])
def pdf_to_text():
    if request.method == "POST":
        app.logger.info("Post")
        if 'archivo' not in request.files:
            app.logger.info("No se subio file")
            return redirect(request.url)
        else:
            file = request.files['archivo']
            app.logger.info(f"Se subio archivo {file.filename}")
            if file and allowed_file(file.filename):
                app.logger.info(f"Se subio archivo {file.filename}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_DIR, filename))
                texto = u.pdf_to_text(os.path.join(BASE_DIR, filename))
                return jsonify({"Convertido": "exito", "Texto": texto})
            else:
                return jsonify({"Respuesta": "Fallo, la extension no es permitida"})
    return render_template("pdf-to-text.html")


@app.route("/pdf-to-json", methods=["GET", "POST"])
def pdf_to_json():
    if request.method == "POST":
        app.logger.info("Post")
        if 'archivo' not in request.files:
            app.logger.info("No se subio file")
            return redirect(request.url)
        else:
            file = request.files['archivo']
            app.logger.info(f"Se subio archivo {file.filename}")
            if file and allowed_file(file.filename):
                app.logger.info(f"Se subio archivo {file.filename}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_DIR, filename))
                texto = u.pdf_to_text_json(os.path.join(BASE_DIR, filename))
                return jsonify({"Convertido": "exito", "json": texto})
            else:
                return jsonify({"Respuesta": "Fallo, la extension no es permitida"})
    return render_template("pdf-to-json.html")

@app.route("/pdf-to-html", methods=["GET", "POST"])
def pdf_to_html():
    if request.method == "POST":
        app.logger.info("Post")
        if 'archivo' not in request.files:
            app.logger.info("No se subio file")
            return redirect(request.url)
        else:
            file = request.files['archivo']
            app.logger.info(f"Se subio archivo {file.filename}")
            if file and allowed_file(file.filename):
                app.logger.info(f"Se subio archivo {file.filename}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_DIR, filename))
                texto = u.pdf_to_text_html(os.path.join(BASE_DIR, filename))
                return render_template("html-pdf.html", contenido=texto)
            else:
                return jsonify({"Respuesta": "Fallo, la extension no es permitida"})
    return render_template("pdf-to-html.html")


@app.route("/pdf-to-html-json", methods=["GET", "POST"])
def pdf_to_html_json():
    if request.method == "POST":
        app.logger.info("Post")
        if 'archivo' not in request.files:
            app.logger.info("No se subio file")
            return redirect(request.url)
        else:
            file = request.files['archivo']
            app.logger.info(f"Se subio archivo {file.filename}")
            if file and allowed_file(file.filename):
                app.logger.info(f"Se subio archivo {file.filename}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_DIR, filename))
                texto = u.pdf_to_text_html(os.path.join(BASE_DIR, filename))
                return jsonify({"Convertido": "exito", "Json": texto})
            else:
                return jsonify({"Respuesta": "Fallo, la extension no es permitida"})
    return render_template("pdf-to-html.html")

@app.route("/image-to-json", methods=["GET", "POST"])
def image_to_json():
    if request.method == "POST":
        app.logger.info("Post")
        if 'archivo' not in request.files:
            app.logger.info("No se subio file")
            return redirect(request.url)
        else:
            file = request.files['archivo']
            app.logger.info(f"Se subio archivo {file.filename}")
            if file and allowed_image(file.filename):
                app.logger.info(f"Se subio archivo {file.filename}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_DIR, filename))
                texto = u.ocr_json(os.path.join(BASE_DIR, filename))
                return jsonify({"Convertido": "exito", "Json": texto})
            else:
                return jsonify({"Respuesta": "Fallo, la extension no es permitida"})
    return render_template("image-to-json.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000) 


