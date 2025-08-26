# CUGymStats

![status](https://img.shields.io/badge/status-in_development-brightgreen)
[![language](https://img.shields.io/badge/language-python3%2E13%2E1-blue)](https://www.python.org/)
![release](https://img.shields.io/badge/release-pre--dev-orange)
[![GitHub last commit](https://img.shields.io/github/last-commit/xlaesch/CUGymStats)](#)
[![Run app.py every hour](https://github.com/xlaesch/CUGymStats/actions/workflows/run-app.yml/badge.svg)](https://github.com/xlaesch/CUGymStats/actions/workflows/run-app.yml)

## Overview

CUGymStats is a web application that provides real-time statistics and historical data on gym occupancy at Cornell. The application consists of a backend that scrapes data from the gym's website and a frontend that displays the data in a user-friendly format.

### Architecture: BFF vs Domain API

- BFF (Next.js):
    - Web concerns only: request shaping, aggregation, caching, rate limiting, feature flags, input sanity checks.
    - Calls the Domain API with an HMAC-signed request; no direct DB access and no secrets sent to the browser.
- Domain API (Flask):
    - Owns business logic and data access to Postgres.
    - Verifies HMAC from BFF, applies domain validations and a light “safety” rate-limit.

Local setup:
- Configure shared secret in both apps.
    - Backend: copy `backend/.env.example` to `backend/.env` and set `DOMAIN_API_SECRET` and `DATABASE_URL`.
    - Frontend: copy `frontend-new/.env.example` to `frontend-new/.env` and set `DOMAIN_API_BASE` and `DOMAIN_API_SECRET`.
- Start Flask on 127.0.0.1:5000 and Next.js on 127.0.0.1:3000. The frontend BFF routes call Flask.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Real-time gym occupancy data
- Historical data visualization
- API for accessing gym statistics
- User-friendly web interface

## Installation

### Backend (Flask Domain API)

1. Navigate to the `backend` directory:
    ```sh
    cd backend
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    ```

5. Run the backend server:
    ```sh
    export FLASK_APP=routes.py
    flask run --host 127.0.0.1 --port 5000
    ```

### Frontend (Next.js BFF + UI)

1. Navigate to the `frontend-new` directory:
    ```sh
    cd frontend-new
    ```

2. Install dependencies and run dev server:
    ```sh
    npm install
    npm run dev
    ```
3. Visit http://127.0.0.1:3000/dashboard

## Usage

1. Start the backend server as described in the installation steps.
2. Open the frontend in your web browser.
3. View real-time and historical gym occupancy data.

## API Endpoints

- BFF (Next.js):
    - `GET /api/gymstats`
    - `GET /api/average-occupancy?dayofweek=0..6`
- Domain API (Flask):
    - `GET /api/gymstats` (HMAC protected)
    - `GET /api/average-occupancy?dayofweek=0..6` (HMAC protected)

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for more details.
