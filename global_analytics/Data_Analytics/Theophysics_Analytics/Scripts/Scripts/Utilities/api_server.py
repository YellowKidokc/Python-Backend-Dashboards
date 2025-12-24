import os, json, uvicorn, requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
PROVIDER = os.getenv("AI_PROVIDER", "stub")  # "openai" | "anthropic" | "stub"

class Payload(BaseModel):
    yaml: str = ""
    body: str = ""

app = FastAPI(title="Theophysics AI Service")

def stub_reply() -> Dict[str, Any]:
    return {
        "version":"1.0",
        "meta":{"model":"stub","latency_ms": 12,"cost_estimate":0.0},
        "classify":{
            "series":"TH","type":"law","phase":"05_Doctrine","visibility":"research","status":"draft",
            "trinity_aspects":{"Father":0.95,"Son":0.92,"Spirit":0.93}
        },
        "mathematics":{"checks":["CoherenceLagrangian"],"issues":[],"notes":"looks consistent"},
        "metrics":{"breakthrough_score":0.72,"coherence_score":0.91,"trinity_coherence_index":0.90},
        "tags":["theophysics","trinity","master-equation"],
        "relationships":{
            "builds_on":["TH-000-Foundations"],"supports":["JS-002-LightDuality"],
            "contradicts":[],"unifies":["QuantumGraceFunction"],"relates_to":["Grace","Coherence"]
        },
        "links":[{"title":"Grace (G)","target_uid":"TH-ATOM-G","rel":"relates_to"}],
        "next_actions":["Add math derivation"],
        "proposed_yaml_overrides":{
            "keywords":["coherence","negentropy"],"experiments":["DorothyProtocol"],"scripture_refs":["John 1:1"]
        },
        "ai_block":"- breakthrough_score: 0.72\n- add tag: #theophysics"
    }

@app.post("/analyze")
def analyze(p: Payload):
    if not p.yaml and not p.body:
        raise HTTPException(status_code=400, detail="empty note")

    if PROVIDER == "stub" or (PROVIDER == "openai" and not OPENAI_KEY) or (PROVIDER == "anthropic" and not ANTHROPIC_KEY):
        return stub_reply()

    try:
        if PROVIDER == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
            sys = "You are the Theophysics Vault Architect. Return JSON ONLY matching the agreed schema."
            user = f"YAML:\n{p.yaml}\n\nBODY:\n{p.body}"
            payload = {"model":"gpt-4o-mini","messages":[{"role":"system","content":sys},{"role":"user","content":user}], "temperature":0}
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            txt = r.json()["choices"][0]["message"]["content"]
            return json.loads(txt)

        elif PROVIDER == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
            headers = {"x-api-key": ANTHROPIC_KEY, "anthropic-version":"2023-06-01", "content-type":"application/json"}
            sys = "You are the Theophysics Vault Architect. Return JSON ONLY matching the agreed schema."
            user = f"YAML:\n{p.yaml}\n\nBODY:\n{p.body}"
            payload = {"model":"claude-3-5-sonnet-20241022","max_tokens":2000,"system":sys,"messages":[{"role":"user","content":user}]}
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            txt = "".join([b.get("text","") for b in r.json().get("content",[]) if b.get("type")=="text"])
            return json.loads(txt)

    except Exception as e:
        return stub_reply()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
