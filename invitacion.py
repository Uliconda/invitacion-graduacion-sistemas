import streamlit as st
import streamlit.components.v1 as components
import datetime
import pandas as pd
import base64
from PIL import Image
from io import BytesIO

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Graduación Sistemas CESBA",
    page_icon="💻", 
    layout="centered", 
    initial_sidebar_state="collapsed" 
)

# --- CONTROL DE MEMORIA (¡Para no repetir la animación!) ---
if 'primera_vez' not in st.session_state:
    st.session_state.primera_vez = True
    mostrar_animacion = True
else:
    mostrar_animacion = False

# --- VARIABLES PERSONALIZABLES ---
CARRERA = "Ingeniería en Sistemas Computacionales"
UNIVERSIDAD = "CESBA"
FECHA_EVENTO = datetime.datetime(2026, 6, 27, 18, 0, 0) 

# --- DATOS DE LA ORGANIZADORA (Enlace oculto) ---
# Pon aquí el nombre y teléfono real de la organizadora
ORGANIZADORA = {"nombre": "Mariana Hdz", "telefono": "524427474146"}

DIRECTORIO_GRADUADOS = {
    "melina": {"nombre": "Melina", "telefono": "524426024744"},
    "alejandra": {"nombre": "Alejandra", "telefono": "524421719459"},
    "adabella": {"nombre": "Adabella", "telefono": "527209086526"},
    "alan": {"nombre": "Alan", "telefono": "524425063652"},
    "brian": {"nombre": "Brian", "telefono": "524422812225"},
    "fernando": {"nombre": "Fernando", "telefono": "524423387097"},
    "roberto": {"nombre": "Roberto", "telefono": "524426578813"},
    "ulises": {"nombre": "Ulises", "telefono": "524426498849"}
}

LATITUD = 20.679033
LONGITUD = -100.462507
LUGAR_NOMBRE = "Salones La Concordia"
DIRECCION_TEXTO = "Carlos Salinas de Gortari 18, Jurica Pueblo, 76100 Santiago de Querétaro, Qro."

FOTOS_CARRUSEL = [
    "foto1.jpg", "foto2.jpg", "foto3.jpg", "foto4.jpeg", "foto5.jpeg", "foto6.jpeg", 
    "foto7.jpeg", "foto8.jpeg", "foto9.jpeg", "foto10.jpeg", "foto11.jpeg", "foto12.jpeg", 
    "foto13.jpeg", "foto14.jpeg", "foto15.jpeg", "foto16.jpeg", "foto17.jpeg", "foto18.jpeg", "foto19.jpeg"
] 

# --- FUNCIÓN PARA COMPRIMIR FOTOS (Evita que se trabe) ---
def obtener_base64_comprimido(ruta):
    try:
        img = Image.open(ruta)
        # Convertir a RGB por si hay PNGs con transparencia
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Reducimos tamaño (max 800px) para que sea súper ligero
        img.thumbnail((800, 800))
        buffered = BytesIO()
        # Guardamos en memoria con calidad 70% (imperceptible a la vista, excelente para rendimiento)
        img.save(buffered, format="JPEG", quality=70)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        return ""

# --- ESTILOS CSS GENERALES ---
st.markdown("""
    <style>
        .tarjeta-info {
            background: rgba(22, 27, 34, 0.8);
            border: 1px solid #30363D;
            border-left: 4px solid #00E5FF;
            padding: 20px;
            border-radius: 10px; text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 15px; color: #E5E7EB;
        }
        .tarjeta-info:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
            border-left: 4px solid #FFD700;
        }

        @keyframes pulseTech {
            0% { box-shadow: 0 0 0 0 rgba(0, 229, 255, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(0, 229, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 229, 255, 0); }
        }
        
        [data-testid="stAudio"] {
            position: fixed; bottom: 20px; right: 20px; z-index: 9999999;
            width: 280px; background: rgba(13, 17, 23, 0.9);
            border: 2px solid #00E5FF; border-radius: 40px;
            box-shadow: 0 0 15px rgba(0,229,255,0.4);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        [data-testid="stAudio"]:hover {
            transform: scale(1.05); box-shadow: 0 0 25px rgba(0,229,255,0.7);
        }
        [data-testid="stAudio"] audio { height: 40px; }
        header[data-testid="stHeader"], footer { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- PANTALLA DE CARGA ---
if mostrar_animacion:
    st.markdown("""
        <style>
            #pantalla-carga {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: #000000; z-index: 9999999; display: flex;
                flex-direction: column; justify-content: center; align-items: center;
                font-family: 'Courier New', Courier, monospace;
                animation: ocultarPantalla 1.5s ease-in-out forwards; animation-delay: 8s; 
                padding: 20px; box-sizing: border-box; transform: translateZ(0); 
            }
            .consola { width: 100%; max-width: 700px; color: #00FF41; text-align: left; font-size: clamp(0.75rem, 3.5vw, 1.3rem); line-height: 1.6;}
            .linea-codigo { white-space: pre-wrap; word-break: break-word; opacity: 0; animation: aparecerCodigo 0.5s ease-out forwards; margin-bottom: 5px; }
            .l1 { animation-delay: 1.0s; }
            .l2 { animation-delay: 2.5s; }
            .l3 { animation-delay: 4.0s; }
            .l4 { animation-delay: 5.5s; color: #00E5FF; font-weight: bold;}
            @keyframes aparecerCodigo { 0% { opacity: 0; transform: translate3d(0, 15px, 0); } 100% { opacity: 1; transform: translate3d(0, 0, 0); } }
            @keyframes ocultarPantalla { 0% { opacity: 1; visibility: visible; } 100% { opacity: 0; visibility: hidden; display: none; } }
        </style>
        <div id="pantalla-carga">
            <div class="consola">
                <div class="linea-codigo l1">> Iniciando sistema_graduacion.exe... [OK]</div>
                <div class="linea-codigo l2">> Cargando base de datos CESBA... [OK]</div>
                <div class="linea-codigo l3">> Compilando a los 8 Ingenieros... [OK]</div>
                <div class="linea-codigo l4">> STATUS: ÉXITO. Lanzando invitación_oficial... █</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #00E5FF; font-size: 2.8rem; margin-bottom: 0;">&lt; ¡Nos Graduamos! /&gt;</h1>
        <p style="font-size: 1.2rem; color: #8B949E; margin-top: 10px;">System.out.println("Los invitamos a nuestra celebración");</p>
        <h2 style="font-size: 1.6rem; margin-top: 10px; color: #FFD700;">{CARRERA}</h2>
        <p style="font-size: 1.2rem; font-weight: bold; color: #E5E7EB;">{UNIVERSIDAD}</p>
    </div>
""", unsafe_allow_html=True)

# --- MÚSICA ---
try:
    st.audio("musica.mp3", format="audio/mpeg", loop=True)
except FileNotFoundError:
    pass

# --- CUENTA REGRESIVA ---
st.markdown("<h3 style='text-align: center; color: #00E5FF;'>[ ⏳ Tiempo de Ejecución Restante ]</h3>", unsafe_allow_html=True)
ahora = datetime.datetime.now()
diferencia = FECHA_EVENTO - ahora

if diferencia.total_seconds() > 0:
    dias = diferencia.days
    horas, resto = divmod(diferencia.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    col1, col2, col3 = st.columns(3)
    estilo_card = '<div class="tarjeta-info"><h2 style="color:#00E5FF; margin:0; font-size:2rem;">{valor}</h2><p style="margin:0; color:#8B949E; font-weight:bold;">{etiqueta}</p></div>'
    col1.markdown(estilo_card.format(valor=dias, etiqueta="Días"), unsafe_allow_html=True)
    col2.markdown(estilo_card.format(valor=horas, etiqueta="Horas"), unsafe_allow_html=True)
    col3.markdown(estilo_card.format(valor=minutos, etiqueta="Minutos"), unsafe_allow_html=True)
else:
    st.success("¡EL SCRIPT HA FINALIZADO! EL DÍA LLEGÓ 🎉")

st.markdown("---")

# --- GENERACIÓN ---
st.markdown("<h3 style='text-align: center; color: #00E5FF;'>{ 👨‍💻 Array de Graduados }</h3>", unsafe_allow_html=True)
st.markdown("""
    <div class="tarjeta-info" style="text-align: left;">
        <p style="color: #8B949E; text-align: center;">/* 8 Ingenieros listos para deployar en producción */</p>
        <ul style="color: #E5E7EB; font-weight: 500; font-size: 1.1rem; line-height: 1.8; list-style-type: square;">
            <li>1. MELINA CRISTAL SANCHEZ HERNANDEZ</li>
            <li>2. ALEJANDRA VANEGAS URIBE</li>
            <li>3. ADABELLA VAZQUEZ CRUZ</li>
            <li>4. ALAN IEHOSHUA PRADO CASANOVA</li>
            <li>5. BRIAN OMAR ORTIZ GARCIA</li>
            <li>6. FERNANDO SAMAEL GARCIA RUBIO</li>
            <li>7. JOSE ROBERTO ESPINOZA SEGOVIA</li>
            <li>8. ULISES GONZÁLEZ HERNÁNDEZ</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- ITINERARIO ---
col_iti, col_vest = st.columns(2)
with col_iti:
    st.markdown('<div class="tarjeta-info"><h4 style="color:#FFD700; margin-top:0;">📋 def itinerario():</h4><p style="margin:5px 0; font-size:0.9rem;"><strong>18:00</strong> -> Recepción</p><p style="margin:5px 0; font-size:0.9rem;"><strong>20:00</strong> -> Cena_de_Gala()</p><p style="margin:5px 0; font-size:0.9rem;"><strong>21:30</strong> -> Brindis()</p><p style="margin:5px 0; font-size:0.9rem;"><strong>22:00</strong> -> while True: Bailar()</p></div>', unsafe_allow_html=True)
with col_vest:
    st.markdown('<div class="tarjeta-info"><h4 style="color:#FFD700; margin-top:0;">👔 css.DressCode</h4><p style="font-size:2rem; margin:10px 0;">✨</p><p style="margin:5px 0; font-weight:bold;">Formal / Etiqueta</p><p style="font-size:0.8rem; color:#8B949E;"># Que el outfit no tenga bugs.</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- CARRUSEL AUTOMÁTICO (SIN BOTONES Y SIN RECORTES) ---
st.markdown("<h3 style='text-align: center; color: #00E5FF;'># Nuestros Recuerdos</h3>", unsafe_allow_html=True)

# Creamos la estructura HTML y CSS para que las fotos pasen solas con animación
html_carousel = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; padding: 0; background-color: transparent; }
    .carrusel-contenedor {
        width: 100%; height: 450px; position: relative;
        background-color: #0D1117; border-radius: 15px;
        border: 1px solid #30363D; box-shadow: 0 8px 25px rgba(0,229,255,0.15);
        overflow: hidden; box-sizing: border-box;
    }
    .slide {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0; transition: opacity 1.5s ease-in-out; /* FADE SUAVE */
        display: flex; justify-content: center; align-items: center;
    }
    .slide.activa { opacity: 1; z-index: 2; }
    .slide img {
        max-width: 100%; max-height: 100%;
        object-fit: contain; /* ESTO EVITA QUE SE RECORTEN */
        border-radius: 15px;
    }
</style>
</head>
<body>
<div class="carrusel-contenedor">
"""

# Procesamos e insertamos cada imagen de forma segura y ligera
es_primera = True
for foto in FOTOS_CARRUSEL:
    b64 = obtener_base64_comprimido(foto)
    if b64:
        clase = "slide activa" if es_primera else "slide"
        html_carousel += f'<div class="{clase}"><img src="{b64}"></div>\n'
        es_primera = False

# Agregamos el Script que pasa las fotos automáticamente
html_carousel += """
</div>
<script>
    let slides = document.querySelectorAll('.slide');
    let index = 0;
    if(slides.length > 1) {
        setInterval(() => {
            slides[index].classList.remove('activa');
            index = (index + 1) % slides.length;
            slides[index].classList.add('activa');
        }, 3500); // Cambia de foto cada 3.5 segundos
    }
</script>
</body>
</html>
"""
components.html(html_carousel, height=460)

st.markdown("---")

# --- UBICACIÓN ---
st.markdown("<h3 style='text-align: center; color: #00E5FF;'>📍 Localización del Servidor</h3>", unsafe_allow_html=True)
st.markdown(f'<div class="tarjeta-info"><h4 style="margin:0; color:#E5E7EB;">{LUGAR_NOMBRE}</h4><p style="color:#8B949E; font-size:0.9rem; margin-top:5px;">{DIRECCION_TEXTO}</p><p style="color:#FFD700; font-weight:bold; margin-bottom:0;">{FECHA_EVENTO.strftime("%d de %B, %Y a las %H:%M hrs")}</p></div>', unsafe_allow_html=True)
datos_mapa = pd.DataFrame({'lat': [LATITUD], 'lon': [LONGITUD]})
st.map(datos_mapa, zoom=14)
st.markdown("---")

# --- CONTACTO Y WHATSAPP ---
st.markdown("<h3 style='text-align: center; color: #00E5FF;'>🎟️ POST /api/reservar_boletos</h3>", unsafe_allow_html=True)
if "invitador" in st.query_params:
    invitador_url = st.query_params["invitador"].lower()
else:
    invitador_url = ""

# Lógica mágica: Si el enlace dice ?invitador=organizadora, mostramos a la organizadora
if invitador_url == "organizadora":
    anfitrion = ORGANIZADORA
    st.write(f"<div style='text-align: center; color: #E5E7EB; margin-bottom: 15px;'>Comunícate con nuestra organizadora <b>{anfitrion['nombre']}</b> para apartar tus boletos:</div>", unsafe_allow_html=True)

# Si el enlace es de un graduado, lo mostramos a él
elif invitador_url in DIRECTORIO_GRADUADOS:
    anfitrion = DIRECTORIO_GRADUADOS[invitador_url]
    st.write(f"<div style='text-align: center; color: #E5E7EB; margin-bottom: 15px;'>Confirma tu asistencia enviándole un WhatsApp a <b>{anfitrion['nombre']}</b>:</div>", unsafe_allow_html=True)

# Si entraron sin enlace o con uno incorrecto, muestran la lista desplegable (SIN la organizadora)
else:
    st.write("<div style='text-align: center; color: #E5E7EB; margin-bottom: 15px;'>¿Quién te invitó a la graduación? Selecciona su nombre:</div>", unsafe_allow_html=True)
    nombres_opciones = [datos["nombre"] for datos in DIRECTORIO_GRADUADOS.values()]
    nombre_elegido = st.selectbox("Selecciona a tu invitador", nombres_opciones, label_visibility="collapsed")
    anfitrion = next(datos for datos in DIRECTORIO_GRADUADOS.values() if datos["nombre"] == nombre_elegido)

numero_final = anfitrion["telefono"]
nombre_final = anfitrion["nombre"]

# Mensaje diferente si es la organizadora
if invitador_url == "organizadora":
    mensaje_personalizado = f"¡Hola {nombre_final}! Me interesa apartar boletos para la graduación de Sistemas CESBA. ¿Me podrías dar información por favor?"
else:
    mensaje_personalizado = f"¡Hola {nombre_final}! Me encantaría asistir a tu graduación de Sistemas. ¿Me podrías apartar boletos por favor?"

link_whatsapp = f"https://wa.me/{numero_final}?text={mensaje_personalizado.replace(' ', '%20')}"

st.markdown(f'<div style="text-align: center; margin: 20px 0 40px 0;"><a href="{link_whatsapp}" target="_blank" style="text-decoration: none;"><button style="background-color: #0D1117; color: #00E5FF; border: 2px solid #00E5FF; padding: 15px 30px; font-size: 1.2rem; font-weight: bold; font-family: \'Courier New\', Courier, monospace; border-radius: 8px; width: 90%; max-width: 350px; cursor: pointer; animation: pulseTech 2s infinite; transition: all 0.3s ease;">> return WhatsApp(Mensaje);</button></a></div>', unsafe_allow_html=True)

st.markdown("---")
# --- PIE DE PÁGINA ---
st.markdown(f'<div style="text-align: center; color: #484F58; font-size: 0.8rem; padding-bottom: 20px;">/* Generación de Ing. en Sistemas - CESBA */<br>© {datetime.datetime.now().year} v1.0.0<br>Hecho con código y desvelos ☕</div>', unsafe_allow_html=True)