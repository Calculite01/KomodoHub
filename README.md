# Komodo Hub

> A national digital platform for community-supported conservation of Indonesia's endangered species, built from a live multi-stakeholder case study spanning schools, communities, researchers, and government-adjacent management teams.

[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge)](https://www.sqlalchemy.org/)
[![Neon](https://img.shields.io/badge/Neon-Serverless%20Postgres-00E599?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![Flask-WTF](https://img.shields.io/badge/Flask--WTF-Forms-000000?style=for-the-badge)](https://flask-wtf.readthedocs.io/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-Markup-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Vercel](https://img.shields.io/badge/Vercel-Deployment-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Agile](https://img.shields.io/badge/Methodology-Agile%20Scrum-6DB33F?style=for-the-badge)](#)

## Website Link
https://komodo-hub-eight.vercel.app/

To access all features, log in using [Test User Accounts](#test-user-accounts).

## How It's Built

Komodo Hub was developed from a real stakeholder case study: requirements were gathered from talks with every user group the platform now serves (school teachers, students, community admins, conservation researchers, and Komodo Hub's own management team), and the system was designed to satisfy all of them at once rather than a single "customer."

**Backend & Data**
- **Flask** powers the application backend, routing, and business logic
- **SQLAlchemy** models the relational schema (users, organisations, courses, assignments, sightings, chat, moderation)
- **Flask-WTF** handles form validation and CSRF-protected submissions across login, registration, assignments, and contributions
- **Neon** (serverless Postgres) is the production database, chosen for its scalability without needing to manage infrastructure

**Frontend**
- Server-rendered **HTML/Jinja2** templates with a shared `layout.html` for a consistent navbar and structure across every page
- **CSS** styling following the 10:30:60 colour-ratio design principle for visual hierarchy
- **JavaScript** for dynamic, interactive UI elements (chat, games, flash messaging)

**Deployment**
- Hosted on **Vercel**, connected to the Neon serverless database for a fully managed, zero-maintenance production environment

**Process**
- Delivered using **Agile Scrum** across 2 sprints (8 weeks total), with rotating Scrum Master, Product Owner, Frontend, Backend, and Support Developer roles each week
- Backed by a Product Backlog, Sprint Backlogs, a Risk Assessment Matrix, and a Gantt chart, refined weekly against direct stakeholder feedback

## My Role — Rotating Scrum Lead & Full-Stack Developer

Over the 8-week Agile delivery, our 5-person team rotated through Scrum Master, Product Owner, Frontend Developer, Backend Developer, and Support Developer each week so everyone gained end-to-end ownership of the platform. Highlights from my rotations:

- **Scrum Master**: compiled and prioritised stakeholder requirements from the case study across every user type (schools, communities, management), and built the project's Risk Assessment Matrix covering data breaches, weak passwords, and content-moderation risks
- **Product Owner**: maintained and refined the Product Backlog against live stakeholder feedback, keeping user stories accurately reflecting real-time development progress
- **Backend Developer**: implemented authentication (login/registration logic and routes), organisation login via access codes, forgotten-password recovery via email, and designed and expanded the database schema and table relationships in SQLAlchemy
- **Frontend Developer**: built the base template system and shared page layout (navbar, structure) in Jinja2; designed and implemented the landing, home, login, and registration pages; later built out the full course ecosystem, including workshops, assignments, submissions & grading, organisation pages, course pages, common room, materials, and the manager's analytics tools (feature popularity, subscription data, moderation queue)
- **Support Developer**: migrated the email provider to Google SMTP, restructured the entire project to an industry-standard layout, added organisation access-code login and password recovery, and fixed cross-cutting bugs across OTP verification and templating
- Closed out the project with UI polish (login page redesign, navbar, About page) and final role-based access control implementation and bug fixes

## Team & Methodology

Built by a 5-person team for Coventry University's *5005CMD Software Engineering* module, using **Agile Scrum** across 2 sprints and weekly stakeholder reviews with the project's module-leader stakeholder. Roles rotated weekly across the team so that Scrum Master, Product Owner, and Developer responsibilities were shared rather than fixed, giving every member exposure to both technical delivery and project ownership.

## Overview and Vision
Komodo Hub is a national digital platform. It was built to help raise awareness about the endangered species of Indonesia. In Komodo Hub we bring together students, researchers, and even enthusiasts to participate in conservation programs across Indonesia. On Komodo Hub, schools and communities are active participants and use it to manage their organisations.

## The Problem it's solving
Despite millions spent by the government, species like the Javan Rhinoceros, Sumatran Tiger, and others are still endangered. Habitat loss, pollution, and over-exploitation are the main causes.

#### Community Involvement
The platform shifts conservation from being just a government responsibility to a nationwide community effort by involving:

- Primary schools across Indonesia
- Local communities and organisations
- Individual citizens from remote villages to urban areas

#### Education

Students learn about endangered species through class activities and outdoor programs. Teachers integrate conservation into their school syllabus. Learning materials and games are available on the platform.

#### Species Sighting Reports

Registered users can report sightings of rare and endangered species. This helps build a national database of species locations and population tracking.

#### Knowledge Base

Both registered and non-registered users can access a rich library of information about Indonesian endemic species. Communities and schools can contribute articles, essays, and columns.

#### Data-Driven Decisions

Management can monitor the platform through a business dashboard, tracking which programs are working and where improvements are needed.

## Objectives
- Raise awareness about Indonesia's endangered species
- Involve schools, local communities, and citizens in conservation efforts
- Facilitate access to sighting and reporting opportunities for everyone
- Support national conservation efforts

## Endangered species
| Species | Status | Population |
|---|---|---|
| Sumatran Tiger | Critically Endangered | ~400 remaining |
| Javan Rhinoceros | Critically Endangered | ~76 remaining |
| Bali Myna | Critically Endangered | ~100 remaining |
| Komodo Dragon | Endangered | ~6,000 remaining |
| Tapanuli Orangutan | Critically Endangered | ~800 remaining |
| Talaud Fruit Bat | Vulnerable | ~Unknown |
| Sun Bear | Vulnerable | ~Unknown |
| Bawean Deer | Critically Endangered | ~300 remaining |
| Silvery Gibbon | Endangered | ~2,000 remaining |
| Javan Leopard | Critically Endangered | ~250 remaining |
| Mentawai Macaque | Endangered | ~Unknown |
| Sunda Pangolin | Critically Endangered | ~Unknown |
| Green Sea Turtle | Endangered | ~85,000 nesting females |

## Features

### Virtual learning spaces
- We provide spaces where teachers can interact with their students by posting teaching material and assigning assignments

### Games and Quizzes
Komodo Hub has a couple of interactive games that serve our objectives:
- Wordle & Riddle

### Open source contributions
- Share research findings
- List sightings
- Interact with others' work

## Using the Web App

### Test User Accounts
If you want to log in as an individual (no organisation), you can use the individual@example.com email to log in, or register using your own email account. The following tables show the users generated by the database for each organisation.

**IMPORTANT:** All the accounts below share the same password: **`12345678a@`**

> **Note:** Verified indicates whether the account is accessible or not. When an organisation creates a new account to add to the organisation, the account is not verified until the access code is used in organisation login. Once that's done, the account's verification status is updated to True and the account can be logged in to normally.

**Komodo Hub**
| Email | Role | Verified |
|---|---|---|
| sysadmin@example.com | System Admin | Yes |
| manager@example.com | Manager | Yes |

**Coventry University (School)**
| Email | Role | Verified |
|---|---|---|
| admin@example.com | School Admin | Yes |
| teacher1@example.com | Teacher | Yes |
| student1@example.com | Student | Yes |
| student2@example.com | Student | Yes |
| student3@example.com | Student | No |

> **Note:** The unique access code for the unverified user is: **`12345678`**

**Oakwood School (School)**
| Email | Role | Verified |
|---|---|---|
| admin2@example.com | School Admin | Yes |
| teacher2@example.com | Teacher | Yes |
| student4@example.com | Student | Yes |
| student5@example.com | Student | Yes |

**Solihull Tech Collective (Community)**
| Email | Role | Verified |
|---|---|---|
| admin3@example.com | Community Admin | Yes |
| teacher4@example.com | Teacher | Yes |
| member1@example.com | Student Member | Yes |
| member2@example.com | Student Member | Yes |

**Additional Notes:**
- Communities do not have any courses. To view courses, ensure you log in using a school member account.
- Furthermore, you may not be able to see your contributions added in the public library since they are sent to the system admin for moderation before appearing publicly.
- You can view the programs and sightings in the conservation programs section of the public library, while the other section shows all contributions.
- In order to access a course, you can either use the courses link on the home page (only available to school members) or go to a school's page (organisation page) showing their list of courses. If the account is enrolled in the course, you can view assignments, workshops, materials, and even the common room.

## Security & Safety Standards

This platform adheres to *ISO 9241-210:2019*, the international standard for human-centred design of interactive systems, ensuring:

- *Usability*: Intuitive navigation with minimal clicks, and clear language
- *Interactivity*: Used CSS for advanced styling and JavaScript to create a dynamic website. We also used design rules like the 10:30:60 colour ratio to make the UI more appealing
- *Security*: Encryption, hashing and salting, two-factor authentication, and access control

### Data Privacy

- Student profiles and personal data are *never* visible to the public
- Only the school library is publicly accessible; student profiles are restricted
- Role-based access control (RBAC) limits data visibility by user role
