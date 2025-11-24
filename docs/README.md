# 🌸 Preditor de Espécies de Iris

Este é um aplicativo web interativo construído com **Streamlit** que atua como **cliente** de uma **API RESTful** (hospedada no Vercel) para classificar a espécie da flor Iris, baseada em suas características morfológicas.

## Funcionalidades

* **Autenticação JWT:** implementa **Login** e **Registro** de usuários, protegendo o acesso ao endpoint de predição através de **Tokens Web JSON (JWT)**.
* **Predição em Tempo Real:** permite a submissão interativa das quatro características da Iris (**Comprimento/Largura da Sépala/Pétala**) para serem processadas por um modelo de Machine Learning via API externa.
* **Histórico de Predições:** após o login, o usuário pode visualizar e paginar (*limit* e *offset*) seu histórico de predições, que é persistido no banco de dados da API.

## Arquitetura e Tecnologias

A aplicação atua como um frontend (cliente) que se comunica com um backend (API) externo.

| Componente | Tecnologia | Versão (Especificada) | Descrição |
| :--- | :--- | :--- | :--- |
| **Frontend/App** | **Streamlit** | `^1.51.0` | Framework Python para a interface web. |
| **Comunicação** | **Requests** | `^2.32.5` | Biblioteca para interagir com a API REST. |
| **Backend/API** | **Flask** (+ JWT) | *(Externo)* | API RESTful responsável pela lógica de ML e segurança. |
| **Ambiente** | **Python** | `>=3.11, <4.0` | Versões compatíveis para a execução do projeto. |
| **Gerenciamento** | **Poetry** | `2.2.1` | Gerenciador de dependências e ambientes virtuais. |

### URL da API Externa

O aplicativo está configurado para interagir com o *backend* no Vercel:

`https://postech-flask-ml-fase-1.vercel.app`

---

## 🛠️ Configuração e Execução

### 1. Pré-requisitos

Você deve ter o **Python** (versão 3.11 ou superior) e o gerenciador de dependências **Poetry** instalados em seu sistema.

### 2. Configuração do Ambiente

1. **Clone o Repositório:**

```bash
git clone [URL_DO_SEU_REPOSITÓRIO]
cd preditor-iris
```

2. **Instalação de Dependências:** o Poetry lerá o `pyproject.toml` e instalará todas as dependências no ambiente virtual.

```bash
poetry install
```

### 3. Executando o Aplicativo (Frontend)

Com o ambiente virtual ativo, inicie o aplicativo Streamlit:

```bash
poetry run streamlit run app.py