import requests
import json
import os
from datetime import datetime

# Proje detayları
project_data = {
    "project_title": "Ornek Proje İsmi",
    "index": 1,
    "estimated_time": "",
    "metadata": {
        "description": "Kısa Açıklama",
        "company": "Şirket",
        "department": "Departman",
        "year": 2025,
        "languages": []
    },
    "project_description": "1. Proje Adı\nInsightTrack – AI Destekli Görev ve Verimlilik Takip Sistemi\n2. Proje Özeti\nInsightTrack, bireysel ve kurumsal kullanıcıların üretkenliğini artırmak için geliştirilmiş AI destekli görev ve zaman yönetim sistemidir. Sistem, kullanıcı alışkanlıklarını analiz ederek görev önceliklendirmesi ve verimlilik önerileri sunar. Masaüstü ve web platformlarında çalışır ve Llama 3.2 modeli ile görev sınıflandırma, özetleme ve raporlama yapar.\n3. Amaç ve Hedefler\n• Amaç: Zaman yönetimini optimize ederek görev tamamlama oranlarını artırmak.\n• Hedefler:\n o Görevlerin AI ile kategorize edilmesi\n o Tamamlama süresinin %25 azaltılması\n o Haftalık otomatik verimlilik raporları\n o 3 ay içinde MVP sürümü\n4. Proje Kapsamı\n• Dahil: Web/masaüstü istemci (React + Electron), AI görev sınıflandırma, RESTful API, PostgreSQL, raporlama ekranı\n• Dış: Mobil uygulama, kurumsal lisans, takvim entegrasyonu\n5. Sistem Mimarisi\nKullanıcı → API → AI Modülü → Veritabanı → Raporlama\n• Frontend: Görev ekleme, öneriler\n• Backend: CRUD, kimlik doğrulama\n• AI Modülü: Görev sınıflandırma ve özetleme\n• Veritabanı: Kullanıcı, görev, etkileşim\n• Raporlama: Haftalık PDF\n6. İşlevsel Gereksinimler\n• Kullanıcı girişi (JWT)\n• Görev ekleme ve analizi\n• Haftalık PDF rapor\n• Görev öncelik önerisi\n7. Zaman Çizelgesi\n• Planlama & Tasarım: 2 hafta (1–14 Kasım 2025)\n• Backend: 3 hafta (15 Kasım–5 Aralık)\n• Frontend: 3 hafta (6–26 Aralık)\n• Model Entegrasyonu: 2 hafta (27 Aralık–10 Ocak)",
    "possible_solution": "Opsiyonel ",
    "team": [
        {
            "employee_id": "e42",
            "name": "Jane Smith",
            "skills": ["web", "react", "restapi"],
            "department": "Frontend"
        },
        {
            "employee_id": "e44",
            "name": "Bob Johnson",
            "skills": ["python", "react", "docker"],
            "department": "Full Stack"
        },
        {
            "employee_id": "e14",
            "name": "John Doe",
            "skills": ["python", "LLM", "NLP"],
            "department": "AI"
        }
    ],
    "tasks": []
}

# API'nin beklediği format

payload = {
    "json_input": project_data,  # ✅ json_input anahtarı içinde gönderin
    "project_key": "INSIGHT",
    "use_model": True  # False = Direkt Parse (hızlı), True = Model + Parse
}

# Ngrok URL
url = "https://252b70dec01e.ngrok-free.app/api/generate"

# API isteği gönder
try:
    print("📤 API'ye istek gönderiliyor...")
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    
    # Başarılı sonuç
    if result.get("success"):
        print(f"\n✅ İşlem başarılı!")
        print(f"📊 Toplam Task: {result.get('total_tasks', 0)}")
        print(f"🔧 Yöntem: {result.get('method', 'N/A')}")
        
        # Task planını göster (opsiyonel)
        if "task_plan" in result:
            print("\n📝 Oluşturulan Task Planı:")
            print(result["task_plan"][:500] + "..." if len(result["task_plan"]) > 500 else result["task_plan"])
        
        # Jira JSON'u kaydet
        jira_json = result.get("jira_json", {})
        if jira_json:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/jira_{timestamp}.json"
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(jira_json, f, indent=4, ensure_ascii=False)
            
            print(f"\n💾 Jira JSON kaydedildi: {output_file}")
            
            # İlk 2 task'ı örnek olarak göster
            tasks = jira_json.get("tasks", [])
            if tasks:
                print(f"\n📋 Örnek Task (ilk 2/{len(tasks)}):")
                for i, task in enumerate(tasks[:2], 1):
                    print(f"\nTask {i}:")
                    print(f"  Epic: {task.get('epic_name', 'N/A')}")
                    print(f"  Başlık: {task['fields'].get('summary', 'N/A')}")
                    print(f"  Atanan: {task['fields'].get('assignee', {}).get('name', 'N/A')}")
                    print(f"  Öncelik: {task['fields'].get('priority', {}).get('name', 'N/A')}")
                    print(f"  Deadline: {task['fields'].get('duedate', 'N/A')}")
    else:
        print(f"\n⚠️ İşlem tamamlandı ama hata var:")
        print(json.dumps(result, indent=4, ensure_ascii=False))

except requests.exceptions.Timeout:
    print("⏱️ Timeout hatası: API yanıt vermedi (120 saniye)")
except requests.exceptions.RequestException as e:
    # Hata durumunda klasöre kaydet
    os.makedirs("hatalar", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_file = f"hatalar/hata_{timestamp}.txt"
    
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(f"Hata: {str(e)}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}\n\n")
        f.write("Response:\n")
        if 'response' in locals():
            f.write(response.text)
    
    print(f"❌ Hata oluştu, detaylar {error_file} dosyasına kaydedildi.")
    print(f"Hata: {str(e)}")