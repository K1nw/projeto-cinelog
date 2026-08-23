import Header from './components/Header'
import SecaoConteudos from './components/SecaoConteudos'
import './App.css'

const conteudos = [
    {
        id: 1,
        titulo: 'Interestelar',
        tipo: 'Filme',
        nota: 9.5
    },
    {
        id: 2,
        titulo: 'O Poderoso Chefão',
        tipo: 'Filme',
        nota: 10
    },
    {
        id: 3,
        titulo: 'Clube da Luta',
        tipo: 'Filme',
        nota: 8.5
    },
    {
        id: 4,
        titulo: 'Matrix',
        tipo: 'Filme',
        nota: 9
    }
]

function App() {
    return (
        <>
            <Header />

            <main className="home">
                <section className="hero">
                    <span>CINELOG</span>
                    <h1>Seu universo de filmes, séries e animes.</h1>
                    <p>
                        Descubra, avalie e organize tudo o que você assiste.
                    </p>

                    <div className="barra-busca">
                        <span>⌕</span>
                        <input
                            type="text"
                            placeholder="Buscar filmes, séries e animes..."
                        />
                    </div>
                </section>

                <SecaoConteudos
                    titulo="🔥 Em destaque"
                    conteudos={conteudos}
                />

                <SecaoConteudos
                    titulo="⭐ Mais bem avaliados"
                    conteudos={conteudos}
                />

                <SecaoConteudos
                    titulo="🎬 Filmes"
                    conteudos={conteudos}
                />

                <SecaoConteudos
                titulo="📺 Séries"
                    conteudos={conteudos}
                />
                
                <SecaoConteudos
                titulo="🎌 Animes"
                    conteudos={conteudos}
                />
            </main>
        </>
    )
}

export default App