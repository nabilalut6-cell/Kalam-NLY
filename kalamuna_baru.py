import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# 1. KONFIGURASI HALAMAN & DESIGN (CSS)
# ==========================================
st.set_page_config(
    page_title="Kalamuna - Maharah Kalam AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan elegan, modern, dan bernuansa edukasi islami (Emerald & Gold)
st.markdown("""
    <style>
    /* Mengubah warna dasar background dan font */
    .stApp {
        background-color: #f7f9f8;
    }
    
    /* Styling Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d47a1;
        background: linear-gradient(180deg, #064e3b 0%, #022c22 100%);
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] label {
        color: #fef08a !important;
        font-weight: 600;
    }
    
    /* Main Header Styling */
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #064e3b;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .main-subtitle {
        text-align: center;
        color: #4b5563;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    
    /* Welcome Card */
    .welcome-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #d97706;
        margin-bottom: 20px;
    }
    
    /* Custom Button */
    .stButton>button {
        background-color: #d97706 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #b45309 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. PROMPT & DATA KONTEKS (PERSONA & MATERI)
# ==========================================
MATERI_DETAILS = {
    "Al-Hayah al-Yaumiyah (الحياة اليومية)": {
        "deskripsi": "Materi yang membahas tentang aktivitas sehari-hari mulai dari bangun tidur hingga tidur kembali.",
        "topik_ar": "الحياة اليومية (Aktivitas Sehari-hari)"
    },
    "Al-Mihnah (المهنة)": {
        "deskripsi": "Materi yang membahas jenis-jenis profesi/pekerjaan, cita-cita, dan tempat bekerja.",
        "topik_ar": "المهنة (Profesi / Pekerjaan)"
    },
    "Al-Usroh (الأسرة)": {
        "deskripsi": "Materi yang membahas tentang anggota keluarga, silsilah keluarga, dan kegiatan bersama keluarga.",
        "topik_ar": "الأسرة (Kehidupan Keluarga)"
    }
}

PERSONA_DETAILS = {
    "Ustadz Khalid": {
        "karakter": "seorang guru laki-laki yang tegas namun ramah, sangat terstruktur, membimbing secara bertahap, dan sering memberikan pujian seperti 'Mumtaz!' atau 'Ahsant!'.",
        "avatar": "👨‍🏫"
    },
    "Ustadzah Khaulah": {
        "karakter": "seorang guru perempuan yang sangat sabar, lembut, penuh kasih sayang, menggunakan pendekatan yang hangat, dan menyemangati dengan kata-kata manis seperti 'Thayyip ya talamidzi' atau 'Maa syaa Allah bagus sekali'.",
        "avatar": "👩‍🏫"
    }
}


# ==========================================
# 3. SIDEBAR INPUT (AUTHENTICATION & SETTING)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>💬 KALAMUNA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🔐 Akses Masuk")
    username = st.text_input("Nama Pengguna (Username)", placeholder="Masukkan nama Anda...")
    api_key = st.text_input("Google AI Studio API Key", type="password", placeholder="AIzaSy...")
    
    st.markdown("---")
    st.markdown("### 📚 Pengaturan Pembelajaran")
    
    pilihan_ustadz = st.selectbox("Pilih Guru Pendamping:", list(PERSONA_DETAILS.keys()))
    pilihan_materi = st.selectbox("Pilih Materi Kelas X:", list(MATERI_DETAILS.keys()))
    
    st.markdown("---")
    if st.button("🔄 Reset & Keluar Sesi", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ==========================================
# 4. LOGIKA UTAMA APLIKASI
# ==========================================

if not username or not api_key:
    st.markdown("<h1 class='main-title'>كَلَامُنَا — KALAMUNA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='main-subtitle'>Media Pembelajaran Interaktif Maharah Kalam Kelas X Madrasah Aliyah</p>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="welcome-card">
        <h3>Ahlan wa Sahlan di Kalamuna! 👋</h3>
        <p>Aplikasi ini dirancang khusus untuk membantumu melatih keterampilan berbicara (<b>Maharah Kalam</b>) menggunakan bahasa Arab secara interaktif yang didukung oleh teknologi Kecerdasan Buatan (AI).</p>
        <p><b>Langkah Mudah untuk Memulai:</b></p>
        <ol>
            <li>Masukkan <b>Nama Pengguna</b> di panel sebelah kiri.</li>
            <li>Masukkan <b>Google AI Studio API Key</b> Anda yang valid.</li>
            <li>Pilih Guru Pendamping (Ustadz/Ustadzah) dan materi yang ingin dipelajari.</li>
            <li>Mulai percakapan interaktif!</li>
        </ol>
        <small style="color: #6b7280;">*Catatan: Sesi percakapan Anda aman dan riwayat akan tersimpan selama tab browser ini aktif.</small>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"<h2 class='main-title'>Sesi Percakapan Kalamuna</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='main-subtitle'>Siswa: <b>{username}</b> | Pendamping: <b>{pilihan_ustadz}</b> | Materi: <b>{pilihan_materi}</b></p>", unsafe_allow_html=True)
    
    system_prompt = (
        f"Anda adalah {pilihan_ustadz}, {PERSONA_DETAILS[pilihan_ustadz]['karakter']}. "
        f"Tugas utama Anda adalah menjadi partner latihan bicara bahasa Arab (Maharah Kalam) untuk siswa bernama {username} yang berada di kelas X Madrasah Aliyah. "
        f"Fokus topik percakapan saat ini adalah tentang '{MATERI_DETAILS[pilihan_materi]['topik_ar']}'. "
        "Aturan percakapan:\n"
        "1. Gunakan bahasa Arab yang sederhana, jelas, dan sesuai dengan tingkat kemampuan anak SMA/MA kelas 10 (gunakan harakat pada kata-kata penting jika diperlukan).\n"
        "2. Jangan memberikan teks balasan yang terlalu panjang agar siswa tidak bingung dan mudah merespons kembali.\n"
        "3. Berikan tanggapan, ajukan pertanyaan pancingan satu per satu yang berkaitan dengan topik agar percakapan terus mengalir berjalan dua arah.\n"
        "4. Jika siswa melakukan kesalahan dalam struktur kalimat atau kosakata (baik mereka merespons dengan bahasa Arab yang keliru atau menyelipkan bahasa Indonesia), berikan koreksi secara lembut, edukatif, lalu contohkan cara pengucapan yang benar dalam bahasa Arab, kemudian lanjutkan obrolan.\n"
        "5. Jawablah dengan menggunakan karakter kepribadian Anda yang telah ditentukan."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        intro_greetings = {
            "Ustadz Khalid": f"Ahlan wa sahlan ya {username}! Ismi Ustadz Khalid. Selamat datang di kelas Maharah Kalam. Hari ini kita akan berlatih percakapan tentang {pilihan_materi}. Kaifa haluk? Mari kita mulai pembicaraan kita, siap?",
            "Ustadzah Khaulah": f"Ahlan bika ya talamidzi al-aziz, {username} 🌸 Ismi Ustadzah Khaulah. Senang sekali bisa menemani kamu belajar hari ini. Kita akan mengobrol santai seputar {pilihan_materi} menggunakan bahasa Arab ya. Kaifa haluk hari ini?"
        }
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": intro_greetings[pilihan_ustadz],
            "avatar": PERSONA_DETAILS[pilihan_ustadz]['avatar']
        })

    # 🌟 KUNCI PERBAIKAN: Ikat client dan session ke dalam session_state agar tidak ter-destroy saat rerun
    if "gemini_client" not in st.session_state:
        try:
            st.session_state.gemini_client = genai.Client(api_key=api_key)
        except Exception as e:
            st.error(f"Gagal inisialisasi API Client: {e}")
            st.stop()

    if "chat_session" not in st.session_state:
        try:
            st.session_state.chat_session = st.session_state.gemini_client.chats.create(
                model="models/gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
            )
        except Exception as e:
            st.error(f"Gagal membuat sesi obrolan: {e}")
            st.stop()

    # Tampilkan Riwayat
    for message in st.session_state.messages:
        avatar_icon = message.get("avatar", "👤")
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    # Logika Input Chat
    if user_input := st.chat_input("Tulis pesan bahasa Arab atau respons kamu di sini..."):
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
            
        st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "👤"})
        
        try:
            with st.spinner(f"{pilihan_ustadz} sedang mengetik balasan..."):
                response = st.session_state.chat_session.send_message(user_input)
                bot_reply = response.text
                
            with st.chat_message("assistant", avatar=PERSONA_DETAILS[pilihan_ustadz]['avatar']):
                st.markdown(bot_reply)
                
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_reply, 
                "avatar": PERSONA_DETAILS[pilihan_ustadz]['avatar']
            })
            
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghubungi API Google Studio AI: {e}. Coba klik tombol 'Reset & Keluar Sesi' di sidebar lalu masukkan kembali API Key Anda.")