import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

# .env 파일 로드
if load_dotenv:
    load_dotenv()
else:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, sep, value = line.partition("=")
                if sep:
                    os.environ.setdefault(key.strip(), value.strip())

# 환경 변수 확인
print("[OK] API 키 설정됨" if os.getenv("OPENAI_API_KEY") else "[ERROR] API 키 미설정")
