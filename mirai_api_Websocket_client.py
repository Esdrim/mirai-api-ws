import websocket
import json


class ws:
    """
    This function uses json to pass information.
        Format:
            {
                "id": 0~2       // This uses to pass state id
                    // 0:normal 1:allowed error 2:uncorrectable error
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
        self.ws = websocket.WebSocket()
        self.url = "ws://"+str(server_url)
        self.key = str(key)
        self.qqid = int(qqid)

    def connect(self) -> dict:
        """
        This function is used to connect server and subscribe to messages and event.
        """
        try:
            self.ws.connect(str(self.url) + "/all",
                            header=[
                "verifyKey:" + str(self.key),
                "qq:" + str(self.qqid)
            ]
            )
        except:
            return {"id": 2, "msg": "Connection failed"}
        if self.ws.connected:
            json_data = json.loads(self.ws.recv())
            try:
                self.key = json_data["data"]["session"]
                return {"id": 0, "msg": "Connection succeeded"}
            except:
                return {"id": 2, "msg": json_data["msg"], "data": json_data}

    def get(self) -> dict:
        """
        This function is used to get information from server.
        """
        if self.ws.connected:
            json_data = json.loads(self.ws.recv())
            try:
                if str(json_data["syncId"]) == '-1':
                    return {"id": 0, "msg": "Received the news", "data": json_data}
                elif str(json_data["syncId"]) == '1':
                    if str(json_data["data"]["msg"]) == "success":
                        if json_data["data"]["messageId"] != -1:
                            return {"id": 0, "msg": "Sent successfully", "data": json_data}
                        else:
                            return {"id": 1, "msg": "Wrong message id", "data": json_data}
                    else:
                        return {"id": 1, "msg": "Sent failed", "data": json_data}
            except:
                pass
            return {"id": 0, "msg": "Event return", "data": json_data}
        else:
            return {"id": 2, "msg": "Connection lost"}

    def disconnect(self):
        """
        This function is used to disconnect from server.
        """
        try:
            self.ws.close()
            return {"id": 0, "msg": "Closed successfully"}
        except:
            return {"id": 1, "msg": "Connection lost"}
    def command(self, passch: int, cmd: str, content: dict = {}, subcmd: str = "") -> dict:
        try:
            self.ws.send(
                json.dumps(
                    {
                        "syncId": passch,
                        "command": cmd,
                        "subCommand": subcmd,
                        "content": content
                    },
                    ensure_ascii=False
                )
            )
            return {"id": 0}
        except:
            return {"id": 1}

    """
    ???????????????mirai-api-http??????????????????????????????????????????????????????
    """

    def about(self) -> dict:
        """
        ?????????????????????mirai-api-http??????????????????????????????
        """
        return self.command(
            2,
            "about"
        )

    def messageFromId(self, message_id: int) -> dict:
        """
        ???????????????messageId??????????????????,
        """
        return self.command(
            3,
            "messageFromId",
            {
                "id": message_id
            }
        )

    def friendList(self) -> dict:
        """
        ?????????????????????bot???????????????
        """
        return self.command(
            4,
            "friendList"
        )

    def groupList(self) -> dict:
        """
        ?????????????????????bot????????????
        """
        return self.command(
            5,
            "groupList"
        )

    def memberList(self, group_id: int) -> dict:
        """
        ?????????????????????bot???????????????????????????
        """
        return self.command(
            6,
            "memberList",
            {
                "target": group_id
            }
        )

    def botProfile(self) -> dict:
        """
        ???????????????session??????bot???????????????
        """
        return self.command(
            7,
            "botProfile"
        )

    def friendProfile(self, user_id: int) -> dict:
        """
        ????????????????????????????????????
        """
        return self.command(
            8,
            "friendProfile",
            {
                "target": user_id
            }
        )

    def memberProfile(self, group_id: int, user_id: int) -> dict:
        """
        ???????????????????????????????????????
        """
        return self.command(
            9,
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
        return self.command(
            10,
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
        return self.command(
            11,
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
        return self.command(
            12,
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
        return self.command(
            13,
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
        return self.command(
            14,
            "recall",
            {
                "target": messageId
            }
        )

    def file_list(self, target_id: int, path_id: str = "") -> dict:
        """
        ??????????????????
        """
        return self.command(
            15,
            "file_list",
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
        return self.command(
            16,
            "file_info",
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
        return self.command(
            17,
            "file_mkdir",
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
        return self.command(
            18,
            "file_delete",
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
        return self.command(
            19,
            "file_move",
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
        return self.command(
            20,
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

    def deleteFriend(self, user_id) -> dict:
        """
        ????????????
        """
        return self.command(
            21,
            "deleteFriend",
            {
                "target": user_id
            }
        )

    def mute(self, group_id: int, user_id: int, set_time: int = 600) -> dict:
        """
        ???????????????
        """
        return self.command(
            22,
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
        return self.command(
            23,
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
        return self.command(
            24,
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
        return self.command(
            25,
            "quit",
            {
                "target": group_id
            }
        )

    def muteAll(self, group_id: int) -> dict:
        """
        ????????????
        """
        return self.command(
            26,
            "muteAll",
            {
                "target": group_id
            }
        )

    def unmuteAll(self, group_id: int) -> dict:
        """
        ??????????????????
        """
        return self.command(
            27,
            "unmuteAll",
            {
                "target": group_id
            }
        )

    def setEssence(self, messageId: int) -> dict:
        """
        ?????????????????????
        """
        return self.command(
            28,
            "setEssence",
            {
                "target": messageId
            }
        )

    def groupConfig_get(self, group_id: int) -> dict:
        """
        ???????????????
        """
        return self.command(
            29,
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
        return self.command(
            30,
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
        return self.command(
            31,
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
        return self.command(
            32,
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
        return self.command(
            33,
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
        return self.command(
            34,
            "resp_newFriendRequestEvent",
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
        return self.command(
            35,
            "resp_memberJoinRequestEvent",
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
        return self.command(
            36,
            "resp_botInvitedJoinGroupRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )
