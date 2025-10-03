# Messaging System with RabbitMQ, Celery, Nginx, and FastAPI

## Project Overview

This project demonstrates a **messaging system** with asynchronous task processing using **Celery** and **RabbitMQ**.  
It allows users to send emails asynchronously and log the current server time via a **FastAPI** application served behind **Nginx**, with optional public access through **ngrok**.

---

## How It Works

1. **User Interaction**  
   Users send requests via a web browser or API call. Two actions are supported: sending an email or logging the current time.

2. **FastAPI Backend**  
   The FastAPI application receives the request.  
   - For emails, it **enqueues a task** in Celery.  
   - For logging, it writes the timestamp to a log file immediately (or optionally via Celery).  

3. **Celery & RabbitMQ**  
   - **RabbitMQ** acts as a message broker, holding tasks until a Celery worker picks them up.  
   - **Celery workers** run in the background and process tasks asynchronously, such as sending emails.  

4. **SMTP Email Sending**  
   The email task connects to Gmail's SMTP server using credentials stored in environment variables. Once the email is sent, it logs the result.

5. **Nginx Reverse Proxy**  
   Nginx handles incoming requests and forwards them to the FastAPI app, providing production-like routing and request handling.

6. **Ngrok**  
   Ngrok exposes the local server to the internet, allowing external testing of email sending and logging.

7. **Logging**  
   All operations, including email sends and timestamp logs, are recorded in a log file (`messaging_system.log`) for monitoring and debugging.

---

## Architecture Summary

- **FastAPI**: Handles incoming web requests.  
- **Celery**: Processes tasks asynchronously in the background.  
- **RabbitMQ**: Acts as the message broker for task queuing.  
- **SMTP**: Sends emails via Gmail.  
- **Nginx**: Reverse proxy for routing HTTP requests.  
- **Ngrok**: Optional tool for exposing local server to the internet.  
- **Logging**: Tracks all task executions and errors.  
---
