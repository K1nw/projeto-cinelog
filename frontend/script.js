//pegar elementos do HTML
const containerVitrine = document.querySelector('.container-vitrine');
const barraBusca = document.querySelector('.barra-filtros input');

//verifica se a vitrine existe
function desenharCardsNaTela(filmes) {
    if (!containerVitrine) return;
    containerVitrine.innerHTML = '';

    filmes.forEach(filme => {
        const cardHtml = `
            <div class="card-filme" data-id="${filme.id}" data-nota="${filme.nota}">
                <h3>${filme.titulo}</h3>
                <span class="nota">⭐ ${filme.nota}/10</span>
                <p class="review">"${filme.review}"</p>
                <button class="btn-excluir">Excluir</button>
            </div>
        `;
        containerVitrine.innerHTML += cardHtml;
    });
}
// Modal
const modal = document.getElementById('modal-adicionar');
const btnAdicionar = document.querySelector('.barra-filtros button');
const btnFechar = document.querySelector('.fechar-modal');
const formAdicionar = document.getElementById('form-adicionar');

if (btnAdicionar) {
    btnAdicionar.addEventListener('click', () => {
        modal.style.display = 'block';
    });
}

if (btnFechar) {
    btnFechar.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}

window.addEventListener('click', (evento) => {
    if (evento.target === modal) {
        modal.style.display = 'none';
    }
});

if (formAdicionar) {
    formAdicionar.addEventListener('submit', function(evento) {
        evento.preventDefault();

        const titulo = document.getElementById('titulo').value.trim();
        const nota = document.getElementById('nota').value;
        const review = document.getElementById('review').value.trim();

        fetch('http://127.0.0.1:5000/api/filmes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                titulo: titulo,
                nota: parseFloat(nota),
                review: review
            })
        })
        .then(resposta => {
            if (!resposta.ok) throw new Error('Erro ao adicionar');
            return resposta.json();
        })
        .then(filmeNovo => {
            console.log('Filme adicionado:', filmeNovo);
            formAdicionar.reset();          // Limpa o formulário
            modal.style.display = 'none';   // Fecha o modal
            carregarFilmesDoServidor();     // Atualiza a lista
        })
        .catch(erro => {
            console.error(erro);
            alert('Não foi possível adicionar o filme.');
        });
    });
}

//botão excluir filme
function excluirFilme(id) {
    fetch(`http://127.0.0.1:5000/api/filmes/${id}`, {
        method: 'DELETE'
    })
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao excluir o filme');
        }
        return resposta.json();
    })
    .then(dados => {
        console.log(dados.mensagem);
        // Recarrega a lista depois de excluir
        carregarFilmesDoServidor();
    })
    .catch(erro => {
        console.error('Erro:', erro);
        alert('Não foi possível excluir o filme.');
    });
}

containerVitrine.addEventListener('click', function(evento) {
    if (evento.target.classList.contains('btn-excluir')) {
        const card = evento.target.closest('.card-filme');
        const id = card.dataset.id;

        const confirmar = confirm('Tem certeza que deseja excluir este filme?');
        if (confirmar) {
            excluirFilme(id);
        }
    }
});
//função buscar filmes do python, app.py
function carregarFilmesDoServidor() {
    fetch(`http://127.0.0.1:5000/api/filmes?v=${Date.now()}`)
        .then(resposta => resposta.json())
        .then(listaDeFilmes => {
            desenharCardsNaTela(listaDeFilmes);
        })
        .catch(erro => console.error('Erro ao buscar filmes:', erro));
}

if (barraBusca) {
    barraBusca.addEventListener('input', function(evento) {
        const termoBuscado = evento.target.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.card-filme');
        
        cards.forEach(function(card) {
            const tituloFilme = card.querySelector('h3').textContent.toLowerCase();
            if (tituloFilme.includes(termoBuscado)) {
                card.style.display = "block"; 
            } else {
                card.style.display = "none";  
            }
        });
    });
}

carregarFilmesDoServidor();