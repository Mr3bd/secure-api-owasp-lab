# 🛡️ Secure API (OWASP Top 10 Lab) -- FastAPI + NGINX + Docker

A hands-on **API Security Lab** demonstrating the difference between an
intentionally vulnerable REST API and a hardened, production-style
secure API.

This project is built for:

-   🔐 Cloud Security Engineers\
-   ⚙️ DevSecOps Engineers\
-   🧑‍💻 Backend Developers\
-   🎯 Anyone preparing for security-focused technical interviews

It provides a real-world demonstration of **OWASP Top 10 API
vulnerabilities** and how to properly mitigate them using modern
security controls.

------------------------------------------------------------------------

## 🚀 What This Project Demonstrates

This lab contains **two API implementations**:

### 1️⃣ Vulnerable API

An intentionally insecure FastAPI application demonstrating:

-   Broken Authentication
-   Broken Access Control
-   Missing Rate Limiting
-   Excessive Data Exposure
-   Security Misconfiguration
-   Injection-like insecure patterns (simulated)

### 2️⃣ Secure API

A hardened implementation applying real-world API security best
practices.

Both APIs are deployed behind **NGINX Reverse Proxy** using **Docker
Compose**.

------------------------------------------------------------------------

## 🧱 Technologies Used

-   🐍 FastAPI (Python 3.10)
-   🌐 NGINX Reverse Proxy
-   ⚡ NGINX njs (JWT claim extraction)
-   🔑 JWT (python-jose)
-   🐳 Docker & Docker Compose
-   📊 Structured Security Logging

------------------------------------------------------------------------

## 🔐 Security Controls Implemented (Secure API)

| Control                        | Implementation                                             |
|--------------------------------|------------------------------------------------------------|
| JWT Validation                 | Signature, expiration, issuer & audience validation        |
| Role-Based Access Control      | Admin endpoint protected via role enforcement              |
| Input Validation               | Strict Pydantic models                                     |
| Rate Limiting                  | Per-user rate limiting via NGINX                          |
| Login Protection               | IP-based rate limiting for `/auth/login`                  |
| Secure CORS                    | Restricted origins and headers                            |
| Security Headers               | X-Frame-Options, X-Content-Type-Options, X-XSS-Protection |
| Suspicious Activity Logging    | Structured logging for failed auth and validation errors  |

------------------------------------------------------------------------

## 🏗️ Architecture Overview

Client → NGINX → FastAPI

### NGINX Responsibilities

-   Rate limiting (`limit_req`)
-   JWT claim extraction (`sub` → user_id)
-   CORS policy enforcement
-   Security headers
-   Access logging

### Secure API Responsibilities

-   JWT signature verification
-   Role enforcement
-   Input validation
-   Security event logging

------------------------------------------------------------------------

## 📁 Project Structure

    secure-api-owasp-lab/
    ├── docker-compose.yml
    ├── nginx/
    │   ├── vulnerable/
    │   └── secure/
    ├── vulnerable_api/
    ├── secure_api/
    └── scripts/

------------------------------------------------------------------------

## 🧪 Included Security Test Scenarios

The project includes automated tests via:

    scripts/attack_examples.sh

Demonstrations include:

-   Accessing admin endpoint without authentication
-   Self-assigning admin role (vulnerable API)
-   Invalid JWT usage
-   Role enforcement (403)
-   Input validation failures (422)
-   Rate limiting enforcement (429)
-   Comparison of secure vs insecure CORS behavior

------------------------------------------------------------------------

## 📊 Rate Limiting Example

Per authenticated user:

    limit_req_zone $user_id zone=user_zone:10m rate=60r/m;
    limit_req zone=user_zone burst=10 nodelay;

Meaning:

-   60 requests per minute per user
-   Allows 10 immediate burst requests
-   Returns HTTP 429 when exceeded

------------------------------------------------------------------------

## ⚡ Quick Start

Clone the repository:

``` bash
git clone https://github.com/Mr3bd/secure-api-owasp-lab.git
cd secure-api-owasp-lab
```

Start the environment:

``` bash
docker compose up -d --build
```

Run the automated demo:

``` bash
bash scripts/demo_flow.sh
```

------------------------------------------------------------------------

## 🌍 Access URLs

Vulnerable API: http://localhost:8081/docs

Secure API: http://localhost:8082/docs

------------------------------------------------------------------------

## 📜 Logs & Monitoring

View NGINX rate limit logs:

``` bash
docker compose logs nginx_secure
```

View application security logs:

``` bash
docker compose logs secure_api
```

------------------------------------------------------------------------

## 🎯 Ideal For

-   API Security learning
-   DevSecOps demonstrations
-   Cloud Security portfolio projects
-   OWASP Top 10 hands-on practice
-   Security-focused GitHub portfolio enhancement

------------------------------------------------------------------------

## ⚠️ Educational Use Only

The vulnerable API is intentionally insecure and must never be used in
production environments.

It exists solely for educational and demonstration purposes.

------------------------------------------------------------------------

## 🌟 Star this repository if you found it useful

Made with 💻 by a Cloud Security Engineer for DevSecOps and Cloud
Security professionals.

------------------------------------------------------------------------

## 👨‍💻 Author

Abdullrahman Alhawamdeh

🔗 https://www.linkedin.com/in/mr3bd

🌐 https://mr3bd.com

Made with ❤️ using FastAPI, NGINX, Docker, and modern API security best
practices.
