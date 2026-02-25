import os

APP_NAME = "Secure API (OWASP Lab)"

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-prod")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_ISSUER = os.getenv("JWT_ISSUER", "secure-api-owasp-lab")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "secure-api-clients")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "15"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")