from fastapi import FastAPI, Request
import uvicorn
from starlette.responses import HTMLResponse
from authentication.oauth import google, github
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret", max_age=100)

@app.get("/login")
async def login():
    return HTMLResponse(
        """
        <p>Please choose which to use for authenticating:</p>
        <a href='/login/google'> Google </a>
        <br>
        <a href='/login/github'> Github </a>
        """
    )


@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_callback_google")
    return await google.authorize_redirect(request, redirect_uri)

@app.get("/login/github")
async def login_github(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await github.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token_data = await github.authorize_access_token(request)
    token = token_data.get('access_token')
    print(f"GITHUB TOKEN: {token}")
    return {'token': token}



@app.get("/auth/callback/google")
async def auth_callback_google(request: Request):
    token_data = await google.authorize_access_token(request)
    token = token_data.get('access_token')
    return {'token': token}


@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return 'Logged out successfully'


if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8001)


