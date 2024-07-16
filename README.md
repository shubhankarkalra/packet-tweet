# packet-tweet
This Web App core functionality of fetching tweet data and generating a screenshot. 

## Overview

Brief description of the project.

## Prerequisites

- Python 3.8 or newer
- Mac OS

## Setting Up the Environment

For this application, I recommend using Python 3.8 or newer. Here are the steps to set up the environment on your Mac OS machine:

1. **Check Python Version:**

    Ensure you have Python 3.8 or newer installed:
    ```bash
    python3 --version
    ```
    If it's not 3.8 or newer, you'll need to install a newer version.

2. **Install Python (if needed):**

    The easiest way to install Python on Mac is using Homebrew. If you don't have Homebrew installed, install it first:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
    Then install Python:
    ```bash
    brew install python@3.11
    ```
    This will install Python 3.11, which is a recent stable version.

3. **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    ```

4. **Activate the Virtual Environment:**

    ```bash
    source venv/bin/activate
    ```

5. **Upgrade pip:**

    ```bash
    pip install --upgrade pip
    ```

6. **Check pip Version:**

    ```bash
    pip --version
    ```
    You should have pip 21.0 or newer.

7. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

8. **Install Playwright Browsers:**

    ```bash
    playwright install
    ```

## **Running the Application**

**Now your environment is set up and ready to run the application. To start the server:**

```bash
uvicorn app.main:app --reload


