import { useRef, useState } from 'react'
import './HeroFilmes.css'

function HeroFilmes({ filmes }) {
const trackRef = useRef(null)
const [indiceAtivo, setIndiceAtivo] = useState(2)

const arrastando = useRef(false)
const inicioX = useRef(0)
const deslocamentoAtual = useRef(0)

function iniciarArraste(e) {
    arrastando.current = true
    inicioX.current = e.clientX
    deslocamentoAtual.current = 0

    trackRef.current?.setPointerCapture(e.pointerId)
}

function moverArraste(e) {
    if (!arrastando.current) return

    deslocamentoAtual.current = e.clientX - inicioX.current
}

function finalizarArraste() {
    if (!arrastando.current) return

    const deslocamento = deslocamentoAtual.current

    if (Math.abs(deslocamento) > 60) {
        if (deslocamento < 0 && indiceAtivo < filmes.length - 1) {
            setIndiceAtivo(indiceAtivo + 1)
        }

        if (deslocamento > 0 && indiceAtivo > 0) {
            setIndiceAtivo(indiceAtivo - 1)
        }
    }

    arrastando.current = false
    deslocamentoAtual.current = 0
}

if (!filmes || filmes.length === 0) {
    return null
}

return (
    <section className="hero-filmes">
        <div
            ref={trackRef}
            className="hero-track"
            onPointerDown={iniciarArraste}
            onPointerMove={moverArraste}
            onPointerUp={finalizarArraste}
            onPointerCancel={finalizarArraste}
        >
            {filmes.slice(0, 5).map((filme, index) => {
                const distancia = Math.abs(index - indiceAtivo)

                return (
                    <article
                        key={filme.id}
                        className={`hero-poster ${
                            index === indiceAtivo ? 'ativo' : ''
                        }`}
                        style={{
                            '--distancia': distancia,
                            '--posicao': index - indiceAtivo
                        }}
                    >
                        <img
                            src={`https://image.tmdb.org/t/p/w500${filme.poster_path}`}
                            alt={filme.titulo}
                            draggable="false"
                        />

                        {index === indiceAtivo && (
                            <div className="hero-info">
                                <h1>{filme.titulo}</h1>

                                <span>
                                    ⭐ {Number(filme.nota_tmdb).toFixed(1)}/10
                                </span>
                            </div>
                        )}
                    </article>
                )
            })}
        </div>
    </section>
)
}

export default HeroFilmes