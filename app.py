import streamlit as st
import random

# ==============================================================================
# 1. CLASES DE DATOS Y LÓGICA (MODEL)
# ==============================================================================

class Paciente_Urg:
    def __init__(self, nombre, genero, edad, motivo, gravedad, patologia):
        self._nombre = nombre
        self._genero = genero
        self._edad = edad
        self._motivo = motivo
        self._gravedad = gravedad
        self._patologia = patologia
        self._prioridad = 0

    @property
    def nombre(self): return self._nombre
    @property
    def genero(self): return self._genero
    @property
    def edad(self): return self._edad
    @property
    def motivo(self): return self._motivo
    @property
    def gravedad(self): return self._gravedad
    @property
    def patologia(self): return self._patologia
    @property
    def patologia_texto(self): return "Sí" if self._patologia == 1 else "No"
    @property
    def prioridad(self): return self._prioridad
    @prioridad.setter
    def prioridad(self, valor): self._prioridad = valor

class Paciente:
    def __init__(self, nombre, genero, edad, especialidad, turno, num_cita):
        self._nombre = nombre
        self._genero = genero
        self._edad = edad
        self._especialidad = especialidad
        self._turno = turno
        self._num_cita = num_cita

    @property
    def nombre(self): return self._nombre
    @property
    def turno(self): return self._turno
    @property
    def especialidad(self): return self._especialidad # Necesario para el recuento

class Medico:
    def __init__(self, nombre, especialidad, turno):
        self._nombre = nombre
        self._especialidad = especialidad
        self._turno = turno
        self._ocupado = 0 

    @property
    def nombre(self): return self._nombre
    @property
    def especialidad(self): return self._especialidad
    @property
    def turno(self): return self._turno
    @property
    def ocupado(self): return self._ocupado
    @ocupado.setter
    def ocupado(self, valor): self._ocupado = valor
    
    def mostrar_informacion(self):
        return f"Fecha: {self._turno} | Médico: {self._nombre}"

# --- SISTEMAS DE GESTIÓN ---

class Urgencias:
    def __init__(self):
        self.lista_espera_urg = list()

    def asignar_prioridad(self, paciente):
        prioridad = 100 - paciente.gravedad * 15
        if paciente.edad <= 3: prioridad -= 15
        elif 3 < paciente.edad < 6: prioridad -= 10
        elif 6 <= paciente.edad <= 12: prioridad -= 7
        elif 12 < paciente.edad < 20: prioridad -= 3
        elif 20 <= paciente.edad < 44: prioridad -= 5
        elif 44 <= paciente.edad < 60: prioridad -= 8
        elif 60 <= paciente.edad < 75: prioridad -= 12
        elif paciente.edad >= 75: prioridad -= 15
        if paciente.patologia == 1: prioridad -= 9
        return prioridad

    def registrar_paciente(self, paciente):
        paciente.prioridad = self.asignar_prioridad(paciente)
        self.lista_espera_urg.append(paciente)
        self.lista_espera_urg.sort(key=lambda p: p.prioridad)

class Consultas:
    def __init__(self):
        self._especialidades = ['Medicina Interna', 'Pediatría', 'Geriatría', 'Cardiología', 
                                'Neumología', 'Gastroentereología', 'Endocrinología', 
                                'Hematología', 'Neurología', 'Psiquiatría']
        self._medicos = [
            Medico("Dr. Justes Pérez-Alto","Medicina Interna","Lunes 10h"),
            Medico("Dr. López López","Pediatría","Lunes 15h"),
            Medico("Dra. Gómez Salado","Geriatría","Martes 11h"),
            Medico("Dra. Sánchez Castillo","Cardiología","Martes 13h"),
            Medico("Dr. Servios Servantum","Neumología","Miércoles 8.30h"),
            Medico("Dr. Sanz Silvestre","Gastroentereología","Miércoles 18.30h"),
            Medico("Dra. Rodami Ento","Endocrinología","Miércoles 19h"),
            Medico("Dra. Longa Niza","Hematología","Jueves 8h"),
            Medico("Dr. Ingen Ieros","Neurología","Jueves 12h"),
            Medico("Dra. Campos Plaza","Psiquiatría","Viernes 11h")
        ]
        self._contador = 1

    def obtener_medicos_disponibles(self, especialidad):
        return [m for m in self._medicos if m.especialidad == especialidad and m.ocupado == 0]

class Analitica(Consultas):
    def __init__(self):
        self._analitica_turnos = ['Lunes 8h', 'Martes 8h', 'Miércoles 8h', 'Jueves 8h', 'Viernes 9h']
        self._contadora = 1

# ==============================================================================
# 2. CONFIGURACIÓN GLOBAL
# ==============================================================================

st.set_page_config(page_title="Hospital Politécnico", page_icon="🏥", layout="wide")

class SistemaHospitalario:
    def __init__(self):
        self.urgencias = Urgencias()
        self.consultas = Consultas()
        self.analitica = Analitica()
        self.pacientes_db = dict()

@st.cache_resource
def obtener_sistema_global():
    return SistemaHospitalario()

sistema = obtener_sistema_global()
urg = sistema.urgencias
con = sistema.consultas
ana = sistema.analitica
db_pacientes = sistema.pacientes_db

# --- MÚSICA LOCAL ---
def poner_musica():
    st.sidebar.markdown("### 🎵 Sala de Espera")
    try:
        # Busca el archivo en la misma carpeta del repositorio
        st.sidebar.audio("musica_ascensor.mp3", format="audio/mp3", loop=True)
    except:
        st.sidebar.warning("Sube el archivo 'musica_ascensor.mp3' para escuchar música.")
poner_musica()

# --- BOTÓN ACTUALIZAR CON REDIRECCIÓN A INICIO ---
if st.sidebar.button("🔄 Actualizar datos"):
    # Forzamos la variable de sesión del menú para que vaya a "Inicio"
    st.session_state["menu_nav"] = "Inicio"
    st.rerun()

# ==============================================================================
# 3. INTERFAZ GRÁFICA
# ==============================================================================

# Imagen corporativa
try:
    st.image("image_0.png", width=500)
except:
    # Imagen por defecto si no encuentra la tuya
    st.image("https://cdn-icons-png.flaticon.com/512/3304/3304567.png", width=100)

#st.title("🏥 Hospital Politécnico")
st.markdown("---")

# Barra lateral de navegación con KEY para poder controlarla desde el botón
menu = st.sidebar.radio(
    "Menú Principal", 
    ["Inicio", "Urgencias", "Pedir Cita Médica", "Entrada Consulta", "Pedir Cita Analítica", "Entrada Analítica"],
    key="menu_nav" 
)

# --- PÁGINA DE INICIO ---
if menu == "Inicio":
    st.info("Bienvenido al Hospital Politécnico. **Seleccione una opción en el menú izquierdo.**")
    
    # CÁLCULO DE ESTADÍSTICAS
    num_urgencias = len(urg.lista_espera_urg)
    # Filtramos el diccionario global para separar analíticas de consultas médicas
    # Usamos _especialidad para evitar errores con pacientes antiguos en memoria
    num_analiticas = len([p for p in db_pacientes.values() if p._especialidad == "Analítica"])
    num_consultas = len([p for p in db_pacientes.values() if p._especialidad != "Analítica"])

    # VISUALIZACIÓN DE CONTADORES
    col1, col2, col3 = st.columns(3)
    col1.metric("🚑 Pacientes en Urgencias", num_urgencias)
    col2.metric("🩺 Citas registradas", num_consultas)
    col3.metric("🩸 Analíticas registradas", num_analiticas)
    
    #st.markdown("---")
    # Imagen corporativa
    #try:
    #    st.image("image_0.png", use_container_width=True)
    #except:
    #    st.image("https://cdn-icons-png.flaticon.com/512/3304/3304567.png", width=200)

# --- URGENCIAS ---
elif menu == "Urgencias":
    st.header("🚨 Servicio de Urgencias")
    tab1, tab2 = st.tabs(["Registrar Paciente", "Ver Lista de Espera"])

    with tab1:
        with st.form("form_urg"):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre")
            edad = c2.number_input("Edad", min_value=0, step=1)
            genero = c1.selectbox("Género", ["Hombre", "Mujer", "Otro"])
            
            motivos = {
                "Cardiovascular": 5, "Respiratorio": 4, "Neurológico": 5,
                "Digestivo": 3, "Traumatismo": 3, "Infección": 4,
                "Dolor": 2, "Psiquiátrico": 2, "Obstetricia": 5, "Otros": 1
            }
            motivo_sel = c2.selectbox("Motivo", list(motivos.keys()))
            patologia = st.radio("Patologías previas", ["No", "Sí"], horizontal=True)
            
            submitted = st.form_submit_button("Registrar")
            
            if submitted and nombre:
                pat_val = 1 if patologia == "Sí" else 0
                nuevo_p = Paciente_Urg(nombre, genero, edad, motivo_sel, motivos[motivo_sel], pat_val)
                urg.registrar_paciente(nuevo_p)
                st.success(f"Paciente {nombre} registrado con Prioridad: {nuevo_p.prioridad}")
            elif submitted:
                st.error("Debe introducir su nombre.")

    with tab2:
        if not urg.lista_espera_urg:
            st.info("No hay pacientes en espera.")
        else:
            for i, p in enumerate(urg.lista_espera_urg):
                st.markdown(f"**{i+1}. {p.nombre}** | Motivo: {p.motivo} | Prioridad: **{p.prioridad}**")
                st.progress(max(0, min(100, p.prioridad)) / 100)

# --- PEDIR CITA CONSULTA ---
elif menu == "Pedir Cita Médica":
    st.header("📅 Pedir Consulta Médica")
    
    col1, col2 = st.columns(2)
    p_nombre = col1.text_input("Nombre completo")
    p_edad = col2.number_input("Edad", min_value=0)
    p_genero = col1.selectbox("Género", ["Hombre", "Mujer", "Otro"])
    
    especialidad_sel = st.selectbox("Seleccione Especialidad", con._especialidades)
    
    medicos_disp = con.obtener_medicos_disponibles(especialidad_sel)
    
    if medicos_disp:
        st.write("Turnos disponibles:")
        mapa_medicos = {f"{m.turno} - {m.nombre}": m for m in medicos_disp}
        seleccion = st.selectbox("Seleccione turno", list(mapa_medicos.keys()))
        
        if st.button("Confirmar Cita"):
            if p_nombre:
                medico_obj = mapa_medicos[seleccion]
                medico_obj.ocupado = 1 
                
                codigo = f"{especialidad_sel[0]}{con._medicos.index(medico_obj)}{random.randint(1,999)}00{con._contador}{p_nombre[0].upper()}{p_nombre[-1].upper()}"
                
                nuevo_paciente = Paciente(p_nombre, p_genero, p_edad, especialidad_sel, medico_obj.turno, codigo)
                db_pacientes[codigo] = nuevo_paciente
                con._contador += 1
                
                st.balloons()
                st.success("✅ Cita reservada con éxito")
                st.warning(f"📌 Su CÓDIGO de CONSULTA es: **{codigo}** (Guárdelo para entrar)")
            else:
                st.error("Debe introducir su nombre.")
    else:
        st.warning("No hay citas disponibles para esta especialidad")

# --- ENTRADA CONSULTA ---
elif menu == "Entrada Consulta Médica":
    st.header("🩺 Check-in Consulta")
    
    with st.form("checkin_consulta"):
        codigo_input = st.text_input("Introduzca su CÓDIGO de Consulta:")
        btn_verificar = st.form_submit_button("Buscar Consulta")
    
    if btn_verificar:
        if codigo_input in db_pacientes:
            paciente = db_pacientes[codigo_input]
            if paciente.especialidad != "Analítica":
                st.session_state['paciente_actual_consulta'] = paciente
                if 'mensaje_resultado' in st.session_state: del st.session_state['mensaje_resultado']
            else:
                st.error("Este código corresponde a una Analítica.")
                if 'paciente_actual_consulta' in st.session_state: del st.session_state['paciente_actual_consulta']
        else:
            st.error("Código no encontrado.")
            if 'paciente_actual_consulta' in st.session_state: del st.session_state['paciente_actual_consulta']

    if 'paciente_actual_consulta' in st.session_state:
        p = st.session_state['paciente_actual_consulta']
        
        st.info(f"✅ Paciente encontrado: **{p.nombre}**")
        st.info(f"📅 Cita programada: **{p.turno}**")
        st.markdown("---")
        
        st.write("### ⏱️ Control de horario")
        col1, col2, col3 = st.columns(3)
        
        if col1.button("✅ Es la hora correcta"):
            st.success(f"Perfecto. Es su hora. **Pase a la sala de espera.**")
            
        if col2.button("❌ La cita ya ha pasado"):
            st.error(f"Lo sentimos, ha pasado su hora de consulta. **Por favor, pida otra cita.**")
            
        if col3.button("⏳ Todavía no es la hora"):
            st.warning(f"Todavía no es su consulta. **Su consulta es el {p.turno}.** Espere fuera.")
            
        if st.button("🔄 Limpiar / Nuevo Paciente"):
            del st.session_state['paciente_actual_consulta']
            st.rerun()

# --- PEDIR CITA ANALÍTICA ---
elif menu == "Pedir Cita Analítica":
    st.header("💉 Pedir Analítica")
    
    a_nombre = st.text_input("Nombre completo", key="a_nom")
    c1, c2 = st.columns(2)
    a_edad = c1.number_input("Edad", min_value=0, key="a_edad")
    a_genero = c2.selectbox("Género", ["Hombre", "Mujer", "Otro"], key="a_gen")
    
    turno_sel = st.selectbox("Turnos disponibles", ana._analitica_turnos)
    
    if st.button("Confirmar Analítica"):
        if a_nombre:
            codigo = f"A{ana._analitica_turnos.index(turno_sel)}{random.randint(1,999)}00{ana._contadora}{a_nombre[0].upper()}{a_nombre[-1].upper()}"
            nuevo_paciente = Paciente(a_nombre, a_genero, a_edad, "Analítica", turno_sel, codigo)
            db_pacientes[codigo] = nuevo_paciente
            ana._contadora += 1
            st.balloons()
            st.success("✅ Analítica reservada con éxito")
            st.warning(f"📌 Su CÓDIGO de ANALÍTICA es: **{codigo}** (Guárdelo para entrar)")
        else:
            st.error("Debe introducir su nombre.")

# --- ENTRADA ANALÍTICA ---
elif menu == "Entrada Analítica":
    st.header("🩸 Check-in Analítica")
    
    with st.form("checkin_analitica"):
        codigo_input_a = st.text_input("Introduzca su CÓDIGO de Analítica:")
        btn_verificar_a = st.form_submit_button("Buscar Analítica")
    
    if btn_verificar_a:
        if codigo_input_a in db_pacientes:
            paciente = db_pacientes[codigo_input_a]
            if paciente.especialidad == "Analítica":
                st.session_state['paciente_actual_analitica'] = paciente
            else:
                st.error("Este código es de Consulta Médica.")
                if 'paciente_actual_analitica' in st.session_state: del st.session_state['paciente_actual_analitica']
        else:
            st.error("Código no encontrado.")
            if 'paciente_actual_analitica' in st.session_state: del st.session_state['paciente_actual_analitica']

    if 'paciente_actual_analitica' in st.session_state:
        p = st.session_state['paciente_actual_analitica']
        st.info(f"✅ Paciente: **{p.nombre}**")
        st.info(f"🩸 Turno: **{p.turno}**")
        st.markdown("---")
        st.write("### ⏱️ Control de horario")
        c1, c2, c3 = st.columns(3)
        if c1.button("✅ Es la hora", key="btn_a_ok"):
            st.success("Es su hora. **Puede pasar a la sala de extracción**")
        if c2.button("❌ Ya pasó", key="btn_a_late"):
            st.error("Ha pasado su hora de analítica. **Por favor, pida nueva cita**")
        if c3.button("⏳ Aún no", key="btn_a_wait"):
            st.warning(f"Todavía no es su analítica. **Su turno es el {p.turno}**")
        if st.button("🔄 Nueva Búsqueda"):
            del st.session_state['paciente_actual_analitica']
            st.rerun()