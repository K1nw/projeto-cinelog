function CardConteudo({ conteudo }) {
    return (
        <article className="card-conteudo">
            <div className="poster">
                {conteudo.poster ? (
                    <img src={conteudo.poster} alt={conteudo.titulo} />
                ) : (
                    <span>{conteudo.titulo}</span>
                )}
            </div>

            <div className="info-conteudo">
                <h3>{conteudo.titulo}</h3>
                <span>{conteudo.tipo}</span>
                <strong>⭐ {conteudo.nota}</strong>
            </div>
        </article>
    )
}

export default CardConteudo