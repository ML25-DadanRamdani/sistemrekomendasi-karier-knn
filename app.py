import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px

class CareerRecommendationApp:
    def __init__(self):
        # Konfigurasi halaman
        st.set_page_config(
            page_title="Sistem Rekomendasi Karier",
            page_icon="🤖",
            layout="wide"
        )

        # CSS custom
        self.add_custom_css()

        # Database skill
        self.career_skills = {
            "Software Engineer": ["Pemrograman (Python, Java, C++)", "Struktur Data & Algoritma", "Framework (React, Django, dll.)", "Database (SQL, NoSQL)", "Version Control (Git)"],
            "Data Scientist": ["Statistika & Probabilitas", "Machine Learning", "Python (Pandas, NumPy)", "SQL", "Visualisasi Data (Tableau, Matplotlib)"],
            "UI/UX Designer": ["Prinsip Desain Visual", "User Research", "Wireframing & Prototyping", "Tools (Figma, Sketch)", "User Empathy"],
            "IT Project Manager": ["Manajemen Proyek (Agile, Scrum)", "Manajemen Risiko", "Anggaran & Jadwal", "Komunikasi & Kepemimpinan", "Tools (Jira, Trello)"],
            "Database Administrator": ["Administrasi Database (MySQL, PostgreSQL)", "SQL Lanjutan", "Backup & Recovery", "Keamanan Database", "Performa Tuning"],
            "Network Engineer": ["Protokol Jaringan (TCP/IP)", "Konfigurasi Router & Switch", "Keamanan Jaringan (Firewall)", "Sertifikasi (CCNA)", "Monitoring Jaringan"],
            "DevOps Engineer": ["CI/CD Pipelines (Jenkins, GitLab)", "Containerization (Docker, Kubernetes)", "Cloud Computing (AWS, Azure)", "Scripting (Bash, Python)", "Infrastructure as Code (Terraform)"],
            "QA Engineer": ["Manual & Automated Testing", "Pembuatan Skenario Uji", "Tools (Selenium, Cypress)", "API Testing", "Bug Tracking (Jira)"]
        }

        # Load model & scaler
        self.model, self.scaler = self.load_model_and_scaler()

        # Load dataset
        self.df = self.load_dataset()

    def add_custom_css(self):
        st.markdown("""
        <style>
            .stForm [data-testid="stFormSubmitButton"] button {
                background-color: #FF4B4B; color: white; border: none;
            }
            .stForm [data-testid="stFormSubmitButton"] button:hover {
                background-color: #D63434; color: white; border: none;
            }
            .sidebar-title {
                font-size: 22px; font-weight: bold; color: #2E4053; margin-bottom: 10px;
            }
            .sidebar-subheader {
                font-size: 18px; font-weight: bold; color: #5D6D7E; margin-top: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

    @st.cache_resource
    def load_model_and_scaler(_self=None):
        try:
            with open('model_knn.pkl', 'rb') as file:
                model = pickle.load(file)
            with open('scaler.pkl', 'rb') as file:
                scaler = pickle.load(file)
            return model, scaler
        except FileNotFoundError:
            st.error("File model atau scaler tidak ditemukan.")
            return None, None

    @st.cache_data
    def load_dataset(_self=None):
        try:
            df = pd.read_csv('dataset_bersih.csv')
            return df
        except FileNotFoundError:
            st.error("File dataset 'dataset_bersih.csv' tidak ditemukan.")
            return None

    def show_recommendation_page(self):
        st.title("👨‍💻 Sistem Rekomendasi Karier Interaktif")

        with st.expander("Lihat Petunjuk Penggunaan", expanded=True):
            st.write("Berikan penilaian pada setiap pernyataan dengan skala 1 sampai 5.")
            col1, col2 = st.columns([1, 4])
            with col1: st.markdown("### 1️⃣ Pemula")
            with col2: st.info("Hanya tahu teori, belum bisa praktik mandiri.")
            col1, col2 = st.columns([1, 4])
            with col1: st.markdown("### 2️⃣ Cukup Paham")
            with col2: st.info("Bisa praktik dengan panduan atau tutorial.")
            col1, col2 = st.columns([1, 4])
            with col1: st.markdown("### 3️⃣ Mampu")
            with col2: st.success("Bisa mengerjakan tugas dasar secara mandiri.")
            col1, col2 = st.columns([1, 4])
            with col1: st.markdown("### 4️⃣ Mahir")
            with col2: st.success("Bisa mengerjakan tugas kompleks dengan sedikit referensi.")
            col1, col2 = st.columns([1, 4])
            with col1: st.markdown("### 5️⃣ Sangat Mahir")
            with col2: st.warning("Mampu bekerja secara profesional dan mandiri.")

        st.sidebar.markdown('<p class="sidebar-subheader">📊 Ukur Minat Anda</p>', unsafe_allow_html=True)

        if self.model and hasattr(self.model, 'feature_names_in_'):
            feature_names = self.model.feature_names_in_
        elif self.df is not None:
            feature_names = self.df.drop('target_karier', axis=1).columns
        else:
            feature_names = ["skor_pemrograman", "skor_analisis_data", "skor_jaringan", "skor_desain", "skor_manajemen"]

        with st.sidebar.form(key='recommendation_form'):
            user_input = {}
            for feature in feature_names:
                label = feature.replace('_', ' ').replace('skor', '').title()
                user_input[feature] = st.slider(label, 1.0, 5.0, 3.0, 0.5)
            submit_button = st.form_submit_button(label='Dapatkan Rekomendasi Saya!')

        if self.model and self.scaler and submit_button:
            with st.spinner("Menganalisis profil Anda..."):
                input_array = np.array(list(user_input.values())).reshape(1, -1)
                input_scaled = self.scaler.transform(input_array)

                prediction = self.model.predict(input_scaled)
                probabilities = self.model.predict_proba(input_scaled)

            st.success("### Rekomendasi Karier Utama Untuk Anda:")
            st.markdown(f"## **{prediction[0]}**")

            predicted_career = prediction[0]
            if predicted_career in self.career_skills:
                with st.expander(f"**Lihat Skill Utama yang Dibutuhkan untuk Menjadi {predicted_career}**"):
                    for skill in self.career_skills[predicted_career]:
                        st.markdown(f"- {skill}")

            st.write("---")
            st.subheader("Alternatif Karier Lainnya:")
            prob_df = pd.DataFrame({'Karier': self.model.classes_, 'Kecocokan (%)': probabilities[0] * 100})
            prob_df = prob_df.sort_values(by='Kecocokan (%)', ascending=False)
            top_alternatives = prob_df[prob_df['Karier'] != predicted_career].head(3)

            for _, row in top_alternatives.iterrows():
                st.write(f"- **{row['Karier']}** (Tingkat Kecocokan: {row['Kecocokan (%)']:.2f}%)")

    def show_exploration_page(self):
        st.title("📊 Eksplorasi Dataset Latihan Model")
        if self.df is not None:
            st.header("Sampel Data")
            st.dataframe(self.df.head())

            with st.expander("1. Lihat Distribusi Karier"):
                career_counts = self.df['target_karier'].value_counts().reset_index()
                career_counts.columns = ['Karier', 'Jumlah Responden']
                fig = px.bar(career_counts, x='Karier', y='Jumlah Responden', title='Distribusi Jumlah Responden per Karier', text_auto=True)
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("2. Lihat Statistik Skor Keahlian"):
                st.dataframe(self.df.describe())

            with st.expander("3. Lihat Distribusi Skor per Karier (Boxplot)"):
                df_melted = self.df.melt(id_vars='target_karier', var_name='jenis_keahlian', value_name='skor')
                fig = px.box(df_melted, x='target_karier', y='skor', color='target_karier',
                             title='Distribusi Skor Keahlian untuk Setiap Karier')
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("4. Lihat Korelasi Antar Keahlian"):
                df_scores = self.df.drop('target_karier', axis=1)
                corr_matrix = df_scores.corr()
                fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                                title='Heatmap Korelasi Antar Skor Keahlian', color_continuous_scale='viridis')
                st.plotly_chart(fig, use_container_width=True)

    def show_about_page(self):
        st.title("📄 Tentang Proyek Skripsi Ini")
        st.write("---")
        col1, col2 = st.columns([2, 1.5], gap="large")

        with col1:
            st.header("📖 Judul Proyek")
            st.info("**SISTEM REKOMENDASI KARIER BERDASARKAN MINAT DAN KEAHLIAN MENGGUNAKAN ALGORITMA K-NEAREST NEIGHBOR**")
            st.header("⚙️ Metodologi")
            st.markdown("- **Algoritma**: K-Nearest Neighbors (KNN).\n- **Data**: Dilatih menggunakan 297 sampel data minat.\n- **Tools**: Python, Streamlit, Pandas, Scikit-learn.")

        with col2:
            st.header("👨‍💻 Pengembang & Institusi")
            st.markdown("- **Nama**: Dadan Ramdani (21110052)\n- **Program Studi**: Teknik Informatika S1\n- **Institusi**: STMIK Mardira Indonesia\n- **Tahun**: 2025")

    def run(self):
        st.sidebar.markdown('<p class="sidebar-title">🧭 Navigasi</p>', unsafe_allow_html=True)
        page = st.sidebar.radio("Pilih Halaman:", ["Rekomendasi Karier", "Eksplorasi Data", "Tentang Proyek"],
                                label_visibility="collapsed")

        if page == "Rekomendasi Karier":
            self.show_recommendation_page()
        elif page == "Eksplorasi Data":
            self.show_exploration_page()
        elif page == "Tentang Proyek":
            self.show_about_page()


if __name__ == "__main__":
    app = CareerRecommendationApp()
    app.run()
