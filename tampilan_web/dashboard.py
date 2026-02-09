import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# =========================
# Mapping label musim & cuaca
# =========================
SEASON_MAP = {1: "Musim Semi (Spring)", 2: "Musim Panas (Summer)", 3: "Musim Gugur (Fall)", 4: "Musim Dingin (Winter)"}
WEATHER_MAP = {
    1: "Cerah / Sedikit Berawan",
    2: "Berkabut / Berawan",
    3: "Hujan/Salju Ringan",
    4: "Hujan/Salju Lebat",
}

# =========================
# Label kolom untuk tampilan UI
# =========================
COLUMN_LABELS = {
    "temp": "Suhu (Temperature)",
    "atemp": "Suhu Terasa (Feels Like)",
    "hum": "Kelembaban (Humidity)",
    "windspeed": "Kecepatan Angin",
    "cnt": "Jumlah Penyewaan Sepeda",
    "casual": "Pengguna Kasual",
    "registered": "Pengguna Terdaftar",
}

# =========================
# Loaders
# =========================
@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "dteday" not in df.columns:
        raise ValueError(f"Kolom 'dteday' tidak ditemukan di {path}")

    df["dteday"] = pd.to_datetime(df["dteday"])
    df["season_label"] = df["season"].map(SEASON_MAP)
    df["weather_label"] = df["weathersit"].map(WEATHER_MAP)
    return df


@st.cache_data
def load_cluster_csv(path: str) -> pd.DataFrame:
    """
    Memuat file hasil clustering (bike_final_model_ready.csv)
    yang sudah punya kolom 'cluster' dan 'cluster_tag'.
    """
    dfc = pd.read_csv(path)
    if "dteday" not in dfc.columns:
        raise ValueError(f"Kolom 'dteday' tidak ditemukan di {path}")

    dfc["dteday"] = pd.to_datetime(dfc["dteday"])
    dfc["season_label"] = dfc["season"].map(SEASON_MAP)
    dfc["weather_label"] = dfc["weathersit"].map(WEATHER_MAP)

    if "cluster" not in dfc.columns or "cluster_tag" not in dfc.columns:
        raise ValueError("File cluster harus punya kolom 'cluster' dan 'cluster_tag'.")

    
    return dfc


# =========================
# Helpers
# =========================
def apply_filters(df: pd.DataFrame, date_range, seasons, weathers) -> pd.DataFrame:
    start_date, end_date = date_range
    mask = (df["dteday"].dt.date >= start_date) & (df["dteday"].dt.date <= end_date)

    if seasons:
        mask &= df["season_label"].isin(seasons)
    if weathers:
        mask &= df["weather_label"].isin(weathers)

    return df.loc[mask].copy()


def attach_daily_cluster_to_hour(df_hour: pd.DataFrame, df_cluster_day: pd.DataFrame) -> pd.DataFrame:
    """
    Join cluster harian ke data per jam berdasarkan 'dteday'.
    Semua jam dalam satu hari akan mewarisi cluster harian itu.
    """
    dfc = df_cluster_day[["dteday", "cluster", "cluster_tag"]].drop_duplicates("dteday")
    out = df_hour.merge(dfc, on="dteday", how="left")
    out["cluster_tag"] = out["cluster_tag"].fillna("Tidak diketahui")
    return out


def label(col: str) -> str:
    """Ambil label bahasa Indonesia untuk nama kolom."""
    return COLUMN_LABELS.get(col, col)


# =========================
# Header UI
# =========================
st.title("Dashboard Penyewaan Sepeda (Streamlit)")
st.caption("Filter di sidebar akan mengubah tabel & grafik secara real-time.")

# =========================
# Pilih dataset
# =========================
dataset = st.sidebar.selectbox("Pilih Dataset", ["day.csv", "hour.csv"])
df = load_csv(dataset)

# =========================
# Sidebar - Filters
# =========================
st.sidebar.header("Filter Data")

min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

st.sidebar.subheader("Filter Tanggal")

colA, colB = st.sidebar.columns(2)
start_date = colA.date_input(
    "Mulai",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key=f"start_{dataset}",
)
end_date = colB.date_input(
    "Sampai",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key=f"end_{dataset}",
)

if start_date > end_date:
    start_date, end_date = end_date, start_date

date_range = (start_date, end_date)

season_options = sorted(df["season_label"].dropna().unique().tolist())
weather_options = sorted(df["weather_label"].dropna().unique().tolist())

selected_seasons = st.sidebar.multiselect("Filter Musim", season_options, default=season_options)
selected_weathers = st.sidebar.multiselect("Filter Cuaca", weather_options, default=weather_options)

# Apply filter ke dataset utama (untuk KPI, line chart, table)
df_f = apply_filters(df, date_range, selected_seasons, selected_weathers)

# Bukti filter bekerja
st.sidebar.markdown("---")
st.sidebar.metric("Jumlah data (awal)", f"{len(df):,}")
st.sidebar.metric("Jumlah data (setelah filter)", f"{len(df_f):,}")

# =========================
# KPI
# =========================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Penyewaan Sepeda", f"{int(df_f['cnt'].sum()) if len(df_f) else 0:,}")
c2.metric("Rata-rata Penyewaan", f"{float(df_f['cnt'].mean()) if len(df_f) else 0:,.2f}")
c3.metric("Rata-rata Suhu", f"{float(df_f['temp'].mean()) if len(df_f) else 0:,.3f}")
c4.metric("Rata-rata Kelembaban", f"{float(df_f['hum'].mean()) if len(df_f) else 0:,.3f}")

st.markdown("---")

# =========================
# Load clustering results (hasil tim analisis)
# =========================
CLUSTER_PATH = "bike_final_model_ready.csv"

try:
    df_cluster_day = load_cluster_csv(CLUSTER_PATH)
    # filter yang sama untuk data cluster (harian)
    df_cluster_day_f = apply_filters(df_cluster_day, date_range, selected_seasons, selected_weathers)

    # kalau user pilih hour.csv, cluster harian diwariskan ke hour via join dteday
    if dataset == "hour.csv":
        df_cluster = attach_daily_cluster_to_hour(df_f, df_cluster_day_f)
    else:
        df_cluster = df_cluster_day_f.copy()

except FileNotFoundError:
    st.error("File 'bike_final_model_ready.csv' tidak ditemukan. Pastikan ada di folder yang sama.")
    df_cluster = df_f.copy()
    df_cluster["cluster_tag"] = "Tidak diketahui"

except Exception as e:
    st.error(f"Gagal memuat clustering: {e}")
    df_cluster = df_f.copy()
    df_cluster["cluster_tag"] = "Tidak diketahui"

# =========================
# Charts
# =========================
left, right = st.columns((1.2, 1))

# ---- Scatter plot clustering ----
with left:
    st.subheader("Scatter Plot Clustering (Hasil Analisis)")
    st.caption("Warna titik menunjukkan kelompok (cluster). Filter akan memengaruhi titik yang tampil.")

    if len(df_cluster) == 0:
        st.warning("Tidak ada data setelah filter.")
    else:
        x_options = ["temp", "hum", "windspeed"]
        y_options = ["cnt", "hum", "temp", "windspeed"]

        x_axis = st.selectbox("Sumbu X", x_options, index=0, format_func=label, key="x_scatter")
        y_axis = st.selectbox("Sumbu Y", y_options, index=0, format_func=label, key="y_scatter")

        fig_scatter = px.scatter(
            df_cluster,
            x=x_axis,
            y=y_axis,
            color="cluster_tag" if "cluster_tag" in df_cluster.columns else None,
            hover_data=["dteday", "season_label", "weather_label", "cnt"]
            + (["hr"] if "hr" in df_cluster.columns else []),
            title=f"Clustering: {label(y_axis)} vs {label(x_axis)}",
        )

        # ubah label axis agar ramah user
        fig_scatter.update_xaxes(title_text=label(x_axis))
        fig_scatter.update_yaxes(title_text=label(y_axis))

        st.plotly_chart(fig_scatter, use_container_width=True)

# ---- Line chart tren penyewaan ----
with right:
    st.subheader("Line Chart Tren Penyewaan")
    st.caption("Menampilkan tren jumlah penyewaan berdasarkan data yang sudah ter-filter.")

    if len(df_f) == 0:
        st.warning("Tidak ada data setelah filter.")
    else:
        if "hr" in df_f.columns:
            agg = st.radio("Agregasi Tren", ["Per Hari", "Per Bulan"], horizontal=True)
            if agg == "Per Hari":
                trend = df_f.groupby(df_f["dteday"].dt.date)["cnt"].sum().reset_index()
                trend.columns = ["dteday", "cnt"]
                trend["dteday"] = pd.to_datetime(trend["dteday"])
            else:
                trend = df_f.set_index("dteday").resample("M")["cnt"].sum().reset_index()
        else:
            agg = st.radio("Agregasi Tren", ["Per Hari", "Per Bulan"], horizontal=True)
            if agg == "Per Hari":
                trend = df_f.groupby("dteday", as_index=False)["cnt"].sum()
            else:
                trend = df_f.set_index("dteday").resample("M")["cnt"].sum().reset_index()

        fig_line = px.line(
            trend,
            x="dteday",
            y="cnt",
            markers=True,
            title="Tren Jumlah Penyewaan Sepeda",
        )
        fig_line.update_xaxes(title_text="Tanggal")
        fig_line.update_yaxes(title_text="Jumlah Penyewaan Sepeda")

        st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# =========================
# Table
# =========================
st.subheader("Data (setelah filter)")

df_display = df_f.copy()
rename_map = {k: v for k, v in COLUMN_LABELS.items() if k in df_display.columns}
df_display = df_display.rename(columns=rename_map)

sort_cols = ["dteday"] + (["hr"] if "hr" in df_f.columns else [])
st.dataframe(df_display.sort_values(sort_cols), use_container_width=True)

with st.expander("Debug Filter"):
    st.write(
        {
            "dataset": dataset,
            "tanggal_mulai": str(date_range[0]),
            "tanggal_akhir": str(date_range[1]),
            "musim_dipilih": selected_seasons,
            "cuaca_dipilih": selected_weathers,
            "jumlah_data_awal": len(df),
            "jumlah_data_setelah_filter": len(df_f),
        }
    )
