# Student Marks Calculation System

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automated_Testing-red.svg)](https://www.selenium.dev/)
[![GitHub](https://img.shields.io/badge/GitHub-shruti22--svg-black.svg)](https://github.com/shruti22-svg/Student-Marks-Calculation)

## Overview
**Assignment 9: Student Marks Calculation**
- **9.a**: Web application to input marks for three subjects and calculate total, average, percentage, and grade. Source code pushed and managed on GitHub.
- **9.b**: Dockerized application with complete Selenium automated end-to-end test cases verifying calculations on the live web application.

---

## Port Configuration
| Component | Port | Description |
| :--- | :--- | :--- |
| **Docker Container Port** | `5000` | Port exposed inside the Docker container (`EXPOSE 5000`) |
| **Host Application Port** | `5003` | Port mapped on host machine (`-p 5003:5000`) |
| **Live Web App URL** | `http://localhost:5003` | Accessible in browser |

---

## Features
- **Accurate Calculation**:
  - $\text{Total Marks} = \text{Subject 1} + \text{Subject 2} + \text{Subject 3}$
  - $\text{Average Marks} = \frac{\text{Total}}{3}$
  - $\text{Percentage} = \frac{\text{Total}}{300} \times 100\%$
  - **Passing Criteria**: Individual subject passing mark $\ge 35$.
  - **Grade Bands**: $A+ (\ge 90), A (\ge 80), B (\ge 70), C (\ge 60), D (\ge 50), F (< 50)$.
- **Responsive UI**: Built with modern CSS cards, status badges, and reset functionality.
- **REST API**: `/api/calculate` endpoint and `/api/health` monitoring endpoint.
- **Containerized**: Production-ready Dockerfile with slim runtime and healthcheck.
- **Automated Verification**: Selenium test suite covering UI loading, standard marks, boundary decimals, failing marks, and reset buttons.

---

## Quick Start Instructions

### Option 1: Run via Docker (Recommended)
```bash
# 1. Build the Docker image
docker build -t student-marks-calculation:latest .

# 2. Run the container
docker run -d -p 5003:5000 --name student-marks-calculation-app student-marks-calculation:latest

# 3. Access in browser
http://localhost:5003
```
Or using Docker Compose:
```bash
docker compose up -d
```

### Option 2: Run Locally with Python
```bash
py app.py
```
App runs locally on `http://localhost:5000` (or set `PORT=5003`).

---

## Running Selenium Test Cases
Run the automated test suite against the live running application:
```bash
# Live visible browser window
py tests/test_marks_calculation.py

# Or headless execution
$env:HEADLESS="true"; py tests/test_marks_calculation.py
```

### Test Cases Covered:
1. `Test 1`: Page load, title assertion, form element visibility.
2. `Test 2`: Calculation with high marks (Sub1: 85, Sub2: 90, Sub3: 95) -> Total: 270, Avg: 90.0, Grade: A+, Status: Passed.
3. `Test 3`: Calculation with average marks (Sub1: 70, Sub2: 75, Sub3: 80) -> Total: 225, Avg: 75.0, Grade: B.
4. `Test 4`: Decimal numbers handling (Sub1: 82.5, Sub2: 77.5, Sub3: 80.0) -> Total: 240.0, Avg: 80.0.
5. `Test 5`: Boundary check for failing grade (Sub1: 30) -> Status: Failed.
6. `Test 6`: Form reset button verification.

---

## GitHub Repository
Source code is maintained on GitHub:
- **Repository**: [https://github.com/shruti22-svg/Student-Marks-Calculation](https://github.com/shruti22-svg/Student-Marks-Calculation)
- **Author**: Shruti (`shruti22-svg`)
- **Email**: `shrutibhagavatham@gmail.com`
