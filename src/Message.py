import mimetypes
from base64 import b64encode


class Message:
    messageEnd = '\r\n.\r\n'  # 结束DATA指令
    lf = '\n'  # 不同的header字段以换行分隔(\n)
    bl = '\n\n'
    boundaryChars = 'Star-Boundary'  # Content-Type: Multipart/xxx 头后定义分隔符
    boundary = f'--{boundaryChars}'  # 多部分分隔,分隔符前追加--
    boundaryEnds = f'--{boundaryChars}--'  # 分隔结束, 分隔符前后追加--
    types = [{'type': 'text', 'subType': {'plain', 'html', 'xml', 'css'}}]

    def __init__(self, subject: str, content: str = ''):

        self.headers = {
            'Subject': subject,
            'Content-Type': f'Multipart/Mixed; boundary={self.boundaryChars}',
        }
        self.body = [{
            'Content-Type': 'text/plain; charset=utf-8',
            'content': content
        }]
        self.message = ''

    def add_content(self, content: str, types: str = 'text/plain', charset: str = 'utf-8'):
        if self.is_valid_type(types):
            self.body.append({
                'Content-Type': f'{types}; charset={charset}',
                'content': content
            })
        else:
            pass

    def attach(self, filepath: str = None):
        body = self.read_file(filepath)
        if body:
            self.body.append(body)
        else:
            pass

    def is_valid_type(self, types):
        t, subType = types.split('/')
        for item in self.types:
            if t == item['type'] and subType in item['subType']:
                return True
        return False

    @staticmethod
    def read_file(filepath=None) -> dict:
        if not filepath:
            return {}
        mime_type, _ = mimetypes.guess_type(filepath)
        filename = filepath.split('/')[-1]

        with open(filepath, 'rb') as f:
            img = b64encode(f.read()).decode()

        return {
            'Content-Type': f'{mime_type}; name="{filename}',
            'Content-Transfer-Encoding': 'base64',
            'content': img
        }

    def _toStr(self):
        # header 与body之间以空行分隔
        self.message = self._strHeaders + self.bl + self._strBody + self.messageEnd

    @property
    def _strBody(self) -> str:
        body = ''
        for b in self.body:
            body += self.boundary + self.lf
            content = b.pop('content')
            for name, value in b.items():
                body += name + ':' + value + self.lf
            # 内容前后空行
            body += self.bl + content + self.bl
        body += self.boundaryEnds
        return body

    @property
    def _strHeaders(self) -> str:
        header = ''
        for key, value in self.headers.items():
            header += key + ':' + value + self.lf
        return header

    def encode(self) -> bytes:
        if not self.message:
            self._toStr()
        return self.message.encode()

    def endswith(self, end: str) -> bool:
        if not self.message:
            self._toStr()
        return self.message.endswith(end)

    def __add__(self, other: str) -> str:
        return self.message + other
