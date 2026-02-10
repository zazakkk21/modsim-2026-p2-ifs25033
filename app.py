import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Dashboard Kuesioner",
    page_icon="📊",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
df = pd.read_excel("data_kuesioner.xlsx")
pertanyaan = df.iloc[:, 1:]
semua_jawaban = pertanyaan.values.flatten()

skor = {
    "SS": 6,
    "S": 5,
    "CS": 4,
    "CTS": 3,
    "TS": 2,
    "STS": 1
}

# ======================
# SIDEBAR
# ======================
st.sidebar.title("⚙️ Pengaturan")

selected_q = st.sidebar.selectbox(
    "Pilih Pertanyaan",
    ["Semua"] + list(pertanyaan.columns)
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Kategori Skala**
    - Positif: SS, S
    - Netral: CS
    - Negatif: CTS, TS, STS
    """
)

# ======================
# HEADER
# ======================
st.title("📊 Dashboard Analisis Kuesioner")
st.markdown("Visualisasi interaktif hasil kuesioner responden")

# ======================
# FILTER DATA
# ======================
if selected_q == "Semua":
    data_view = pertanyaan
else:
    data_view = pertanyaan[[selected_q]]

flat_data = data_view.values.flatten()

# ======================
# KPI METRICS
# ======================
total_respon = len(flat_data)

positif = sum(j in ["SS", "S"] for j in flat_data)
netral = sum(j == "CS" for j in flat_data)
negatif = sum(j in ["CTS", "TS", "STS"] for j in flat_data)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Respon", total_respon)
col2.metric("Positif (%)", f"{positif/total_respon*100:.1f}")
col3.metric("Netral (%)", f"{netral/total_respon*100:.1f}")
col4.metric("Negatif (%)", f"{negatif/total_respon*100:.1f}")

# ======================
# DISTRIBUSI JAWABAN
# ======================
st.markdown("---")
st.subheader("Distribusi Jawaban")

dist = pd.Series(flat_data).value_counts().reset_index()
dist.columns = ["Skala", "Jumlah"]

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        dist,
        x="Skala",
        y="Jumlah",
        color="Skala",
        text="Jumlah"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        dist,
        names="Skala",
        values="Jumlah",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

# ======================
# STACKED BAR
# ======================
st.markdown("---")
st.subheader("Distribusi Jawaban per Pertanyaan")

stacked = pertanyaan.apply(pd.Series.value_counts).fillna(0)

fig = px.bar(
    stacked,
    x=stacked.index,
    y=stacked.columns,
    barmode="stack"
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# RATA-RATA SKOR
# ======================
st.markdown("---")
st.subheader("Rata-rata Skor per Pertanyaan")

df_score = pertanyaan.replace(skor).infer_objects(copy=False)
rata = df_score.mean().reset_index()
rata.columns = ["Pertanyaan", "Rata-rata Skor"]

fig = px.bar(
    rata,
    x="Pertanyaan",
    y="Rata-rata Skor",
    color="Rata-rata Skor",
    text="Rata-rata Skor"
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# HEATMAP (BONUS)
# ======================
st.markdown("---")
st.subheader("Heatmap Rata-rata Skor")

fig = px.imshow(
    [rata["Rata-rata Skor"]],
    x=rata["Pertanyaan"],
    y=["Skor"],
    aspect="auto",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# DATA TABLE
# ======================
with st.expander("📋 Lihat Data Mentah"):
    st.dataframe(df)
