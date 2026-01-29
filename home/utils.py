
from PyPDF2 import PdfReader
import re

def extract_results_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    
    pattern = re.compile(
        r"(\d{6})"                       
        r"(?:\s*[\(\{])?"                  
        r"((?:\s*gpa\d+:\s*[\w\.]+,?)*)"  
        , re.IGNORECASE
    )

    data = []

    for page in reader.pages:
        text = page.extract_text() or ""
        for m in pattern.finditer(text):
            roll = int(m.group(1))
            gpas_text = m.group(2)

            gpas = {}
            if gpas_text:
            
                for g in re.finditer(r"gpa(\d+):\s*([\w\.]+)", gpas_text, re.IGNORECASE):
                    key, value = g.groups()
                    cleaned_value = "ref" if value.strip().lower() in ["-", "ref"] else value
                    gpas[f"gpa{key}"] = cleaned_value
                    
            data.append({
                "roll": roll,
                **gpas
            })

    return data


