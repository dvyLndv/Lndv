# Hello Im dvy if u can see this line U IS DOG :-)
import re
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi import Message, ThreadType, Mention, MessageStyle, MultiMsgStyle
import time
import threading
import psutil
from datetime import datetime
import shutil
import json

print(f"\033[34mThis is blue text\033[34m")

def lenhadminvip():
    try:
        with open('admin.json', 'r') as adminvip:
            adminzalo = json.load(adminvip)
            return set(adminzalo.get('idadmin', []))
    except FileNotFoundError:
        return set()

idadmin = lenhadminvip()

class Lndv(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.spamming = False
        self.spam_thread = None
        self.spammingvip = False
        self.spam_threadvip = None
        self.sendCard = None
        self.start_time = time.time()

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type, phone=None):
        if not isinstance(message, str):
            try:
                # Xử lý lỗi nếu tin nhắn không phải là chuỗi
                message_text = str(message)  # Chuyển đổi đối tượng tin nhắn thành chuỗi
            except Exception as e:
                print(f'Lỗi khi xử lý tin nhắn: {e}')
                return
        else:
            message_text = message

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"THỜI GIAN NOW: {current_time}")
        print(f"[{current_time}] tin nhắn nhận được: {message_text}")
        print(f"Id: {author_id}")

        # Xử lý tin nhắn
        if message_text == "upt":
            uptime_info = self.uptime()
            try:
                self.sendBusinessCard(
                    userId=author_id,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    phone=uptime_info,
                    qrCodeUrl=""
                )
            except ZaloAPIException as e:
                print(f"Lỗi: {e}")
                self.replyMessage(
                    Message(text="Đã xảy ra lỗi"),
                    message_object,
                    thread_id,
                    thread_type
                )
        print(f"\033[34m{message} \033[39m|\033[31m {author_id}\033[0m\n")
        content = message_object.content if message_object and hasattr(message_object, 'content') else ""
        if not isinstance(message, str):
            print(f"{type(message)}")
            return                                            
        if message.startswith(">help"):
            mention = Mention(author_id, length=7, offset=0)
            color = MessageStyle(style="color", color="#a24ffb", offset=0, length=2500, auto_format=False)
            smallfont = MessageStyle(style="italic", size="12", offset=0, length=2500, auto_format=False)
            smallfont = MessageStyle(style="font", size="10", offset=0, length=2500, auto_format=False)           
            style = MultiMsgStyle([color, smallfont])
            self.send(
                Message(
            text=('''
        
 @member\n*All Commands:\n
▓▓▓▓█░░░L░░░░▓▓▓▓█
▓▓▓▓█░░░n░░░░▓▓▓▓█
▓▓▓▓█░░░d░░░░▓▓▓▓█
▓▓▓▓█░░░v░░░░▓▓▓▓█
 👾👾👾👾👾👾👾👾
>help: User Command
  To show all commands
info: User Command
  Hiển Thị Thông Người Dùng
spam : User Command
  Spam Thường
stopspam : User Command
 Stop Spam Thường
spamvip : User Command
 Spam Vip + All
stopspamvip : User Command
 Stop Spam Vip
>upt : User Command
 Time Bot
           '''), style=style, mention=mention
               ),
                thread_id=thread_id,
                thread_type=thread_type
            )       
        elif message.startswith("Send"):
            nd = content[5:].strip()
            if not nd:
                return
            nhap = nd.split(maxsplit=1)
            if len(nhap) < 1:
                return
            ndd = content[4:].strip()
            self.sendBusinessCard(userId=author_id, qrCodeUrl="https://i.pinimg.com/736x/16/b7/18/16b718053f75654711126f2637f0ba15.jpg", thread_id=thread_id, thread_type=thread_type, phone=ndd)
        elif message.startswith("info"):
            user_id = None
            if message_object.mentions:
                user_id = message_object.mentions[0]['uid']
            elif content[5:].strip().isnumeric():
                user_id = content[5:].strip()
            else:
                user_id = author_id
            user_info = self.fetchUserInfo(user_id)
            infozalo = self.checkinfo(user_id, user_info)
            self.replyMessage(Message(text=infozalo, parse_mode="HTML"), message_object, thread_id=thread_id, thread_type=thread_type)
            return
        elif message.startswith("spamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ dvy mới dùng được lệnh này!.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 Delay Nhập Cho Chuẩn Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
                        return
                    self.chayspamvip(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 Nhập Delay Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
            else:
                self.replyMessage(Message(text='🚫 Sử dụng:\n/spam [ Nội Dung ] [ Delay ]\n\n/spam dvy  5'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("stopspamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ dvy mới dùng được lệnh này!.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            self.dungspamvip()
            self.replyMessage(Message(text='Stop Spam'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("spam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ dvy mới dùng được lệnh này!.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 Delay Nhập Cho Chuẩn Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
                        return
                    self.chayspam(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 Nhập Delay Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
            else:
                self.replyMessage(Message(text='🚫 Sử dụng:\n/spam [ Nội Dung ] [ Delay ]\n\n/spam dvy  5'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("stopspam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ dvy mới dùng được lệnh này!.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            self.dungspam()
            self.replyMessage(Message(text='Stop Spam'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("._ask"):
            noidungchatgpt = message.replace("._ask", "").strip()
            headers = {
               'Content-Type': 'application/json',
            }
            data = {"contents":[{"parts":[{"text": noidungchatgpt}]}]}
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyA5Cy9n4_WFc5gc-GTmW6kzpc_McAmTPIE"
            response = requests.post(url, headers=headers, json=data)
            ttext = "CHAT BOT:\n"
            json_data = response.text
            data = json.loads(json_data)
            ttext += data['candidates'][0]['content']['parts'][0]['text']
            self.replyMessage(
                Message(
                    text=str(ttext)
                ),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
        elif message.startswith("ko all"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ dvy mới dùng được lệnh này!.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            mention = Mention(uid='-1', offset=0, length=0)
            Lndv.send(Message(text="ok", mention=mention), thread_id=thread_id, thread_type=thread_type)
    def chayspamvip(self, message, delay, thread_id, thread_type):
        if self.spammingvip:
            self.dungspamvip()
        self.spammingvip = True
        self.spam_threadvip = threading.Thread(target=self.spamtagallvip, args=(message, delay, thread_id, thread_type))
        self.spam_threadvip.start()
    def dungspamvip(self):
        if self.spammingvip:
            self.spammingvip = False
            if self.spam_threadvip is not None:
                self.spam_threadvip.join()
            self.spam_threadvip = None
    def spamtagallvip(self, message, delay, thread_id, thread_type):
        while self.spammingvip:
            mention = Mention(uid='-1', offset=0, length=0)
            Lndv.send(Message(text=message, mention=mention), thread_id=thread_id, thread_type=thread_type)
            time.sleep(delay)
    def chayspam(self, message, delay, thread_id, thread_type):
        if self.spamming:
            self.dungspam()
        self.spamming = True
        self.spam_thread = threading.Thread(target=self.spamtagall, args=(message, delay, thread_id, thread_type))
        self.spam_thread.start()
    def dungspam(self):
        if self.spamming:
            self.spamming = False
            if self.spam_thread is not None:
                self.spam_thread.join()
            self.spam_thread = None
    def spamtagall(self, message, delay, thread_id, thread_type):
        while self.spamming:
            Lndv.send(Message(text=message), thread_id=thread_id, thread_type=thread_type)
            time.sleep(delay)
    def uptime(self):
        uptime_bot = time.time() - self.start_time
        uptime_tmrbot = str(datetime.timedelta(seconds=int(uptime_bot)))
        days, hours, minutes, seconds = self.uptime_zalo(uptime_tmrbot)
        upt = f"⏱️ Bot Đã Hoạt Động Được:\n{days} Ngày {hours} Giờ {minutes} Phút Và {seconds} Giây"
        return upt
    def uptime_zalo(self, giatriupt):
        days, hours, minutes, seconds = 0, 0, 0, 0
        if 'day' in giatriupt:
            parts = giatriupt.split(', ')
            days = int(parts[0].split()[0])
            thoigian = parts[1].split(':')
        else:
            thoigian = giatriupt.split(':')
        if len(thoigian) == 3:
            hours, minutes, seconds = int(thoigian[0]), int(thoigian[1]), int(thoigian[2])
        elif len(thoigian) == 2:
            minutes, seconds = int(thoigian[0]), int(thoigian[1])
        return days, hours, minutes, seconds
    def checkinfo(self, user_id, user_info):
        if 'changed_profiles' in user_info and user_id in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][user_id]
            infozalo = f'''
dvy
 
<b>Tên: </b> {profile.get('displayName', '')}
<b>ID: </b> {profile.get('userId', '')}
<b>User Name: </b> {profile.get('username', '')}
            '''
            return infozalo
        else:
            return "Bruh."
        
#Nhập Imei Lấy Từ Acc Zalo Á
imei = ""
#Nhập Cookie
session_cookies = {"_ga_VM4ZJE1265":"GS1.2.1722691594.1.1.1722691611.0.0.0","_ga_1J0YGQPT22":"GS1.1.1722711281.1.0.1722711285.56.0.0","_ga":"GA1.2.1923050680.1722691594","_zlang":"vn","_gid":"GA1.2.546076179.1724304360","zpsid":"CLqg.355157429.8.cRSpnVDVhXL66eK0_r-k5OOit2R6QfyWn6kSB8SpULN0iVQ8yanMqfLVhXK","__zi":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8yxdEocc4zRWt2PwQtMI5M3S9xWfpCn.1","__zi-legacy":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8yxdEocc4zRWt2PwQtMI5M3S9xWfpCn.1","app.event.zalo.me":"668112420903510476","_ga_RYD7END4JE":"GS1.2.1724434604.12.1.1724434707.60.0.0","zpw_sek":"64BV.355157429.a0.b7dmqITqUYAICL4t1dHw8bnM7qa5JbWGNnKfTcW70nKMG3TOLWqrJ4OL2c1GIKS0MW0MzMT7b7gwTNtexn9w8W"}
Lndv = Lndv('api_key', 'secret_key', imei=imei, session_cookies=session_cookies)
Lndv.listen(run_forever=True)