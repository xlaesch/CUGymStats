# CUGymStats

![status](https://img.shields.io/badge/status-in_development-brightgreen)
[![language](https://img.shields.io/badge/language-python3%2E13%2E1-blue)](https://www.python.org/)
![release](https://img.shields.io/badge/release-pre--dev-orange)
[![GitHub last commit](https://img.shields.io/github/last-commit/xlaesch/CUGymStats)](#)

## Overview

CUGymStats is a web application that provides real-time statistics and historical data on gym occupancy at Cornell. The application consists of a backend that scrapes data from the gym's website and a frontend that displays the data in a user-friendly format.

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

### Backend

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
    flask run
    ```

### Frontend

1. Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```

2. Open `index.html` in your web browser.

## Usage

1. Start the backend server as described in the installation steps.
2. Open the frontend in your web browser.
3. View real-time and historical gym occupancy data.

## API Endpoints

- `GET /api/gymstats`: Retrieve all gym statistics.
- `GET /api/average-occupancy?dayofweek=<day>`: Retrieve average occupancy for a specific day of the week.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.