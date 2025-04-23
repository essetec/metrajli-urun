import streamlit as st
import pandas as pd

st.set_page_config(page_title="Metrajlı Ürün Girişi", layout="wide")

st.title("📏 Metrajlı Ürün Giriş Paneli")

# Renk kodları
RENK_KODLARI = {
    "Bıçak": "#ff4d4d",       # kırmızı
    "Pilyaj": "#4CAF50",      # yeşil
    "Dentelaj": "#2196F3",    # mavi
    "Perforaj": "#FFEB3B",    # sarı
    "Combi": "#A52A2A",       # kahverengi
    "Fermuar": "#FFA500"       # turuncu
}

# Oturumda kayıtlı veriler
if "metrajli_urunler" not in st.session_state:
    st.session_state.metrajli_urunler = []

st.subheader("➕ Yeni Ürün Girişi")

col1, col2, col3 = st.columns(3)

with col1:
    urun = st.selectbox("1. Ürün", list(RENK_KODLARI.keys()))
    kalinlik = st.selectbox("4. Kalınlık", ["1.5PT", "2PT", "3PT", "4PT", "6PT"])
    marka = st.text_input("6. Marka")

with col2:
    agiz = st.selectbox("2. Ağız Yapısı", ["CB", "LCB", "SB", "R", "DR", "WAVE", "SHARK"])
    tur = st.selectbox("5. Tür", ["Şapkalı", "Tozsuz", "2x2", "3x3", "8x8"])
    seri = st.text_input("7. Seri")

with col3:
    yukseklik = st.selectbox("3. Yükseklik", [
        "12.00", "21.00", "22.10", "22.20", "22.30", "22.40", "22.50", "22.60",
        "22.80", "23.00", "23.10", "23.20", "23.30", "23.40", "23.50", "23.60",
        "23.70", "23.80", "23.85", "25.40", "30.00", "40.00", "50.00", "60.00"])
    metraj = st.number_input("8. Metraj (m)", min_value=0.0, step=0.1)
    kritik = st.number_input("9. Kritik Miktar", min_value=0, step=1)

# Kayıt kontrolü
yeni_kayit = {
    "Ürün": urun,
    "Ağız Yapısı": agiz,
    "Yükseklik": yukseklik,
    "Kalınlık": kalinlik,
    "Tür": tur,
    "Marka": marka,
    "Seri": seri,
    "Metraj": metraj,
    "Kritik": kritik,
    "Renk": RENK_KODLARI.get(urun, "#FFFFFF")
}

tekrar_var_mi = any(
    k["Ürün"] == yeni_kayit["Ürün"] and
    k["Ağız Yapısı"] == yeni_kayit["Ağız Yapısı"] and
    k["Yükseklik"] == yeni_kayit["Yükseklik"] and
    k["Kalınlık"] == yeni_kayit["Kalınlık"] and
    k["Tür"] == yeni_kayit["Tür"] and
    k["Seri"] == yeni_kayit["Seri"]
    for k in st.session_state.metrajli_urunler
)

if st.button("Ürünü Kaydet"):
    if tekrar_var_mi:
        st.warning("⚠️ Bu ürün zaten kayıtlı!")
    else:
        st.session_state.metrajli_urunler.append(yeni_kayit)
        st.success("✅ Ürün başarıyla eklendi.")

# Listeleme ve filtre
st.subheader("📋 Ürün Listesi")

filtre_urun = st.selectbox("Ürün türüne göre filtrele", ["Tümü"] + list(RENK_KODLARI.keys()))

data = st.session_state.metrajli_urunler

if filtre_urun != "Tümü":
    data = [d for d in data if d["Ürün"] == filtre_urun]

# Renkli tablo oluştur
# Renkli tablo oluştur
if data:
    df = pd.DataFrame(data)
    if "Renk" in df.columns:
        def renk_format(row):
            color = row["Renk"]
            return [f"background-color: {color}" for _ in row]

        st.dataframe(df.drop(columns=["Renk"]).style.apply(renk_format, axis=1))
    else:
        st.dataframe(df)
else:
    st.info("Henüz ürün girilmedi.")
