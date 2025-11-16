from google.adk.tools import ToolContext
from google.oauth2.credentials import Credentials

def send_email(tool_context: ToolContext, **kwargs):
    '''
    Gmail Apiを使ってユーザーに作成済みのコードを配信します。
    '''
    

