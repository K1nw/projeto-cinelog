//pegar elementos do HTML
const containerVitrine = document.querySelector('.container-vitrine');
const barraBusca = document.querySelector('.barra-filtros input');

//verifica se a vitrine existe
function desenharCardsNaTela(filmes) {
    if (!containerVitrine) return;
    containerVitrine.innerHTML = '';
//monta o html do card
    filmes.forEach(filme => {
        const cardHtml = `
            <div class="card-filme" data-nota="${filme.nota}">
                <h3>${filme.titulo}</h3>
                <span class="nota">⭐ ${filme.nota}/10</span>
                <p class="review">"${filme.review}"</p>
            </div>
        `;
        containerVitrine.innerHTML += cardHtml;
    });
}
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