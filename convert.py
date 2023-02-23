import pandas as pd
from xml.etree import ElementTree as ET
import os
import xhtml2pdf.pisa as pisa
from datetime import datetime

out_folder = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
os.mkdir(out_folder)

all_xml_files = [
    os.path.join(_, file_name) for _, subdirs, arquivos in os.walk('.')
    for file_name in arquivos if file_name.endswith('.xml')]

for file_path in all_xml_files:
    file_name = os.path.splitext(file_path)[0]
    tree = ET.parse(file_path)
    root = tree.getroot()

    dados = []

    for child in root.iter():
        tag = child.tag.split('}')[1]
        valor = child.text
        dados.append((tag, valor))
    df = pd.DataFrame(dados, columns=['tag', 'valor'])

    output_folder = os.path.join(out_folder, file_name)

    df.to_excel(output_folder + '.xlsx', index=False)

    html_string = df.to_html(index=False)
    with open(output_folder + '.pdf', "w+b") as f:
        pisa.CreatePDF(html_string, dest=f)
