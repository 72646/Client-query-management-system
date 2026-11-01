# Client Query Management System

A Python-based web application designed to manage client queries and support requests efficiently. The system provides separate interfaces for clients 
and support staff, allowing clients to submit queries while support staff can view, filter, and manage submitted requests.
The application integrates Python, Streamlit, MySQL, and Pandas to provide a centralized query management solution. It also includes a CSV data ingestion 
script for importing bulk query records into the database.

## Project Overview

Managing customer queries manually can become challenging when dealing with multiple clients and support requests.
This project addresses that challenge by providing a centralized platform where clients can submit queries and support staff can monitor and manage them.
The application implements role-based access with two user roles:

- **Client:** Can register, log in, and submit queries.
- **Support:** Can access the support dashboard, view submitted queries, filter them by status, and close queries.

## Key Features

### Client Module
- User registration and login.
- Role-based user access.
- Submit queries with email address and mobile number.
- Provide query headings and detailed descriptions.
- Store submitted queries in a MySQL database.
- Automatically assign an initial Open status to submitted queries.

### Support Module
- Dedicated support dashboard.
- View submitted client queries.
- Filter queries by status (All, Open, Closed).
- Display query records in a tabular format.
- Close queries after resolution.
- Automatically record query closure timestamps.

### Authentication
- User registration and login functionality.
- SHA-256 password hashing.
- Separate Client and Support roles.
- Session management using Streamlit session state.

### CSV Data Import
- Import synthetic client query records from CSV files.
- Rename dataset columns to match the MySQL database schema.
- Handle missing values before database insertion.
- Perform bulk record insertion into MySQL.

## Technology Stack

 Technology | Purpose 

 Python | Application development |
 Streamlit | Interactive web interface |
 MySQL | Relational database management |
 MySQL Connector | Python-MySQL connectivity |
 Pandas | Data manipulation and CSV processing |
 NumPy | Numerical and missing-value handling |
 Hashlib | Password hashing |
 Datetime | Query timestamps |

## Project Architecture

The application is organized into separate Python modules to maintain code readability and modularity.

| File | Description |

| `app.py` | Main Streamlit application containing client and support interfaces. |
| `auth.py` | Handles user registration, password hashing, and login authentication. |
| `db.py` | Establishes database connections with MySQL. |
| `load_csv.py` | Reads synthetic query records from CSV and inserts them into MySQL. |
| `synthetic_client_queries.csv` | Dataset containing synthetic client query records. |

## Database Design

The application uses a MySQL database named `query_system` with two primary tables.

### 1. Users Table

Stores registered user information.

| Column | Description |
|---|---|
| user_id | Unique user identifier |
| username | User's login name |
| hashed_password | SHA-256 hashed password |
| role | User role (Client or Support) |

### 2. Queries Table

Stores client queries and their corresponding status information.

| Column | Description |

 query_id | Unique query identifier |
 mail_id | Client email address |
 mobile_number | Client mobile number |
 query_heading | Query subject |
 query_description | Detailed query description |
 status | Current query status |
 query_created_time | Query submission timestamp |
 query_closed_time | Query closure timestamp |

## Application Workflow

1. Users register with a username, password, and role.
2. Registered users log in through the authentication module.
3. The application identifies the user's role.
4. Clients submit queries through the client interface.
5. Submitted queries are stored in MySQL with an initial Open status.
6. Support staff access the dashboard to view submitted queries.
7. Support staff filter queries based on their current status.
8. Support staff close queries after resolution.
9. The database records the query closure timestamp.

### CSV Data Ingestion Workflow

The project also includes a separate CSV import process.

1. Read synthetic client query records using Pandas.
2. Rename CSV columns to match the MySQL database schema.
3. Convert missing values into SQL-compatible NULL values.
4. Establish a connection to the MySQL database.
5. Insert records into the queries table.
6. Commit the transaction.

## Project Structure

```text
Client-Query-Management-System/
│
├── app.py
├── auth.py
├── db.py
├── load_csv.py
├── synthetic_client_queries.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.x
- MySQL Server
- pip package manager

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd YOUR_PROJECT_FOLDER
```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install streamlit pandas numpy mysql-connector-python
```

Alternatively, if a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

Make sure your MySQL server is running.

Create the database:

```sql
CREATE DATABASE query_system;
USE query_system;
```

Create the users table:

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    hashed_password VARCHAR(256),
    role VARCHAR(20)
);
```

Create the queries table:

```sql
CREATE TABLE queries (
    query_id INT AUTO_INCREMENT PRIMARY KEY,
    mail_id VARCHAR(100),
    mobile_number VARCHAR(15),
    query_heading VARCHAR(200),
    query_description TEXT,
    status VARCHAR(20),
    query_created_time DATETIME,
    query_closed_time DATETIME
);
```

### 5. Configure Database Connection

Update the MySQL connection credentials in `db.py` according to your local MySQL configuration.

Make sure not to publish actual database credentials on GitHub.

### 6. Import Synthetic Dataset (Optional)

To populate the database with sample query records, execute:

```bash
python load_csv.py
```

Make sure `synthetic_client_queries.csv` is available in the project directory.

### 7. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open your browser and navigate to:

```text
http://localhost:8501
```

## Security Considerations

- Passwords are hashed using SHA-256 before storage.
- Database credentials should be stored securely using environment variables rather than hardcoded values.
- For production applications, use password hashing algorithms specifically designed for password storage, such as bcrypt or Argon2.

## Learning Outcomes

Through this project, I gained practical experience in:

- Python application development.
- MySQL database connectivity.
- SQL CRUD operations.
- Relational database design.
- User authentication and role-based access.
- Password hashing.
- CSV data ingestion and preprocessing.
- Handling missing values using Pandas and NumPy.
- Building interactive web applications using Streamlit.

## Future Enhancements

- Add query assignment to individual support staff.
- Implement query search functionality.
- Introduce query priority levels.
- Add email notifications for query updates.
- Develop query resolution reports and analytics.
- Improve input validation and authentication security.
- Implement pagination for large query datasets.

## Author

**Mohamed Ameen**

Integrated M.Tech in Computer Science and Engineering

Vellore Institute of Technology

GitHub: [72646](https://github.com/72646)
