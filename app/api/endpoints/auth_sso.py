from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.config import Config

from ...adapters.auth.googleAuth import oauth
from ..dependencies.databaseConfig import get_db
from app.models.user import User
from ...service.auth import create_access_token

config = Config(".env")
BASE_URL = config("BASE_URL", default="http://localhost:8000")

# Map provider name → oauth client
PROVIDERS = {
    "google": oauth.google,
    "microsoft": oauth.microsoft,
}

router = APIRouter( tags=["sso"])


# ─────────────────────────────────────────────
# 1. Redirect user to SSO provider
# ─────────────────────────────────────────────
@router.get("/auth/login/{sso_type}")
async def sso_login(sso_type: str, request: Request):
    provider = PROVIDERS.get(sso_type.lower())
    if not provider:
        raise HTTPException(status_code=400, detail=f"Unsupported SSO type: {sso_type}")

    redirect_uri = f"{BASE_URL}/auth/callback/{sso_type}"
    return await provider.authorize_redirect(request, redirect_uri)


# ─────────────────────────────────────────────
# 2. Google redirects back here (MUST be GET)
# ─────────────────────────────────────────────
@router.get("/auth/callback/{sso_type}", name="sso_callback")  # ← GET not POST
async def sso_callback(
    sso_type: str,
    request: Request,
    db: Session = Depends(get_db)
):
    provider = PROVIDERS.get(sso_type.lower())
    if not provider:
        raise HTTPException(status_code=400, detail="Unsupported SSO type")

    # Exchange the ?code= query param for a token (authlib handles this)
    try:
        token = await provider.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Could not fetch user info")

    email = user_info.get("email")

    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(
                email=email,
                name=user_info.get("name", email.split("@")[0]),
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ─────────────────────────────────────────────
# 3. Microsoft fixed callback (no sso_type in path)
# ─────────────────────────────────────────────
@router.get("/auth/callback", name="microsoft_callback")
async def microsoft_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.microsoft.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Could not fetch user info")

    email = user_info.get("email")

    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                name=user_info.get("name", email.split("@")[0]),
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ─────────────────────────────────────────────
# 4. Logout
# ─────────────────────────────────────────────
@router.post("/logout")   # POST is safer than GET for logout
async def logout(request: Request):
    request.session.clear()
    # JWT is stateless — to fully invalidate, add token to a Redis blocklist here
    return {"message": "Logged out. JWT will expire on its own."}

@router.get("/debug-uri")
async def debug_uri(request: Request):
    uri = request.url_for("sso_callback", sso_type="google")
    return {"redirect_uri": str(uri)}