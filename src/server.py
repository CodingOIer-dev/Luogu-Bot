from loguru import logger as log
import luogu as requests
import json
import time
import openai
import threading

_uid = 0
max_token = 0
tips = ''
cookie = ''
__client_id = ''
deepseek_key = ''
allow = {}
reporting = {}
command = {}
black = []


def loadSettings():
    '''
    从 ./settings.json 中读取设置
    '''
    global cookie, _uid, __client_id, command, deepseek_key, max_token, tips, allow
    try:
        try:
            with open('./allow.json', 'r', encoding='utf-8') as f:
                allow = json.load(f)
            log.success('Load allow users')
        except:
            pass
        with open('./settings.json', 'r', encoding='utf-8') as f:
            js = json.load(f)
            command = js['command']
            _uid = js['_uid']
            __client_id = js['__client_id']
            cookie = f'_uid={_uid}; __client_id={__client_id};'
            deepseek_key = js['deepseek-key']
            max_token = js['max_token']
            tips = js['tips']
        log.success('Load settings')
    except:
        log.critical('Can not load settings')


def getGetHeaders():
    '''
    获取 GET 请求的请求头
    '''
    # log.info('Get headers for GET')
    return {
        'user-agent': '',
        'referer': 'https://www.luogu.com.cn/',
        'cookie': cookie,
        'x-luogu-type': 'content-only',
    }


def getCsrfToken():
    '''
    获取 x-csrf-token 鉴权 token
    '''
    # log.info('Get csrf token')
    return (
        requests.get(url=f'https://www.luogu.com.cn/', headers=getGetHeaders())
        .text.split("<meta name=\"csrf-token\" content=\"")[-1]
        .split("\">")[0]
    )


def getPostHeaders():
    '''
    获取 POST 请求的请求头
    '''
    # log.info('Get headers for POST')
    return {
        'user-agent': '',
        'referer': 'https://www.luogu.com.cn/',
        'cookie': cookie,
        'x-csrf-token': getCsrfToken(),
    }


def send(uid, msg):
    '''
    发送私信
    '''
    try:
        response = requests.post(
            url='https://www.luogu.com.cn/api/chat/new',
            headers=getPostHeaders(),
            json={
                'user': uid,
                'content': msg,
            },
        )
        if response.status_code == 200:
            log.success(f'Send message to {uid}')
        else:
            log.warning(
                f"Can not send message to {uid}, HTTP ERROR {response.status_code}, {json.loads(response.content)['data']}"
            )
    except:
        log.error('Run time error')


def problem(pid):
    '''
    获取题目信息
    '''
    try:
        pid = str(pid).split('/')[-1]
        response = requests.get(
            url=f'http://www.luogu.com.cn/problem/{pid}', headers=getGetHeaders()
        )
        js = json.loads(response.content)
        if js['code'] == 200:
            log.success(f'Get problem {pid}')
            return f"""
# 题目编号：
{js['currentData']['problem']['pid']}

# 题目标题：
{js['currentData']['problem']['title']}

# 题目提供者：
{js['currentData']['problem']['provider']['name']}

# 题目描述：
{js['currentData']['problem']['description']}

# 输入格式：
{js['currentData']['problem']['inputFormat']}

# 输出格式：
{js['currentData']['problem']['outputFormat']}

# 提示信息：
{js['currentData']['problem']['hint']}
"""
        else:
            log.warning(
                f"Can not get problem {pid}, HTTP ERROR {js['code']}, {js['currentData']['errorMessage']}"
            )
            return 'ERROR'
    except:
        log.error('Run time error')
        return 'ERROR'


def paste(pid):
    '''
    获取剪切板信息
    '''
    try:
        pid = str(pid).split('/')[-1]
        response = requests.get(
            url=f'https://www.luogu.com/paste/{pid}', headers=getGetHeaders()
        )
        js = json.loads(response.content)
        if js['code'] == 200:
            log.success(f'Get paste {pid}')
            return f"""
# 剪切板编号
{pid}

# 剪切板作者
{js['currentData']['paste']['user']['name']}

# 剪切板内容
{js['currentData']['paste']['data']}
"""
        else:
            log.warning(
                f"Can not get paste {pid}, HTTP ERROR {js['code']}, {js['currentData']['errorMessage']}"
            )
            return 'ERROR'
    except:
        log.error('Run time error')
        return 'ERROR'


def discuss(did):
    '''
    帖子信息
    '''
    try:
        did = str(did).split('/')[-1]
        response = requests.get(
            url=f'https://www.luogu.com.cn/discuss/{did}', headers=getGetHeaders()
        )
        js = json.loads(response.content)
        if js['code'] == 200:
            log.success(f'Get discuss {did}')
            res = f"""
# 帖子标题
{js['currentData']['post']['title']}

# 帖子内容
{js['currentData']['post']['content']}

# 帖子作者
{js['currentData']['post']['author']['name']}

# 回复
"""
            for reply in js['currentData']['replies']['result']:
                res = f"""{res}
{reply['author']['name']}: {reply['content']}
"""
            return res
        else:
            log.warning(
                f"Can not get discuss {did}, HTTP ERROR {js['code']}, {js['currentData']['errorMessage']}"
            )
            return 'ERROR'
    except:
        log.error('Run time error')


def progressMessage(content):
    '''
    处理消息中的链接
    '''
    try:
        res = ''
        inUrl = False
        url = ''
        for x in content:
            if x == '「':
                url = ''
                inUrl = True
                continue
            if x == '」':
                if url.find('problem') != -1:
                    res += f'「{problem(url)}」'
                elif url.find('paste') != -1:
                    res += f'「{paste(url)}」'
                elif url.find('discuss') != -1:
                    res += f'「{discuss(url)}」'
                else:
                    res += '「ERROR」'
                inUrl = False
                continue
            if inUrl:
                url += x
            else:
                res += x
        log.info('Process a message')
        return res
    except:
        log.error('Run time error')


def chat(uid):
    '''
    获取对话信息
    '''
    try:
        res = []
        response = requests.get(
            f'https://www.luogu.com.cn/api/chat/record?user={uid}',
            headers=getGetHeaders(),
        )
        js = json.loads(response.content)
        count = js['messages']['count']
        page = (count + 49) // 50
        l2 = js['messages']['result']
        if page != 1:
            response = requests.get(
                f'https://www.luogu.com.cn/api/chat/record?user={uid}&page={page-1}',
                headers=getGetHeaders(),
            )
            l1 = js['messages']['result']
        else:
            l1 = []
        bk = False
        l1 = l1[::-1]
        l2 = l2[::-1]
        for ms in l2:
            if ms['content'] == ':clear':
                bk = True
                break
            if ms['content'][0] == ':' or ms['content'][0] == '~':
                continue
            if ms['sender']['uid'] == uid:
                res.append(
                    {
                        'role': 'user',
                        'content': progressMessage(ms['content']),
                    }
                )
            else:
                res.append(
                    {
                        'role': 'assistant',
                        'content': progressMessage(ms['content']),
                    }
                )
        if not bk:
            for ms in l1:
                if ms['content'] == ':clear':
                    break
                if ms['sender']['uid'] == uid:
                    res.append(
                        {
                            'role': 'user',
                            'content': progressMessage(ms['content']),
                        }
                    )
                else:
                    res.append(
                        {
                            'role': 'assistant',
                            'content': progressMessage(ms['content']),
                        }
                    )
        res = res[::-1]
        log.success(f'Get chat of user {uid}, count is {len(res)}')
        return res
    except:
        log.error('Run time error')


def user(uid):
    '''
    获取用户信息
    '''
    try:
        res = json.loads(
            requests.get(
                url=f'https://www.luogu.com.cn/api/user/search?keyword={uid}',
                headers=getGetHeaders(),
            ).content
        )['users'][0]
        log.success(f'Get the information of {uid}')
        return res
    except:
        log.warning(f'Can not get information of {uid}, return user 1')
        return user(1)


def report(uid):
    '''
    回复用户
    '''
    try:
        log.info(f'Start report user {uid}')
        memory = chat(uid)
        memory = memory[::-1]
        memory.append(
            {
                'role': 'assistant',
                'content': tips.replace('{username}', user(uid)['name']),
            }
        )
        memory = memory[::-1]
        client = openai.OpenAI(
            api_key=deepseek_key, base_url='https://api.deepseek.com'
        )
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=memory,
            stream=True,
            max_tokens=max_token,
        )
        temp = ''
        reason = None
        for data in response:
            if data == '[DONE]':
                break
            temp += data.choices[0].delta.content
            if len(temp) >= 250:
                send(uid, temp)
                temp = ''
            if data.choices[0].finish_reason != None:
                if data.choices[0].finish_reason == 'length':
                    reason = '达到最大 token 限制，请缩减上下文。'
                elif data.choices[0].finish_reason == 'content_filter':
                    reason = '模型输出内容被过滤，请重新审视你发送的信息。'
                elif data.choices[0].finish_reason == 'insufficient_system_resource':
                    reason = '服务商后端推理压力过大，请稍后重试。'
        if len(temp) != 0:
            send(uid, temp)
        if reason != None:
            send(uid, reason)
            log.warning(f'Unexpected ending, {reason}')
        log.success(f'Finish reporting user {uid}')
    except:
        log.error('Run time error')
    reporting[uid] = False


currentTime = int(time.time())


def slowMain():
    global black
    while True:
        try:
            with open('./black.txt', 'r', encoding='utf-8') as f:
                list = f.readlines()
                black = []
                for x in list:
                    black.append(x.replace('\n', ''))
        except:
            black = []
        with open('./allow.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(allow))
        time.sleep(15)


def main():
    '''
    主循环 获取发送的消息
    '''
    global currentTime
    while True:
        try:
            response = requests.get(
                url='https://www.luogu.com.cn/chat', headers=getGetHeaders()
            )
            js = json.loads(response.content)
            for session in js['currentData']['latestMessages']['result']:
                if session['time'] > currentTime and session['sender']['uid'] != _uid:
                    try:
                        send(session['sender']['uid'], command[session['content']])
                        if session['content'] == ':on':
                            allow[str(session['sender']['uid'])] = True
                        elif session['content'] == ':off':
                            allow[str(session['sender']['uid'])] = False
                        log.success(f"User {session['sender']['uid']} use command")
                    except:
                        if reporting.get(session['sender']['uid'], False):
                            log.warning(
                                f"User {session['sender']['uid']} ask too quickly"
                            )
                        elif (
                            session['content'][0] != '~'
                            and session['content'][0] != ':'
                            and session['sender']['uid'] not in black
                            and allow.get(str(session['sender']['uid']), True)
                        ):
                            threading.Thread(
                                target=report, args=(session['sender']['uid'],)
                            ).start()
            currentTime = js['currentData']['latestMessages']['result'][0]['time']
        except:
            log.error('Run time error')
        time.sleep(1)


if __name__ == '__main__':
    loadSettings()
    tips = tips.replace('{root}', user(_uid)['name'])
    threading.Thread(target=slowMain).start()
    threading.Thread(target=main).start()
