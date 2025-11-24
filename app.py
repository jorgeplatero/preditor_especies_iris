import streamlit as st
import pandas as pd
import requests


API_URL = 'https://postech-flask-ml-fase-1.vercel.app' 
ENDPOINT_PREVER = f'{API_URL}/predict'
ENDPOINT_LOGIN = f'{API_URL}/login'
ENDPOINT_REGISTRO = f'{API_URL}/register'
ENDPOINT_PREDICOES = f'{API_URL}/predictions'

st.set_page_config(
    page_title='Preditor de Espécies Iris 🌸',
    layout='wide'
)

if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'token_acesso' not in st.session_state:
    st.session_state.token_acesso = None
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None


def login(usuario, senha):
    '''Lida com o login do usuário e recupera o token JWT.'''
    try:
        response = requests.post(ENDPOINT_LOGIN, json={'username': usuario, 'password': senha})
        if response.status_code == 200:
            token = response.json().get('access_token')
            st.session_state.token_acesso = token
            st.session_state.usuario = usuario
            st.session_state.logado = True
            st.rerun()
        else:
            try:
                erro_data = response.json()
                erro_msg = erro_data.get('error', 'Credenciais inválidas.')
            except requests.exceptions.JSONDecodeError:
                erro_msg = f'Erro de comunicação com a API (Status: {response.status_code}).'
            st.error(erro_msg)
    except requests.exceptions.ConnectionError:
        st.error(f'Erro de conexão: não foi possível conectar à API em {API_URL}.')
    except Exception as e:
        st.error(f'Ocorreu um erro inesperado durante o login: {e}')


def register(usuario, senha):
    '''Lida com o registro do usuário.'''
    try:
        response = requests.post(ENDPOINT_REGISTRO, json={'username': usuario, 'password': senha})
        
        if response.status_code == 201:
            st.success('Registro realizado com sucesso. Faça o login.')
        else:
            try:
                erro_data = response.json()
                erro_msg = erro_data.get('error', 'Falha no registro.')
            except requests.exceptions.JSONDecodeError:
                erro_msg = f'Erro de comunicação com a API (Status: {response.status_code}).'
            st.error(erro_msg)
    except requests.exceptions.ConnectionError:
        st.error(f'Erro de nonexão: não foi possível conectar à API em {API_URL}.')
    except Exception as e:
        st.error(f'Ocorreu um erro inesperado durante o registro: {e}')


def predict(comp_sepala, larg_sepala, comp_petala, larg_petala):
    '''Envia dados de características para o endpoint seguro de predição.'''
    if not st.session_state.logado:
        st.error('Por favor, faça login para realizar uma predição.')
        return None

    headers = {
        'Authorization': f'Bearer {st.session_state.token_acesso}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'sepal_length': comp_sepala,
        'sepal_width': larg_sepala,
        'petal_length': comp_petala,
        'petal_width': larg_petala
    }

    try:
        response = requests.post(ENDPOINT_PREVER, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('predicted_specie')
        elif response.status_code == 401:
            st.error('Autenticação necessária. Seu token pode ter expirado. Por favor, faça login novamente.')
            st.session_state.logado = False
            st.session_state.token_acesso = None
            st.rerun()
        else:
            st.error(f"Falha na predição (Status {response.status_code}): {response.json().get('error', 'Erro da API')}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f'Erro de Conexão: Não foi possível conectar à API em {API_URL}.')
        return None


@st.cache_data(show_spinner=False)
def history(token, limit=10, offset=0):
    '''Recupera o histórico de predições com paginação (limit e offset).'''
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {'limit': limit, 'offset': offset}
    try:
        response = requests.get(ENDPOINT_PREDICOES, headers=headers, params=params) 
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
                df.rename(columns={
                    'created_at': 'Data',
                    'sepal_length': 'Comp. Sépala (cm)',
                    'sepal_width': 'Larg. Sépala (cm)',
                    'petal_length': 'Comp. Pétala (cm)',
                    'petal_width': 'Larg. Pétala (cm)',
                    'predicted_specie': 'Espécie Prevista'
                }, inplace=True)
                return df[['Data', 'Comp. Sépala (cm)', 'Larg. Sépala (cm)', 'Comp. Pétala (cm)', 'Larg. Pétala (cm)', 'Espécie Prevista']]
            else:
                return pd.DataFrame()
        elif response.status_code == 401:
            history.clear()
            st.session_state.logado = False
            st.session_state.token_acesso = None
            st.rerun()
            return pd.DataFrame()
        else:
            error_msg = response.json().get('error', response.json().get('msg', 'Erro da API'))
            st.error(f"Falha ao obter histórico (Status {response.status_code}): {error_msg}")
            return pd.DataFrame()
    except requests.exceptions.ConnectionError:
        st.error(f'Erro de Conexão: Não foi possível conectar à API em {API_URL}.')
        return pd.DataFrame()


def show_login():
    '''Renderiza os formulários de login e registro.'''
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        st.title('Preditor de Espécies Iris 🌸')
        opcao_login, opcao_cadastro = st.tabs(['Login', 'Cadastro'])
        with opcao_login:
            with st.form('form_login', clear_on_submit=False):
                st.subheader('Entrar')
                usuario = st.text_input('Usuário', key='input_usuario')
                senha = st.text_input('Senha', type='password', key='input_senha')
                entrar = st.form_submit_button('Entrar')
                if entrar:
                    login(usuario, senha)
        with opcao_cadastro:
            with st.form('form_cadastro', clear_on_submit=True):
                st.subheader('Criar Conta')
                usuario = st.text_input('Novo Usuário', key='input_novo_usuario')
                senha = st.text_input('Nova Senha', type='password', key='input_nova_senha')
                cadastrar = st.form_submit_button('Cadastrar')
                if cadastrar:
                    register(usuario, senha)
        st.info(f'URL base da API: {API_URL}')


def show_app():
    '''Renderiza o aplicativo'''
    st.title('Preditor de Espécies Iris 🌸')
    container_header = st.container()
    with container_header:
        st.markdown(f'**Logado como: {st.session_state.usuario}**')
        if st.button('Sair', key='logout_btn'):
            history.clear()
            st.session_state.logado = False
            st.session_state.token_acesso = None
            st.session_state.usuario = None
            st.info('Sessão encerrada com sucesso.')
            st.rerun()
    st.markdown('---')
    st.subheader('🛠️ Parâmetros de entrada')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        comp_sepala = st.slider('Comp. Sépala', 0.0, 10.0, 5.4, 0.1, key='sl')
    with col2:
        larg_sepala = st.slider('Larg. Sépala', 0.0, 10.0, 3.4, 0.1, key='sw')
    with col3:
        comp_petala = st.slider('Comp. Pétala', 0.0, 10.0, 1.3, 0.1, key='pl')
    with col4:
        larg_petala = st.slider('Larg. Pétala', 0.0, 10.0, 0.2, 0.1, key='pw')
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Dados Fornecidos')
        dados_entrada = pd.DataFrame({
            'Comp. Sépala (cm)': [comp_sepala],
            'Larg. Sépala (cm)': [larg_sepala],
            'Comp. Pétala (cm)': [comp_petala],
            'Larg. Pétala (cm)': [larg_petala]
        })
        st.table(dados_entrada)
        if st.button('Prever', key='botao_prever'):
            with st.spinner('Solicitando predição à API...'):
                especie_prevista = predict(comp_sepala, larg_sepala, comp_petala, larg_petala)
                if especie_prevista:
                    st.session_state.last_prediction = especie_prevista
                    history.clear() 
                    st.rerun()
                else:
                    st.session_state.last_prediction = None
        if st.session_state.last_prediction:
            st.success(f'A espécie de Iris prevista é: **{st.session_state.last_prediction.capitalize()}**')
    with col2:
        st.subheader('Histórico de Predições')
        col_limit, col_offset = st.columns(2)
        with col_limit:
            limite = st.number_input(
                'Limite', 
                min_value=1, 
                max_value=50, 
                value=10, 
                step=1,
                key='limite'
            )
        with col_offset:
            offset = st.number_input(
                'Offset', 
                min_value=0, 
                value=0, 
                step=10,
                key='offset'
            )
        df_historico = history(st.session_state.token_acesso, limit=limite, offset=offset)
        if not df_historico.empty:
            st.dataframe(df_historico, use_container_width=True)
        else:
            st.info('Nenhum histórico para exibir ou falha ao recuperar.')


if st.session_state.logado:
    show_app()
else:
    show_login()