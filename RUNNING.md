# Running Provenance Guard

## Environment
Tested environment:

- OS: Linux / WSL
- Python: 3.11.18
- PyTorch: 2.15.0
- Transformers: 4.57.6
- Flask: 3.1.3
- Flask-Limiter: 3.12

The detector runs locally using GPT-2 on CPU. The first run downloads approximately 526 MB of model files from Hugging Face. An internet connection is required for this initial download.

## Setup
Clone the repository:

```
git clone git@github.com:Dennis-Shlaih/ai201-project4-provenance-guard-starter-v2026.git
cd ai201-project4-provenance-guard-starter-v2026
```

Create and activate a virtual environment:

```
python3.11 -m venv .venv
source .venv/bin/activate
```

Install the pinned dependencies:

```
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
```

## Start the service
From the project root, run:

```
python app.py
```

The service starts locally at:

`http://127.0.0.1:5000`

The first startup or first scoring request may take longer because GPT-2 needs to be downloaded and loaded.

## Verify the service
In another terminal, check the health endpoint:

```
curl http://127.0.0.1:5000/health
```

Check the example endpoint:

```
curl http://127.0.0.1:5000/ping
```

Submit a sample:

```
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "creator_id": "running-test",
    "text": "This is a sample submission used to verify that Provenance Guard is running."
  }'
```

A successful submission returns the classification, confidence, individual signal scores, and combined score.

## Logs
Decision and appeal records are written to the configured audit log as JSON Lines. The `/log` endpoint can be used to inspect recorded entries.

## Limitations

- This is a local deployment, not a publicly hosted service.
- GPT-2 runs on CPU in the tested environment.
- The first model download requires an internet connection.
- Classification scores are heuristic signals, not proof of authorship.

## Troubleshooting

- If Python 3.11 is not installed, install it before creating the virtual environment.
- If dependency installation fails, verify that the virtual environment is activated.
- If GPT-2 fails to load, check your internet connection and available disk space.
- If port 5000 is already in use, stop the other process before restarting the service.