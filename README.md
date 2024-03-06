# currency-converter-stats-calculator
Web Application to Convert Currencies and Perform Calculations Statistics

# Engineering Department Codebase Setup Guide

This guide provides step-by-step instructions for setting up the development environment for the Engineering department's codebase. The codebase utilizes Python with Flask for the backend and Tailwind CSS for the frontend.

## Supported Operating Systems
- Windows
- macOS
- Linux

## Prerequisites
Before you begin, ensure you have the following software installed on your system:
- [Python](https://www.python.org/)
- [Node.js](https://nodejs.org/en) and npm
- Git

## Getting Started

### Clone the Repository
1. Open a terminal or command prompt.
2. Navigate to the directory where you want to store the codebase.
3. Run the following command to clone the repository:
   ```
   git clone <repository_url>
   ```

### Install Dependencies
1. Navigate to the root directory of the cloned repository.
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Node.js dependencies:
   ```
   npm install
   ```

### Running the Codebase
1. Start the Flask app by running:
   ```
   python app.py
   ```
2. If working with Tailwind CSS, build the CSS file:
   ```
   npm run buildcss
   ```

## Troubleshooting
- **Dependency Issues**: Ensure correct versions of Python and Node.js/npm are installed. Check `requirements.txt` and `package.json` for correct dependencies.
- **Permission Denied**: Authenticate with appropriate permissions to access the repository on GitHub.
- **Flask App Not Running**: Check for missing dependencies or incorrect configurations in the Flask application.
- **Tailwind CSS Build Error**: Verify paths in `tailwind.config.js` for input and output files.

https://www.exchangerate-api.com/docs/supported-codes-endpoint

