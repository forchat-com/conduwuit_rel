import requests
import time

# 生成用户名列表
usernames = [f"test{i}" for i in range(1, 101)]

# 注册API的URL
register_url = "http://127.0.0.1:8008/_matrix/client/v3/register"

# 注册请求的固定部分
password = "test123"
kind = "user"
registration_token = "o&^uCtes4HPf0Vu@F20jQeeWE7"  # 请确保这是有效的注册令牌

# 头信息，Content-Type设为application/json
headers = {
    "Content-Type": "application/json"
}

for username in usernames:
    # 首先获取新的 session
    init_response = requests.post(register_url, json={}, headers=headers, verify=False)
    if init_response.status_code == 401:
        init_data = init_response.json()
        session = init_data.get('session')
        if not session:
            print(f"无法获取 session，用户名 {username} 注册失败，响应: {init_response.status_code}，内容: {init_response.text}")
            continue  # 跳过当前用户名

        # 构建 auth 字段
        auth = {
            "type": "m.login.registration_token",
            "session": session,
            "token": registration_token
        }

        # 构建注册请求的 JSON 数据
        data = {
            "username": username,
            "password": password,
            "kind": kind,
            "auth": auth
        }

        try:
            # 发送注册请求
            response = requests.post(register_url, json=data, headers=headers, verify=False)
            if response.status_code == 200 or response.status_code == 201:
                print(f"用户 {username} 注册成功")
            else:
                print(f"用户 {username} 注册失败，响应: {response.status_code}，内容: {response.text}")
        except Exception as e:
            print(f"用户 {username} 注册时发生错误: {e}")
    else:
        print(f"无法获取新的 session，用户名 {username} 注册失败，响应: {init_response.status_code}，内容: {init_response.text}")

    # 为了避免触发频率限制，休眠一段时间
    # time.sleep(0.01)
