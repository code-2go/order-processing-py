import os
import re
import pandas as pd
import pdfplumber

file_path = r'C:\Users\b_gur\OneDrive\Documentos\order-processing-py\pdfs\type-a\ORV Suporte Rei - Imperio dos freios 12dez.pdf'

def clean_text(text):
    # Remove espaços extras em valores monetários e normaliza os números
    text = re.sub(r"R\$ (\d+)\s,(\d+)", r"R$ \1,\2", text)
    text = re.sub(r"(\S+)(\d+\.\d+%)", r"\1 \2", text)
    text = re.sub(r"(\d+)\s(\d+)", r"\1\2", text)
    return text

def extract_pdf(path):
    data = {
        "Cliente": None,
        "Data": None,
        "Produtos": []
    }

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            text = " ".join(text.split())
            text = clean_text(text) 
            #print(f'texto processado: \n{text}\n {"-"*80}')

            if not data["Cliente"] or not data["Data"]:
                match_cliente = re.search(r"Cliente:\s*(.+?)\s+\d{2}/\d{2}/\d{4}", text)
                match_data = re.search(r"\d{2}/\d{2}/\d{4}", text)
                if match_cliente:
                    data["Cliente"] = match_cliente.group(1).strip()
                if match_data:
                    data["Data"] = match_data.group(0)

            #Processamento da tabela produtos
            lines = text.split("\n")
            
            for line in lines:
                print(f"Processando linha: {line}")
                # Regex ajustado para capturar código, IPI, quantidade, e valores
                match_product = re.match(
                    r"(\S+)\s+(\d+\.\d+%)\s+\d+\s+\d+\s+R\$ ([\d,.]+)\s+R\$ ([\d,.]+)\s+R\$ ([\d,.]+)", 
                    line
                )
                if match_product:
                    produto = {
                        "Código": match_product.group(1),
                        "IPI": match_product.group(2),
                        "Valor s/Impostos": f"R$ {match_product.group(3)}",
                        "Qt": f"{match_product.group(4)}",
                        "Total s/Impostos": f"R$ {match_product.group(5)}"
                    }
                    data["Produtos"].append(produto)
    return data


dados = extract_pdf(file_path)
df = pd.DataFrame(dados)
print(df)