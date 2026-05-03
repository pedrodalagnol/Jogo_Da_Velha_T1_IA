import streamlit as st
import joblib
import numpy as np
import random

st.set_page_config(page_title="IA Tic-Tac-Toe PUCRS", layout="centered")

st.markdown("""
    <style>
    .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .stButton > button {
        width: 100% !important;
        min-width: 0 !important;
        height: 92px !important;
        min-height: 92px !important;
        max-width: 92px !important;
        margin: 0 auto !important;
        font-size: 44px !important;
        font-weight: bold; border-radius: 2px; border: 2px solid #2f2f2f;
        background-color: #ffffff; color: black;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #f5f5f5;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }

    .stButton > button:focus-visible {
        outline: 3px solid rgba(47, 47, 47, 0.25);
        outline-offset: 2px;
    }
    
    .restart-button > button {
        width: 100% !important; max-width: 260px !important;
        height: 48px !important; min-height: 48px !important;
        margin: 20px auto 0 auto !important;
        font-size: 16px !important;
        font-weight: bold; border-radius: 2px; border: 2px solid #2f2f2f;
        background-color: #4CAF50; color: white;
    }

    .restart-button > button:hover {
        background-color: #43a047;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(67, 160, 71, 0.18);
    }

    .restart-button > button:focus-visible {
        outline: 3px solid rgba(67, 160, 71, 0.25);
        outline-offset: 2px;
    }
    
    /* Cabeçalhos de Status com as cores da Profª Silvia */
    .status-header { padding: 15px; border-radius: 4px; text-align: center; font-weight: bold; color: black; font-size: 20px; margin-bottom: 20px; }
    .tem-jogo { background-color: #C1E1C1; }         /* Verde */
    .possibilidade-fim { background-color: #B2D8E5; } /* Azul Claro */
    .empate { background-color: #E0E0E0; }            /* Cinza */
    .o-vence { background-color: #FFCC33; }           /* Amarelo/Laranja */
    .x-vence { background-color: #5DADE2; }           /* Azul */
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load('models/modelo_arvore_decisao.joblib')

modelo_ia = load_model()

if 'board' not in st.session_state:
    st.session_state.board = np.zeros(9).astype(int) 
    st.session_state.score = {"Acertos": 0, "Erros": 0}
    st.session_state.game_over = False
    st.session_state.round_counted = False


def check_winner(board):
    """Verifica o estado real das regras do jogo"""
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != 0:
            return "X vence" if board[line[0]] == 1 else "O vence"
    if np.count_nonzero(board) == 9:
        return "Empate"
    return "Tem jogo"

def get_ia_status():
    """Lógica com a trava para 'Possibilidade de Fim de Jogo'"""
    input_ia = st.session_state.board.reshape(1, -1)
    ia_pred = modelo_ia.predict(input_ia)[0]
    real_stat = check_winner(st.session_state.board)
    
    if "vence" in ia_pred and real_stat == "Tem jogo":
        return "Possibilidade de Fim de Jogo"
    
    if ia_pred == "Tem jogo" and real_stat != "Tem jogo":
        return real_stat
        
    return ia_pred

def robo_move():
    vazios = [i for i, x in enumerate(st.session_state.board) if x == 0]
    if vazios:
        move = random.choice(vazios)
        st.session_state.board[move] = -1 


st.markdown("<h1 style='text-align:center; margin-bottom: 0.8rem;'>Tic-Tac-Toe IA Classifier</h1>", unsafe_allow_html=True)

ia_status = get_ia_status()
real_status = check_winner(st.session_state.board)

status_map = {
    "Tem jogo": "tem-jogo",
    "Possibilidade de Fim de Jogo": "possibilidade-fim",
    "Empate": "empate",
    "O vence": "o-vence",
    "X vence": "x-vence"
}

status_class = status_map.get(ia_status, "tem-jogo")
st.markdown(f'<div class="status-header {status_class}">IA PREVÊ: {ia_status.upper()}</div>', unsafe_allow_html=True)

if not st.session_state.round_counted:
    if real_status in ["X vence", "O vence", "Empate"]:
        if real_status == ia_status:
            st.session_state.score["Acertos"] += 1
            st.success(f" ACERTO! IA identificou {real_status} corretamente.")
        else:
            st.session_state.score["Erros"] += 1
            st.error(f"ERRO! O jogo {real_status.lower()}, mas a IA previu {ia_status}.")
        st.session_state.round_counted = True
        st.session_state.game_over = True

score_left, score_spacer, score_right = st.columns([1, 0.3, 1])
score_left.metric("Acertos", st.session_state.score["Acertos"])
score_right.metric("Erros", st.session_state.score["Erros"])

st.markdown("<div style='max-width: 310px; margin: 0 auto;'>", unsafe_allow_html=True)
for row in range(3):
    cols = st.columns([1, 1, 1], gap="small")
    for col in range(3):
        idx = row * 3 + col
        val = st.session_state.board[idx]
        label = "X" if val == 1 else ("O" if val == -1 else " ")
        
        if cols[col].button(label, key=f"btn_{idx}", disabled=st.session_state.game_over):
            if val == 0:
                st.session_state.board[idx] = 1 # Humano
                if check_winner(st.session_state.board) == "Tem jogo":
                    robo_move()
                st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

col_restart = st.columns([1])[0]
with col_restart:
    st.markdown('<div class="restart-button">', unsafe_allow_html=True)
    if st.button("Reiniciar Jogo", use_container_width=True):
        st.session_state.board = np.zeros(9).astype(int)
        st.session_state.game_over = False
        st.session_state.round_counted = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

