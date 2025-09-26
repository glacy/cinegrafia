import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI

# -------------------------------
# Configuración inicial
# -------------------------------
st.title("CineGraphIA: Asistente para Gráficas Cinemáticas")
st.markdown("Explora cómo la posición, velocidad y aceleración cambian con el tiempo en un movimiento MRUA.")

# -------------------------------
# Configuración de la API
# -------------------------------
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])  # Coloca aquí tu API key

# -------------------------------
# Entrada de parámetros
# -------------------------------
st.sidebar.header("Condiciones iniciales")
v0 = st.sidebar.number_input("Velocidad inicial v₀ (m/s):", value=10.0, step=1.0)
a = st.sidebar.number_input("Aceleración a (m/s²):", value=-9.8, step=0.1)
tmax = st.sidebar.number_input("Tiempo máximo tₘₐₓ (s):", value=5.0, step=0.5)
dt = 0.01

# -------------------------------
# Cálculos cinemáticos
# -------------------------------
t = np.arange(0, tmax, dt)
v = v0 + a * t
x = v0 * t + 0.5 * a * t**2
acc = np.full_like(t, a)

# -------------------------------
# Generación de gráficas
# -------------------------------
fig, axs = plt.subplots(3, 1, figsize=(6, 8))

axs[0].plot(t, x, label="x(t)")
axs[0].set_title("Posición vs Tiempo")
axs[0].set_xlabel("Tiempo (s)")
axs[0].set_ylabel("Posición (m)")
axs[0].grid()

axs[1].plot(t, v, label="v(t)", color="orange")
axs[1].set_title("Velocidad vs Tiempo")
axs[1].set_xlabel("Tiempo (s)")
axs[1].set_ylabel("Velocidad (m/s)")
axs[1].grid()

axs[2].plot(t, acc, label="a(t)", color="green")
axs[2].set_title("Aceleración vs Tiempo")
axs[2].set_xlabel("Tiempo (s)")
axs[2].set_ylabel("Aceleración (m/s²)")
axs[2].grid()

plt.tight_layout()
st.pyplot(fig)

# -------------------------------
# Sección de retroalimentación con IA
# -------------------------------
st.subheader("Interpreta la gráfica con ayuda de IA")
pregunta = st.text_input("Escribe una pregunta o interpreta la gráfica:")

if pregunta:
    prompt = f"""
    Estás analizando un movimiento con v₀={v0} m/s, a={a} m/s² y tiempo máximo {tmax} s.
    El estudiante pregunta o interpreta: "{pregunta}".
    Proporciona una respuesta clara, adaptada a un nivel de primer año de universidad.
    """

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un tutor de física muy claro y pedagógico."},
                {"role": "user", "content": prompt}
            ]
        )
        st.write("**IA:** " + respuesta.choices[0].message.content)
    except Exception as e:
        st.error(f"No se pudo conectar con la API: {e}")
