# LinkedIn Data Extractor 🚀

A Python and FastAPI application for reading LinkedIn URLs from an Excel spreadsheet and extracting structured profile data using batching, checkpointing, and reporting.

## 📁 Project Structure

```text
linkedin_data_extractor/
│
├── data/
│   ├── input.xlsx       # Input Excel file with LinkedIn URLs
│   ├── output.json      # Extracted profile records
│   └── errors.json      # Error logs & performance metrics
│
├── app/
│   ├── __init__.py
│   ├── excel_reader.py  # Reads and validates LinkedIn URLs
│   ├── extractor.py     # Profile extraction engine with fallback mode
│   ├── processor.py     # Normalizes and saves records
│   └── reporter.py      # Generates summary statistics & metrics
│
├── config.py            # Environment configurations
├── main.py              # FastAPI server & CLI pipeline
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
└── README.md
```

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kratikasharma2003-byte/Linkdin_excel.git
   cd Linkdin_excel/linkedin_data_extractor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your settings (API URL, API Key, LinkedIn credentials, etc.).

## 🚀 Running the Project

### Option 1: FastAPI Web Server (Uvicorn)
Start the ASGI server:
```bash
uvicorn main:app --reload --port 8001
```
- Open Swagger UI in browser: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- Base URL: [http://127.0.0.1:8001](http://127.0.0.1:8001)

### Option 2: CLI Mode
Run the extraction directly from the command line:
```bash
python main.py --cli
```

## 📡 API Endpoints

- `GET /` - Service status & overview
- `GET /docs` - Interactive Swagger documentation
- `POST /extract` - Trigger extraction synchronously
- `POST /extract/background` - Trigger extraction as a background task
- `GET /status` - Check current extraction progress & last report
- `GET /records` - View extracted profiles
- `GET /errors` - View error logs and validation issues
