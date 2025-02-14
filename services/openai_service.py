from openai import OpenAI
from config import OPENAI_API_KEY

# Crear una instancia del cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def query_openai(context: str, question: str) -> str:
    """
    Envía una solicitud a la API de OpenAI con el contexto y la pregunta.
    """
    try:
        prompt = f"Contexto:\n{context}\n\nPregunta:\n{question}\n\nRespuesta:"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente médico con inteligencia artificial llamado MediBot que responde preguntas basadas en un historial clínico y puede brindar recomendaciones."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        raise Exception(f"Error al interactuar con OpenAI: {str(e)}")