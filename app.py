import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuración da páxina (sidebar colapsado por defecto)
st.set_page_config(
    page_title="Pensas por ti ou segues o que se espera de ti?",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Ficheiro CSV para persistencia local de resultados
DATA_FILE = "resultados_corresponsables.csv"


def init_csv():
  if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["timestamp", "genero", "puntuacion", "perfil"])
    df.to_csv(DATA_FILE, index=False)


init_csv()


# Función para mostrar os tres logos centrados na parte inferior
def mostrar_logos():
  logos = ["logo1.png", "logo2.png", "logo3.png"]
  existentes = [l for l in logos if os.path.exists(l)]

  if existentes:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    cols = st.columns(len(existentes))
    for i, logo in enumerate(existentes):
      with cols[i]:
        st.image(logo, use_container_width=True)


# Definición de preguntas e perfís
QUESTIONS = [
    {
        "q": (
            'Se alguén di: "Iso é de rapazas" ou "Os rapaces non choran", que'
            " pensas?"
        ),
        "a": [
            "Paréceme normal. Cada persoa ten o seu papel.",
            "Nunca o pensei moito. Escoítase dicir a miúdo.",
            "Faime dubidar un pouco, pero non sei moi ben que pensar.",
            (
                "Non estou de acordo. Chorar ou emocionarse é algo normal en"
                " calquera persoa."
            ),
        ],
    },
    {
        "q": (
            "Hai que organizar un plan ou recoller despois dunha festa. Como se"
            " reparten as tarefas?"
        ),
        "a": [
            "Os rapaces poden facer o máis pesado e as rapazas recollen.",
            "Repartímolo, pero ao final as rapazas adoitan facer máis.",
            (
                "Intentamos repartir todo entre todos, aínda que ás veces non"
                " sae perfecto."
            ),
            "Axuda quen poida. Non depende de ser rapaz ou rapaza.",
        ],
    },
    {
        "q": (
            "Un compañeiro ou compañeira rompe a chorar porque está mal. Que"
            " fas?"
        ),
        "a": [
            "Creo que debería aguantar máis.",
            "Déixoo tranquilo, síntome incómodo/a.",
            "Paréceme ben que chore, aínda que me resulta algo raro.",
            "Achégome a el ou ela e intento axudarlle.",
        ],
    },
    {
        "q": (
            "Cando coñeces a alguén por primeira vez, que importancia ten para"
            " ti saber se é rapaz ou rapaza?"
        ),
        "a": [
            (
                "É moi importante, porque penso que iso xa me di moitas cousas"
                " desa persoa."
            ),
            "É bastante importante, aínda que tamén miro outras cousas.",
            "Ten pouca importancia; prefiro coñecer á persoa antes de opinar.",
            (
                "Non ten importancia; fíxome en como é e en como trata aos"
                " demais."
            ),
        ],
    },
    {
        "q": "A valentía e a sensibilidade son cousas de rapaces ou de rapazas?",
        "a": [
            (
                "Si. A valentía é máis de rapaces e a sensibilidade máis de"
                " rapazas."
            ),
            "Creo que normalmente é así.",
            (
                "Todos podemos ter as dúas cousas, aínda que a sociedade ás"
                " veces nos separa."
            ),
            "Son cualidades de todas as persoas.",
        ],
    },
    {
        "q": (
            "Un compañeiro decide coidar máis a súa imaxe, usar cremas ou"
            " depilarse. Que opinas?"
        ),
        "a": [
            "Paréceme raro.",
            "É cousa súa, pero tampouco me gusta demasiado.",
            "Paréceme ben, aínda que me sorprende un pouco.",
            (
                "Cada persoa debe poder coidarse como queira sen que a"
                " xulguen."
            ),
        ],
    },
    {
        "q": (
            "Cres que tes que cambiar a túa forma de ser para encaixar ou"
            " gustar aos demais?"
        ),
        "a": [
            "Si. Hai que facer o que se espera de ti.",
            "Ás veces sinto que teño que cambiar para encaixar.",
            (
                "Intento ser eu mesmo/a, aínda que ás veces me preocupa o que"
                " pensen."
            ),
            "Prefiro ser eu mesmo/a antes que finxir.",
        ],
    },
    {
        "q": "Ves unha rapaza mecánica ou un rapaz bailarín. Que pensas?",
        "a": [
            "Paréceme raro.",
            "Sorpréndeme un pouco.",
            (
                "Paréceme ben. Gustaríame que todo o mundo puidese facer o que"
                " lle gusta."
            ),
            "Encántame ver persoas que fan o que realmente lles gusta.",
        ],
    },
    {
        "q": "Hai persoas que mostran moito as súas emocións. Que che parece?",
        "a": [
            "Exaxeran demasiado.",
            "Ás veces cansa un pouco.",
            "É a súa forma de ser, aínda que ás veces me sorprende.",
            "Paréceme moi ben que a xente poida expresar o que sente.",
        ],
    },
    {
        "q": "Cres que o teu futuro depende de ser rapaz ou rapaza?",
        "a": [
            "Si. Hai cousas para rapaces e outras para rapazas.",
            "É difícil escapar do que a sociedade espera.",
            "Intento que non sexa así, aínda que non sempre é fácil.",
            "O meu futuro depende das miñas decisións, non do meu sexo.",
        ],
    },
    {
        "q": 'É verdade que as rapazas son "máis maduras"?',
        "a": [
            "Si. Son así por natureza.",
            "Pode ser, porque viven experiencias diferentes.",
            "Creo que depende de cada persoa.",
            "É unha etiqueta que fai dano tanto aos rapaces coma ás rapazas.",
        ],
    },
    {
        "q": "Cando te equivocas, pides perdón?",
        "a": [
            "Non. Iso faime parecer débil.",
            "Cústame moito pedir perdón.",
            "Ás veces cústame, pero inténtoo.",
            "Pedir perdón cando me equivoco é algo importante.",
        ],
    },
    {
        "q": (
            "Nun anuncio de produtos de limpeza só aparecen mulleres. Que"
            " pensas?"
        ),
        "a": [
            "É normal.",
            "Non lle dou importancia.",
            "É un estereotipo ao que estamos afeitos.",
            "Ese tipo de anuncios xa non representan a realidade.",
        ],
    },
    {
        "q": "Alguén fai un comentario machista no grupo. Que fas?",
        "a": [
            "Río para non quedar mal.",
            "Non digo nada e sigo co meu.",
            "Dígolle con educación que ese comentario sobra.",
            "Explícolle con calma por que ese comentario non está ben.",
        ],
    },
    {
        "q": "Para ti, como é unha persoa ideal?",
        "a": [
            "Alguén que fai o que se espera dun rapaz ou dunha rapaza.",
            "Alguén educado que sempre fai o correcto.",
            "Alguén con bos valores, aínda que ás veces se equivoque.",
            "Alguén que é fiel a si mesmo/a e respecta aos demais.",
        ],
    },
]

RESULTS = [
    {
        "max": 15,
        "title": "Modo automático",
        "sub": "Estás moi influído/a polos estereotipos",
        "body": (
            "As túas respostas indican que moitas das ideas tradicionais sobre"
            ' como deben ser os rapaces e as rapazas seguen presentes na túa'
            ' forma de pensar. Isto non significa que estea "mal", xa que todas'
            " as persoas aprendemos estas ideas desde pequenos a través da"
            " familia, da escola, da televisión, das redes sociais ou dos"
            " amigos.<br><br>Agora que as coñeces, podes empezar a"
            " preguntarte:<br>• ¿Penso isto porque realmente o creo ou porque"
            " sempre mo dixeron?<br>• ¿Trato igual ás persoas independentemente"
            " de que sexan rapaces ou rapazas?<br>• ¿Respecto que cada persoa"
            " sexa como queira?<br><br><strong>Lembra</strong>: cuestionar os"
            " estereotipos é o primeiro paso para construír unha sociedade"
            " máis xusta e respectuosa."
        ),
    },
    {
        "max": 30,
        "title": "Estás no camiño",
        "sub": "Estás aprendendo a pensar con máis liberdade",
        "body": (
            "As túas respostas mostran que xa cuestionas moitas ideas"
            " tradicionais, aínda que algunhas seguen influíndo na túa forma de"
            " pensar ou actuar. É algo completamente normal, porque cambiar a"
            " maneira de ver o mundo leva"
            " tempo.<br><br><strong>Probablemente</strong>:<br>• Respectes"
            " bastante ás persoas aínda que sexan diferentes.<br>• Ás veces"
            " detectes comentarios ou situacións inxustas.<br>• En ocasións"
            " aínda sintas presión por facer o que os demais esperan de"
            " ti.<br><br>Segue facendo preguntas, escoitando outras opinións e"
            " reflexionando. Cada vez que pensas por ti mesmo/a, estás dando un"
            " paso cara a unha maior igualdade."
        ),
    },
    {
        "max": 45,
        "title": "Persoa libre",
        "sub": "Pensas de forma crítica e respectuosa",
        "body": (
            "As túas respostas indican que valoras ás persoas polo que son e"
            " non polos estereotipos relacionados co seu xénero. Entendes que"
            " cada persoa ten dereito a decidir como vestir, que lle gusta,"
            " como expresar as súas emocións ou que profesión"
            " elixir.<br><br>Isto significa que:<br>• Respectas a"
            " diversidade.<br>• Non cres que existan cousas \"de rapaces\" ou"
            ' "de rapazas".<br>• Comprendes que todas as persoas teñen as'
            " mesmas oportunidades e dereitos.<br>• Axudas a crear un ambiente"
            " no que os demais poden sentirse aceptados e seguros sendo eles"
            " mesmos.<br><br>Ser unha persoa crítica tamén significa seguir"
            " aprendendo, porque todos e todas podemos descubrir prexuízos que"
            " non sabiamos que tiñamos."
        ),
    },
]

# Menú lateral
st.sidebar.title("Navegación")
modo = st.sidebar.radio("Elixir vista", ["Facer o Test", "Panel de Control (N)"])

if modo == "Facer o Test":
  st.markdown(
      "<h1 style='color: #cf202e; text-align: center;'>Pensas por ti ou"
      " segues o que se espera de ti?</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; font-weight: bold;'>TEST do Programa"
      " “Corresponsables”</p>",
      unsafe_allow_html=True,
  )

  if "step" not in st.session_state:
    st.session_state.step = "intro"
  if "genero" not in st.session_state:
    st.session_state.genero = "Home"
  if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(QUESTIONS)
  if "current_q" not in st.session_state:
    st.session_state.current_q = 0

  if st.session_state.step == "intro":
    st.info(
        "Desde pequenos e pequenas escoitamos moitas mensaxes sobre como"
        ' "deberían" ser os rapaces e as rapazas: como vestir, que lles ten que'
        " gustar, como comportarse ou mesmo como sentir.\n\nEste cuestionario"
        " serve para pensar se esas ideas inflúen na túa forma de ver ás"
        " persoas e de actuar.\n\n**Non hai respostas boas nin malas.** O"
        " importante é responder con sinceridade."
    )

    st.session_state.genero = st.selectbox(
        "Indica o teu xénero:", ["Home", "Muller", "Non binario"]
    )

    if st.button("Comezar o test", type="primary"):
      st.session_state.step = "quiz"
      st.session_state.current_q = 0
      st.session_state.answers = [None] * len(QUESTIONS)
      st.rerun()

  elif st.session_state.step == "quiz":
    q_idx = st.session_state.current_q
    total = len(QUESTIONS)

    st.progress((q_idx + 1) / total)
    st.write(f"**Pregunta {q_idx + 1} de {total}**")

    item = QUESTIONS[q_idx]
    st.subheader(item["q"])

    selected_option = st.radio(
        "Escolle unha opción:",
        options=range(len(item["a"])),
        format_func=lambda x: item["a"][x],
        index=(
            st.session_state.answers[q_idx]
            if st.session_state.answers[q_idx] is not None
            else 0
        ),
        key=f"q_{q_idx}",
    )

    st.session_state.answers[q_idx] = selected_option

    col1, col2 = st.columns(2)
    with col1:
      if q_idx > 0:
        if st.button("← Anterior"):
          st.session_state.current_q -= 1
          st.rerun()
    with col2:
      if q_idx < total - 1:
        if st.button("Seguinte →", type="primary"):
          st.session_state.current_q += 1
          st.rerun()
      else:
        if st.button("Ver o resultado", type="primary"):
          score = sum(st.session_state.answers)
          tier = next(r for r in RESULTS if score <= r["max"])
          new_row = pd.DataFrame([{
              "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "genero": st.session_state.genero,
              "puntuacion": score,
              "perfil": tier["title"],
          }])
          df_existing = pd.read_csv(DATA_FILE)
          df_updated = pd.concat([df_existing, new_row], ignore_index=True)
          df_updated.to_csv(DATA_FILE, index=False)

          st.session_state.step = "result"
          st.rerun()

  elif st.session_state.step == "result":
    score = sum(st.session_state.answers)
    tier = next(r for r in RESULTS if score <= r["max"])

    st.markdown(f"### A túa puntuación: {score} de {len(QUESTIONS)*3} puntos")
    st.markdown(f"<h2 style='color: #cf202e;'>{tier['title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"**{tier['sub']}**")
    st.markdown(tier["body"], unsafe_allow_html=True)

    st.write("")
    if st.button("Repetir o test"):
      st.session_state.step = "intro"
      st.session_state.answers = [None] * len(QUESTIONS)
      st.session_state.current_q = 0
      st.rerun()

elif modo == "Panel de Control (N)":
  st.title("Panel de Control - Corresponsables")

  PASSWORD_SECRETA = "corresponsables2026"
  password_ingresada = st.text_input(
      "Introduce o contrasinal de acceso:", type="password"
  )

  if password_ingresada == PASSWORD_SECRETA:
    st.success("Acceso concedido.")
    st.write("Vista interna de rexistro de participación e xénero.")

    if os.path.exists(DATA_FILE):
      df = pd.read_csv(DATA_FILE)
      st.metric(label="Total de Enquisas Realizadas (N)", value=len(df))

      if not df.empty:
        # Gráfico de Xénero
        st.subheader("Desglose por Xénero")
        genero_counts = df["genero"].value_counts()
        st.bar_chart(genero_counts)

        # Gráfico de Perfís Académicos/Resultados (Novo)
        st.subheader("Desglose por Perfil Obtido")
        perfil_counts = df["perfil"].value_counts()
        st.bar_chart(perfil_counts)

        st.subheader("Detalle de Rexistros")
        st.dataframe(df)

        # Botón para borrar/limpar todos os rexistros de proba (Novo)
        st.markdown("---")
        if st.button("🗑️ Borrar todos os rexistros (Reiniciar datos)"):
          df_vacio = pd.DataFrame(
              columns=["timestamp", "genero", "puntuacion", "perfil"]
          )
          df_vacio.to_csv(DATA_FILE, index=False)
          st.success("Elimináronse todos os rexistros correctamente.")
          st.rerun()

      else:
        st.info("Aínda non hai rexistros gardados.")
    else:
      st.info("Aínda non existe o ficheiro de datos.")

  elif password_ingresada != "":
    st.error("Contrasinal incorrecto.")

# Mostrar os tres logos centrados na parte inferior
mostrar_logos()
