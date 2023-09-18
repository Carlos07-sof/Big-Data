import folium
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
import io

df = pd.read_csv('new-york-city-art-galleries-1.csv')

df = df.drop_duplicates()

df = df.drop("ADDRESS2", axis=1)

df = df[(df['CITY'] == 'Brooklyn')]

df = df.sort_values(by='GRADING', ascending=False)

tres_calificados = df.head(3)

print(tres_calificados)

#GENERAR MAPA

m = folium.Map(location=[40.7037979,-74.0202391], zoom_start=13)

for index, row in tres_calificados.iterrows():
    name = row['NAME']
    address = row['ADDRESS1']
    lat, lon = map(float, row['the_geom'].replace('POINT (', '').replace(')', '').split())
    lat, lon = round(lon, 4), round(lat, 4)
    rating = row['GRADING']

    popup_text = f"Name: {name}<br>Address: {address} <br>Grade: {rating}"
    folium.Marker(location=[float(lat), float(lon)], popup=popup_text).add_to(m)

temp_html_file = 'temp_map.html'
m.save(temp_html_file)

img_data = m._to_png()
img = PILImage.open(io.BytesIO(img_data))
img.save('temp_map.png')

# Generar el informe PDF
doc = SimpleDocTemplate("informe_final.pdf", pagesize=letter)

styles = getSampleStyleSheet()
contenido = []

titulo = "The best Galleries and Museums\n"
contenido.append(Paragraph(titulo, styles["Title"]))

imagen_mapa = Image("temp_map.png", width=500, height=400)
contenido.append(imagen_mapa)

for index, row in tres_calificados.iterrows():
    name = row['NAME']
    address = row['ADDRESS1']
    rating = row['GRADING']

    # Crear un párrafo de texto con los datos
    texto_datos = f"Name: {name} Address: {address} Grade: {rating}"
    contenido.append(Paragraph(texto_datos, styles["Normal"]))

# Construir el informe y guardarlo en un archivo PDF
doc.build(contenido)

df.to_csv('NewFormat.csv', index=False)
