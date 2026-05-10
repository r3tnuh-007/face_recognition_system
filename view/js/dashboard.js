const API_BASE_URL = 'http://10.18.32.206:8000';

async function carregarRostos() {
    const galleryContainer = document.getElementById('galleryContainer');
    galleryContainer.innerHTML = '<div class="loading">Carregando rostos...</div>';

    try {
        const formData = new FormData();
        const response = await fetch(`${API_BASE_URL}/dashboard`, {
        method: 'POST',
        body: formData
        });

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}` );
        }

        const faces = await response.json();

        if (!faces || faces.length === 0) {
            galleryContainer.innerHTML = '<div class="info-text">Nenhum rosto publicado ainda.</div>';
            return;
        }

        exibirRostos(faces);
    } catch (error) {
        console.error('Erro ao carregar rostos:', error);
        galleryContainer.innerHTML = `
            <div class="message error">
                Erro ao carregar rostos: ${error.message}<br>
                Verifique se o backend está rodando em ${API_BASE_URL}
            </div>
        `;
    }
}

function exibirRostos(faces) {
    const galleryContainer = document.getElementById('galleryContainer');

    galleryContainer.innerHTML = faces.map(face => `
        <div class="face-card" data-id="${face.id}">
            <img src="${face.imageUrl}"
                 alt="${face.nome || 'Rosto'}"
                 class="face-image"
                 onerror="this.src='https://via.placeholder.com/250x250?text=Erro+Imagem'">
            <div class="face-info">
                <div class="face-name">${face.nome || 'Anônimo'}</div>
                <div class="face-date">${face.data_upload}</div>
            </div>
        </div>
    `).join('');

    // Adicionar evento de clique nos cards
    document.querySelectorAll('.face-card').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.dataset.id;
            alert(`Detalhes do rosto ID: ${id}\nFuncionalidade em desenvolvimento`);
        });
    });
}

// Atualizar automaticamente a cada 30 segundos
let autoRefreshInterval;

function iniciarAutoRefresh() {
    if (autoRefreshInterval) clearInterval(autoRefreshInterval);
    autoRefreshInterval = setInterval(carregarRostos, 300000);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    carregarRostos();
    iniciarAutoRefresh();

    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', carregarRostos);
    }
});

// Limpar intervalo ao sair da página
window.addEventListener('beforeunload', () => {
    if (autoRefreshInterval) clearInterval(autoRefreshInterval);
});
