# Preditor de Espécies Iris 🌸

Este é um aplicativo web interativo construído com **Streamlit** que atua como **cliente** de uma **API RESTful** que classfica espécies Iris com base em suas características morfológicas.

### Pré-requisitos

Certifique-se de ter o Python 3.11 e o Poetry instalados em seu sistema.

Para instalar o Poetry, use o método oficial:

```bash
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
```

### Instalação

Clone o repositório e instale as dependências listadas no pyproject.toml:

```bash
git clone https://github.com/jorgeplatero/preditor_especies_iris.git
cd preditor-iris
poetry install
```

O Poetry criará um ambiente virtual isolado e instalará todas as bibliotecas necessárias.

### Como Rodar a Aplicação

Execute o script Python:

```bash
poetry run streamlit run app.py
```

### Funcionalidades

* **Autenticação:** implementa interface para login e registro de usuários.
* **Predição:** permite a submissão interativa das quatro características da Iris (**comprimento/largura da sépala/pétala**) para serem processadas por um modelo de Machine Learning via API externa e retorna a classe predita.
* **Histórico de predições:** o usuário pode visualizar e paginar o histórico de predições persistido no banco de dados da API.

### Tecnologias

A aplicação atua como cliente que se comunica com a API externa.

| Componente | Tecnologia | Versão (Especificada) | Descrição |
| :--- | :--- | :--- | :--- |
| **Frontend/App** | **Streamlit** | `^1.51.0` | Framework Python para a interface web. |
| **Comunicação** | **Requests** | `^2.32.5` | Biblioteca para interagir com a API REST. |
| **Backend/API** | **Flask** (+ JWT) | *(Externo)* | API RESTful responsável pela lógica de ML e segurança. |
| **Ambiente** | **Python** | `>=3.11, <4.0` | Versões compatíveis para a execução do projeto. |
| **Gerenciamento** | **Poetry** | `2.2.1` | Gerenciador de dependências e ambientes virtuais. |

### Integrações

O aplicativo está configurado para interagir com API em produção no Vercel, cujo link e repositório pode ser acessado no link abaixo:

API: `https://postech-flask-ml-fase-1.vercel.app`

Repositório GitHub: `https://github.com/jorgeplatero/postech_flask_ml_fase_1`
