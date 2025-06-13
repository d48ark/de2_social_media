# 📊 Social Media Sentiment Analysis - Data Engineering Project

This project is a complete data engineering pipeline to analyze *Twitter sentiment* using batch and stream processing. It uses a simulated Twitter dataset and integrates various tools like Apache Kafka, Apache Spark, Vertex AI, and Docker to demonstrate scalable data engineering workflows.

## 🚀 Project Overview

- *Domain*: Social Media  
- *Goal*: Analyze sentiment of tweets using both batch and streaming pipelines  
- *Output*: Dashboards, ML predictions, and processed sentiment insights  

---

## ✅ Tasks Completed

### 1. 📐 Architecture Design
- Designed a modular data pipeline with:
  - Kafka for streaming data ingestion
  - Spark for batch and real-time processing
  - Vertex AI for ML model training and deployment
  - Flask API for model inference
  - PostgreSQL for storage (optional)
  - Docker for containerization

---

### 2. 🛠 Data Generation & Ingestion
- *Batch Data*:
  - Used a static cleaned dataset (cleaned_data.csv)
- *Streaming Data*:
  - Simulated real-time Twitter stream using Kafka Producer
  - Sent data every 3 seconds to a Kafka topic

---

### 3. 🧼 Batch Data Pipeline
- Processed historical tweets using *PySpark*
- Performed:
  - Sentiment classification
  - Word frequency analysis
  - Grouped stats by date and location
- Output saved as CSV + visualized using Jupyter Notebooks

---

### 4. 🔁 Stream Processing
- Kafka Consumer setup using Python
- Real-time analytics every 30 seconds:
  - Count of tweets
  - Sentiment breakdown (positive, negative, neutral)
  - Spike detection (threshold alerts)
- Logs results to console (can be extended to dashboard)

---

### 5. 🤖 Machine Learning Integration
- Trained a Logistic Regression classifier using sklearn
- Metrics:
  - Accuracy, Precision, F1 Score
- Hosted model with *Flask API*
- Live inference used in both batch and streaming outputs

---

### 6. 📉 Monitoring & Documentation
- Logged events using Python logging module
- Monitored:
  - Volume of incoming tweets
  - Sentiment trends
  - Processing time
- Documentation:
  - Project steps detailed in report.pdf
  - Presentation available in presentation.pptx

---

## 🧰 Technologies Used

| Tool         | Purpose                           |
|--------------|------------------------------------|
| Apache Kafka | Real-time streaming & ingestion   |
| Apache Spark | Batch processing with PySpark     |
| Vertex AI    | ML training & deployment          |
| Flask        | ML model API endpoint             |
| Docker       | Containerization of services      |
| PostgreSQL   | Optional storage layer            |
| Python       | Data processing and scripting     |

---

## 🧪 How to Run

### 🐳 Docker Setup

```bash
# Start containers
docker-compose up --build

# Stop containers
docker-compose down