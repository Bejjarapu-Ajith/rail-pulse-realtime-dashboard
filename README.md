# RailPulse – Real-Time Train Analytics Dashboard

## Overview

RailPulse is a real-time train monitoring and analytics project developed using Kafka, Apache Druid, and Streamlit.

The system continuously streams train data through Kafka, stores and processes it using Apache Druid, and displays live insights on an interactive Streamlit dashboard.

---

## Features

* Real-time train data streaming
* Kafka-based producer and consumer pipeline
* Live analytics with Apache Druid
* Interactive Streamlit dashboard
* Dynamic train status and platform updates
* Real-time visualization of train information

---

## Technologies Used

* Python
* Apache Kafka
* Apache Druid
* Streamlit
* Docker

---

## Project Structure

* `producer.py` – Generates and streams train data
* `consumer.py` – Consumes Kafka messages
* `app.py` – Streamlit dashboard application
* `docker-compose.yml` – Docker service configuration

---

## How to Run the Project

### 1. Start Docker Services

```
docker-compose up
```

### 2. Run the Kafka Producer

```
python producer.py
```

### 3. Run the Kafka Consumer

```
python consumer.py
```

### 4. Launch the Streamlit Dashboard

```
streamlit run app.py
```

---

## Future Enhancements

* AI-based train delay prediction
* Integration with real Indian Railways APIs
* Advanced analytics and filtering
* Alert and notification system

---

## Author

Ajith Bejjarapu
