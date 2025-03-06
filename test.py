from flask import Flask, redirect, request, session, url_for, render_template_string
from requests_oauthlib import OAuth2Session
from itsdangerous import URLSafeSerializer
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 必须设置密钥用于session加密
app.config['SESSION_COOKIE_NAME'] = 'session'

# OAuth2 配置
OAUTH_SERVER = 'https://itoauth.ctrip.com'
CLIENT_ID = 'test'
CLIENT_SECRET = 'test_secret'
REDIRECT_URI = 'http://127.0.0.1:5000/auth/it/cb'

# 初始化CSRF保护
csrf_serializer = URLSafeSerializer(app.secret_key)

def get_oauth_client(token=None):
    """创建OAuth2Session实例"""
    return OAuth2Session(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=['user'],
        token=token,
        auto_refresh_kwargs={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        auto_refresh_url=f'{OAUTH_SERVER}/oauth/token'
    )

@app.route('/')
def index():
    if not session.get('userId'):
        # 生成CSRF token
        state = csrf_serializer.dumps({'csrf': os.urandom(24).hex()})
        session['state'] = state
        
        # 构建授权URL
        oauth = get_oauth_client()
        auth_url, _ = oauth.authorization_url(
            f'{OAUTH_SERVER}/oauth/authorize',
            state=state,
            identityauth2=request.args.get('identityauth2')
        )
        return redirect(auth_url)
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Demo</title></head>
        <body>
            <h1>Hello {{ user_id }}</h1>
        </body>
        </html>
    ''', user_id=session['user_id'])

@app.route('/auth/it/cb')
def callback():
    # 错误处理
    if 'error' in request.args:
        return f"{request.args['error']}: {request.args.get('error_description')}"
    
    # 验证state参数
    state = request.args.get('state')
    if not state or state != session.get('state'):
        return "Invalid state parameter", 400
    
    # 获取access token
    oauth = get_oauth_client()
    token = oauth.fetch_token(
        f'{OAUTH_SERVER}/oauth/token',
        client_secret=CLIENT_SECRET,
        authorization_response=request.url,
        include_client_id=True
    )
    
    # 获取用户信息
    response = oauth.get(f'{OAUTH_SERVER}/oauth/user/getUserInfo')
    user_info = response.json()
    session['user_id'] = user_info.get('userId')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)

