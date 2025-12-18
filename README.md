
# 📅 Event Scheduler & Resource Management System

A web-based Event Scheduling and Resource Management system built using **Flask** and **SQLite**.  
This application helps users create events, allocate resources, and manage schedules efficiently with a clean UI.

---

## 🚀 Features

- 🔐 User Authentication (Signup & Login)
- 📅 Create, Edit, Delete Events
- 🕒 Schedule events with start & end date-time
- 🧾 Event descriptions support
- 📦 Manage Resources
- 🔗 Allocate Resources to Events
- 📊 Dashboard with statistics
- ⚠️ Conflict section (UI ready)
- 📑 Reports page
- 🎨 Responsive UI using HTML & CSS

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** Session-based login
- **Tools:** VS Code, Git

---

## 📁 Project Structure

```

Pro1/
│
├── app.py
├── requirements.txt
├── instance/
│   └── app.db
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── events.html
│   ├── event_form.html
│   ├── resources.html
│   ├── resource_form.html
│   ├── allocations.html
│   ├── allocation_form.html
│   ├── conflicts.html
│   └── report.html
│
└── README.md

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-link>
cd Pro1
````

---

### 2️⃣ Create & Activate Virtual Environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
python app.py
```

OR

```bash
flask run
```

---

### 5️⃣ Open in Browser 🌐

```
http://127.0.0.1:5000
```

---

## 🔑 Default Pages

* `/` → Home Page
* `/signup` → User Registration
* `/login` → Login
* `/dashboard` → Dashboard
* `/events` → Events Management
* `/resources` → Resources
* `/allocations` → Allocations
* `/conflicts` → Conflicts
* `/report` → Report

---

## 🧠 Database

* SQLite database stored at:

  ```
  instance/app.db
  ```
* Automatically created on first run.

---

## 🧪 Future Enhancements

* ⚠️ Automatic conflict detection
* 📧 Email notifications
* 📊 Advanced reports
* 👥 Role-based access
* 📆 Calendar view

---
