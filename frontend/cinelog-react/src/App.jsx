import { useEffect, useState } from 'react'

import {
    BrowserRouter,
    Routes,
    Route
} from 'react-router-dom'

import Header from './components/Header'
import SecaoConteudos from './components/SecaoConteudos'
import HeroFilmes from './components/HeroFilmes'
import Filme from './pages/Filme'

import './App.css'


function Home() {

    const [filmes, setFilmes] = useState([])
    const [populares, setPopulares] = useState([])
    const [avaliados, setAvaliados] = useState([])

    useEffect(() => {

        fetch('http://127.0.0.1:5000/api/filmes')
            .then(resposta => resposta.json())
            .then(dados => setFilmes(dados))
            .catch(erro =>
                console.error('Erro ao carregar filmes:', erro)
            )

        fetch('http://127.0.0.1:5000/api/filmes/populares')
            .then(resposta => resposta.json())
            .then(dados => setPopulares(dados))
            .catch(erro =>
                console.error('Erro ao carregar populares:', erro)
            )

        fetch('http://127.0.0.1:5000/api/filmes/avaliados')
            .then(resposta => resposta.json())
            .then(dados => setAvaliados(dados))
            .catch(erro =>
                console.error('Erro ao carregar avaliados:', erro)
            )

    }, [])

    return (
        <>
            <Header />

            <main className="home">

                <HeroFilmes filmes={avaliados} />

                <section className="hero">

                    <span>CINELOG</span>

                    <h1>
                        Seu universo de filmes, séries e animes.
                    </h1>

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
                    conteudos={populares}
                />

                <SecaoConteudos
                    titulo="⭐ Mais bem avaliados"
                    conteudos={avaliados}
                />

                <SecaoConteudos
                    titulo="🎬 Filmes"
                    conteudos={filmes}
                />

                <SecaoConteudos
                    titulo="📺 Séries"
                    conteudos={[]}
                />

                <SecaoConteudos
                    titulo="🎌 Animes"
                    conteudos={[]}
                />

            </main>
        </>
    )
}


function App() {

    return (
        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Home />}
                />

                <Route
                    path="/filmes/:id"
                    element={<Filme />}
                />

            </Routes>

        </BrowserRouter>
    )
}

export default App