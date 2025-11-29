document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileElem');
    const gallery = document.getElementById('gallery');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileList = document.getElementById('fileList');
    const refreshFilesBtn = document.getElementById('refreshFilesBtn');
    
    let filesToUpload = [];

    // Cargar lista inicial
    fetchFiles();

    // --- Drag & Drop ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
    });

    dropArea.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', (e) => handleFiles(e.target.files), false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        filesToUpload = [...files];
        updateGallery();
        uploadBtn.disabled = filesToUpload.length === 0;
    }

    function updateGallery() {
        gallery.innerHTML = '';
        filesToUpload.forEach(file => {
            let div = document.createElement('div');
            div.className = 'file-tag';
            div.textContent = `📄 ${file.name}`;
            gallery.appendChild(div);
        });
    }

    // --- Subir Archivos ---
    uploadBtn.onclick = async () => {
        uploadBtn.textContent = "Subiendo...";
        uploadBtn.disabled = true;

        for (let file of filesToUpload) {
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    console.log(`Subido: ${file.name}`);
                } else {
                    alert(`Error subiendo ${file.name}`);
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Error de conexión con el servidor local.");
            }
        }

        alert("✅ Archivos subidos a Bronze exitosamente.");
        filesToUpload = [];
        updateGallery();
        uploadBtn.textContent = "Subir a Azure Storage";
        uploadBtn.disabled = true;
        fetchFiles(); // Actualizar lista
    };

    // --- Listar Archivos ---
    async function fetchFiles() {
        fileList.innerHTML = '<li class="loading">Cargando archivos de Azure...</li>';
        try {
            const response = await fetch("/files");
            const data = await response.json();
            
            fileList.innerHTML = '';
            
            if (data.files && data.files.length > 0) {
                data.files.forEach(filename => {
                    let li = document.createElement('li');
                    li.innerHTML = `
                        <span class="fname">📄 ${filename}</span>
                        <span class="badge-bronze">Bronze</span>
                    `;
                    fileList.appendChild(li);
                });
            } else {
                fileList.innerHTML = '<li class="empty">Carpeta Bronze vacía</li>';
            }
        } catch (error) {
            fileList.innerHTML = '<li class="error">Error al conectar con Azure</li>';
            console.error(error);
        }
    }

    refreshFilesBtn.onclick = fetchFiles;
});