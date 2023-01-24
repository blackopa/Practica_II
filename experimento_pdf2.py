
import re
from PyPDF2 import PdfReader
import tabula

# Read a PDF File
df = tabula.read_pdf("RBD 7707 - INFORME FINAL FASE 1 - ASESORÍA DISEÑO DE RED - AULAS CONECTADAS 2022.pdf", pages='all')[0]
# convert PDF into CSV
tabula.convert_into("RBD 7707 - INFORME FINAL FASE 1 - ASESORÍA DISEÑO DE RED - AULAS CONECTADAS 2022.pdf", "test.csv", output_format="csv", pages='all')
print(df)