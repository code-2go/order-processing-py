import os
import re
import pandas as pd
import pdfplumber

file_path = r'C:\Users\b_gur\OneDrive\Documentos\order-processing-py\pdfs\type-a\ORV Suporte Rei - Imperio dos freios 12dez.pdf'

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

            if not data["Cliente"] or not data["Data"]:
                match_cliente = re.search(r"Cliente:\s*(.+?)\s+\d{2}/\d{2}/\d{4}", text)
                match_data = re.search(r"\d{2}/\d{2}/\d{4}", text)
                if match_cliente:
                    data["Cliente"] = match_cliente.group(1).strip()
                if match_data:
                    data["Data"] = match_data.group(0)

            lines = text.split("\n")
            for line in lines:
                match_product = re.match(r"(\S+)\s+\d+%?\s+\d+\s+\d+\s+R\$ ([\d,.]+)\s+R\$ ([\d,.]+)\s+R\$ ([\d,.]+)", line)
                if match_product:
                    produto = {
                        "Código": match_product.group(1),
                        "Qt": match_product.group(3),
                        "Valor s/Impostos": match_product.group(4),
                        "IPI": match_product.group(5)
                    }
                    data["Produtos"].append(produto)
            
            # for page_num, page in enumerate(pdf.pages, start=1):
            #     text = page.extract_text()
            #     print(f"texto extraido - página {page_num}:")
            #     print(text)
            #     print("-"*80)

    return data

dados = extract_pdf(file_path)

print(dados)