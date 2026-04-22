# 🚀 Intern Bridge - Internship Management System

## 📌 Overview

Intern Bridge is a custom ERP module developed using Odoo to manage the complete internship lifecycle. It provides a centralized platform for managing interns, assigning tasks, tracking performance, generating reports, and monitoring activities through an admin dashboard with role-based access control.

---

## 🎯 Problem Statement

Internship management in many organizations is often inefficient due to:

* Lack of centralized systems
* Informal task assignment
* Poor tracking of intern performance
* Limited visibility for mentors and administrators

---

## 💡 Solution

Intern Bridge provides a structured ERP-based solution that:

* Centralizes internship data
* Enables task-based workflow management
* Automates reporting and progress tracking
* Provides real-time dashboard insights
* Ensures secure access through role-based permissions

---

## ⚙️ Key Features

### 👤 User & Role Management

* Dedicated models for:

  * Students
  * Mentors
  * Guides
* Automatic user creation with role assignment
* Unique enrollment number generation
* Email validation for students

---

### 🔐 Role-Based Access Control

Custom security groups:

* InternBridge Student
* InternBridge Company Mentor
* InternBridge College Guide
* InternBridge Admin

Access control implemented using:

* Security groups (`groups.xml`)
* Access rights (`ir.model.access.csv`)
* Record rules (`record_rules.xml`)

---

### 📋 Task Log System (Core Feature ⭐)

* Mentors assign tasks to interns
* Interns log:

  * Work description
  * Hours spent
* Task lifecycle:

  * Draft → Assigned → Submitted → Approved/Rejected → Completed

#### Validations:

* Only mentor can assign tasks
* Only assigned student can submit work
* Student cannot be modified after assignment

---

### 🔄 Workflow Management

* Student: Submits assigned tasks
* Mentor: Assigns, approves, or rejects tasks
* Guide/Admin: Monitors overall progress

---

### 📊 Admin Dashboard (Key Highlight 🚀)

* Displays system-wide metrics:

  * Total Students
  * Internships
  * Tasks
  * Weekly Reports
  * Monthly Reports
  * Mentors & Guides

* Interactive navigation:

  * Direct access to records via dashboard actions

---

### 📝 Reporting System (QWeb PDF Reports ⭐)

* Weekly and Monthly reports generated dynamically
* Implemented using Odoo QWeb templating engine

#### Features:

* Downloadable PDF reports
* Structured and professional layout
* Real-time data aggregation
* Integrated with system workflow

#### Reports Included:

* Weekly Report (PDF)
* Monthly Report (PDF)

#### Technical Implementation:

* QWeb templates:

  * `weekly_report_template.xml`
  * `monthly_report_template.xml`
* XML-based report actions
* Dynamic data rendering from models

---

### 📈 Progress Tracking

* Automatic calculation of progress percentage
* Based on submitted reports and completed work

---

### 🎨 UI & Styling

* Custom dashboard styling using CSS
* Clean and structured user interface

---

### 🌐 Controllers

* Includes controller layer for handling web interactions
* Enables extensibility for future frontend integration

---

## 🛠️ Technical Implementation

* Framework: Odoo
* Language: Python
* Database: PostgreSQL
* ORM: Odoo ORM
* Frontend: XML Views + CSS
* Reporting: QWeb-based dynamic PDF generation
* Security: Groups, Access Control, Record Rules

---

## 🏗️ Module Structure

```
intern_bridge/
├── controllers/
├── data/
├── demo/
├── models/
│   ├── student.py
│   ├── mentor.py
│   ├── guide.py
│   ├── internship.py
│   ├── task_log.py
│   ├── weekly_report.py
│   ├── monthly_report.py
│   ├── internship_dashboard.py
├── views/
├── security/
│   ├── groups.xml
│   ├── ir.model.access.csv
│   ├── record_rules.xml
├── reports/
├── static/
│   ├── src/css/
├── __manifest__.py
```

---

## ▶️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/intern-bridge.git
```

2. Add module path in Odoo config:

```
addons_path = /path/to/custom_addons
```

3. Restart Odoo server

4. Install module from Apps menu

---

## 🌐 Usage Flow

1. Create Internship
2. Add Students, Mentors, Guides
3. Assign roles (security groups)
4. Mentor assigns tasks
5. Intern submits work
6. Mentor reviews (approve/reject)
7. Reports generated automatically
8. Admin monitors via dashboard

---

## 📸 Screenshots

(Add screenshots for:)

* Dashboard
* Task workflow
* Reports
* Role-based UI

---

## 🚀 Deployment

* Localhost (development)
* Cloud server (production-ready)
* Public demo using tunneling tools

---

## 🔮 Future Enhancements

* Email notifications
* Advanced analytics dashboard
* Mobile-friendly UI
* API integration

---

## 👨‍💻 Author

**Shaswat Kotecha**

---

## 📄 License

This project is developed for academic purposes.

---

## 🎯 Key Highlights

* Role-based access control
* Task-driven workflow system
* Dynamic QWeb PDF reporting
* Real-time dashboard analytics
* Scalable ERP-based architecture

```
```
