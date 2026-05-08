const API_BASE_URL = 'http://localhost:8000';

// Preview da imagem
const imagemInput = document.getElementById('imagem');
const preview = document.getElementById('preview');

if (imagemInput) {
    imagemInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            preview.style.display = 'none';
            preview.src = '';
        }
    });
}

// Submissão do formulário
const publishForm = document.getElementById('publishForm');
const messageDiv = document.getElementById('message');

publishForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nome = document.getElementById('nome').value;
    const imagemFile = document.getElementById('imagem').files[0];

    if (!imagemFile) {
        mostrarMensagem('Por favor, selecione uma imagem.', 'error');
        return;
    }

    // Validar tamanho (max 5MB)
    if (imagemFile.size > 5 * 1024 * 1024) {
        mostrarMensagem('A imagem deve ter no máximo 5MB.', 'error');
        return;
    }

    // Validar tipo
    const tiposPermitidos = ['image/jpeg', 'image/png', 'image/gif'];
    if (!tiposPermitidos.includes(imagemFile.type)) {
        mostrarMensagem('Formato não suportado. Use JPG, PNG ou GIF.', 'error');
        return;
    }

    mostrarMensagem('Publicando...', 'info');

    try {
        const formData = new FormData();
        formData.append('imagem', imagemFile);
        if (nome) formData.append('nome', nome);

        const response = await fetch(`${API_BASE_URL}/faces`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || '🚫 Erro ao publicar rosto');
        }

        const result = await response.json();
        mostrarMensagem('🟢 Rosto publicado com sucesso!', 'success');

        // Limpar formulário
        publishForm.reset();
        preview.style.display = 'none';
        preview.src = '';

        // Redirecionar após 2 segundos
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);

    } catch (error) {
        console.error('Erro ao publicar:', error);
        mostrarMensagem(`🚫 Erro: ${error.message}`, 'error');
    }
});

function mostrarMensagem(msg, tipo) {
    messageDiv.innerHTML = msg;
    messageDiv.className = `message ${tipo}`;

    if (tipo !== 'info') {
        setTimeout(() => {
            if (messageDiv) {
                messageDiv.style.opacity = '0';
                setTimeout(() => {
                    messageDiv.innerHTML = '';
                    messageDiv.className = 'message';
                    messageDiv.style.opacity = '1';
                }, 300);
            }
        }, 5000);
    }
}
