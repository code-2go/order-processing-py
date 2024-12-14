import PyPDF2
import pandas as pd
import re


file_path = r"C:\Users\b_gur\OneDrive\Documentos\order-processing-py\pdfs\pdfexample.pdf"

def normalize_line(line):
    line = re.sub(r'(\d+\.?\d*)\s*R\$', r'R$ \1' , line)
    return line

def extract_pdf(path):
    data = {
        "Cliente": None,
        "Data": None,
        "Produtos": []
    }
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() 

    if not data["Cliente"] or not data["Data"]:
                match_cliente = re.search(r"Cliente:\s*(.+?)\s+\d{2}/\d{2}/\d{4}", text)
                match_data = re.search(r"\d{2}/\d{2}/\d{4}", text)
                if match_cliente:
                    data["Cliente"] = match_cliente.group(1).strip()
                if match_data:
                    data["Data"] = match_data.group(0)  


    lines = text.split("\n")     
    for line in lines:
        line = normalize_line(line)
        print(f"Processando linha: {line}")
        # Regex ajustado para capturar código, IPI, quantidade, e valores
        match_product = re.match(
            r"(\S+)\s+(\d+)\s+R\$ ([\d.,]+)\s+R\$ ([\d.,]+)\s+R\$ ([\d.,]+)", 
            line
        )
        if match_product:
            produto = {
                "Código": match_product.group(1),
                "Qt": match_product.group(2),
                "Valor s/Impostos": match_product.group(3),
                "IPI": match_product.group(4)
            }
            data["Produtos"].append(produto)

    return data

dados = extract_pdf(file_path)
print(dados)

df = pd.DataFrame(dados)
print(df)