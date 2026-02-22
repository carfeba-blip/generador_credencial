import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io


st.set_page_config(page_title='Generador credencial', layout="wide")

def limpiar_formulario():
    for key in st.session_state.keys():
        del st.session_state[key]
        
def generar_carnet(nombre, cargo, id_emp, color, foto_upload):
    ANCHO, ALTO = 400, 600
    carnet = Image.new('RGB', (ANCHO, ALTO), color='white')
    draw = ImageDraw.Draw(carnet)
    
    try:
        font_nombre = ImageFont.truetype("arial.ttf", 35)
        font_cargo = ImageFont.truetype("arial.ttf", 20)
        font_id = ImageFont.truetype("arial.ttf", 16)
        font_footer = ImageFont.truetype("arial.ttf", 12)
    except:
        font_nombre = font_cargo = font_id = font_footer = ImageFont.load_default()

    draw.rectangle([0, 0, ANCHO, 180], fill=color)

    if foto_upload is not None:
        foto_original = Image.open(foto_upload)
        foto_perfil = ImageOps.fit(foto_original, (180, 180), centering=(0.5, 0.5))
        mask = Image.new('L', (180, 180), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 180, 180), fill=255)
        carnet.paste(foto_perfil, (110, 90), mask)
    else:
        draw.ellipse((110, 90, 290, 270), fill="#cccccc", outline="#666666")
        draw.text((200, 180), "FOTO", fill="white", anchor="mm")
    
    draw.text((ANCHO/2, 310), nombre.upper(), font=font_nombre, fill="black", anchor="mm")
    draw.text((ANCHO/2, 350), cargo,font=font_cargo, fill="#555555", anchor="mm")
    draw.line([120, 380, 280, 380], fill=color, width=3)
    draw.text((ANCHO/2, 410), f"EMPLEADO ID: {id_emp if id_emp else 'EMP-0001'}", font=font_id, fill="black", anchor="mm")

    draw.rectangle([0, ALTO-60, ANCHO, ALTO], fill="#f8f9fa")
    draw.text((ANCHO/2, ALTO-30), "PROPIEDAD PRIVADA - USO INTERNO", font=font_footer, fill="#adb5bd", anchor="mm")
    
    return carnet

with st.sidebar:
    st.header("⚙️ Configuración")
    nombre_input = st.text_input("Nombre Completo", placeholder="Nombre y apellidos")
    cargo_input = st.text_input("Cargo", placeholder="Cargo")
    id_input = st.text_input("Número de Empleado", placeholder="Codigo empleado")
    
    st.subheader("🎨 Estética")
    color_banner = st.color_picker(label="Selecciona el colora del banner", value="#1d3a8a")
    
    
    st.subheader("📷 Multimedia")
    foto = st.file_uploader("Subir foto de perfil", type=["jpg", "png", "jpeg"])
    st.button("✨ Limpiar Todo", use_container_width=True, on_click=limpiar_formulario)
_, col_titulo, _ = st.columns([1, 4, 1])
with col_titulo:
    st.header("🆔 ID-Gen Pro")
    st.caption("Proyecto Final: Generador de Identidad Corporativa")
st.divider()
col1, col2 = st.columns([1, 1],gap='large')
if foto is not None:
    img_carnet = generar_carnet(nombre_input, cargo_input, id_input, color_banner, foto)
    
    with col1:
        st.subheader("Vista Previa")
        st.image(img_carnet, use_container_width=True)

    with col2:
        st.subheader("Exportar")
        st.write("Verifica que los datos sean correctos. La imagen se descargará en formato PNG.")
    
        buf = io.BytesIO()
        img_carnet.save(buf, format="PNG")
        byte_im = buf.getvalue()
        nombre_archivo = nombre_input.strip().replace(" ", "_") if nombre_input else "credencial"
        nombre_final = f" credencial {nombre_archivo}.png"
    
        st.download_button(
            label="📥 Descargar Credencial",
            data=byte_im,
            file_name = nombre_final,
            mime="image/png",
            type="primary",
            use_container_width=True
        )
    
else:
    st.info("👋 Sube una foto en el panel lateral para generar el carnet.")
   
st.divider()
st.caption("<center>Carnet Generado</center>", unsafe_allow_html=True)