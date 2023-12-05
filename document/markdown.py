import os
import re
from typing import Self
from .base import Data, Document, Message

END = '\n'
SPACE = '\x20'
TITLE_SIGN = '#'
REPLACE_FORMATTER = (
    (r'(\\)',  r'\\\1'),     # 转义\号
    (r'(\*)',  r'\\\1'),     # 转义*号
    (r'(\_)',  r'\\\1'),     # 转义_号
    (r'(\`)',  r'\\\1'),     # 转义`号
    (r'(\|)',  r'\\\1'),     # 转义|号
    (r'(!)',  r'\\\1'),      # 转义!号
    (r'(\[|\])',  r'\\\1'),  # 转义[]
    (r'(\(|\))',  r'\\\1'),  # 转义()
    (r'^(\x20*[0-9]+)(\.)(\x20)',  r'\1\\\2\3'),   # 有序列表
    (r'^(\x20*)(-|\*|\+)(\x20)',  r'\1\\\2\3'),    # 无序列表
    (r'^(\x20*)(#{1,6})(\x20)',  r'\1\\\2\3'),     # 标题
    (r'^(\x20*)(>)(.*)',  r'\1\\\2\3'),            # 引用
    (r'^(\x20*)(\*{3,}|-{3,}|_{3,})(\x20*)$',  r'\1\\\2\3'),  # 分隔线
    (r'^\s*$',  ''),
)

RECOGNIZE_FORMATTER = ()


class Markdown(Document):

    def __init__(self, data: str = "") -> None:
        super().__init__(data)

    def escape(text: str):
        """
        转义文本
        - text: str, 待转义文本
        """
        if isinstance(text, Markdown):
            text = text.content
        for pattern, repl in REPLACE_FORMATTER:
            text = re.sub(pattern, repl, text, flags=re.M)
        return text

    def last_line(self):
        "切换到上一行"
        self.data >> END

    def next_line(self):
        "切换到下一行"
        self.data << END

    def add_title(self, text: str, level: int):
        self.data << TITLE_SIGN * level << SPACE << text << END

    def add_text(self, text: str):
        text = self.escape(text)
        self.data << text

    def normalize(self) -> Message:
        ...

    def export(self, name: str, directory: str = './'):
        directory = os.path.abspath(directory)
        with open(directory + '/' + name + '.md', 'w+', encoding='utf-8') as file:
            file.write(self.__str__())

    @staticmethod
    def transform(source: Document) -> 'Markdown':
        document = Markdown.load_from_message(source.message)
        return document
    
    def load_from_message(message: Message | list[Message]) -> Self:
        """
        从消息中加载markdown。
        - message: Message, 传入的消息。
        """
        data = Data()

        return Markdown(data.content)

    @staticmethod
    def load(path: str) -> 'Markdown':
        with open(path, 'r+', encoding='utf-8') as file:
            text = file.read()
        return Markdown(text)

            
    def __document__(self):
        ...