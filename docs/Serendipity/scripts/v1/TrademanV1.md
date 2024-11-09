# TradeManV1 - Development Branch

TradeManV1 is a trading management system designed to streamline and automate various trading operations. This README pertains to the `dev` branch, which includes ongoing developments and experimental features.

## Project Structure

The repository is organized into several key directories and files:

- **.devcontainer/**: Configuration files for development container setups.
- **.github/workflows/**: GitHub Actions workflows for CI/CD processes.
- **Data/**: Contains related database tables/csv files.
- **Executor/**: Main folder for the execution engine responsible for order placements and management.
- **MarketInfo/**: As of now there are files related to backtesting, MarketInfoDashboard etc.
- **TestCases/**: Test cases for validating system functionalities.
- **User/**: Main purpose is to handle the user related activities like fastapi endpoints.
- **alembic/**: Database migration scripts managed by Alembic.
- **db/**: Database-related configurations and scripts.
- **.flake8**: Configuration for the flake8 linter.
- **.gitignore**: Specifies files and directories for Git to ignore.
- **README.md**: This documentation file.
- **alembic.ini**: Alembic configuration file.
- **poetry.lock**: Dependency lock file managed by Poetry.
- **postgres.readme.md**: Documentation related to PostgreSQL setup.
- **pyproject.toml**: Project configuration file for Poetry.
- **requirements.txt**: List of Python dependencies.


## Setup and Installation

To set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Serendipity2-0/TradeManV1.git
   cd TradeManV1
   git checkout dev
   ```

2. **Install Dependencies**:
   - Alternatively, using pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Database Setup**:
   - Ensure PostgreSQL is installed and running.


## Usage

- **Running the Application**:
  ```bash
  python User/UserApi/main.py
  ```

- **Celery script to run the scheduled tasks**:
  ```bash
  celery -A User.UserApi.celery_worker.celery_app worker --loglevel=info
  celery -A User.UserApi.celery_worker.celery_app beat --loglevel=info
  ```

- **Current Developments**:
  - As of now, we are running the celery commands in the terminal of the server.
  - The scripts run in this order:
    - 1. DailyMorning (Which logins to all users, downloads the instrument csv file and starts the equity calculation)
    - 2. During the market orders, the strategy script is called and the trades are placed.
    - 3. After the market hours, GoodEvening scripts are executed(sweep orders, dailytradevalidator, dailyeodblog, dailytradereport)


## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [Alembic](https://alembic.sqlalchemy.org/) for database migrations.
