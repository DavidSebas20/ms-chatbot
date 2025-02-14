from fastapi import FastAPI, HTTPException
from schemas.request_response import ChatRequest, ChatResponse
from services.openai_service import query_openai
from services.clinical_data_service import build_context
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Medical Chatbot",
    description="Un chatbot para consultar historiales clínicos utilizando la API de OpenAI.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        try:
            context = build_context(request.patient_id)
        except Exception as e:
            context = f"Advertencia: No se pudo recuperar el historial clínico del paciente. Error: {str(e)}"
        
        # Usar OpenAI para generar una respuesta
        answer = query_openai(context, request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

