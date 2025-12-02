from linebot.models import TextSendMessage, FlexSendMessage
import random
from constants import MAFIA_CONFIG, COLORS

class MafiaGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.players = {}
        self.phase = "registration"
        self.day = 0
        self.votes = {}
        self.night_actions = {}
        self.group_id = None

    def start_game(self):
        self.phase = "registration"
        self.players = {}
        self.votes = {}
        self.night_actions = {}
        self.day = 0
        return self.registration_flex()

    def registration_flex(self):
        return FlexSendMessage(
            alt_text="لعبة المافيا - التسجيل",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": "🎭 لعبة المافيا", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center"}
                        ], "backgroundColor": COLORS['primary'], "paddingAll": "20px", "cornerRadius": "12px"},
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": "⚠️ مهم: أضف البوت كصديق لاستلام دورك", "size": "xs", "color": COLORS['warning'], "weight": "bold", "wrap": True, "align": "center"}
                        ], "backgroundColor": f"{COLORS['warning']}1A", "paddingAll": "10px", "cornerRadius": "8px", "margin": "lg"},
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": f"👥 اللاعبون: {len(self.players)}", "size": "md", "color": COLORS['text_dark'], "weight": "bold", "align": "center"},
                            {"type": "text", "text": f"الحد الأدنى: {MAFIA_CONFIG['min_players']}", "size": "sm", "color": COLORS['text_light'], "margin": "xs", "align": "center"}
                        ], "margin": "lg"},
                        {"type": "separator", "margin": "lg"},
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "button", "action": {"type": "message", "label": "🎮 انضم", "text": "انضم مافيا"}, "style": "primary", "color": COLORS['primary'], "height": "sm"},
                            {"type": "button", "action": {"type": "message", "label": "▶️ بدء اللعبة", "text": "بدء مافيا"}, "style": "secondary", "height": "sm", "margin": "sm"},
                            {"type": "button", "action": {"type": "message", "label": "📖 شرح اللعبة", "text": "شرح مافيا"}, "style": "secondary", "height": "sm", "margin": "sm"}
                        ], "margin": "lg"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "20px"
                }
            }
        )

    def explanation_flex(self):
        return FlexSendMessage(
            alt_text="شرح لعبة المافيا",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": "📖 شرح المافيا", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center"}
                        ], "backgroundColor": COLORS['primary'], "paddingAll": "20px", "cornerRadius": "12px"},
                        {"type": "text", "text": "🎯 الهدف", "size": "md", "color": COLORS['text_dark'], "weight": "bold", "margin": "lg"},
                        {"type": "text", "text": "المافيا: قتل الجميع\nالمواطنون: اكتشاف المافيا", "size": "sm", "color": COLORS['text_light'], "wrap": True, "margin": "xs"},
                        {"type": "separator", "margin": "md"},
                        {"type": "text", "text": "🎭 الأدوار", "size": "md", "color": COLORS['text_dark'], "weight": "bold", "margin": "md"},
                        {"type": "text", "text": "🔪 المافيا: يقتل في الليل\n🔍 المحقق: يفحص اللاعبين\n⚕️ الدكتور: يحمي من القتل\n👤 المواطن: يصوت فقط", "size": "sm", "color": COLORS['text_light'], "wrap": True, "margin": "xs"},
                        {"type": "separator", "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "العودة", "text": "مافيا"}, "style": "primary", "color": COLORS['primary'], "height": "sm", "margin": "lg"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "20px"
                }
            }
        )

    def add_player(self, user_id, name):
        if self.phase != "registration":
            return {"response": TextSendMessage(text="اللعبة بدأت")}
        if user_id in self.players:
            return {"response": TextSendMessage(text="أنت مسجل")}
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        return {"response": self.registration_flex()}

    def assign_roles(self):
        if len(self.players) < MAFIA_CONFIG["min_players"]:
            return {"response": TextSendMessage(text=f"نحتاج {MAFIA_CONFIG['min_players']} لاعبين على الأقل")}
        
        roles = ["mafia", "detective", "doctor"] + ["citizen"] * (len(self.players) - 3)
        random.shuffle(roles)
        
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
            self.send_role_private(uid, role)
        
        self.phase = "night"
        self.day = 1
        return {"response": [
            TextSendMessage(text="✅ تم توزيع الأدوار"),
            self.night_flex()
        ]}

    def send_role_private(self, user_id, role):
        role_info = {
            "mafia": {"title": "🔪 المافيا", "desc": "اقتل شخص كل ليلة", "color": "#8B0000"},
            "detective": {"title": "🔍 المحقق", "desc": "افحص شخص كل ليلة", "color": "#1E90FF"},
            "doctor": {"title": "⚕️ الدكتور", "desc": "احمِ شخص كل ليلة", "color": "#32CD32"},
            "citizen": {"title": "👤 مواطن", "desc": "صوّت في النهار", "color": "#808080"}
        }
        
        info = role_info[role]
        flex = FlexSendMessage(
            alt_text="دورك",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": info["title"], "weight": "bold", "size": "xl", "color": "#FFFFFF", "align": "center"}
                        ], "backgroundColor": info["color"], "paddingAll": "20px", "cornerRadius": "10px"},
                        {"type": "text", "text": info["desc"], "size": "md", "color": COLORS['text_dark'], "wrap": True, "margin": "lg", "align": "center"},
                        {"type": "text", "text": "🤫 لا تشارك دورك", "size": "xs", "color": COLORS['text_light'], "align": "center", "margin": "md"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "20px"
                }
            }
        )
        
        try:
            self.line_bot_api.push_message(user_id, flex)
            if role != "citizen":
                import time
                time.sleep(1)
                self.send_action_buttons(user_id, role)
        except:
            pass

    def send_action_buttons(self, user_id, role):
        alive = [p for u, p in self.players.items() if p["alive"] and u != user_id]
        action = {"mafia": "اقتل", "detective": "افحص", "doctor": "احمي"}[role]
        
        buttons = []
        if role == "doctor":
            buttons.append({"type": "button", "action": {"type": "message", "label": "🛡️ احمي نفسي", "text": f"{action} نفسي"}, "style": "primary", "height": "sm"})
        
        for p in alive[:10]:
            buttons.append({"type": "button", "action": {"type": "message", "label": p['name'], "text": f"{action} {p['name']}"}, "style": "secondary", "height": "sm", "margin": "xs"})
        
        flex = FlexSendMessage(
            alt_text="اختر هدفك",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"اختر من تريد {action}ه", "size": "lg", "weight": "bold", "align": "center"},
                        {"type": "box", "layout": "vertical", "contents": buttons, "margin": "lg"}
                    ],
                    "paddingAll": "20px"
                }
            }
        )
        
        try:
            self.line_bot_api.push_message(user_id, flex)
        except:
            pass

    def night_flex(self):
        return FlexSendMessage(
            alt_text="الليل",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"🌙 الليل - اليوم {self.day}", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center", "backgroundColor": COLORS['primary'], "paddingAll": "20px", "cornerRadius": "12px"},
                        {"type": "text", "text": "الأدوار الخاصة تعمل الآن", "size": "sm", "align": "center", "margin": "lg"},
                        {"type": "button", "action": {"type": "message", "label": "▶️ إنهاء الليل", "text": "إنهاء الليل"}, "style": "primary", "color": COLORS['primary'], "margin": "lg"}
                    ],
                    "paddingAll": "20px"
                }
            }
        )

    def process_night(self):
        mafia = self.night_actions.get("mafia_target")
        doctor = self.night_actions.get("doctor_target")
        
        if mafia and mafia != doctor:
            self.players[mafia]["alive"] = False
            msg = f"☀️ النهار... تم قتل {self.players[mafia]['name']} 💀"
        else:
            msg = "☀️ النهار... لم يُقتل أحد!"
        
        self.night_actions = {}
        self.phase = "day"
        
        winner = self.check_winner()
        if winner:
            return winner
        
        return {"response": [TextSendMessage(text=msg), self.day_flex()]}

    def day_flex(self):
        return FlexSendMessage(
            alt_text="النهار",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"☀️ النهار - اليوم {self.day}", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center", "backgroundColor": COLORS['primary'], "paddingAll": "20px", "cornerRadius": "12px"},
                        {"type": "text", "text": "ناقشوا واختاروا من تظنونه المافيا", "size": "sm", "align": "center", "wrap": True, "margin": "lg"},
                        {"type": "button", "action": {"type": "message", "label": "🗳️ تصويت", "text": "تصويت مافيا"}, "style": "primary", "color": COLORS['primary'], "margin": "lg"}
                    ],
                    "paddingAll": "20px"
                }
            }
        )

    def voting_flex(self):
        alive = [p for p in self.players.values() if p["alive"]]
        buttons = [{"type": "button", "action": {"type": "message", "label": p["name"], "text": f"صوت {p['name']}"}, "style": "secondary", "height": "sm", "margin": "xs"} for p in alive[:10]]
        buttons.append({"type": "button", "action": {"type": "message", "label": "✅ إنهاء التصويت", "text": "إنهاء التصويت"}, "style": "primary", "color": COLORS['primary'], "margin": "md"})
        
        return FlexSendMessage(
            alt_text="التصويت",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "🗳️ التصويت", "weight": "bold", "size": "xl", "align": "center"},
                        {"type": "box", "layout": "vertical", "contents": buttons, "margin": "lg"}
                    ],
                    "paddingAll": "20px"
                }
            }
        )

    def vote(self, user_id, target_name):
        if self.phase != "voting" or user_id not in self.players or not self.players[user_id]["alive"]:
            return {"response": TextSendMessage(text="لا يمكنك التصويت")}
        
        for uid, p in self.players.items():
            if p["name"] == target_name and p["alive"]:
                self.votes[user_id] = uid
                return {"response": TextSendMessage(text=f"✅ تم تصويتك لـ {target_name}")}
        
        return {"response": TextSendMessage(text="لاعب غير صحيح")}

    def end_voting(self):
        if not self.votes:
            self.phase = "night"
            self.day += 1
            return {"response": [TextSendMessage(text="لا توجد أصوات"), self.night_flex()]}
        
        killed = max(self.votes, key=lambda k: list(self.votes.values()).count(self.votes[k]))
        self.players[killed]["alive"] = False
        name = self.players[killed]["name"]
        
        self.votes = {}
        self.phase = "night"
        self.day += 1
        
        winner = self.check_winner()
        if winner:
            return winner
        
        return {"response": [TextSendMessage(text=f"تم إعدام {name}"), self.night_flex()]}

    def check_winner(self):
        mafia = sum(1 for p in self.players.values() if p["alive"] and p["role"] == "mafia")
        citizens = sum(1 for p in self.players.values() if p["alive"] and p["role"] != "mafia")
        
        if mafia == 0:
            self.phase = "ended"
            return {"response": self.winner_flex("المواطنون"), "game_over": True}
        
        if mafia >= citizens:
            self.phase = "ended"
            return {"response": self.winner_flex("المافيا"), "game_over": True}
        
        return None

    def winner_flex(self, winner_team):
        # كشف الأدوار
        roles_content = []
        for uid, p in self.players.items():
            role_emoji = {"mafia": "🔪", "detective": "🔍", "doctor": "⚕️", "citizen": "👤"}[p["role"]]
            role_name = {"mafia": "المافيا", "detective": "المحقق", "doctor": "الدكتور", "citizen": "مواطن"}[p["role"]]
            status = "✅" if p["alive"] else "💀"
            
            roles_content.append({
                "type": "box",
                "layout": "baseline",
                "contents": [
                    {"type": "text", "text": role_emoji, "size": "sm", "flex": 0},
                    {"type": "text", "text": p["name"], "size": "sm", "flex": 2, "margin": "sm"},
                    {"type": "text", "text": role_name, "size": "xs", "color": COLORS['text_light'], "flex": 2, "align": "center"},
                    {"type": "text", "text": status, "size": "sm", "flex": 0, "align": "end"}
                ],
                "margin": "md" if len(roles_content) > 0 else "sm"
            })
        
        return FlexSendMessage(
            alt_text="نتيجة اللعبة",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": "🏆 انتهت اللعبة", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center"}
                        ], "backgroundColor": COLORS['primary'], "paddingAll": "20px", "cornerRadius": "12px"},
                        {"type": "text", "text": "الفائز", "size": "sm", "color": COLORS['text_light'], "align": "center", "margin": "lg"},
                        {"type": "text", "text": winner_team, "size": "xxl", "color": COLORS['success'], "weight": "bold", "align": "center", "margin": "xs"},
                        {"type": "separator", "margin": "lg"},
                        {"type": "text", "text": "🎭 كشف الأدوار", "size": "md", "color": COLORS['text_dark'], "weight": "bold", "margin": "lg"},
                        {"type": "box", "layout": "vertical", "contents": roles_content, "margin": "md"},
                        {"type": "separator", "margin": "lg"},
                        {"type": "button", "action": {"type": "message", "label": "🔄 إعادة", "text": "مافيا"}, "style": "primary", "color": COLORS['primary'], "margin": "lg"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "20px"
                }
            }
        )

    def check_answer(self, text, user_id, display_name):
        text = text.strip()
        
        if text == "انضم مافيا":
            return self.add_player(user_id, display_name)
        if text == "بدء مافيا":
            return self.assign_roles()
        if text == "شرح مافيا":
            return {"response": self.explanation_flex()}
        if text == "إنهاء الليل" and self.phase == "night":
            return self.process_night()
        if text == "تصويت مافيا":
            self.phase = "voting"
            return {"response": self.voting_flex()}
        if text.startswith("صوت "):
            return self.vote(user_id, text.replace("صوت ", ""))
        if text == "إنهاء التصويت" and self.phase == "voting":
            return self.end_voting()
        
        # أوامر الخاص
        if text.startswith("اقتل ") and self.players.get(user_id, {}).get("role") == "mafia":
            target = text.replace("اقتل ", "")
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"]:
                    self.night_actions["mafia_target"] = uid
                    return {"response": TextSendMessage(text=f"✅ تم اختيار {target}")}
        
        if text.startswith("افحص ") and self.players.get(user_id, {}).get("role") == "detective":
            target = text.replace("افحص ", "")
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"]:
                    result = "🔪 مافيا" if p["role"] == "mafia" else "✅ بريء"
                    return {"response": TextSendMessage(text=f"{target}: {result}")}
        
        if text.startswith("احمي ") and self.players.get(user_id, {}).get("role") == "doctor":
            target = text.replace("احمي ", "")
            if target == "نفسي":
                self.night_actions["doctor_target"] = user_id
                return {"response": TextSendMessage(text="✅ تم حماية نفسك")}
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"]:
                    self.night_actions["doctor_target"] = uid
                    return {"response": TextSendMessage(text=f"✅ تم حماية {target}")}
        
        return None
    
    def next_question(self):
        return None
