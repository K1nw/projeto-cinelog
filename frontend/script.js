const barraBusca = document.querySelector('.acoes input');

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
