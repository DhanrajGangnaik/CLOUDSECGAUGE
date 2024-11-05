# 🛡️🌥️ Cloud Security Gauge   

**Cloud Security Gauge** is a robust tool designed to detect and prevent SQL injections and other security vulnerabilities in cloud-hosted applications. Built with Flask and integrated with PostgreSQL in a Dockerized environment, this tool is ideal for developers and security professionals looking to enhance the security of their cloud applications.

---

## ✨ Features

- 🔒 **SQL Injection Detection**: Real-time SQL injection detection with advanced JavaScript validation.
- 💄 **PostgreSQL Database Integration**: Connects securely with PostgreSQL databases in a Dockerized container environment.
- 👤 **User Authentication**: A secure login system with input validation.
- 🗒️ **Real-time Logs**: Detailed logging for debugging and monitoring.

---

## 🏗️ Project Structure

```
cloudsecgauge/
├── config/                   # Configuration files and Docker setup
├── data/                     # Sample data files (e.g., CSV files)
├── static/                   # Static files (CSS, JavaScript)
├── templates/                # HTML templates for Flask app
└── app.py                    # Main Flask application
```

---

## 🛠️ Prerequisites

Before you begin, ensure you have:

- **Docker** 🐳 installed (for containerized deployment)
- **Python 3.9** 🐍 or higher installed
- **Git** installed (to clone the repository)

---

## ⬇️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/DhanrajGangnaik/Cloud-Security-Gauge.git
cd Cloud-Security-Gauge
```

### Step 2: Set Up the Docker Container

1. Build the Docker image:
   ```bash
   docker build -t cloudsecgauge_image -f config/Dockerfile .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 --name cloudsecgauge_container cloudsecgauge_image
   ```

This will build and run the container, exposing the application on `http://localhost:5000`.

### Step 3: Access the Application

🌐 Open your browser and go to:

```
http://localhost:5000
```

---

## ⚠️ Troubleshooting

If you encounter any issues, check the container logs:

```bash
docker logs cloudsecgauge_container
```

---

## 🖥️ Running Locally (Without Docker)

To run the project on your local device without Docker, follow these steps:

### Step 1: Install Python Dependencies

1. Navigate to the project directory:
   ```bash
   cd Cloud-Security-Gauge
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r config/requirements.txt
   ```

### Step 2: Run the Flask Application

Start the app with:

```bash
python app.py
```

🌐 Open `http://127.0.0.1:5000` in your browser to access the application.

---

## 🤝 Contributing

Contributions are welcome! Please fork this repository and create a pull request with your feature or bug fix. Make sure to update the documentation as needed.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 🙋🏻‍♂️ Contact 

Created by [Dhanraj Gangnaik](https://github.com/DhanrajGangnaik) – feel free to reach out with any questions or suggestions!
