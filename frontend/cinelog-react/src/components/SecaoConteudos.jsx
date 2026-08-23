import { useRef } from 'react'
import CardConteudo from './CardConteudo'

function SecaoConteudos({ titulo, conteudos }) {
    const listaRef = useRef(null)

    function moverCarrossel(direcao) {
        if (!listaRef.current) return

        listaRef.current.scrollBy({
            left: direcao * 500,
            behavior: 'smooth'
        })
    }

    return (
        <section className="secao-conteudos">
            <div className="titulo-secao">
                <h2>{titulo}</h2>

                <div className="controles-carrossel">
                    <button onClick={() => moverCarrossel(-1)}>‹</button>
                    <button onClick={() => moverCarrossel(1)}>›</button>
                </div>
            </div>

            <div className="lista-conteudos" ref={listaRef}>
                {conteudos.map(conteudo => (
                    <CardConteudo
                        key={conteudo.id}
                        conteudo={conteudo}
                    />
                ))}
            </div>
        </section>
    )
}

export default SecaoConteudos