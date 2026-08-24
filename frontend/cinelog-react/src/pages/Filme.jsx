import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { createPortal } from 'react-dom'

import './Filme.css'

function Filme() {

    const { id } = useParams()

    const [filme, setFilme] = useState(null)
    const [carregando, setCarregando] = useState(true)
    const [erro, setErro] = useState(false)
    const [mostrarAvaliacao, setMostrarAvaliacao] = useState(false)
    const [minhaNota, setMinhaNota] = useState(null)
    const [notaSelecionada, setNotaSelecionada] = useState(0)
    const [favoritado, setFavoritado] = useState(false)
    useEffect(() => {
        
    const favoritoSalvo = localStorage.getItem(
    `favorito_filme_${id}`
    )

            if (favoritoSalvo === 'true') {
            setFavoritado(true)
    }

        setCarregando(true)
        setErro(false)

        fetch(`http://127.0.0.1:5000/api/filmes/${id}`)
            .then(resposta => {

                if (!resposta.ok) {
                    throw new Error('Filme não encontrado')
                }

                return resposta.json()
            })
    .then(dados => {
        setFilme(dados)
    const avaliacaoSalva = localStorage.getItem(
        `avaliacao_filme_${dados.tmdb_id}`
    )

    if (avaliacaoSalva) {
        setMinhaNota(Number(avaliacaoSalva))
    }

    const favoritoSalvo = localStorage.getItem(
        `favorito_filme_${dados.tmdb_id}`
    )
    if (favoritoSalvo === 'true') {
        setFavoritado(true)
    }
    setCarregando(false)
})

    }, [id])

    if (carregando) {
        return (
            <main className="pagina-filme carregando">
                <div className="loader"></div>
                <p>Carregando filme...</p>
            </main>
        )
    }

    if (erro || !filme) {
        return (
            <main className="pagina-filme erro-filme">
                <h1>Filme não encontrado</h1>

                <Link to="/">
                    ← Voltar para o CineLog
                </Link>
            </main>
        )
    }

    const posterUrl = filme.poster_path
        ? `https://image.tmdb.org/t/p/w780${filme.poster_path}`
        : null

    const nota = Number(filme.nota_tmdb).toFixed(1)

    return (
        <main className="pagina-filme">

            {posterUrl && (
                <div
                    className="filme-background"
                    style={{
                        backgroundImage: `url(${posterUrl})`
                    }}
                />
            )}

            <div className="filme-overlay" />

            <Link
                to="/"
                className="botao-voltar"
            >
                ← Voltar
            </Link>

            <section className="filme-detalhes">
             {mostrarAvaliacao &&
    createPortal(
        <div
            className="modal-fundo"
            onClick={() => setMostrarAvaliacao(false)}
        >
            <div
                className="modal-avaliacao"
                onClick={e => e.stopPropagation()}
            >
                <button
                    type="button"
                    className="fechar-modal"
                    onClick={() => setMostrarAvaliacao(false)}
                >
                    ×
                </button>

                <span className="modal-label">
                    SUA AVALIAÇÃO
                </span>

                <h2>
                    O que você achou?
                </h2>

                <p>
                    {filme.titulo}
                </p>

                <div className="notas">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(nota => (
                        <button
                            type="button"
                            key={nota}
                            className={
                                nota === notaSelecionada
                                    ? 'nota ativa'
                                    : 'nota'
                            }
                            onClick={() => setNotaSelecionada(nota)}
                        >
                            {nota}
                        </button>
                    ))}
                </div>

                <div className="nota-atual">
                    {notaSelecionada
                        ? `${notaSelecionada}/10`
                        : 'Escolha uma nota'
                    }
                </div>

                <button
                    type="button"
                    className="confirmar-avaliacao"
                    disabled={!notaSelecionada}
                    onClick={() => {
                        localStorage.setItem(
                            `avaliacao_filme_${filme.tmdb_id}`,
                            String(notaSelecionada)
                        )

                        setMinhaNota(notaSelecionada)
                        setMostrarAvaliacao(false)
                    }}
                >
                    Confirmar avaliação
                </button>
            </div>
        </div>,
        document.body
    )
}
                <div className="filme-poster-container">

                    {posterUrl ? (
                        <img
                            className="filme-poster"
                            src={posterUrl}
                            alt={filme.titulo}
                        />
                    ) : (
                        <div className="filme-sem-poster">
                            {filme.titulo}
                        </div>
                    )}

                </div>

                <div className="filme-conteudo">

                    <span className="filme-tipo">
                        🎬 {filme.tipo}
                    </span>

                    <h1>
                        {filme.titulo}
                    </h1>

                    {filme.titulo_original &&
                        filme.titulo_original !== filme.titulo && (
                            <p className="titulo-original">
                                {filme.titulo_original}
                            </p>
                        )
                    }

                    <div className="filme-meta">

                        <div className="nota-tmdb">
                            <span>TMDB</span>

                            <strong>
                                ⭐ {nota}
                            </strong>

                            <small>/10</small>
                        </div>

                        <div className="meta-item">
                            <span>Lançamento</span>
                            <strong>
                                {filme.data_lancamento || 'Não informado'}
                            </strong>
                        </div>

                        <div className="meta-item">
                            <span>Idioma</span>
                            <strong>
                                {filme.idioma?.toUpperCase() || 'N/A'}
                            </strong>
                        </div>

                    </div>

                    <div className="filme-sinopse">

                        <h2>Sinopse</h2>

                        <p>
                            {filme.sinopse || 'Sinopse não disponível.'}
                        </p>

                    </div>

                    <div className="filme-acoes">

                        <button
                        className="botao-avaliar"
                        onClick={() => {
                            setNotaSelecionada(minhaNota || 0)
                            setMostrarAvaliacao(true)
                        }}
>
                        {minhaNota
                        ? `⭐ Minha avaliação: ${minhaNota}/10`
                        : '⭐ Avaliar filme'
                        }
                        </button>

                        <button
                            className={`botao-favoritar ${favoritado ? 'favorito' : ''}`}
                            onClick={() => {
                                const novoEstado = !favoritado
                                setFavoritado(novoEstado)
                                localStorage.setItem(
                                    `favorito_filme_${filme.tmdb_id}`,
                                    novoEstado.toString()
                                )
                            }}
                        >
                            {favoritado ? '❤️ Favoritado' : '♡ Favoritar'}
                        </button>

                    </div>

                </div>

            </section>

            <section className="filme-reviews">

                <div className="titulo-reviews">

                    <div>
                        <span>OPINIÃO DA COMUNIDADE</span>
                        <h2>Reviews</h2>
                    </div>

                    <button>
                        + Escrever review
                    </button>

                </div>

                <div className="review-vazio">

                    <span>✦</span>

                    <h3>Nenhuma review ainda</h3>

                    <p>
                        Seja o primeiro a compartilhar sua opinião
                        sobre este filme.
                    </p>

                </div>

            </section>

        </main>
    )
}

export default Filme