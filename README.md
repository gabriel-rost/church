# Church App 🙏

Plataforma web para comunidades cristãs, desenvolvida em Django. Permite que membros de igrejas interajam entre si, acompanhem planos de leitura bíblica e se organizem em canais temáticos.

[![CI](https://github.com/gabriel-rost/church/actions/workflows/django.yml/badge.svg)](https://github.com/gabriel-rost/church/actions)
[![Coverage](https://codecov.io/gh/gabriel-rost/church/graph/badge.svg)](https://app.codecov.io/github/gabriel-rost/church)
---

## Funcionalidades

- **Autenticação e Perfis** — Cadastro, login, edição de perfil com avatar
- **Feed e Posts** — Publicação de conteúdo com comentários, curtidas, scroll infinito e posts em destaque
- **Bíblia** — Leitura por livro, capítulo e versículo com a tradução NVI
- **Planos de Leitura** — Criação e acompanhamento de planos semanais com progresso por tarefa
- **Canais** — Comunidades temáticas com membros e feed próprio
- **Notificações Push** — Envio de notificações via Web Push (service worker)
- **Busca** — Pesquisa de conteúdo e usuários
- **Upload de Arquivos** — Armazenamento de mídia via Cloudflare R2

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.10 + Django 5 |
| Banco de dados | PostgreSQL |
| Armazenamento | Cloudflare R2 (bucket S3-compatible) |
| Containerização | Docker |
| Hospedagem | VM com containers |
| CI/CD | GitHub Actions |
| Cobertura | Codecov |

---

## Estrutura do Projeto
```
church_project/
├── church_app/         # App principal
│   ├── models/         # User, Post, Channel, Bible, ReadingPlan
│   ├── views/          # Organizadas por domínio
│   ├── templates/      # HTML por funcionalidade
│   └── tests/          # Testes unitários por camada
├── church_site/        # Configurações Django
├── static/             # CSS e JS
└── manage.py
```

---

## Rodando localmente

**Pré-requisitos:** Python 3.10+, PostgreSQL, Docker (opcional)
```bash
git clone https://github.com/gabriel-rost/church.git
cd church_project

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Configure as variáveis de ambiente:
```bash
SECRET_KEY=sua-secret-key
DEBUG=True
DATABASE_URL=postgres://usuario:senha@localhost:5432/church_db
CLOUDFLARE_R2_BUCKET=seu-bucket
```
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Para importar a Bíblia (NVI):
```bash
python import_bible.py
```

---

## Testes
```bash
# Rodar testes
python manage.py test church_app

# Com cobertura
coverage run manage.py test church_app
coverage report
```

---

## Deploy

A infraestrutura atual roda em containers Docker em uma VM. Deploy em **Render** para ambiente de sandbox.

---

## Boas práticas adotadas

- Custom User Model (`AbstractUser`)
- `AUTH_USER_MODEL` nos relacionamentos
- Views organizadas por domínio (não um único `views.py`)
- Models separados por contexto (`post/`, `channel/`, `bible/`)
- Testes unitários com CI automático no GitHub Actions