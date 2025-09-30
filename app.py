from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) 

# --- File Paths ---
NOTICE_FILE = "notices.json"
LINK_FILE = "links.json"
GALLERY_FILE = "gallery.json" # New file for gallery images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Utility Functions (no change) ---
def read_json(file_path):
    if not os.path.exists(file_path): return []
    try:
        with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): return []
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

# --- Frontend Routes (no change) ---
@app.route("/")
def index(): return render_template("index.html")
@app.route("/admin")
def admin(): return render_template("admin.html")

# --- API for Notices (no change) ---
# ... (The handle_notices and handle_single_notice functions remain the same) ...
@app.route("/api/notices", methods=["GET", "POST"])
def handle_notices():
    if request.method == "GET": return jsonify(read_json(NOTICE_FILE))
    if request.method == "POST":
        data = request.json
        notices = read_json(NOTICE_FILE)
        new_notice = {"id": int(time.time()), "text": data.get("text", "")}
        notices.append(new_notice)
        write_json(NOTICE_FILE, notices)
        return jsonify({"status": "success", "notice": new_notice}), 201
@app.route("/api/notices/<int:notice_id>", methods=["PUT", "DELETE"])
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

# --- API for Links (no change) ---
# ... (The handle_links and handle_single_link functions remain the same) ...
@app.route("/api/links", methods=["GET", "POST"])
def handle_links():
    if request.method == "GET": return jsonify(read_json(LINK_FILE))
    if request.method == "POST":
        if 'image' not in request.files or request.files['image'].filename == '':
            return jsonify({"status": "error", "message": "No image file provided"}), 400
        title = request.form.get('title'); url = request.form.get('url'); file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        links = read_json(LINK_FILE)
        new_link = {"id": int(time.time()), "title": title, "url": url, "image": filename}
        links.append(new_link)
        write_json(LINK_FILE, links)
        return jsonify({"status": "success", "link": new_link}), 201
@app.route("/api/links/<int:link_id>", methods=["PUT", "DELETE"])
def handle_single_link(link_id):
    links = read_json(LINK_FILE)
    if request.method == "PUT":
        link_to_update = next((l for l in links if l.get("id") == link_id), None)
        if not link_to_update: return jsonify({"status": "error", "message": "Link not found"}), 404
        link_to_update["title"] = request.form.get("title", link_to_update["title"])
        link_to_update["url"] = request.form.get("url", link_to_update["url"])
        if 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], link_to_update['image']))
            except OSError: pass
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            link_to_update["image"] = filename
        write_json(LINK_FILE, links)
        return jsonify({"status": "updated"})
    if request.method == "DELETE":
        link_to_delete = next((l for l in links if l.get("id") == link_id), None)
        if link_to_delete:
            try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], link_to_delete['image']))
            except OSError: pass
        links = [l for l in links if l.get("id") != link_id]
        write_json(LINK_FILE, links)
        return jsonify({"status": "deleted"})

# --- NEW API for Gallery ---

@app.route("/api/gallery", methods=["GET", "POST"])
def handle_gallery():
    if request.method == "GET":
        return jsonify(read_json(GALLERY_FILE))
    
    if request.method == "POST":
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
def handle_single_gallery_image(image_id):
    gallery_images = read_json(GALLERY_FILE)
    image_to_delete = next((img for img in gallery_images if img.get("id") == image_id), None)
    
    if image_to_delete:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_to_delete['filename']))
        except OSError as e:
            print(f"Error deleting file: {e.strerror}") # Log error but continue
            
    images_to_keep = [img for img in gallery_images if img.get("id") != image_id]
    write_json(GALLERY_FILE, images_to_keep)
    return jsonify({"status": "deleted"})

# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)