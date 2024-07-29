import datetime
import pandas as pd
import streamlit as st
import os
import json
import uuid

# Türkiye Saat Dilimi
turkey_tz = 'Europe/Istanbul'
now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=3)))

# Günün Tarih ve Saati
saat = st.container()
saat.text(f"🕘 {now.strftime('%d-%m-%Y')} / {now.strftime('%H:%M:%S')}")

# Dosya Yolu
tasks_file = "tasks.json"

# Dosyayı Yükle
if not os.path.exists(tasks_file):
    with open(tasks_file, "w") as f:
        json.dump([], f)

# Veri Yapısı
with open(tasks_file, "r") as f:
    tasks = json.load(f)

# Raporu Oluştur
completed_tasks = [task for task in tasks if task["completed"]]
pending_tasks = [task for task in tasks if not task["completed"]]

# Durum container'ları
durum_container = st.container()
# Görev durumu kontrolü
if pending_tasks:
    durum_container.warning(f"🔴 {len(pending_tasks)} kadar tamamlanmamış görevleriniz var. !")
else:
    durum_container.success("✅ Tamamlanmamış görevleriniz yok.")

# Sayfa Başlığı
st.image("ceri.png")

# Seçim Kutusu
option = st.selectbox("Seçenekler", ["Görevler", "Rapor"])

def mark_task_completed(task_id):
    global tasks
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
    with open(tasks_file, "w") as f:
        json.dump(tasks, f)
    st.balloons()
    st.experimental_rerun()

def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    with open(tasks_file, "w") as f:
        json.dump(tasks, f)
    st.experimental_rerun()

if option == "Rapor":
    st.markdown("<h5 style='text-align: center;'>Görev Durumu</h5>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(f"<div style='text-align: center; background-color: #d4edda; border-radius: 10px; padding: 5px;'><h11>💪Tamamlanmış Görevler</h11><p style='font-size: 18px;'>{len(completed_tasks)}</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='text-align: center; background-color: #f8d7da; border-radius: 10px; padding: 5px;'><h11>😴Bekleyen Görevler</h11><p style='font-size: 18px;'>{len(pending_tasks)}</p></div><br>", unsafe_allow_html=True)
    
    # Tamamlanmış Görevler Listesi
    st.markdown("#### ✅ Tamamlanmış Görevler")
    for task in completed_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<div style='border-radius: 8px; padding: 10px; margin: 5px; background-color: #d4edda; border-left: 5px solid #28a745;'>{task['task']}<br>{task['description']}<br>{task['date']}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("Sil", key=f"del-{task['id']}"):
                delete_task(task["id"])

    # Bekleyen Görevler Listesi
    st.markdown("#### 🕘 Bekleyen Görevler")
    for task in pending_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<div style='border-radius: 8px; padding: 10px; margin: 5px; background-color: #f8d7da; border-left: 5px solid #dc3545;'>{task['task']}<br>{task['description']}<br>{task['date']}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("Sil", key=f"del-{task['id']}"):
                delete_task(task["id"])

else:
    # Yeni Görev Ekleme
    st.markdown("### Yeni Plan Ekle")
    new_task = st.text_input("Yeni Plan")
    new_description = st.text_input("Açıklama")
    new_date = st.date_input("Tarih", datetime.date.today())

    if st.button("Ekle"):
        if new_task:
            task = {
                "id": str(uuid.uuid4()),
                "task": new_task,
                "description": new_description,
                "date": new_date.strftime('%d-%m-%Y'),
                "completed": False
            }
            st.warning("Plan Eklendi.")
            
            tasks.append(task)
            with open(tasks_file, "w") as f:
                json.dump(tasks, f)
            
            st.experimental_rerun()

# CSS ile Daha İyi UI
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 7px 15px;
        text-align: center;
        font-size: 9px;
        margin: 4px 2px;
        border-radius: 8px;
    }
    .stTextInput > div > div > input {
        padding: 10px;
        font-size: 16px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

seç = st.container() 
with seç:
    # Seçim kutusunu oluştur
    seçim = st.selectbox("📚 Bir Hikaye Seç", ["Seçimin;", "🔞 Rıza'nın Hikayesi", "🔪 Ceri'nin Hikayesi"])

    # Seçilen seçenek "🔞 Rıza'nın Hikayesi" ise, iframe'i göster
    if seçim == "🔞 Rıza'nın Hikayesi":
        st.markdown("""<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/4jXGg7QYHA2eGLXqHRYY01?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>""", unsafe_allow_html=True)
    elif seçim == "🔪 Ceri'nin Hikayesi":
        st.markdown("""<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/2D6r8QJKiDXijio2QycK3u?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>""", unsafe_allow_html=True)
    elif seçim == "Seçimin;":
        st.info("🐣 Çalışırken biraz rahatlamak istersen hikayelerden birini seçmelisin.")
    else:
        st.warning("Beni delirteceksin.")
