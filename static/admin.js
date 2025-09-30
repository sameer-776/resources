document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:5000/api';

    // --- Notices Management ---
    const noticeForm = document.getElementById('notice-form');
    const noticeIdInput = document.getElementById('notice-id');
    const noticeTextInput = document.getElementById('notice-text');
    const noticesTableBody = document.querySelector('#notices-table tbody');

    const loadNotices = async () => {
        const response = await fetch(`${API_BASE_URL}/notices`);
        const notices = await response.json();
        noticesTableBody.innerHTML = '';
        notices.forEach(notice => {
            const row = noticesTableBody.insertRow();
            row.innerHTML = `
                <td>${escapeHTML(notice.text)}</td>
                <td>
                    <button class="edit-btn" data-id="${notice.id}" data-text="${escapeHTML(notice.text)}">Edit</button>
                    <button class="delete-btn" data-id="${notice.id}">Delete</button>
                </td>
            `;
        });
    };

    noticeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = noticeIdInput.value;
        const text = noticeTextInput.value;
        const method = id ? 'PUT' : 'POST';
        const url = id ? `${API_BASE_URL}/notices/${id}` : `${API_BASE_URL}/notices`;

        await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        noticeForm.reset();
        noticeIdInput.value = '';
        loadNotices();
    });

    noticesTableBody.addEventListener('click', async (e) => {
        const target = e.target;
        const id = target.dataset.id;

        if (target.classList.contains('edit-btn')) {
            noticeIdInput.value = id;
            noticeTextInput.value = target.dataset.text;
            window.scrollTo(0, noticeForm.offsetTop);
        }

        if (target.classList.contains('delete-btn')) {
            if (confirm('Are you sure you want to delete this notice?')) {
                await fetch(`${API_BASE_URL}/notices/${id}`, { method: 'DELETE' });
                loadNotices();
            }
        }
    });

    // --- Links Management ---
    const linkForm = document.getElementById('link-form');
    const linkIdInput = document.getElementById('link-id');
    const linkTitleInput = document.getElementById('link-title');
    const linkUrlInput = document.getElementById('link-url');
    const linksTableBody = document.querySelector('#links-table tbody');

    const loadLinks = async () => {
        const response = await fetch(`${API_BASE_URL}/links`);
        const links = await response.json();
        linksTableBody.innerHTML = '';
        links.forEach(link => {
            const row = linksTableBody.insertRow();
            row.innerHTML = `
            <td>${escapeHTML(link.title)}</td>
            <td>${escapeHTML(link.url)}</td>
            <td>
                <button class="edit-btn" data-id="${link.id}" data-title="${escapeHTML(link.title)}" data-url="${escapeHTML(link.url)}">Edit</button>
                <button class="delete-btn" data-id="${link.id}">Delete</button>
            </td>
        `;
        });
    };

    linkForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = linkIdInput.value;
        const body = {
            title: linkTitleInput.value,
            url: linkUrlInput.value
        };
        const method = id ? 'PUT' : 'POST';
        const url = id ? `${API_BASE_URL}/links/${id}` : `${API_BASE_URL}/links`;

        await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        linkForm.reset();
        linkIdInput.value = '';
        loadLinks();
    });

    linksTableBody.addEventListener('click', async (e) => {
        const target = e.target;
        const id = target.dataset.id;
        if (target.classList.contains('edit-btn')) {
            linkIdInput.value = id;
            linkTitleInput.value = target.dataset.title;
            linkUrlInput.value = target.dataset.url;
            window.scrollTo(0, linkForm.offsetTop);
        }
        if (target.classList.contains('delete-btn')) {
            if (confirm('Are you sure you want to delete this link?')) {
                await fetch(`${API_BASE_URL}/links/${id}`, { method: 'DELETE' });
                loadLinks();
            }
        }
    });
    // --- Gallery Management ---
    const galleryForm = document.getElementById('gallery-form');
    const galleryImageInput = document.getElementById('gallery-image');
    const galleryPreview = document.getElementById('gallery-preview');

    const loadGalleryImages = async () => {
        const response = await fetch(`${API_BASE_URL}/gallery`);
        const images = await response.json();
        galleryPreview.innerHTML = ''; // Clear preview
        images.forEach(image => {
            const imgContainer = document.createElement('div');
            imgContainer.className = 'gallery-item';
            imgContainer.innerHTML = `
            <img src="/static/uploads/${image.filename}" alt="Gallery Image">
            <button class="delete-btn" data-id="${image.id}">Delete</button>
        `;
            galleryPreview.appendChild(imgContainer);
        });
    };

    galleryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (galleryImageInput.files.length === 0) {
            alert('Please select an image to upload.');
            return;
        }
        const formData = new FormData();
        formData.append('image', galleryImageInput.files[0]);

        await fetch(`${API_BASE_URL}/gallery`, {
            method: 'POST',
            body: formData
        });

        galleryForm.reset();
        loadGalleryImages(); // Refresh the gallery preview
    });

    galleryPreview.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const id = e.target.dataset.id;
            if (confirm('Are you sure you want to delete this gallery image?')) {
                await fetch(`${API_BASE_URL}/gallery/${id}`, {
                    method: 'DELETE'
                });
                loadGalleryImages(); // Refresh the list
            }
        }
    });
    // --- Initial data load ---
    loadNotices();
    loadLinks();
    loadGalleryImages();
});

// Helper function to prevent HTML injection issues from user input
function escapeHTML(str) {
    const p = document.createElement('p');
    p.appendChild(document.createTextNode(str));
    return p.innerHTML;
}