# 🎬 CineLog

Um sistema de gerenciamento e descoberta de filmes, séries e animes inspirado em plataformas como o Letterboxd, desenvolvido para praticar e demonstrar conceitos de desenvolvimento **Full Stack**, desde os fundamentos até uma aplicação integrada com banco de dados e APIs externas.

## 📖 Sobre o projeto

O CineLog começou como uma aplicação de terminal desenvolvida em Python e evoluiu gradualmente para uma aplicação web.

O projeto está sendo desenvolvido em etapas, acompanhando minha evolução como desenvolvedor e permitindo aplicar na prática conceitos de:

* Desenvolvimento Frontend
* Desenvolvimento Backend
* APIs REST
* Banco de dados
* Integração com APIs externas
* Componentização
* Persistência de dados
* Git e GitHub

O objetivo é transformar o projeto inicial de CRUD em uma plataforma completa para descobrir, organizar e avaliar conteúdos.

---

## 🚀 Tecnologias

### Frontend

* ⚛️ React
* ⚡ JavaScript
* 🌐 HTML5
* 🎨 CSS3
* 🟢 Vite

### Backend

* 🐍 Python
* 🌶️ Flask
* 🔗 Flask-CORS

### Banco de dados

* 🗄️ SQLite

### APIs

* 🎬 TMDB — filmes e futuramente séries
* 🎌 AniList — futuramente para animes

### Ferramentas

* 📦 Git
* 🐙 GitHub
* 🔐 python-dotenv
* 🌐 Requests

---

## ✨ Funcionalidades atuais

* ✅ Interface web em React
* ✅ Home do CineLog
* ✅ Header e navegação
* ✅ Hero com barra de busca
* ✅ Cards de conteúdo
* ✅ Carrossel horizontal
* ✅ Navegação pelas setas
* ✅ Hover nos cards
* ✅ Integração com API do TMDB
* ✅ Importação automática de filmes
* ✅ Persistência dos filmes em SQLite
* ✅ API Flask para disponibilizar os dados
* ✅ Exibição dos pôsteres do TMDB
* ✅ Exibição das notas do TMDB
* ✅ Formatação das avaliações em escala de 1 a 10

---

## 🔄 Arquitetura atual

O fluxo principal da aplicação funciona da seguinte maneira:

```text
TMDB
 ↓
importar_filmes.py
 ↓
SQLite (cinelog.db)
 ↓
Flask
 ↓
API REST
 ↓
React
 ↓
Interface CineLog
```

O TMDB é utilizado como **fonte de dados para alimentar o banco**, enquanto o SQLite funciona como banco de dados próprio do CineLog.

A ideia é que o CineLog não dependa diretamente do TMDB para armazenar seus conteúdos.

---

## 🗄️ Banco de dados

Atualmente o projeto utiliza **SQLite**.

Os conteúdos são armazenados na tabela `conteudos`, contendo informações como:

* ID interno
* ID do TMDB
* Título
* Título original
* Tipo de conteúdo
* Sinopse
* Data de lançamento
* Nota do TMDB
* Popularidade
* Idioma
* Caminho do pôster

Exemplo de dados importados:

```text
Spider-Man: Brand New Day → 7.903
The Odyssey → 7.997
Toy Story 5 → 8.135
Spider-Man: No Way Home → 7.941
```

---

## 🛠️ Backend

O backend é desenvolvido em **Python utilizando Flask**.

Sua principal responsabilidade atualmente é:

* Receber requisições do frontend
* Consultar o SQLite
* Disponibilizar os conteúdos através de uma API REST
* Permitir que o React consuma os dados do banco

Uma das rotas disponíveis é:

```text
GET /api/filmes
```

Essa rota retorna os filmes armazenados no banco em formato JSON.

---

## 🎬 Integração com TMDB

O CineLog possui um processo de importação responsável por buscar filmes no TMDB e armazená-los no SQLite.

O processo atualmente utiliza dados como:

* Título
* Título original
* Sinopse
* Data de lançamento
* Nota
* Popularidade
* Idioma
* Pôster

Os caminhos dos pôsteres fornecidos pelo TMDB são transformados em URLs completas no frontend para que as imagens possam ser exibidas nos cards.

As credenciais da API são armazenadas através de variáveis de ambiente e não devem ser versionadas no Git.

---

## 🎨 Frontend

O frontend atualmente utiliza **React** e possui uma estrutura componentizada.

Principais componentes:

```text
src/
├── App.jsx
├── App.css
├── index.css
└── components/
    ├── Header.jsx
    ├── CardConteudo.jsx
    └── SecaoConteudos.jsx
```

O `CardConteudo` é responsável pela apresentação individual dos conteúdos.

O `SecaoConteudos` controla as seções e o carrossel horizontal.

---

## 🏠 Home

A página inicial atualmente possui seções destinadas a:

* 🔥 Em destaque
* ⭐ Mais bem avaliados
* 🎬 Filmes
* 📺 Séries
* 🎌 Animes

A estrutura visual já está preparada para trabalhar com diferentes tipos de conteúdo.

A separação completa entre essas categorias ainda está em desenvolvimento.

---

## 🔜 Próximas funcionalidades

### Conteúdo

* ⌛ Separar conteúdos por categoria
* ⌛ Criar importação de séries através do TMDB
* ⌛ Integrar animes através do AniList
* ⌛ Melhorar sistema de destaque
* ⌛ Melhorar ordenação por avaliação
* ⌛ Busca de conteúdos

### Usuário

* ⌛ Sistema de usuários
* ⌛ Avaliações pessoais
* ⌛ Favoritos
* ⌛ Reviews
* ⌛ Histórico de conteúdos assistidos
* ⌛ Estatísticas pessoais

### Interface

* ⌛ Página individual de conteúdo
* ⌛ Melhorias de responsividade
* ⌛ Animações e interações
* ⌛ Sistema visual de avaliações
* ⌛ Melhorias na busca

### Infraestrutura

* ⌛ Melhorar arquitetura do backend
* ⌛ Migrar futuramente para PostgreSQL, se necessário
* ⌛ Deploy da aplicação
* ⌛ Configuração de domínio próprio
* ⌛ HTTPS
* ⌛ Preparação para utilização pública

---

## 🔐 Segurança

O CineLog utiliza variáveis de ambiente para armazenar credenciais de APIs.

Arquivos sensíveis não devem ser enviados ao GitHub, incluindo:

```text
.env
*.db
.venv/
```

O projeto utiliza `.gitignore` para evitar o versionamento desses arquivos.

---

## 🎯 Objetivo

O CineLog faz parte do meu portfólio e está sendo desenvolvido para praticar conceitos de:

* Python
* JavaScript
* React
* HTML
* CSS
* Flask
* SQLite
* APIs REST
* Integração com APIs externas
* Banco de dados
* CRUD
* Desenvolvimento Full Stack
* Componentização
* Persistência de dados
* Git e GitHub
* Organização de projetos

Mais do que apenas criar uma aplicação, o objetivo é acompanhar a evolução do projeto desde um CRUD simples até uma aplicação Full Stack completa.

---

## 📷 Preview

Em breve.

<img width="1889" height="909" alt="Captura de tela 2026-08-24 225444" src="https://github.com/user-attachments/assets/fde5e4b6-d0ac-4be4-8d67-3676535648ce" />
<img width="1894" height="908" alt="Captura de tela 2026-08-24 225432" src="https://github.com/user-attachments/assets/f1fabee8-e3cd-48db-a58e-4214eefdd2a9" />



## 👨‍💻 Autor

**Nathan Costa**

Desenvolvido como projeto pessoal de estudo e portfólio.
