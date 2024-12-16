import PyPDF2
import pandas as pd
import re


file_path = r"C:\Users\b_gur\OneDrive\Documentos\order-processing-py\pdfs\type-a\ORV Suporte Rei - Imperio dos freios 12dez.pdf"

def normalize_line(line):
    line = re.sub(r'(\d+\.?\d*)\s*R\$', r'R$ \1' , line)
    return line

def extract_pdf(path):
    data = {
        "Cliente": None,
        "Data": None,
        "Fabricante": None,
        "Produtos": []
    }

    if 'type-a' in file_path:
        data['Fabricante'] = 'Suporte Rei'
    elif 'type-b' in file_path:
        data['Fabricante'] = 'Rei Auto Parts'
    elif 'type-c' in file_path:
        data['Fabricante'] = 'Della Rosa'
    else:
        data['Fabricante'] = 'Silpa'

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
        # Regex ajustado para capturar código, IPI, quantidade, e valores
        match_product = re.match(
            r"(\S+)\s+(\d+\.\d+%)\s+(\d+)\s+(\d+)\s+R\$ ([\d.,]+)\s+R\$ ([\d.,]+)\s", 
            line
        )
        if match_product:
            produto = {
                "Código": match_product.group(1),
                "Qt": match_product.group(4),
                "Valor s/Impostos": match_product.group(5),
                "IPI": match_product.group(6)
            }
            data["Produtos"].append(produto)
    return data

Data = extract_pdf(file_path)

df = pd.DataFrame(Data['Produtos'])
df['Cliente'] = Data['Cliente']
df['Data'] = Data['Data']
df['Fabricante'] = Data['Fabricante']

df = df[['Cliente', 'Data', 'Fabricante', 'Código', 'Qt', 'Valor s/Impostos', 'IPI']]

print(df)

save_path = rf'C:\Users\b_gur\OneDrive\Documentos\order-processing-py\staging\{Data["Fabricante"]}-{Data["Cliente"]}-{Data["Data"].replace('/','-')}.csv'

df.to_csv(save_path, index=False, encoding='utf-8-sig')




