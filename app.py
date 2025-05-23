from flask import Flask, request, send_file, render_template, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

@app.route('/')
def home():
    return render_template('index.html')

# para servir imagenes
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(".", filename)

@app.route("/imagenes/<path:filename>")
def serve_imagenes(filename):
    return send_from_directory("imagenes", filename)
# ####

@app.route('/tmp/compress', methods=['POST'])
def compress_pdf():
    if 'pdf' not in request.files:
        return "No se envió archivo PDF", 400

    pdf = request.files['pdf']
    input_filename = f"/tmp/{uuid.uuid4()}.pdf"
    output_filename = f"/tmp/compressed_{uuid.uuid4()}.pdf"

    pdf.save(input_filename)

    try:
        subprocess.run([
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_filename}",
            input_filename
        ], check=True)

        return send_file(output_filename, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return f"Error al comprimir: {e}", 500

    finally:
        # Limpieza de archivos
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

