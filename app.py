
import streamlit as st

# Personalizzazioni CSS

st.markdown(
    """
    <style>
    /* 1. IMPORTA IL FONT MONTSERRAT */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

    .stApp {

        /* *** IMMAGINE DI SFONDO *** */
        background-image: url("BG1.jpg"); /* Assicurati che BG1.jpg sia nella stessa cartella di app.py o fornisci il percorso corretto */
        background-size: cover; /* Copre l'intera area disponibile */
        background-repeat: no-repeat; /* Evita la ripetizione dell'immagine */
        background-position: center; /* Centra l'immagine */
        background-attachment: fixed; /* L'immagine di sfondo rimane fissa durante lo scorrimento */
        /* background-color: #FFFFE0; Commentato o rimosso se l'immagine copre tutto e non serve un colore di fallback visibile */
        color: #191970;

        /* *** AGGIUNGI QUI IL BORDO PER LA CORNICE ESTERNA *** */
        border: 5mm solid #191970 !important; /* Bordo blu di 5mm */
        box-sizing: border-box; /* Include padding e border nella larghezza/altezza totale */
        /* Per avere un po' di spazio tra il bordo e il contenuto */
        padding: 10px; /* Aggiungi un po' di padding interno se vuoi che il contenuto non tocchi il bordo */

    }
/* *** NUOVO CURSORE GLOBALE *** */
    * {
        cursor: url(https://cur.cursors-4u.net/food/foo-5/foo441.cur), auto !important;
    }

    /*Sito da cui prendere il cursore https://www.cursors-4u.com/cursor/2010/11/04/tomato.html*/

    /* Stile per l'input di testo (la casella della domanda) */
    .stTextInput > div > div > input {
        border: 4px solid #191970; /* Bordo blu */
        border-radius: 10px; /* Bordi arrotondati */
        padding: 10px 15px; /* Spazio interno */
        font-size: 16px; /* Dimensione del font */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombra leggera */
    }

    /* Questo scritto sotto mi è servito per ridurre la distanza tra h1 e h2, è une regola che si applica per far funzionare CSS*/
    /* Regola FONDAMENTALE per il contenitore generale dei titoli (h1 e h2) */
    /* Questo selettore mira al div che Streamlit usa per contenere st.title() e st.header() */
    div[data-testid="stHeader"] > div {
        display: flex; /* Attiva il layout Flexbox */
        flex-direction: column; /* Impila gli elementi figli (i tuoi h1 e h2) verticalmente */
        align-items: center; /* Centra gli elementi figli orizzontalmente all'interno del contenitore */
        width: 100%; /* Assicura che questo contenitore occupi tutta la larghezza disponibile */
    }

    h1 {
        color: #0056b3; /* Blu scuro per l'intestazione */
        text-align: center; /* Centra il testo */
        margin-bottom: 1px !important; /*Riduce la distanza sotto l'h1 */
        padding-bottom: 0px !important; /* Rimuove il padding inferiore predefinito dell'h1 */

        /* FONT */
        font-family: 'Montserrat', sans-serif; /* Applica il font Montserrat */
        font-size: 3.2em !important; /* Esempio: dimensione grande */
        font-weight: 900 !important; /* Esempio: extra grassetto */


    }

    /* Stile per l'intestazione "Parla con me!" (generata da st.header) */
    /* Stile per l'header del chatbot */


    h2 {
        color: #0056b3; /* Blu scuro per l'intestazione */
        text-align: center; /* Centra il testo */
        margin-top: 1px !important; /*Riduce la distanza sopra l'h2 */
        padding-top: 0px !important; /* Rimuove il padding superiore predefinito dell'h2 */
        padding-bottom: 20px !important; /* Spazio sotto il sottotitolo */

        /* FONT */
        font-family: 'Montserrat', sans-serif; /* Applica il font Montserrat */
        font-size: 2.5em !important; /* Esempio: dimensione grande del font */
        font-weight: 900 !important; /* Esempio: extra grassetto */

    }
/* Questo serve a modificare la scritta sopra la box dell'input */
    .input-question-text {
        color: #191970;
        font-family: 'Montserrat', sans-serif;
        font-size: 1.0em !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 0px !important; /* Spazio sotto il testo e sopra l'input */
        padding-bottom: 0px !important; /* Assicurati che non ci sia padding interno */
        line-height: 1.2 !important; /* Riduci l'altezza della riga per ridurre lo spazio verticale */
    }



    </style>
    """,
    unsafe_allow_html=True)







#chiave = st.secrets["superkey"]
chiave = "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"

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI

st.title("PARLA CON ME!")
st.header("IL CHATBOT DI CASA MORANA")

from PIL import Image
logo = Image.open("logocm.png")
#st.image(logo, width=200)
st.image(logo, use_container_width=True)

# with st.sidebar:
#  st.title("Carica i tuoi documenti")
#  file = st.file_uploader("Carica il tuo file", type="pdf")
file = "PDFCM.pdf"

from PyPDF2 import PdfReader

if file is not None:
    testo_letto = PdfReader(file)

    testo = ""
    for pagina in testo_letto.pages:
        testo = testo + pagina.extract_text()
        # st.write(testo)

    # Usiamo il text splitter di Langchain
    testo_spezzato = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000, # Numero di caratteri per chunk
        #chunk_overlap=150
        chunk_overlap=500,
        length_function=len
        )

    pezzi = testo_spezzato.split_text(testo)
    # st.write(pezzi)

    # Generazione embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=chiave)

    # Vector store - FAISS (by Facebook)
    vector_store = FAISS.from_texts(pezzi, embeddings)

# --------------------------------------------------
# Gestione prompt
# --------------------------------------------------

    def invia():
      st.session_state.domanda_inviata = st.session_state.domanda
      # salva il contenuto di input in domanda_inviata
      st.session_state.domanda = ""
      # reset dopo invio


    # Vogliamo che appaia sopra la casella di input in basso.
    # ORA USIAMO IL TAG <P> CON LA CLASSE CORRETTA
    st.markdown('<p class="input-question-text">QUALE POMOD... EMM... QUALE INFORMAZIONE TI SERVE?</p>', unsafe_allow_html=True)
    st.text_input("",key="domanda", on_change=invia)
    # key="domanda": assegna a st.session_state ciò che scriviamo (domanda)
    # Ogni volta che l’utente modifica il campo e preme Invio,
    # la funzione invia() viene chiamata.

    domanda = st.session_state.get("domanda_inviata", "")
    # Recupera il valore salvato in "domanda_inviata".
    # Se "domanda_inviata" non è ancora stato definito (es. al primo avvio dell'app),
    # allora il valore predefinito sarà "" (secondo argomento dell'istruzione)

# --------------------------------------------------

    if domanda:
      # st.write("Sto cercando le informazioni che mi hai richiesto...")
      rilevanti = vector_store.similarity_search(domanda)

      # Definiamo l'LLM
      llm = ChatOpenAI(
          openai_api_key = chiave,
          temperature = 1.0,
          #max_tokens = 1000,
          max_tokens = 2000,
          model_name = "gpt-3.5-turbo-0125")
      # https://platform.openai.com/docs/models/compare

      # Output
      # Chain: prendi la domanda, individua i frammenti rilevanti,
      # passali all'LLM, genera la risposta
      chain = load_qa_chain(llm, chain_type="stuff")
      risposta = chain.run(input_documents = rilevanti, question = domanda)
      st.write(risposta)

