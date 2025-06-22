# 📚 AssignEase – Assignment Management Made Easy

AssignEase is a powerful web-based assignment management system built with **Django**. It simplifies how assignments are uploaded, distributed, and submitted between teachers and students. AssignEase provides section-wise assignment distribution, detailed reports, and a clean Bootstrap interface.

---

## 🚀 Features

- 🧑‍🏫 **Teacher Panel**
  - Upload assignments with file attachments.
  - View and download student submissions.
  - Automated grading according to marks
  - Generate reports by students, assignments, and subjects.

- 🎓 **Student Panel**
  - View only relevant assignments.
  - Submit assignments with file uploads.
  - Track submission status and results.

- 🗂 **Admin Panel**
  - Add/edit/delete subjects and sections.
  - Assign subjects to teachers.
  - Manage user accounts.

- 📈 **Smart Help**
  - AI chatbot
  - Google Gemini API
  - Resolve the queries of Students and Teachers

- 🎨 Responsive UI with **Bootstrap 5**

---

## 🛠️ Tech Stack

| Tech        | Description                         |
|-------------|-------------------------------------|
| Django      | Backend framework                   |
| MySQL       | Default or production database      |
| HTML/CSS    | Frontend templating                 |
| Bootstrap 5 | UI components                       |
| JavaScript  | Dynamic behavior on the frontend    |

---

## ✅ Getting Started

1. Clone the repository
   ```bash
    git clone https://github.com/yourusername/Assignease.git
    cd Assignease

2. Create a virtual environment
   ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate

3. Install dependencies
   ```bash
    pip install -r requirements.txt

4. Run migrations
   ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Create a superuser
   ```bash
    python manage.py createsuperuser

6. Start the server
    ```bash
      python manage.py runserver
  
Then go to http://127.0.0.1:8000/ in your browser.

## 📌 To-Do Features

 Assignment Grading

 Notifications (email/reminders)

 Gamification (leaderboards, badges)

 Chatbot Support for FAQ

## 🤝 Contributing

Fork this repo

Create your feature branch: git checkout -b feature/FeatureName

Commit your changes: git commit -m 'Add FeatureName'

Push to the branch: git push origin feature/FeatureName

Open a Pull Request

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.
