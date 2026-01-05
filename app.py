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
        # Heredamos pero usamos listas propias para analítica
        self._analitica_turnos = ['Lunes 8h', 'Martes 8h', 'Miércoles 8h', 'Jueves 8h', 'Viernes 9h']
        self._contadora = 1

# ==============================================================================
# 2. CONFIGURACIÓN DE LA APP Y ESTADO (STREAMLIT)
# ==============================================================================

st.set_page_config(page_title="Hospital Politécnico", page_icon="🏥", layout="wide")

# Inicialización del estado (Persistencia de datos)
if 'urgencias_sys' not in st.session_state:
    st.session_state.urgencias_sys = Urgencias()
if 'consultas_sys' not in st.session_state:
    st.session_state.consultas_sys = Consultas()
if 'analitica_sys' not in st.session_state:
    st.session_state.analitica_sys = Analitica()
if 'pacientes_db' not in st.session_state:
    st.session_state.pacientes_db = dict() # Base de datos general de pacientes (Citas y Analíticas)

# Alias para facilitar la escritura
urg = st.session_state.urgencias_sys
con = st.session_state.consultas_sys
ana = st.session_state.analitica_sys
db_pacientes = st.session_state.pacientes_db

# ==============================================================================
# 3. INTERFAZ GRÁFICA (VIEW)
# ==============================================================================

st.title("🏥 Hospital Politécnico")
st.markdown("---")

# Barra lateral de navegación
menu = st.sidebar.radio(
    "Menú Principal", 
    ["Inicio", "Urgencias", "Pedir Cita Consulta", "Entrada Consulta Médica", "Pedir Cita Analítica", "Entrada Analítica"]
)

# --- PÁGINA DE INICIO ---
if menu == "Inicio":
    st.info("Bienvenido al sistema de gestión hospitalaria. Seleccione una opción en el menú izquierdo.")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Pacientes en Urgencias", len(urg.lista_espera_urg))
    with col2: st.metric("Citas Registradas", len(db_pacientes))
    with col3: st.image("https://cdn-icons-png.flaticon.com/512/3304/3304567.png", width=100)

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
                st.error("Falta el nombre.")

    with tab2:
        if not urg.lista_espera_urg:
            st.info("No hay pacientes en espera.")
        else:
            for i, p in enumerate(urg.lista_espera_urg):
                st.markdown(f"**{i+1}. {p.nombre}** | Motivo: {p.motivo} | Prioridad: **{p.prioridad}**")
                st.progress(max(0, min(100, p.prioridad)) / 100)

# --- PEDIR CITA CONSULTA ---
elif menu == "Pedir Cita Consulta":
    st.header("📅 Pedir Cita Médica")
    
    col1, col2 = st.columns(2)
    p_nombre = col1.text_input("Nombre completo")
    p_edad = col2.number_input("Edad", min_value=0)
    p_genero = col1.selectbox("Género", ["Hombre", "Mujer", "Otro"])
    
    especialidad_sel = st.selectbox("Seleccione Especialidad", con._especialidades)
    
    # Buscar médicos disponibles dinámicamente
    medicos_disp = con.obtener_medicos_disponibles(especialidad_sel)
    
    if medicos_disp:
        st.write("Turnos disponibles:")
        # Diccionario auxiliar para mostrar texto bonito en el selector
        mapa_medicos = {f"{m.turno} - {m.nombre}": m for m in medicos_disp}
        seleccion = st.selectbox("Seleccione turno", list(mapa_medicos.keys()))
        
        if st.button("Confirmar Cita"):
            if p_nombre:
                medico_obj = mapa_medicos[seleccion]
                medico_obj.ocupado = 1 # Marcar ocupado
                
                # Generar código único
                codigo = f"{especialidad_sel[0]}{con._medicos.index(medico_obj)}{random.randint(1,999)}00{con._contador}{p_nombre[0].upper()}{p_nombre[-1].upper()}"
                
                nuevo_paciente = Paciente(p_nombre, p_genero, p_edad, especialidad_sel, medico_obj.turno, codigo)
                db_pacientes[codigo] = nuevo_paciente
                con._contador += 1
                
                st.balloons()
                st.success("✅ Cita Reservada con Éxito")
                st.warning(f"📌 SU CÓDIGO DE CITA ES: **{codigo}** (Guárdelo para entrar)")
            else:
                st.error("Debe introducir su nombre.")
    else:
        st.warning("No hay citas disponibles para esta especialidad.")

# --- ENTRADA CONSULTA ---
elif menu == "Entrada Consulta Médica":
    st.header("🩺 Check-in Consulta")
    codigo_input = st.text_input("Introduzca su CÓDIGO de cita:")
    
    if st.button("Verificar Cita"):
        if codigo_input in db_pacientes:
            paciente = db_pacientes[codigo_input]
            
            # Verificar si es una cita médica (no analítica)
            if paciente._especialidad != "Analítica":
                st.info(f"Paciente: {paciente.nombre}")
                st.info(f"Cita programada: {paciente.turno}")
                
                st.markdown("---")
                st.write("**Simulación de horario:**")
                c1, c2, c3 = st.columns(3)
                if c1.button("Es la hora correcta"):
                    st.success("✅ Puede pasar a la sala de espera.")
                if c2.button("La hora ya pasó"):
                    st.error("❌ Ha llegado tarde. Debe pedir nueva cita.")
                if c3.button("Aún no es la hora"):
                    st.warning("⏳ Por favor espere, aún es temprano.")
            else:
                st.error("Este código corresponde a una Analítica, vaya a la sección correspondiente.")
        else:
            st.error("Código no encontrado en la base de datos.")

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
            # Generar código único para analítica
            codigo = f"A{ana._analitica_turnos.index(turno_sel)}{random.randint(1,999)}00{ana._contadora}{a_nombre[0].upper()}{a_nombre[-1].upper()}"
            
            nuevo_paciente = Paciente(a_nombre, a_genero, a_edad, "Analítica", turno_sel, codigo)
            db_pacientes[codigo] = nuevo_paciente
            ana._contadora += 1
            
            st.balloons()
            st.success("✅ Analítica Reservada")
            st.warning(f"📌 SU CÓDIGO ES: **{codigo}**")
        else:
            st.error("Falta el nombre.")

# --- ENTRADA ANALÍTICA ---
elif menu == "Entrada Analítica":
    st.header("🩸 Check-in Analítica")
    codigo_input = st.text_input("Introduzca su CÓDIGO de analítica:")
    
    if st.button("Verificar Analítica"):
        if codigo_input in db_pacientes:
            paciente = db_pacientes[codigo_input]
            
            if paciente._especialidad == "Analítica":
                st.info(f"Paciente: {paciente.nombre}")
                st.info(f"Turno: {paciente.turno}")
                
                st.markdown("---")
                st.write("**Simulación de horario:**")
                c1, c2, c3 = st.columns(3)
                if c1.button("Es la hora correcta"):
                    st.success("✅ Puede pasar a la sala de extracción.")
                if c2.button("La hora ya pasó"):
                    st.error("❌ Turno perdido.")
                if c3.button("Aún no es la hora"):
                    st.warning("⏳ Espere su turno.")
            else:
                st.error("Este código es de Consulta Médica, no de Analítica.")
        else:
            st.error("Código no encontrado.")