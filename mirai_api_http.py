import requests

class ws:
    """
    This function uses json to pass information.
        Format:
            {
                "id": 0~2       // This uses to pass state id
                    // 0:normal other:error
                "msg": ""       // This uses to pass message information
                    // For example "Connection succeeded",and this will be able to be printed.
                "data": all     // This uses to pass data information
            }
    """

    def __init__(self, server_url: str, key: str, qqid: int):
        """
        Init your config , and need:
            server_url  : your server url(e.g. "xxxx.xxx:xxxx")
            key         : the key you set on the server
            qqid        : your bot's qq ID
        """
        self.url = "http://"+str(server_url)
        self.key = str(key)
        self.qqid = int(qqid)
        self.sessionKey = ""

    def connect(self) -> dict:
        """
        This function is used to connect server and subscribe to messages and event.
        """

        self.sessionKey = requests.post(
                url = self.url + "/verify",
                json={
                    "verifyKey": self.key,
                }
            ).json()["session"]

        rep = requests.post(
            url = self.url + "/bind",
            json = {
                "sessionKey":self.sessionKey,
                "qq": self.qqid
            }
        ).json()
        code = 0
        if rep["code"] != 0:
            code = 2
        return {"id":code,"msg":rep["msg"]}

    def get(self) -> dict:
        """
        This function is used to get information from server.
        """
        while True:
            data = requests.get(
                self.url+f"/fetchMessage?sessionKey={self.sessionKey}&count=1"
            ).json()
            if data["data"] != []:
                return {"id": 0, "msg": "Received the new message", "data": data["data"][0]}

    def disconnect(self):
        """
        This function is used to disconnect from server.
        """
        try:
            requests.post(
                url = self.url + "/release",
                json = {
                    "sessionKey":self.sessionKey,
                    "qq": self.qqid
                }
            )
            return {"id": 0, "msg": "Closed successfully"}
        except:
            return {"id": 1, "msg": "Connection lost"}

    def command_post(self, cmd: str, content: dict={}):
        content["sessionKey"] = self.sessionKey
        return requests.post(
            self.url+f"/{cmd}?",
            json=content
        ).json()

    def command_get(self, cmd: str, content: dict={}):
        content["sessionKey"]=self.sessionKey
        text = ""
        for key,value in content.items():
            text+= f"{str(key)}={str(value)}&"
        return requests.get(
            self.url+f"/{cmd}?{text[:-1]}",
            json=content
        ).json()
    """
    ???????????????mirai-api-http??????????????????????????????????????????????????????
    """

    def about(self) -> dict:
        """
        ?????????????????????mirai-api-http??????????????????????????????
        """
        return self.command_get(
            "about"
        )

    def messageFromId(self, message_id: int) -> dict:
        """
        ???????????????messageId??????????????????,
        """
        return self.command_get(
            "messageFromId",
            {
                "id": message_id
            }
        )

    def friendList(self) -> dict:
        """
        ?????????????????????bot???????????????
        """
        return self.command_get(
            "friendList"
        )

    def groupList(self) -> dict:
        """
        ?????????????????????bot????????????
        """
        return self.command_get(
            "groupList"
        )

    def memberList(self, group_id: int) -> dict:
        """
        ?????????????????????bot???????????????????????????
        """
        return self.command_get(
            "memberList",
            {
                "target": group_id
            }
        )

    def botProfile(self) -> dict:
        """
        ???????????????session??????bot???????????????
        """
        return self.command_get(
            "botProfile"
        )

    def friendProfile(self, user_id: int) -> dict:
        """
        ????????????????????????????????????
        """
        return self.command_get(
            "friendProfile",
            {
                "target": user_id
            }
        )

    def memberProfile(self, group_id: int, user_id: int) -> dict:
        """
        ???????????????????????????????????????
        """
        return self.command_get(
            "memberProfile",
            {
                "target": group_id,
                "memberId": user_id
            }
        )

    def sendFriendMessage(self, user_id: int, messageChain: list) -> dict:
        """
        ??????????????????????????????????????????
        """
        return self.command_post(
            "sendFriendMessage",
            {
                "target": user_id,
                "messageChain": messageChain
            }
        )

    def sendGroupMessage(self, group_id: int, messageChain: list) -> dict:
        """
        ???????????????
        """
        return self.command_post(
            "sendGroupMessage",
            {
                "target": group_id,
                "messageChain": messageChain
            }
        )

    def sendTempMessage(self, user_id: int, group_id: int, messageChain: list) -> dict:
        """
        ????????????????????????
        """
        return self.command_post(
            "sendTempMessage",
            {
                "qq": user_id,
                "group": group_id,
                "messageChain": messageChain
            }
        )

    def sendNudge(self, target: int, subject: int, kind: str) -> dict:
        """
        ???????????????????????????
            target:??????id
            subject:?????????id(?????????????????????QQ???)
            kind:"Group" or "Friend" or "Stranger"
        """
        return self.command_post(
            "sendNudge",
            {
                "target": target,
                "subject": subject,
                "kind": kind
            }
        )

    def recall(self, messageId: int) -> dict:
        """
        ????????????
        """
        return self.command_post(
            "recall",
            {
                "target": messageId
            }
        )

    def file_list(self, target_id: int, path_id: str = "") -> dict:
        """
        ??????????????????
        """
        return self.command_get(
            "file/list",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "withDownloadInfo": False,
                "offset": 0,
                "size": 1
            }
        )

    def file_info(self, target_id: int, path_id: str) -> dict:
        """
        ??????????????????
        """
        return self.command_get(
            "file/info",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "withDownloadInfo": True
            }
        )

    def file_mkdir(self, target_id: int, path_id: str, directoryName: str = "New Folder") -> dict:
        """
        ???????????????
        """
        return self.command_post(
            "file/mkdir",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "directoryName": directoryName
            }
        )

    def file_delete(self, target_id: int, path_id: str) -> dict:
        """
        ????????????
        """
        return self.command_post(
            "file/delete",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None
            }
        )

    def file_move(self, target_id: int, path_id: str, move_path_id: str) -> dict:
        """
        ????????????
        """
        return self.command_post(
            "file/move",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "moveTo": move_path_id,
                "moveToPath": None
            }
        )

    def file_rename(self, target_id: int, path_id: str, name: str) -> dict:
        """
        ???????????????
        """
        return self.command_post(
            "file_rename",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "renameTo": name
            }
        )

    def file_upload(self,group_id:int,file_path:str,file_name) -> dict:
        """
        ???????????????(????????????????????????)
        """
        return self.command_post(
            "file/upload",
            {
                "type": "group",
                "target": group_id,
                "path": file_path,
                "file": file_name,
            }
        )

    def deleteFriend(self, user_id) -> dict:
        """
        ????????????
        """
        return self.command_post(
            "deleteFriend",
            {
                "target": user_id
            }
        )

    def mute(self, group_id: int, user_id: int, set_time: int = 600) -> dict:
        """
        ???????????????
        """
        return self.command_post(
            "mute",
            {
                "target": group_id,
                "memberId": user_id,
                "time": set_time
            }
        )

    def unmute(self, group_id: int, user_id: int) -> dict:
        """
        ?????????????????????
        """
        return self.command_post(
            "unmute",
            {
                "target": group_id,
                "memberId": user_id
            }
        )

    def kick(self, group_id: int, user_id: int, msg: str = "?????????????????????") -> dict:
        """
        ???????????????
        """
        return self.command_post(
            "kick",
            {
                "target": group_id,
                "memberId": user_id,
                "msg": msg
            }
        )

    def quit(self, group_id: int) -> dict:
        """
        ????????????
        """
        return self.command_post(
            "quit",
            {
                "target": group_id
            }
        )

    def muteAll(self, group_id: int) -> dict:
        """
        ????????????
        """
        return self.command_post(
            "muteAll",
            {
                "target": group_id
            }
        )

    def unmuteAll(self, group_id: int) -> dict:
        """
        ??????????????????
        """
        return self.command_post(
            "unmuteAll",
            {
                "target": group_id
            }
        )

    def setEssence(self, messageId: int) -> dict:
        """
        ?????????????????????
        """
        return self.command_post(
            "setEssence",
            {
                "target": messageId
            }
        )

    def groupConfig_get(self, group_id: int) -> dict:
        """
        ???????????????
        """
        return self.command_post(
            "groupConfig",
            {
                "target": group_id
            },
            "get"
        )

    def groupConfig_update(self, group_id: int, config: dict) -> dict:
        """
        ???????????????
        config:
            "name":"",                  // ?????????
            "announcement":"",          // ?????????
            "confessTalk":False,        // ?????????????????????
            "allowMemberInvite":False,  // ????????????????????????
            "autoApprove":False,        // ??????????????????????????????
            "anonymousChat":False       // ????????????????????????
        """
        return self.command_post(
            "groupConfig",
            {
                "target": group_id,
                "config": config
            },
            "update"
        )

    def memberInfo_get(self, group_id: int, user_id: int) -> dict:
        """
        ??????????????????
        """
        return self.command_post(
            "memberInfo",
            {
                "target": group_id,
                "memberId": user_id
            },
            "get"
        )

    def memberInfo_update(self, group_id: int, user_id: int, info: dict) -> dict:
        """
        ??????????????????
        info:
            "name": "?????????",
            "specialTitle": "?????????"
        """
        return self.command_post(
            "memberInfo",
            {
                "target": group_id,
                "memberId": user_id,
                "info": info
            },
            "update"
        )

    def memberAdmin(self, group_id: int, user_id: int, isAdmin: bool) -> dict:
        """
        ?????????????????????
        """
        return self.command_post(
            "memberAdmin",
            {
                "target": group_id,
                "memberId": user_id,
                "assign": isAdmin
            }
        )

    def resp_newFriendRequestEvent(self, event_id: int, bot_id: int, group_id: int, operate: int, msg: str) -> dict:
        """
        ???????????????????????????????????????
        groupId????????????????????????????????????0

        | operate | ??????                                               |
        | ------- | -------------------------------------------------- |
        | 0       | ??????????????????                                       |
        | 1       | ??????????????????                                       |
        | 2       | ??????????????????????????????????????????????????????????????????????????? |
        """
        return self.command_post(
            "resp/newFriendRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )

    def resp_memberJoinRequestEvent(self, event_id:int, bot_id: int, group_id: int, operate: int, msg: str) -> dict:
        """
        ???????????????????????????????????????

        | operate | ??????                                           |
        | ------- | ---------------------------------------------- |
        | 0       | ????????????                                       |
        | 1       | ????????????                                       |
        | 2       | ????????????                                       |
        | 3       | ????????????????????????????????????????????????????????????????????? |
        | 4       | ????????????????????????????????????????????????????????????????????? |
        """
        return self.command_post(
            "resp/memberJoinRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )

    def resp_botInvitedJoinGroupRequestEvent(self, event_id: int, bot_id: int, group_id: int, operate: int, msg: str) -> dict:
        """
        ?????????????????????Bot?????????????????????

        | operate | ??????     |
        | ------- | -------- |
        | 0       | ???????????? |
        | 1       | ???????????? |
        """
        return self.command_post(
            "resp/botInvitedJoinGroupRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )
