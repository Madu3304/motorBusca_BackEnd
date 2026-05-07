from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2

app = FastAPI()

app.add_middleware( #liga com o front
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def metodosubstringsearch(content, palavra):
    #metodo simples, seguindo o da sala de aula. 
    
    n = len(content)
    m = len(palavra)

    for i in range(0, n - m + 1):
        j = 0
        
        while (j < m and content[i + j] == palavra[j]):
            j += 1
        
        if j == m:
            return i
        
    return -1

@app.post("/search")
async def search(
    file: UploadFile = File(...),
    keyword: str = Form(...),
    algorithm: str = Form(...)
):

    texto = ""

    if file.filename.endswith(".txt"):

        conteudo = await file.read()
        texto = conteudo.decode("utf-8")

    elif file.filename.endswith(".pdf"):

        pdf = PyPDF2.PdfReader(file.file)

        for pagina in pdf.pages:

            if pagina.extract_text():
                texto += pagina.extract_text()

        if algorithm == "naive":
            resultado = metodosubstringsearch(texto, keyword)

        elif algorithm == "kmp":
        
            elif algorithm == "boyer":

    resultado = boyer_moore(texto, keyword)

    if resultado != -1:

        trecho = texto[resultado:resultado + 100]

        return {
            "matches": [trecho]
        }

    return {
        "matches": []
    }