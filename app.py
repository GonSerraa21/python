import streamlit as st

# __________________________________________________________________________________
# CLASES (MODELO DE DATOS)
# He limpiado los inputs/prints de las clases para que sean puramente lógicas.

class Paciente_Urg:
    def __init__(self, nombre, genero, edad, motivo, gravedad, patologia):
        self._nombre = nombre
        self._genero = genero
        self._edad = edad
        self._motivo = motivo
        self._gravedad = gravedad
        self._patologia = patologia
        self._prioridad = 0

    # Getters y Properties (Mantenidos igual)
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

    def agregar_paciente(self, paciente):
        paciente.prioridad = self.asignar_prioridad(paciente)
        self.lista_espera_urg.append(paciente)
        self.lista_espera_urg.sort(key=lambda p: p.prioridad)
        return paciente.prioridad


class Paciente:
    def __init__(self, nombre, genero, edad, especialidad, turno, num_cita):
        self._nombre = nombre
        self._genero = genero
        self._edad = edad
        self._especialidad = especialidad
        self._turno = turno
        self._num_cita = num_cita

class Medico:
    def __init__(self, nombre, especialidad, turno):
        self.nombre = nombre
        self.especialidad = especialidad
        self.turno = turno
        self.ocupado = 0 

class Consultas:
    def __init__(self):
        self.nombre = "Hospital Politécnico"
        self.especialidades = ['Medicina Interna', 'Pediatría', 'Geriatría', 'Cardiología', 
                               'Neumología', 'Gastroentereología', 'Endocrinología', 
                               'Hematología', 'Neurología', 'Psiquiatría']
        self.analitica = ['Lunes 8h', 'Martes 8h', 'Miércoles 8h', 'Jueves 8h', 'Viernes 9h']
        self.medicos = [
            Medico("Dr. Justes Pérez-Alto", "Medicina Interna", "Lunes 10h"),
            Medico("Dr. López López", "Pediatría", "Lunes 15h"),
            Medico("Dra. Gómez Salado", "Geriatría", "Martes 11h"),
            Medico("Dra. Sánchez Castillo", "Cardiología", "Martes 13h"),
            Medico("Dr. Servios Servantum", "Neumología", "Miércoles 8.30h"),
            Medico("Dr. Sanz Silvestre", "Gastroentereología", "Miércoles 18.30h"),
            Medico("Dra. Rodami Ento", "Endocrinología", "Miércoles 19h"),
            Medico("Dra. Longa Niza", "Hematología", "Jueves 8h"),
            Medico("Dr. Ingen Ieros", "Neurología", "Jueves 12h"),
            Medico("Dra. Campos Plaza", "Psiquiatría", "Viernes 11h")
        ]
        self.pacientes = dict()
        self.contador = 1

# __________________________________________________________________________________
# CONFIGURACIÓN DE LA APP WEB Y ESTADO (PERSISTENCIA)

st.set_page_config(page_title="Hospital Politécnico", page_icon="🏥")

# Inicializar las clases en la memoria del navegador (Session State)
# Esto evita que se borren los datos al hacer clic en un botón.
if 'urgencias_system' not in st.session_state:
    st.session_state.urgencias_system = Urgencias()

if 'consultas_system' not in st.session_state:
    st.session_state.consultas_system = Consultas()

# Alias cortos para facilitar uso
urg = st.session_state.urgencias_system
hp = st.session_state.consultas_system

# __________________________________________________________________________________
# INTERFAZ GRÁFICA (SIDEBAR Y PÁGINAS)

st.title("🏥 Hospital Politécnico")

# Menú lateral
menu = st.sidebar.radio("Seleccione Departamento", ["Inicio", "Urgencias", "Pedir Cita"])

# --- PÁGINA DE INICIO ---
if menu == "Inicio":
    st.write("Bienvenido al sistema de gestión hospitalaria.")
    st.image("https://img.freepik.com/vector-gratis/edificio-hospital-clinica-ambulancia-medicos-pacientes_107791-13583.jpg", width=300)
    st.info("Seleccione una opción en el menú de la izquierda.")

# --- PÁGINA DE URGENCIAS ---
elif menu == "Urgencias":
    st.header("🚨 Servicio de Urgencias")
    tab1, tab2 = st.tabs(["Registrar Paciente", "Ver Lista de Espera"])

    with tab1:
        with st.form("form_urgencias"):
            st.subheader("Datos del Paciente")
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo")
                edad = st.number_input("Edad", min_value=0, step=1)
            with col2:
                genero = st.selectbox("Género", ["Hombre", "Mujer", "Otro"])
                patologia_input = st.radio("¿Patologías previas?", ["No", "Sí"])
                patologia_val = 1 if patologia_input == "Sí" else 0

            st.subheader("Motivo de consulta")
            motivos_dict = {
                "Cardiovascular": 5, "Respiratorio": 4, "Neurológico": 5,
                "Digestivo": 3, "Traumatismo": 3, "Infección": 4,
                "Dolor": 2, "Psiquiátrico": 2, "Obstetricia": 5, "Otros": 1
            }
            motivo_sel = st.selectbox("Seleccione motivo", list(motivos_dict.keys()))
            
            submit_urg = st.form_submit_button("Registrar en Urgencias")

            if submit_urg:
                if nombre:
                    gravedad = motivos_dict[motivo_sel]
                    nuevo_paciente = Paciente_Urg(nombre, genero, edad, motivo_sel, gravedad, patologia_val)
                    prioridad = urg.agregar_paciente(nuevo_paciente)
                    st.success(f"Paciente {nombre} registrado con éxito.")
                    st.info(f"Prioridad asignada: {prioridad} (Menor número = Mayor urgencia)")
                else:
                    st.error("Por favor, introduzca el nombre del paciente.")

    with tab2:
        st.subheader("Lista de espera (Ordenada por prioridad)")
        if not urg.lista_espera_urg:
            st.write("✅ No hay pacientes en espera.")
        else:
            for i, p in enumerate(urg.lista_espera_urg):
                st.write(f"**{i+1}. {p.nombre}**")
                st.caption(f"Motivo: {p.motivo} | Edad: {p.edad} | Prioridad: {p.prioridad}")
                st.divider()

# --- PÁGINA DE CITAS ---
elif menu == "Pedir Cita":
    st.header("📅 Gestión de Citas")

    # Paso 1: Datos Personales
    st.subheader("1. Datos del Paciente")
    c_nombre = st.text_input("Nombre y Apellidos", key="c_nombre")
    col1, col2 = st.columns(2)
    c_genero = col1.selectbox("Género", ["Hombre", "Mujer", "Otro"], key="c_gen")
    c_edad = col2.number_input("Edad", min_value=0, key="c_edad")

    # Paso 2: Tipo de Cita
    st.subheader("2. Tipo de Servicio")
    tipo_cita = st.radio("Seleccione servicio:", ["Consulta Especialista", "Analítica"], horizontal=True)

    if tipo_cita == "Consulta Especialista":
        # Selección de Especialidad
        especialidad_sel = st.selectbox("Seleccione Especialidad", hp.especialidades)
        
        # Filtrar médicos disponibles
        medicos_disponibles = [m for m in hp.medicos if m.especialidad == especialidad_sel and m.ocupado == 0]
        
        if medicos_disponibles:
            st.write(f"Citas disponibles para **{especialidad_sel}**:")
            # Crear un diccionario para mostrar texto amigable en el selectbox pero recuperar el objeto médico
            opciones_medicos = {f"{m.nombre} ({m.turno})": m for m in medicos_disponibles}
            
            medico_seleccionado_txt = st.selectbox("Elija un turno:", list(opciones_medicos.keys()))
            
            if st.button("Confirmar Cita Especialista"):
                if c_nombre:
                    medico_obj = opciones_medicos[medico_seleccionado_txt]
                    medico_obj.ocupado = 1 # Marcar ocupado
                    
                    # Generar código (lógica original adaptada)
                    codigo = f"{especialidad_sel[0]}X000{hp.contador}{c_nombre[0]}{c_nombre[-1]}"
                    nuevo_paciente = Paciente(c_nombre, c_genero, c_edad, especialidad_sel, medico_obj.turno, codigo)
                    hp.pacientes[codigo] = nuevo_paciente
                    hp.contador += 1
                    
                    st.success(f"Cita confirmada con {medico_obj.nombre}")
                    st.info(f"Turno: {medico_obj.turno} | Código: {codigo}")
                else:
                    st.error("Falta el nombre del paciente.")
        else:
            st.warning("No hay turnos disponibles para esta especialidad.")

    elif tipo_cita == "Analítica":
        turno_analitica = st.selectbox("Turnos disponibles", hp.analitica)
        
        if st.button("Confirmar Analítica"):
            if c_nombre:
                codigo = f"A{hp.analitica.index(turno_analitica)}000{hp.contador}{c_nombre[0]}{c_nombre[-1]}"
                nuevo_paciente = Paciente(c_nombre, c_genero, c_edad, "Analítica", turno_analitica, codigo)
                hp.pacientes[codigo] = nuevo_paciente
                hp.contador += 1
                
                st.success(f"Analítica reservada correctamente.")
                st.info(f"Turno: {turno_analitica} | Código: {codigo}")
            else:
                st.error("Falta el nombre del paciente.")

# Pie de página
st.sidebar.markdown("---")
st.sidebar.caption("Sistema Hospitalario v1.0")