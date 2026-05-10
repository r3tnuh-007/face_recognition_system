const API_BASE_URL = 'http://10.18.32.206:8000';

const searchImage = document.getElementById('searchImage');
const searchPreview = document.getElementById('searchPreview');
const searchBtn = document.getElementById('searchBtn');
const searchResults = document.getElementById('searchResults');

// Preview da imagem de pesquisa
if (searchImage) {
    searchImage.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                searchPreview.src = e.target.result;
                searchPreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            searchPreview.style.display = 'none';
            searchPreview.src = '';
        }
    });
}

// Função para pesquisar rostos similares
async function pesquisarRostosSimilares(imagemFile) {
    if (!imagemFile) {
        mostrarResultado('Por favor, selecione uma imagem para pesquisa.', 'error');
        return;
    }

    // Validar tamanho (max 5MB)
    if (imagemFile.size > 5 * 1024 * 1024) {
        mostrarResultado('A imagem deve ter no máximo 5MB.', 'error');
        return;
    }

    mostrarResultado('🔍 Pesquisando rostos similares...', 'loading');

    try {
        const formData = new FormData();
        formData.append('imagem', imagemFile);


        const response = await fetch(`${API_BASE_URL}/faces/search`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Erro ao pesquisar');
        }

        const resultados = await response.json();

        if (!resultados || resultados.length === 0) {
            mostrarResultado('😔 Nenhum rosto similar encontrado. \nInformaremos assim que encontrarmos a sua pessoa', 'info');
            return;
        }

        alert(resultados[1].imageUrl);
        exibirResultados(resultados);

    } catch (error) {
        console.error('Erro na pesquisa:', error);
        mostrarResultado(` Erro na pesquisa: ${error.message}`, 'error');
    }
}

function exibirResultados(resultados) {
    const resultadosHTML = `
        <div class="results-header">
            <h3>🌍 Resultados Encontrados: ${resultados.length}</h3>
        </div>
        <div class="results-list">
            ${resultados.map(result => `
                <div class="result-card">
                    <img src="${result.imageUrl || result.url}"
                         alt="${result.nome || 'Rosto'}"
                         class="result-image"
                         onerror="this.src='https://via.placeholder.com/80x80?text=Erro'">
                    <div class="result-info">
                        <div class="result-name">${result.nome}</div>
                        <div class="result-similarity">
                            Similaridade: ${(result.similarity * 100).toFixed(2)}%
                        </div>
                        <small>ID: ${result.id}</small>
                    </div>
                </div>
            `).join('')}
        </div>
    `;

    searchResults.innerHTML = resultadosHTML;
}

function mostrarResultado(mensagem, tipo) {
    let className = 'info-text';
    let icon = '📋';

    switch(tipo) {
        case 'error':
            className = 'message error';
            icon = '🚫';
            break;
        case 'loading':
            className = 'loading';
            icon = '⏳';
            break;
        case 'info':
            className = 'info-text';
            icon = '⚠️';
            break;
        default:
            className = 'info-text';
    }

    searchResults.innerHTML = `<div class="${className}">${icon} ${mensagem}</div>`;
}

// Event Listeners
if (searchBtn) {
    searchBtn.addEventListener('click', () => {
        const imagemFile = searchImage.files[0];
        pesquisarRostosSimilares(imagemFile);
    });
}

// Permitir pesquisa com Enter (opcional)
if (searchImage) {
    searchImage.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const imagemFile = searchImage.files[0];
            pesquisarRostosSimilares(imagemFile);
        }
    });
}
