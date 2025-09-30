# Poornima Library - Dynamic Website & Admin Panel 📚✨

This project is a fully functional, dynamic website for the Poornima University Library. It features a modern, responsive public-facing website and a secure admin panel for staff to manage content in real-time without touching any code.

The live website dynamically loads notices, resource links, and gallery images that are managed through the admin interface.

---
## ## Features

* **Dynamic Content Management:** Admins can easily add, edit, and delete notices, resource links, and gallery images.
* **Real-time Updates:** Changes made in the admin panel are immediately reflected on the public website after a refresh.
* **Direct Image Uploads:** The admin panel allows for direct uploading of images for resource links and the photo gallery.
* **Fully Responsive Design:** The layout is optimized for a seamless experience on desktops, tablets, and mobile devices.
* **Dark Mode:** A user-toggleable dark theme for comfortable viewing in low-light conditions.
* **Modern UI/UX:** Built with interactive elements, smooth scroll animations, and a clean, card-based layout.

---
## ## Tech Stack

* **Frontend:**
    * HTML5
    * CSS3 (Flexbox & Grid)
    * Vanilla JavaScript (ES6+)
    * Font Awesome (Icons)
* **Backend:**
    * Python 3
    * Flask (Web Framework)
    * Flask-CORS
* **Data Storage:**
    * JSON files (acting as a simple, file-based database)

---
## ## Project Structure

Here is an overview of the file and folder structure:

```
/poornima-library-website
|
|-- app.py              # The main Flask server application
|-- gallery.json        # Database for gallery images
|-- links.json          # Database for resource links
|-- notices.json        # Database for ticker notices
|
|-- /templates
|   |-- index.html      # The main public-facing website
|   |-- admin.html      # The admin control panel
|
|-- /static
|   |-- script.js       # JavaScript for index.html
|   |-- styles.css      # CSS for index.html
|   |-- admin.js        # JavaScript for admin.html
|   |-- admin.css       # CSS for admin.html
|   |
|   |-- /uploads
|       |-- (Uploaded images will be stored here)
```

---
## ## Setup and Installation

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install Flask Flask-Cors
    ```

4.  **Create initial data files:**
    In the main project folder, create three new, empty files:
    * `notices.json`
    * `links.json`
    * `gallery.json`

    Open each file and put empty square brackets `[]` inside, then save.

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

The application will now be running on `http://127.0.0.1:5000`.

---
## ## Usage

* **Admin Panel:** Navigate to `http://127.0.0.1:5000/admin` in your web browser. From here, you can manage all the dynamic content of the website.

* **Public Website:** Visit `http://127.0.0.1:5000/` to see the live website and how it reflects the changes made in the admin panel.

---
## ## Team & Credits

This project was developed by a team of dedicated students from Poornima University.

* **Sameer** (17768 - B.Tech AIML)
* **Kshitij Soni** (18810 - BCA)
* **Aryan Gaikwad** (18800 - B.Tech AIML)
* **Mohit Kumar** (19405 - BCA)

### ## Under the Supervision Of
* **Dr. Vipin Khattri**
