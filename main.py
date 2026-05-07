from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import time
#openTele
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

app.add_middleware( #liga com o front
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FastAPIInstrumentor.instrument_app(app)

def metodosubstringsearch(content, palavra):
    #metodo simples, seguindo o da sala de aula. 
    
    n = len(content)
    m = len(palavra)

    ocorrencias = []

    for i in range(0, n - m + 1):

        j = 0

        while (j < m and content[i + j].lower() == palavra[j].lower()):
            j += 1

        if j == m:

            ocorrencias.append(i)

    return ocorrencias

@app.post("/search")
async def search(
    file: UploadFile = File(...),
    keyword: str = Form(...),
    algorithm: str = Form(...)
):

    texto = ""

    #txt
    if file.filename.endswith(".txt"):

        conteudo = await file.read()
        texto = conteudo.decode("utf-8")

    #pdf
    elif file.filename.endswith(".pdf"):

        pdf = PyPDF2.PdfReader(file.file)

        for pagina in pdf.pages:

            if pagina.extract_text():
                texto += pagina.extract_text()

    n = len(texto)
    m = len(keyword)

    if algorithm == "naive":
        with tracer.start_as_current_span("substring-search"):

                inicio = time.perf_counter()
        resultado = metodosubstringsearch(texto, keyword)

        fim = time.perf_counter()

        tempo_execucao = (fim - inicio) * 1000
        span = trace.get_current_span()

        span.set_attribute("algorithm", algorithm)
        span.set_attribute("text_size_n", n)
        span.set_attribute("pattern_size_m", m)
        span.set_attribute("occurrences", len(resultado))
        span.set_attribute("execution_time_ms", tempo_execucao)

    elif algorithm == "kmp":
        return {
            "found": False,
            "message": "KMP ainda não implementado",

            "occurrences": 0,
            "positions": [],
            "execution_time_ms": 0,

            "text_size_n": n,
            "pattern_size_m": m,

            "matches": []
    }

    elif algorithm == "boyer":

        return {
            "found": False,
            "message": "Boyer Moore ainda não implementado",

            "occurrences": 0,
            "positions": [],
            "execution_time_ms": 0,

            "text_size_n": n,
            "pattern_size_m": m,

            "matches": []
    }


    if len(resultado) > 0:

        trechos = []

        for posicao in resultado:

            inicio = max(0, posicao - 20)
            fim = min(len(texto), posicao + len(keyword) + 20)

            trecho = texto[inicio:fim]

            trechos.append(trecho)

        return {
            "found": True,
            "occurrences": len(resultado),
            "positions": resultado,
            "execution_time_ms": tempo_execucao,
            "text_size_n": n,
            "pattern_size_m": m,
            "matches": trechos
        }

    return {
        "found": True,
        "occurrences": 0,
        "positions": [],
        "execution_time_ms": tempo_execucao,
        "text_size_n": n,
        "pattern_size_m": m,
        "matches": []
    }
