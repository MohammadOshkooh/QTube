# 🎥 QTube -  A **video-sharing platform**

## 📌 Introduction
QTube is a **video-sharing platform** that allows users to:
- **Upload** and share their videos.
- Watch videos uploaded by other users.
- Find videos using an **advanced search system**.
- Interact with content through **comments and likes**.
- Browse videos categorized into different **genres** like education, entertainment, etc.

**Note:** This project was developed as part of a web development course.

## ⚙️ Key Features
✅ **Video Upload System:** Users can upload videos in any format.

✅ **Video Format Conversion:** Non-MP4 formats are processed in a background job and converted to MP4.

✅ **Video Streaming:** Watch videos online.

✅ **Search System:** Efficient video search functionality.

✅ **Comments & Likes:** Users can leave comments and rate videos.

✅ **Video Categorization:** Content is classified into various categories.

## 🏗️ Technologies Used
🚀 **Framework:** Django + Django REST Framework  
🐍 **Web Server:** Gunicorn  
🐳 **Containerization:** Docker & Docker Compose  
🎭 **Admin Panel:** django-jazzmin  
🔐 **Authentication:** rest_framework_simplejwt  
📜 **Error Logging Middleware:** Logs errors for debugging  
🔄 **Password Recovery:** Temporary token stored in Redis  

## 🏗️ Docker Containers
```yaml
services:
  app:
  redis:
  postgres:
  celery_worker:
  nginx:
```

## 🚀 Project Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/MohammadOshkooh/QTube.git
   cd QTube
   ```
2. Configure environment variables.
3. Run Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Access the project at `http://localhost:8002`.

## 🎯 Contribution
To contribute, feel free to submit a Pull Request or report issues in the Issues section. 🙌

---
🚀 Built with Django ❤️
