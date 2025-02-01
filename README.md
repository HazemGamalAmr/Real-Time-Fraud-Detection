🛡️ Real-Time Fraud Detection System

This repository contains the implementation of a Real-Time Fraud Detection System, designed to detect anomalies and fraudulent activities by leveraging a modern, scalable data engineering and analytics pipeline.
📊 System Architecture
Overview

The system follows an ELT (Extract, Load, Transform) pipeline, powered by Apache Airflow, with seamless integration of Google Cloud Platform (GCP) services for real-time data processing and analytics.
Key Components

    Data Source
        The initial data ingestion begins from various sources such as transactional databases or log systems.

    Extraction
        Kafka: Captures and streams raw data for processing.
        Google Pub/Sub: Manages and distributes messages to downstream services in real time.

    Transformation
        Google Dataflow: Handles data transformations and enrichments, preparing data for storage and analysis.

    Loading
        Google Cloud Storage (GCS): Serves as a staging area for processed data, enabling batch and real-time transformations.

    Processing
        Google Dataproc:
            Facilitates distributed data processing using Apache Spark for advanced analytics.
            Implements machine learning workflows for fraud detection.

    Analytics & Visualization
        Google BigQuery:
            Acts as a data warehouse for running SQL-based analytics on transformed datasets.
        Power BI:
            Provides interactive dashboards and visualizations for stakeholders to monitor fraud detection insights.

    Monitoring
        Google Cloud Monitoring: Tracks system performance, alerting on anomalies or failures in the pipeline.

🎯 Key Features

    Real-Time Data Processing:
    Ensures immediate detection of fraudulent activities by leveraging streaming tools like Kafka and Pub/Sub.

    Scalable Analytics:
    Combines the power of Spark on Dataproc and BigQuery for handling massive datasets.

    Machine Learning Integration:
    Implements fraud detection models that classify and flag suspicious activities.

    End-to-End Orchestration:
    Automated workflows using Apache Airflow for seamless ELT processes.

    Actionable Insights:
    Comprehensive dashboards and reports to assist decision-makers.

🔧 Tools & Technologies

    Data Streaming: Kafka, Google Pub/Sub
    Orchestration: Apache Airflow
    Data Transformation: Google Dataflow
    Storage & Processing: Google Cloud Storage (GCS), Google Dataproc, Apache Spark
    Analytics & Visualization: Google BigQuery, Power BI
    Monitoring: Google Cloud Monitoring

🌟 System Architecture 

![System_Arch](https://github.com/user-attachments/assets/b0a3b862-21cd-4b52-9046-7cfb4118a596)


Team Members:
- Sheref Hamdy ( sherefhamdy10@gmail.com )
- Abdelrahman Mahmoud ( a.mahmoud1803@gmail.com )
- Hazem Amr ( hazemramr@gmail.com )
- Ahmed Magdy ( ahmed.magdyhtc@gmail.com )

    
