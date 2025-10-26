# PlanLLaMA Backend API

**Modern proje yönetimi için Flask tabanlı REST API**

PlanLLaMA Backend, proje, görev ve çalışan yönetimi için geliştirilmiş hafif ve esnek bir API sunucusudur. Hızlı geliştirme için SQLite, ölçeklenebilir üretim ortamları için PostgreSQL desteği sunar.

🔗 **GitHub:** [hubble658/planllama-backend](https://github.com/hubble658/planllama-backend)

---

## ✨ Özellikler

- **RESTful API**: Projeler, görevler ve çalışanlar için eksiksiz CRUD operasyonları
- **İstatistikler ve Analitik**: Proje durumu, çalışan iş yükü ve görev dağılımı raporları
- **Esnek Veritabanı**: Geliştirme için SQLite, production için PostgreSQL
- **CORS Desteği**: Frontend entegrasyonu için hazır
- **Kolay Kurulum**: Minimal konfigürasyon ile hızlıca başlayın

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- pip (Python paket yöneticisi)

### Kurulum

```bash
# Projeyi klonlayın
git clone https://github.com/hubble658/planllama-backend.git
cd planllama-backend

# Sanal ortam oluşturun
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Veritabanını başlatın
python init_db.py --seed  # Örnek verilerle

# Sunucuyu çalıştırın
python app.py
```

API artık `http://localhost:5000` adresinde çalışıyor! 🎉

---

## 🔧 Konfigürasyon

`.env.example` dosyasını `.env` olarak kopyalayın ve ihtiyacınıza göre düzenleyin:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key

# SQLite (Varsayılan - Geliştirme için önerilir)
DATABASE_URL=sqlite:///planllama.db

# PostgreSQL (Production için)
# DATABASE_URL=postgresql://user:pass@localhost:5432/planllama

CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 📚 API Kullanımı

### Temel Endpoint'ler

| Kaynak | Endpoint | Açıklama |
|--------|----------|----------|
| **Projeler** | `GET /api/projects` | Tüm projeleri listele |
| | `POST /api/projects` | Yeni proje oluştur |
| | `GET /api/projects/<id>/stats` | Proje istatistikleri |
| **Görevler** | `GET /api/tasks` | Tüm görevleri listele |
| | `GET /api/tasks?enrich=true` | Görevleri detaylı getir (assignee/project isimleriyle) |
| | `PATCH /api/tasks/<id>/status` | Görev durumunu güncelle |
| **Çalışanlar** | `GET /api/employees` | Tüm çalışanları listele |
| | `GET /api/employees/<id>/workload` | Çalışan iş yükü analizi |

### Örnek İstekler

**Yeni Proje Oluşturma:**
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "p06",
    "name": "Mobil Uygulama",
    "status": "Planning",
    "priority": "high"
  }'
```

**Görev Durumu Güncelleme:**
```bash
curl -X PATCH http://localhost:5000/api/tasks/t01/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'
```

---

## 🗄️ Veri Modeli

### Proje (Project)
- `project_id`: Benzersiz kimlik
- `name`: Proje adı
- `status`: Planning, In Progress, On Hold, Completed
- `priority`: low, medium, high, critical

### Görev (Task)
- `task_id`: Benzersiz kimlik
- `assignee_id`: Atanan çalışan
- `project_id`: Bağlı proje
- `estimatedHours`: Tahmini süre
- `status`: Pending, In Progress, Completed, Blocked

### Çalışan (Employee)
- `employee_id`: Benzersiz kimlik
- `user_role`: pm (Proje Yöneticisi) veya executor (Geliştirici)
- `capacity_hours_per_week`: Haftalık kapasite
- `skills`: Yetenekler ve seviyeleri (JSON)

---

## 🛠️ Geliştirme

### Veritabanı İşlemleri

```bash
# Veritabanını sıfırla
python init_db.py

# Örnek verilerle doldur
python init_db.py --seed

# Flask-Migrate ile migrasyon (Production için)
flask db migrate -m "Yeni özellik"
flask db upgrade
```

### Test

```bash
python test_api.py
```

---

## 🌐 Production Deployment

### Gunicorn ile

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker ile

```bash
docker build -t planllama-backend .
docker run -p 5000:5000 planllama-backend
```

---

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır! Büyük değişiklikler için önce bir issue açarak ne değiştirmek istediğinizi tartışın.

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

---

**Not:** Bu proje hızlı geliştirme ve prototipleme için optimize edilmiştir. Production kullanımında güvenlik best practice'lerini uygulamayı unutmayın.