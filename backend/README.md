# Backend

This is the backend for the LUCY-test project, an epigenetic analysis system.

## Setup

1. Configure environment variables:
   - Copy `.env.example` to `.env.development` and `.env.production`
   - Update the variables in these files according to your development and production environments

## Data Preparation

1. Place IDAT files in the correct directory:
   ```
   data/raw/run1/
   ```

2. Prepare the Sample Sheet (CSV file) with the following columns:
   - Sample_Name
   - Sentrix_ID
   - Sentrix_Position
   - customer (should match user names in the database)

3. Place the Sample Sheet in:
   ```
   data/raw/run1/Sample_Sheet.csv
   ```

## User Creation

Before importing sample data, you need to create user accounts in the database. You can do this using the API endpoint:

1. Ensure the backend server is running.

2. Use a tool like PowerShell or curl to send a POST request to create a user. Here's an example using PowerShell:

   ```powershell
   $body = @{
       name = "Yi-Hsuan Wu"
       email = "yixuan@gmail.com"
       password = "password123123"
       birthday = "1997-02-12"
       phone_number = "0933615427"
   } | ConvertTo-Json

   $headers = @{
       "Content-Type" = "application/json"
   }

   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users/" -Method Post -Body $body -Headers $headers
   ```

   Adjust the user details as needed for each user you want to create.

3. Repeat this process for all users that need to be in the system before importing samples.

## Initial Data Import

1. After creating the necessary user accounts, run the sample import script:
   ```
   python backend/scripts/import_samples.py
   ```
   This will populate the SampleData table with information from the Sample Sheet.

## Generating Reports

To generate reports for the imported samples:

1. Ensure all required R scripts and libraries are installed and properly configured.

2. Run the report generation script:
   ```
   python app/services/report_generator.py
   ```
   This script will:
   -