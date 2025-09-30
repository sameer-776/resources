from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import json
import os
import time
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
CORS(app) 

# IMPORTANT: Add a secret key for session management
app.secret_key = 'your_super_secret_key_change_this'

# --- File Paths & Config ---
NOTICE_FILE = "notices.json"
LINK_FILE = "links.json"
GALLERY_FILE = "gallery.json"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Utility Functions ---
def read_json(file_path):
    if not os.path.exists(file_path): return []
    try:
        with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): return []
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)


# --- Login Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            if request.path.startswith('/api/'):
                return jsonify({"status": "error", "message": "Unauthorized"}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# --- Frontend Routes ---
@app.route("/")
def index(): 
    return render_template("index.html")

# --- Authentication Routes ---
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            with open('credentials.json', 'r', encoding='utf-8') as f:
                creds = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            error = 'Critical error: Could not load credentials file.'
            return render_template("login.html", error=error)

        submitted_username = request.form.get('username')
        submitted_password = request.form.get('password')

        if submitted_username == creds.get('username') and submitted_password == creds.get('password'):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# --- PROTECTED Admin Route ---
@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


# --- PROTECTED API Routes ---
@app.route("/api/notices", methods=["GET", "POST"])
def handle_notices():
    if request.method == "GET":
        return jsonify(read_json(NOTICE_FILE))
    if request.method == "POST":
        if 'logged_in' not in session: return jsonify({"status": "error", "message": "Unauthorized"}), 401
        data = request.json
        notices = read_json(NOTICE_FILE)
        new_notice = {"id": int(time.time()), "text": data.get("text", "")}
        notices.append(new_notice)
        write_json(NOTICE_FILE, notices)
        return jsonify({"status": "success", "notice": new_notice}), 201

@app.route("/api/notices/<int:notice_id>", methods=["PUT", "DELETE"])
@login_required
def handle_single_notice(notice_id):
    notices = read_json(NOTICE_FILE)
    if request.method == "PUT":
        data = request.json
        for notice in notices:
            if notice.get("id") == notice_id: notice["text"] = data.get("text", notice["text"]); break
        write_json(NOTICE_FILE, notices)
        return jsonify({"status": "updated"})
    if request.method == "DELETE":
        notices = [n for n in notices if n.get("id") != notice_id]
        write_json(NOTICE_FILE, notices)
        return jsonify({"status": "deleted"})

@app.route("/api/links", methods=["GET", "POST"])
def handle_links():
    if request.method == "GET": 
        return jsonify(read_json(LINK_FILE))
    if request.method == "POST":
        if 'logged_in' not in session: return jsonify({"status": "error", "message": "Unauthorized"}), 401
        data = request.json
        links = read_json(LINK_FILE)
        new_link = {"id": int(time.time()), "title": data.get("title", ""), "url": data.get("url", "")}
        links.append(new_link)
        write_json(LINK_FILE, links)
        return jsonify({"status": "success", "link": new_link}), 201

@app.route("/api/links/<int:link_id>", methods=["PUT", "DELETE"])
@login_required
def handle_single_link(link_id):
    links = read_json(LINK_FILE)
    if request.method == "PUT":
        data = request.json
        for link in links:
            if link.get("id") == link_id:
                link["title"] = data.get("title", link["title"])
                link["url"] = data.get("url", link["url"])
                break
        write_json(LINK_FILE, links)
        return jsonify({"status": "updated"})
    if request.method == "DELETE":
        links = [l for l in links if l.get("id") != link_id]
        write_json(LINK_FILE, links)
        return jsonify({"status": "deleted"})

@app.route("/api/gallery", methods=["GET", "POST"])
def handle_gallery():
    if request.method == "GET": 
        return jsonify(read_json(GALLERY_FILE))
    if request.method == "POST":
        if 'logged_in' not in session: return jsonify({"status": "error", "message": "Unauthorized"}), 401
        if 'image' not in request.files or request.files['image'].filename == '':
            return jsonify({"status": "error", "message": "No image file provided"}), 400
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gallery_images = read_json(GALLERY_FILE)
        new_image = {"id": int(time.time()), "filename": filename}
        gallery_images.append(new_image)
        write_json(GALLERY_FILE, gallery_images)
        return jsonify({"status": "success", "image": new_image}), 201

@app.route("/api/gallery/<int:image_id>", methods=["DELETE"])
@login_required
def handle_single_gallery_image(image_id):
    gallery_images = read_json(GALLERY_FILE)
    image_to_delete = next((img for img in gallery_images if img.get("id") == image_id), None)
    if image_to_delete:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_to_delete['filename']))
        except OSError as e: print(f"Error deleting file: {e.strerror}")
    images_to_keep = [img for img in gallery_images if img.get("id") != image_id]
    write_json(GALLERY_FILE, images_to_keep)
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)