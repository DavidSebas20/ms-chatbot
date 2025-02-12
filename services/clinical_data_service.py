import requests
from config import URL

def get_exams(patient_id: int):
    url = f"http://{URL}/exams/by-patient/?patient_id={patient_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching exams: {response.status_code}")

def get_prescriptions(patient_id: int):
    url = f"http://{URL}/graphql"
    query = """
    {
        searchPrescriptions(patient_id: "%s") {
            prescription_id
            patient_id
            doctor_id
            medication
            dosage
            notes
        }
    }
    """ % patient_id
    response = requests.post(url, json={"query": query})
    if response.status_code == 200:
        return response.json().get("data", {}).get("searchPrescriptions", [])
    else:
        raise Exception(f"Error fetching prescriptions: {response.status_code}")

def get_clinical_history(patient_id: int):
    url = f"http://{URL}/clinical-history/{patient_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching clinical history: {response.status_code}")

def build_context(patient_id: int):
    """
    Build a context string with the patient's clinical data.
    """
    try:
        exams = get_exams(patient_id)
        prescriptions = get_prescriptions(patient_id)
        clinical_history = get_clinical_history(patient_id)

        context = {
            "exams": exams,
            "prescriptions": prescriptions,
            "clinical_history": clinical_history
        }

        context_text = (
            f"Exámenes médicos: {exams}\n"
            f"Prescripciones: {prescriptions}\n"
            f"Historial clínico: {clinical_history}"
        )

        return context_text
    except Exception as e:
        raise Exception(f"No se pudo recuperar el contexto clínico: {str(e)}")