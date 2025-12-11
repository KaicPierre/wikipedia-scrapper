# Wikipedia Scraper & Summarizer

API FastAPI para extrair e resumir artigos da Wikipedia usando IA (Ollama ou OpenAI).

## 📋 Índice

- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
  - [Opção 1: Rodando Localmente com UV](#opção-1-rodando-localmente-com-uv)
  - [Opção 2: Rodando com Docker Compose](#opção-2-rodando-com-docker-compose)
- [Uso da API](#-uso-da-api)
- [Testes](#-testes)
- [Decisões de Projeto](#-decisões-de-projeto)
- [Estrutura do Projeto](#-estrutura-do-projeto)

## ✨ Características

- Extração automática de conteúdo de artigos da Wikipedia em português
- Geração de resumos usando IA (Ollama ou OpenAI)
- Armazenamento de resumos no banco de dados PostgreSQL
- API REST com documentação automática (Swagger)
- Testes unitários com 100% de cobertura nos services
- Containerização completa com Docker Compose

## 🚀 Tecnologias

- **Python 3.12** - Linguagem principal
- **FastAPI** - Framework web
- **UV** - Gerenciador de pacotes e ambientes Python
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Ollama** - Execução local de modelos LLM
- **LangChain** - Framework para aplicações com LLMs
- **BeautifulSoup4** - Web scraping
- **Docker & Docker Compose** - Containerização

## 📦 Pré-requisitos

### Para execução local:
- Python 3.12+
- UV (gerenciador de pacotes): `pip install uv`
- PostgreSQL 15+
- Ollama (opcional, para usar LLMs locais): [https://ollama.ai](https://ollama.ai)

### Para execução com Docker:
- Docker 20.10+
- Docker Compose 2.0+

## 🔧 Instalação e Execução

### Opção 1: Rodando Localmente com UV

#### 1. Clone o repositório
```bash
git clone https://github.com/KaicPierre/wikipedia-scrapper.git
cd wikipedia-scrapper
```

#### 2. Configure o arquivo .env
```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:
```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=wikipedia_db
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wikipedia_db

# Model Configuration
MODEL=OLLAMA  # ou GPT para usar OpenAI

# OpenAI (opcional - necessário apenas se MODEL=GPT)
OPENAI_API_KEY=sua-chave-aqui

# Ollama (se estiver usando localmente)
OLLAMA_BASE_URL=http://localhost:11434
```

#### 3. Instale as dependências
```bash
uv sync
```

#### 4. Configure o PostgreSQL
Certifique-se de que o PostgreSQL está rodando e crie o banco de dados:
```bash
docker compose up db -d
```

#### 5. (Opcional) Configure o Ollama
Se você escolheu usar Ollama localmente adicione as envs:
```env
MODEL=OLLAMA
OPENAI_API_KEY=not-needed
```

**Instale o Ollama:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Baixe o modelo Mistral:**
```bash
ollama pull mistral
```

**Inicie o servidor Ollama (se não iniciar automaticamente):**
```bash
ollama serve
```

#### 6. Execute a aplicação
```bash
uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em:
- **Documentação**: http://localhost:8000/docs
- **API**: http://localhost:8000

---

### Opção 2: Rodando com Docker Compose

#### 1. Clone o repositório
```bash
git clone https://github.com/KaicPierre/wikipedia-scrapper.git
cd wikipedia-scrapper
```

#### 2. Configure o arquivo .env
```bash
cp .env.example .env
```

Para usar com **OpenAI** (recomendado com Docker):
```env
MODEL=GPT
OPENAI_API_KEY=sua-chave-openai
```

Para usar com **Ollama** (⚠️ veja observação abaixo):
```env
MODEL=OLLAMA
OPENAI_API_KEY=not-needed
```

#### 3. Inicie os containers
```bash
docker compose up -d
```

#### 4. (Se usar Ollama) Baixe o modelo
```bash
docker compose exec ollama ollama pull mistral
```

#### 5. Acesse a aplicação
- **Documentação**: http://localhost:8000/docs
- **API**: http://localhost:8000

#### ⚠️ IMPORTANTE: Sobre o uso do Ollama com Docker Compose

**O Ollama no Docker Compose é MUITO LENTO** devido às limitações de recursos do Docker. O processamento pode levar **4-5 minutos ou mais** por requisição. 

**Recomendações:**

1. **MELHOR OPÇÃO**: Use OpenAI GPT com Docker Compose - funciona normalmente e responde rápido
2. **ALTERNATIVA**: Se quiser usar Ollama, rode-o **localmente** (fora do Docker) e use a execução local da aplicação com UV
3. **NÃO RECOMENDADO**: Ollama dentro do Docker Compose (a menos que você tenha muito tempo e paciência)

Se mesmo assim quiser usar Ollama no Docker, aumente o timeout no Postman/cliente HTTP para pelo menos 10 minutos.

## 📖 Uso da API

### Criar um resumo
```bash
POST http://localhost:8000/summary/
Content-Type: application/json

{
  "url": "https://pt.wikipedia.org/wiki/Python_(linguagem_de_programação)",
  "word_count": 50
}
```

### Buscar resumo existente
```bash
GET http://localhost:8000/summary/Python_(linguagem_de_programação)
```

### Exemplos com cURL

**Criar resumo:**
```bash
curl -X POST "http://localhost:8000/summary/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pt.wikipedia.org/wiki/Python",
    "word_count": 100
  }'
```

**Buscar resumo:**
```bash
curl "http://localhost:8000/summary/Python"
```

## 🧪 Testes

Os testes unitários cobrem 100% dos services (scrapper e summarizer).

### Executar testes localmente
```bash
uv run pytest
```

### Executar testes com coverage
```bash
uv run pytest --cov=app/services --cov-report=term-missing
```

## 💡 Decisões de Projeto

### Controle de Palavras
O controle do número de palavras no resumo é feito de forma simples, usando o parâmetro `word_count` como uma aproximação do número de tokens. **Para um ambiente de produção**, seria necessário:
- Implementar contagem precisa de tokens usando o tokenizer específico do modelo
- Adicionar pós-processamento para garantir o limite exato de palavras
- Implementar validação mais robusta do output

**Limitação conhecida**: LLMs não são eficientes em "contar" coisas. Eles podem gerar textos com mais ou menos palavras do que o solicitado. Uma solução mais robusta envolveria pós-processamento ou técnicas de prompting mais avançadas.

### Escolha do Modelo
O projeto usa **Mistral 7B** como modelo padrão do Ollama por:
- Rodar eficientemente em CPU
- Não requerer GPU ou recursos de hardware específicos
- Ser gratuito e open-source
- Ter bom desempenho em tarefas de sumarização

Alternativamente, pode-se usar **OpenAI GPT-4** para:
- Melhor qualidade de resumos
- Respostas mais rápidas
- Melhor aderência ao limite de palavras

### Performance e Docker
O Ollama tem **performance significativamente reduzida** quando executado dentro do Docker devido às limitações de recursos. Tempos de resposta podem variar de 4-10 minutos dependendo do tamanho do artigo.

**Recomendação para produção**: Use OpenAI API ou configure o Ollama em uma máquina dedicada com recursos adequados.

### Uso de IA no Desenvolvimento
Este projeto utilizou assistência de IA (GitHub Copilot) em:
- ✅ Geração de testes unitários (revisados e validados)
- ✅ Documentação (README, docstrings)
- ✅ Resolução de problemas de configuração do Docker Compose
- ✅ Resolução de problemas de conexão utilizando o ORM

**TODO O CÓDIGO GERADO POR IA FOI:**
- 📖 Lido e compreendido completamente
- ✏️ Revisado e adaptado às necessidades do projeto
- 🧪 Testado e validado
- 🎯 Otimizado para não conter código desnecessário

A IA foi usada como ferramenta de **aceleração de desenvolvimento**, especialmente para tarefas repetitivas, mas **todas as decisões arquiteturais e lógica de negócio foram feitas manualmente**.

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── main.py                 # Entry point da aplicação
│   ├── settings.py             # Configurações e variáveis de ambiente
│   ├── database/
│   │   └── connection.py       # Configuração do banco de dados
│   ├── models/
│   │   └── summary.py          # Modelo SQLAlchemy
│   ├── repositories/
│   │   └── summary.py          # Camada de acesso a dados
│   ├── router/
│   │   └── router.py           # Rotas da API
│   ├── schemas/
│   │   └── summary.py          # Schemas Pydantic
│   └── services/
│       ├── scrapper.py         # Serviço de web scraping
│       └── summarizer.py       # Serviço de sumarização com IA
├── tests/
│   ├── test_scrapper.py        # Testes do scrapper
│   └── test_summarizer.py      # Testes do summarizer
├── docker-compose.yml          # Orquestração de containers
├── Dockerfile                  # Imagem da aplicação
├── pyproject.toml              # Dependências e configuração do projeto
├── .env.example                # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```
