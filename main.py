import re
import nltk
import pylab
import numpy

from nltk.corpus import stopwords
from matplotlib import pyplot
from pandas import Series
from wordcloud import WordCloud
from PIL import Image

stopwords = stopwords.words('spanish')

def leer_documento(ruta):

    # Abrir archivo en formato utf-8
    archivo = open(ruta, 'r', encoding='utf-8')

    # Leer el contenido del archivo
    documento = archivo.read()

    # Cerrar el archivo
    archivo.close()

    # Reemplazar todos los caracteres distintos de a-z, À-ÿ, espacios o saltos de línea por ''
    caracteres = re.compile('[^a-zÀ-ÿ \n\r]', re.IGNORECASE)
    documento = caracteres.sub('', documento)

    # Reemplazar los saltos de línea o múltiples espacios, por un único espacio
    espacios = re.compile('[\n\r]+|\s\s+')
    documento = espacios.sub(' ', documento)
    documento = documento.lower().split()

    # Filtra el contenido por palabras de importancia
    documento = [palabra for palabra in documento if palabra not in stopwords]

    return documento

def calcular_frecuencia(documento, palabras):

    # Cuenta las apariciones de cada palabra en el documento
    distribucion = {}
    for palabra in palabras:
        distribucion[palabra] = documento.count(palabra)

    return distribucion

def diagramar_frecuencias(frecuencias, nombre):

    # Definir los valores a diagramar
    datos_x = list()
    for palabra in frecuencias:
        datos_x.append(frecuencias[palabra])
    x_series = Series.from_array(datos_x)

    # Generar imagen
    imagen = pyplot.figure()
    grafico = x_series.plot(kind='bar')

    # Definir título y etiquetas
    grafico.set_title(nombre)
    grafico.set_xlabel('Palabra')
    grafico.set_ylabel('Frecuencia')
    grafico.set_xticklabels(frecuencias)

    # Guardar imagen
    pyplot.savefig('imágenes/{}.png'.format(nombre), bbox_inches='tight')
    pyplot.close(imagen)

def diagramar_dispersion(documento, palabras, nombre):

    # Obtener los puntos a diagramar
    texto = list(nltk.Text(documento))
    puntos = [(x, y) for x in range(len(texto))
              for y in range(len(palabras))
              if texto[x] == palabras[y]]
    if puntos:
        x, y = list(zip(*puntos))
    else:
        x = y = ()

    # Generar imagen
    pylab.plot(x, y, "b|", scalex=.1)
    pylab.yticks(list(range(len(palabras))), palabras, color="b")
    pylab.ylim(-1, len(palabras))

    # Definir título y etiquetas
    pylab.title(nombre)
    pylab.xlabel("Dispersión")

    # Guardar imagen
    pylab.savefig('imágenes/{}.png'.format(nombre), bbox_inches='tight')
    pylab.close('all')

def wordcloud(frecuencias, nombre):

    # Definir la imagen a generar
    mask = numpy.array(Image.open('mapa.jpg'))
    wc = WordCloud(background_color="white", mask=mask)

    # Remover las palabras sin frecuencia
    palabras = {}
    for palabra in frecuencias:
        if frecuencias[palabra] != 0:
            palabras[palabra] = frecuencias[palabra]
        else:
            palabras[palabra] = 1

    # Generar imagen
    wc.generate_from_frequencies(palabras)

    # Guardar imagen
    wc.to_file('imágenes/{}.png'.format(nombre))

    return

# Abrir documentos como una lista de palabras
constitucion_1886_documento = leer_documento('Constituciones/Constitución 1886.txt');
constitucion_1991_documento = leer_documento('Constituciones/Constitución 1991.txt');

# Abrir archivo de palabras, leyendo línea por línea

numero_linea = 1
constitucion_1886_frecuencia_total = {}
constitucion_1991_frecuencia_total = {}

with open('palabras.txt', 'r', encoding='utf-8') as archivo:
    for linea in archivo:
        palabras = linea.split()

        # Calcular la frecuencia de las palabras en los documentos
        constitucion_1886_frecuencia = calcular_frecuencia(constitucion_1886_documento, palabras)
        constitucion_1991_frecuencia = calcular_frecuencia(constitucion_1991_documento, palabras)

        # Almacenar las palabras
        constitucion_1886_frecuencia_total = {**constitucion_1886_frecuencia_total, **constitucion_1886_frecuencia}
        constitucion_1991_frecuencia_total = {**constitucion_1991_frecuencia_total, **constitucion_1991_frecuencia}

        # Generar gráficos de frecuencias
        diagramar_frecuencias(constitucion_1886_frecuencia, 'Constitución 1886 - Frecuencias - {}'.format(numero_linea))
        diagramar_frecuencias(constitucion_1991_frecuencia, 'Constitución 1991 - Frecuencias - {}'.format(numero_linea))

        # Generar gráficos de dispersión
        diagramar_dispersion(constitucion_1886_documento, palabras, 'Constitución 1886 - Dispesión - {}'.format(numero_linea))
        diagramar_dispersion(constitucion_1991_documento, palabras, 'Constitución 1991 - Dispesión - {}'.format(numero_linea))

        numero_linea += 1

# Generar gráficas wordcloud de los documentos
wordcloud(constitucion_1886_frecuencia_total, 'Constitución 1886 - WordCloud')
wordcloud(constitucion_1991_frecuencia_total, 'Constitución 1991 - WordCloud')
