import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createPortal } from "react-dom";

import "./Filme.css";

function Filme() {
  const { id } = useParams();

  const [filme, setFilme] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(false);
  const [mostrarAvaliacao, setMostrarAvaliacao] = useState(false);
  const [minhaNota, setMinhaNota] = useState(null);
  const [notaSelecionada, setNotaSelecionada] = useState(0);
  const [reviews, setReviews] = useState([]);
  const [mostrarReview, setMostrarReview] = useState(false);
  const [notaReview, setNotaReview] = useState(0);
  const [textoReview, setTextoReview] = useState("");
  const generos = filme?.generos
    ? filme.generos.split(",").map((genero) => genero.trim())
    : [];

  const elenco = filme?.elenco ? JSON.parse(filme.elenco) : [];
  const [favoritado, setFavoritado] = useState(false);
  useEffect(() => {
    const favoritoSalvo = localStorage.getItem(`favorito_filme_${id}`);

    if (favoritoSalvo === "true") {
      setFavoritado(true);
    }

    setCarregando(true);
    setErro(false);

    fetch(`http://127.0.0.1:5000/api/filmes/${id}`)
      .then((resposta) => {
        if (!resposta.ok) {
          throw new Error("Filme não encontrado");
        }

        return resposta.json();
      })
      .then((dados) => {
        setFilme(dados);

        const avaliacaoSalva = localStorage.getItem(
          `avaliacao_filme_${dados.tmdb_id}`,
        );

        if (avaliacaoSalva) {
          setMinhaNota(Number(avaliacaoSalva));
        }

        const favoritoSalvo = localStorage.getItem(
          `favorito_filme_${dados.tmdb_id}`,
        );

        if (favoritoSalvo === "true") {
          setFavoritado(true);
        }

        // Buscar reviews do filme
        return fetch(
          `http://127.0.0.1:5000/api/conteudos/${dados.tmdb_id}/reviews`,
        );
      })
      .then((resposta) => {
        if (!resposta.ok) {
          throw new Error("Erro ao buscar reviews");
        }

        return resposta.json();
      })
      .then((dados) => {
        console.log("REVIEWS RECEBIDAS:", dados);

        setReviews(dados);
        setCarregando(false);
      })
      .catch((erro) => {
        console.error("Erro:", erro);

        setErro(true);
        setCarregando(false);
      });
  }, [id]);

  const excluirReview = async (reviewId) => {
    try {
      const resposta = await fetch(
        `http://127.0.0.1:5000/api/reviews/${reviewId}`,
        {
          method: "DELETE",
        },
      );

      const dados = await resposta.json();

      if (!resposta.ok) {
        alert(dados.erro || "Erro ao excluir review.");
        return;
      }

      setReviews((reviewsAtuais) =>
        reviewsAtuais.filter((review) => review.id !== reviewId),
      );
    } catch (erro) {
      console.error("Erro ao excluir review:", erro);
      alert("Não foi possível excluir a review.");
    }
  };

  if (carregando) {
    return (
      <main className="pagina-filme carregando">
        <div className="loader"></div>
        <p>Carregando filme...</p>
      </main>
    );
  }

  if (erro || !filme) {
    return (
      <main className="pagina-filme erro-filme">
        <h1>Filme não encontrado</h1>

        <Link to="/">← Voltar para o CineLog</Link>
      </main>
    );
  }

  const posterUrl = filme.poster_path
    ? `https://image.tmdb.org/t/p/w780${filme.poster_path}`
    : null;

  const nota = Number(filme.nota_tmdb).toFixed(1);

  return (
    <main className="pagina-filme">
      {posterUrl && (
        <div
          className="filme-background"
          style={{
            backgroundImage: `url(${posterUrl})`,
          }}
        />
      )}

      <div className="filme-overlay" />

      <Link to="/" className="botao-voltar">
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
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  type="button"
                  className="fechar-modal"
                  onClick={() => setMostrarAvaliacao(false)}
                >
                  ×
                </button>

                <span className="modal-label">SUA AVALIAÇÃO</span>

                <h2>O que você achou?</h2>

                <p>{filme.titulo}</p>

                <div className="notas">
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((nota) => (
                    <button
                      type="button"
                      key={nota}
                      className={
                        nota === notaSelecionada ? "nota ativa" : "nota"
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
                    : "Escolha uma nota"}
                </div>

                <button
                  type="button"
                  className="confirmar-avaliacao"
                  disabled={!notaSelecionada}
                  onClick={() => {
                    localStorage.setItem(
                      `avaliacao_filme_${filme.tmdb_id}`,
                      String(notaSelecionada),
                    );

                    setMinhaNota(notaSelecionada);
                    setMostrarAvaliacao(false);
                  }}
                >
                  Confirmar avaliação
                </button>
              </div>
            </div>,
            document.body,
          )}
        <div className="filme-poster-container">
          {posterUrl ? (
            <img className="filme-poster" src={posterUrl} alt={filme.titulo} />
          ) : (
            <div className="filme-sem-poster">{filme.titulo}</div>
          )}
        </div>

        <div className="filme-conteudo">
          <span className="filme-tipo"> {filme.tipo}</span>

          <h1>{filme.titulo}</h1>

          {filme.titulo_original && filme.titulo_original !== filme.titulo && (
            <p className="titulo-original">{filme.titulo_original}</p>
          )}

          <div className="filme-meta">
            <div className="nota-tmdb">
              <span>TMDB</span>
              <strong>⭐ {nota}</strong>
              <small>/10</small>
            </div>

            <div className="meta-item">
              <span>Lançamento</span>
              <strong>{filme.data_lancamento || "Não informado"}</strong>
            </div>

            {filme.diretor && (
              <div className="meta-item">
                <span>Direção</span>
                <strong>{filme.diretor}</strong>
              </div>
            )}
          </div>
          <div className="filme-sinopse">
            <h2>Sinopse</h2>

            <p>{filme.sinopse || "Sinopse não disponível."}</p>
          </div>

          <div className="filme-generos">
            <span>GÊNEROS</span>

            <div className="generos-lista">
              {generos.map((genero) => (
                <span key={genero} className="genero">
                  {genero}
                </span>
              ))}
            </div>
          </div>

          {elenco.length > 0 && (
            <div className="filme-elenco">
              <h2>Elenco</h2>

              <div className="elenco-lista">
                {elenco.map((ator) => (
                  <div key={ator.id} className="ator-card">
                    <div className="ator-foto">
                      {ator.foto ? (
                        <img
                          src={`https://image.tmdb.org/t/p/w185${ator.foto}`}
                          alt={ator.nome}
                          loading="lazy"
                        />
                      ) : (
                        <div className="ator-sem-foto">?</div>
                      )}
                    </div>

                    <div className="ator-info">
                      <strong>{ator.nome}</strong>
                      <span>{ator.personagem}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="filme-acoes">
            <button
              className="botao-avaliar"
              onClick={() => {
                setNotaSelecionada(minhaNota || 0);
                setMostrarAvaliacao(true);
              }}
            >
              {minhaNota
                ? `⭐ Minha avaliação: ${minhaNota}/10`
                : "⭐ Avaliar filme"}
            </button>

            <button
              className={`botao-favoritar ${favoritado ? "favorito" : ""}`}
              onClick={() => {
                const novoEstado = !favoritado;
                setFavoritado(novoEstado);
                localStorage.setItem(
                  `favorito_filme_${filme.tmdb_id}`,
                  novoEstado.toString(),
                );
              }}
            >
              {favoritado ? "❤️ Favoritado" : "♡ Favoritar"}
            </button>
          </div>
        </div>
      </section>

      <section className="filme-reviews">
        {mostrarReview &&
          createPortal(
            <div
              className="modal-fundo"
              onClick={() => setMostrarReview(false)}
            >
              <div
                className="modal-review"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  type="button"
                  className="fechar-modal"
                  onClick={() => setMostrarReview(false)}
                >
                  ×
                </button>

                <span className="modal-label">SUA REVIEW</span>

                <h2>O que você achou?</h2>

                <p className="modal-review-filme">{filme.titulo}</p>

                <div className="review-modal-nota">
                  <span>SUA NOTA</span>

                  <div className="notas">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((nota) => (
                      <button
                        type="button"
                        key={nota}
                        className={nota === notaReview ? "nota ativa" : "nota"}
                        onClick={() => setNotaReview(nota)}
                      >
                        {nota}
                      </button>
                    ))}
                  </div>

                  <div className="nota-atual">
                    {notaReview ? `${notaReview}/10` : "Escolha uma nota"}
                  </div>
                </div>

                <div className="campo-review">
                  <label htmlFor="texto-review">SUA OPINIÃO</label>

                  <textarea
                    id="texto-review"
                    value={textoReview}
                    maxLength={1500}
                    onChange={(e) => setTextoReview(e.target.value)}
                    placeholder="Escreva o que você achou desse filme..."
                    rows="6"
                  />

                  <small className="contador-caracteres">
                    {textoReview.length}/1500
                  </small>
                </div>

                <button
                  type="button"
                  className="confirmar-review"
                  disabled={!notaReview || !textoReview.trim()}
                  onClick={async () => {
                    try {
                      const resposta = await fetch(
                        `http://127.0.0.1:5000/api/conteudos/${id}/reviews`,
                        {
                          method: "POST",
                          headers: {
                            "Content-Type": "application/json",
                          },
                          body: JSON.stringify({
                            user_id: 1,
                            nota: notaReview,
                            texto: textoReview.trim(),
                          }),
                        },
                      );

                      const dados = await resposta.json();

                      if (!resposta.ok) {
                        alert(dados.erro || "Erro ao publicar review.");
                        return;
                      }

                      setMostrarReview(false);

                      setNotaReview(0);
                      setTextoReview("");

                      const reviewsAtualizadas = await fetch(
                        `http://127.0.0.1:5000/api/conteudos/${id}/reviews`,
                      );

                      const novasReviews = await reviewsAtualizadas.json();

                      setReviews(novasReviews);
                    } catch (erro) {
                      console.error("Erro ao publicar review:", erro);
                      alert("Não foi possível publicar a review.");
                    }
                  }}
                >
                  Publicar review
                </button>
              </div>
            </div>,
            document.body,
          )}

        <div className="titulo-reviews">
          <div>
            <span>OPINIÃO DA COMUNIDADE</span>
            <h2>Reviews</h2>
          </div>

          <button type="button" onClick={() => setMostrarReview(true)}>
            + Escrever review
          </button>
        </div>

        {reviews.length === 0 ? (
          <div className="review-vazio">
            <span>✦</span>

            <h3>Nenhuma review ainda</h3>

            <p>Seja o primeiro a compartilhar sua opinião sobre este filme.</p>
          </div>
        ) : (
          <div className="reviews-lista">
            {reviews.map((review) => (
              <article key={review.id} className="review-card">
                <div className="review-card-topo">
                  <strong>{review.username}</strong>

                  <span className="review-nota">⭐ {review.nota}/10</span>

                  {review.user_id === 1 && (
                    <button
                      type="button"
                      className="botao-excluir-review"
                      onClick={() => excluirReview(review.id)}
                      title="Excluir minha review"
                    >
                      🗑️
                    </button>
                  )}
                </div>

                <p className="review-texto">{review.texto}</p>

                <small className="review-data">
                  {new Date(review.created_at).toLocaleDateString("pt-BR")}
                </small>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default Filme;
