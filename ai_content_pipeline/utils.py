import os
import json
import hashlib
import random
from datetime import datetime


def now_ts():
    return datetime.utcnow().isoformat() + 'Z'


def read_env():
    return {k: v for k, v in os.environ.items()}


def seed_from_text(text):
    h = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return int(h[:16], 16)


def deterministic_choice(seed_text, options):
    r = random.Random(seed_from_text(seed_text))
    return r.choice(options)


def save_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_outputs_dir(base):
    out = os.path.join(base, 'outputs')
    os.makedirs(out, exist_ok=True)
    return out


def write_run_log(base, text):
    path = os.path.join(base, 'outputs', 'run_log.txt')
    ts = now_ts()
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {text}\n")
