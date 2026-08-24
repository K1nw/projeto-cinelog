import { Link } from 'react-router-dom'

function CardConteudo({ conteudo }) {

    const posterUrl = conteudo.poster_path
        ? `https://image.tmdb.org/t/p/w500${conteudo.poster_path}`
        : null

    return (
        <Link
            to={`/filmes/${conteudo.tmdb_id}`}
            className="card-link"
        >
            <article className="card-conteudo">

                <div className="poster">

                    {posterUrl ? (
                        <img
                            src={posterUrl}
                            alt={conteudo.titulo}
                        />
                    ) : (
                        <span>{conteudo.titulo}</span>
                    )}

                </div>

                <div className="info-conteudo">

                    <h3>{conteudo.titulo}</h3>

                    <span>{conteudo.tipo}</span>

                    <strong>
                        ⭐ {Number(conteudo.nota_tmdb).toFixed(1)}/10
                    </strong>

                </div>

            </article>
        </Link>
    )
}

export default CardConteudo