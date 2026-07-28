# Komodo Hub

## 🌐 Website Link
https://komodo-hub-eight.vercel.app/

## 🌟 Overview and Vision
Komodo Hub is a national digital platform, it was built to help raise awareness about the endangered species of Indonesia. In Komodo Hub we bring together students, researchers, and even enthusiasts to participate in conservation programs across Indonesia. On Komodo hub schools and communities are active participants and they use it to manage there organisations!.

## The Problem it's solving
Despite millions spent by the government, species like the Javan Rhinoceros, Sumatran Tiger, and others are still endangered. Habitat loss, pollution, and over-exploitation are the main causes.

#### 🤝 Community Involvement
The platform shifts conservation from being just a government responsibility to a nationwide community effort by involving:

- 🏫 Primary schools across Indonesia
- 👥 Local communities and organisations 
- 🧑‍🤝‍🧑 Individual citizens from remote villages to urban areas

#### 📚 Education

Students learn about endangered species through class activities and outdoor programs
Teachers integrate conservation into their school syllabus
Learning materials and games are available on the platform

#### 👁️ Species Sighting Reports

Registered users can report sightings of rare and endangered species
This helps build a national database of species locations and population tracking

#### 📖 Knowledge Base

Both registered and non-registered users can access a rich library of information about Indonesian endemic species
Communities and schools can contribute articles, essays, and columns

#### 📊 Data-Driven Decisions

Management can monitor the platform through a business dashboard
Tracks which programs are working and where improvements are needed

##  🎯 objectives
- Raise awareness about Indonesia's endangered species
- Involve school, local communities, and citizens in  conservation efforts
- Faciliate access to sighting, and reporting oppurtunities for everyone
- Support national conservation efforts


## 🐾 Endangered species
| Species | Status | Population |
|---|---|---|
| 🐯 Sumatran Tiger | Critically Endangered | ~400 remaining |
| 🦏 Javan Rhinoceros | Critically Endangered | ~76 remaining |
| 🐦 Bali Myna | Critically Endangered | ~100 remaining |
| 🦎 Komodo Dragon | Endangered | ~6,000 remaining |
| 🦧 Tapanuli Orangutan | Critically Endangered | ~800 remaining |
| 🦇 Talaud Fruit Bat | Vulnerable | ~Unknown |
| 🐻 Sun Bear | Vulnerable | ~Unknown |
| 🦌 Bawean Deer | Critically Endangered | ~300 remaining |
| 🐒 Silvery Gibbon | Endangered | ~2,000 remaining |
| 🐆 Javan Leopard | Critically Endangered | ~250 remaining |
| 🐵 Mentawai Macaque | Endangered | ~Unknown |
| 🐾 Sunda Pangolin | Critically Endangered | ~Unknown |
| 🐢 Green Sea Turtle | Endangered | ~85,000 nesting females |

## ✨ Features 

### 🖥️ Virtual learning spaces
- We provide spaces where teachers can interact with their students by posting teaching material and assign assignments

### 🧩 Games and Quizzes
Komodo Hub has a couple of interactive games that serve our objectives
- Wordle & Riddle

### 🔬 Open source contributions
- Share research findings
- List sightings
- Interact with other's work

## 🚀 Installation & Setup

### 📋 Phase 1: Install Prerequisites
Before running the web-application, ensure you have the following installed on your computer:

1. **Python** (latest version) installation: Download and install from the official Python site https://www.python.org/downloads/. Ensure that during installation, you check the box saying 'Add Python to PATH' before clicking install.
2. **Git:** Download git for appropriate Operating System from https://git-scm.com/install/.

### 📁 Phase 2: Project Setup
1. Open your preferred Terminal: Open Command Prompt (Windows) or Terminal (Mac/Linux) or open a new terminal in your preferred IDE (VS-Code, Emacs, etc).
2. Clone the Project Repository: Run the following command in your preferred terminal:
```bash
   git clone https://github.coventry.ac.uk/mohame219/ABCSS_Komodo_Hub.git
```
3. Move into the created directory: Enter the cloned repository directory by running this command in your terminal:
```bash
   cd ABCSS_Komodo_Hub
```

### ⚙️ Phase 3: Environment & Application Configuration
1. Create a virtual environment: Run the following command
```bash
   python -m venv venv
```
2. Activate the virtual environment:

On Windows:
```bash
     venv\Scripts\activate
```
On Mac/Linux:
```bash
     source venv/bin/activate
```
3. Once activated, install project dependencies: Run the following command to install required libraries for the web-app to run:
```bash
   pip install -r requirements.txt
```
4. After that, create a file named `.env` in the project's root directory (where run.py is located) and paste the following text into it and save:

   `EMAIL=saadwajid401@gmail.com`
   
   `PASSWORD=REDACTED_SECRET`

### 🗄️ Phase 4: Database Initialisation & Website Launch
1. Generate Database: Before starting the app for the 1st time, you need to create the database and generate test data. Run this command to do so:
```bash
   python generatetestdata.py
```
   > Note: If you need to ever reset the database, re-run this file to recreate the database.

2. Start Server and Launch Application: Run the run.py file using the below command and enter this URL (http://localhost:2222) in your preferred web browser to enter the web app:
```bash
   python run.py
```

### 🧪 Phase 5: Testing (with User Credentials)
If you want to login as an individual (no organisation), you can use the individual@example.com email to log in or register using your own email account. The following tables show the users generated by the database for each organisation.

> **Note:** All the accounts below share the same password - **`12345678a@`**

> **Note:** Verified indicates whether the account is accessible or not. When an organisation creates a new account to add to the organisation, the account is not verified until and unless the access code is used in organisation login. Once that's done the account's verification status is updated to True and the account can be logged in to normally.


**🛡️ Komodo Hub**
| Email | Role | Verified |
|---|---|---|
| sysadmin@example.com | System Admin | ✅ |
| manager@example.com | Manager | ✅ |

**🏫 Coventry University (School)**
| Email | Role | Verified |
|---|---|---|
| admin@example.com | School Admin | ✅ |
| teacher1@example.com | Teacher | ✅ |
| student1@example.com | Student | ✅ |
| student2@example.com | Student | ✅ |
| student3@example.com | Student | ❌ |

> **Note:** The unique access code for the unverified user is - **`12345678`**

**🏫 Oakwood School (School)**
| Email | Role | Verified |
|---|---|---|
| admin2@example.com | School Admin | ✅ |
| teacher2@example.com | Teacher | ✅ |
| student4@example.com | Student | ✅ |
| student5@example.com | Student | ✅ |

**👥 Solihull Tech Collective (Community)**
| Email | Role | Verified |
|---|---|---|
| admin3@example.com | Community Admin | ✅ |
| teacher4@example.com | Teacher | ✅ |
| member1@example.com | Student Member | ✅ |
| member2@example.com | Student Member | ✅ |

**📝 Additional Notes:**
- Communities do not have any courses. To view courses, ensure you login using a school member account.
- Furthermore, you may not be able to see your contributions added in the public library since they are sent to the system admin for moderation before appearing publicly.
- You can view the programs and sightings in the conservation programs section of the public library while the other section shows all contributions.
- In order to access a course, you can either use the courses link in the home page (only available to school members) or go on a school's page (organisation page) showing their list of courses. If the account is enrolled in the course, you can view assignments, workshops, materials and even the common room.

## 🔒 Security & Safety Standards

This platform adheres to *ISO 9241-210:2019* — the international standard for 
human-centred design of interactive systems — ensuring:

- ✅ *Usability* — Intuitive navigation with minimal clicks, and clear language
- 🎨 *Interactivity* — Used css for advanced styling and JavaScript to create a dynamic Website, Moreover we used design rules like the 10:30:60 color ratio to make the UI more appealing 
- 🔐 *Security* — encryption, hashing and salting, two factor authentication, and access control

### 🛡️ Data Privacy

- 🚫 Student profiles and personal data are *never* visible to the public
- 📂 Only the school library is publicly accessible; student profiles are restricted
- 👮 Role-based access control (RBAC) limits data visibility by user role
