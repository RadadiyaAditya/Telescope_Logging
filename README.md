# 🔭 Telescope Logging System

A **web-based Telescope Logging System** built with **Django (Framework)** and **PostrgreSQL (Database)** to facilitate **astronomical observation logging**. This system records essential observational data, including start and end timestamps, telescope configurations, environmental conditions, and instrumentation details.


## 🚀 Features

- **Log Observations** with Start & End Times (UTC &LST)
- **Database Integration** using PostgreSQL(Deployment) & SQLite (Profuction)
- **Django Templates for UI**
- **WebSocket for Live Data Streaming**
- **Real-time LST & UTC Updates**


## ⚙️ Tech Stack

- **Backend:** Django 🚀
- **Frontend:** HTML, CSS, JavaScript, Django Templates
- **Database:** PostgreSQL / SQLite
- **Real-time Communication:** Django Channels (WebSockets)
- **Version Control:** Git & GitHub

## Diagram
![Project Diagram](assets/screenshot.png)


## 🛠️ Installation

### 1️. Clone the Repository

```bash
  git clone https://github.com/RadadiyaAditya/Telescope_Logging.git
  cd Telescope_Logging
```
### 2. Virtual Enviroment Setup

```bash
  python -m venv venv
  source venv/bin/activate  # On macOS/Linux
  venv\Scripts\activate # On Windows
```
### 3. Install Dependencies

```bash
  pip install -r requirements.txt
```
### 4. Start Server

```bash
  daphne -b 0.0.0.0 -p 8000 telescope_log.asgi:application
```
Access the Telescope Logging System at:
👉 http://127.0.0.1:8000/


## 🖥️ API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/log/start` | Start an observation session |
| `POST` | `/log/end` | End an observation session |
| `GET`  | `/logs` | Retrieve all logs |
| `GET`  | `/log/{id}` | Retrieve a specific log entry |

Use [FastAPI Swagger UI](http://127.0.0.1:8000/docs) for API testing.

---

## 🎯 Future Enhancements
- 🔹 **Authentication & User Management**
- 🔹 **Data Export (CSV, JSON)**
- 
---

## 🤝 Contributing
Feel free to fork this repository and submit pull requests! Contributions are always welcome. 🚀

---

## 🛡️ License
This project is licensed under the **MIT License**.

---

## 📞 Contact
For any queries, reach out to:  
👤 **Aditya Radadiya**  
📧 **adityaradadiya294@gmail.com**  
🔗 [GitHub Profile](https://github.com/RadadiyaAditya)

---

**Happy Logging! 🌌**

