
const express = require("express");
const bodyParser = require("body-parser");
const line = require("@line/bot-sdk");
const fs = require("fs");

const config = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.LINE_CHANNEL_SECRET,
};

const client = new line.Client(config);
const app = express();
app.use(bodyParser.json());

// تحميل البيانات من الملفات
let admins = [];
let helpers = [];
let protectedMembers = [];
let allowKick = true;

if (fs.existsSync("admins.json")) admins = JSON.parse(fs.readFileSync("admins.json"));
if (fs.existsSync("helpers.json")) helpers = JSON.parse(fs.readFileSync("helpers.json"));
if (fs.existsSync("protected.json")) protectedMembers = JSON.parse(fs.readFileSync("protected.json"));

function saveAdmins() {
  fs.writeFileSync("admins.json", JSON.stringify(admins, null, 2));
}
function saveHelpers() {
  fs.writeFileSync("helpers.json", JSON.stringify(helpers, null, 2));
}
function saveProtected() {
  fs.writeFileSync("protected.json", JSON.stringify(protectedMembers, null, 2));
}

app.post("/api/webhook", (req, res) => {
  Promise.all(req.body.events.map(handleEvent))
    .then((result) => res.json(result))
    .catch((err) => {
      console.error(err);
      res.status(500).end();
    });
});

async function handleEvent(event) {
  if (event.type !== "message" || event.message.type !== "text") return;

  const userId = event.source.userId;
  const groupId = event.source.groupId || null;
  const msg = event.message.text.trim();

  // يرسل الـ userId تلقائي في الخاص
  if (event.source.type === "user") {
    return client.replyMessage(event.replyToken, {
      type: "text",
      text: `🔑 الـ userId حقك هو:\n${userId}`,
    });
  }

  // أمر !ايدي
  if (msg === "!ايدي") {
    return client.replyMessage(event.replyToken, {
      type: "text",
      text: `🔑 الـ userId حقك هو:\n${userId}`,
    });
  }

  // التحقق من الصلاحيات
  const isAdmin = admins.includes(userId);
  const isHelper = helpers.includes(userId);

  // أوامر الأدمن فقط
  if (isAdmin) {
    if (msg.startsWith("!اضف_ادمن ")) {
      const target = msg.split(" ")[1];
      if (!admins.includes(target)) {
        admins.push(target);
        saveAdmins();
        return reply(event, `✅ تمت إضافة ${target} كأدمن`);
      }
    }

    if (msg.startsWith("!حذف_ادمن ")) {
      const target = msg.split(" ")[1];
      admins = admins.filter((id) => id !== target);
      saveAdmins();
      return reply(event, `🗑️ تم حذف ${target} من الأدمنز`);
    }

    if (msg === "!الادمنز") {
      return reply(event, "👑 الأدمنز:\n" + admins.join("\n"));
    }

    if (msg.startsWith("!اضف_مساعد ")) {
      const target = msg.split(" ")[1];
      if (!helpers.includes(target)) {
        helpers.push(target);
        saveHelpers();
        return reply(event, `✅ تمت إضافة ${target} كمساعد`);
      }
    }

    if (msg.startsWith("!حذف_مساعد ")) {
      const target = msg.split(" ")[1];
      helpers = helpers.filter((id) => id !== target);
      saveHelpers();
      return reply(event, `🗑️ تم حذف ${target} من المساعدين`);
    }

    if (msg === "!المساعدين") {
      return reply(event, "👨‍💼 المساعدين:\n" + helpers.join("\n"));
    }

    if (msg === "!قفل_الطرد") {
      allowKick = false;
      return reply(event, "🔒 تم قفل الطرد (فقط الأدمن يقدر يطرد)");
    }

    if (msg === "!فتح_الطرد") {
      allowKick = true;
      return reply(event, "🔓 تم فتح الطرد (الكل يقدر يطرد)");
    }

    if (msg.startsWith("!طرد ") && groupId) {
      const target = msg.split(" ")[1];
      try {
        await client.kickMember(groupId, target);
        return reply(event, `❌ تم طرد ${target} من القروب`);
      } catch (e) {
        return reply(event, `⚠️ فشل الطرد: ${e.message}`);
      }
    }

    if (msg === "!الاعضاء" && groupId) {
      try {
        const members = await client.getGroupMembersIds(groupId);
        let result = "👥 قائمة الأعضاء:\n";
        for (const m of members) {
          try {
            const profile = await client.getGroupMemberProfile(groupId, m);
            result += `- ${profile.displayName} → ${m}\n`;
          } catch {
            result += `- مجهول → ${m}\n`;
          }
        }
        return reply(event, result);
      } catch (e) {
        return reply(event, `⚠️ فشل في جلب الأعضاء: ${e.message}`);
      }
    }
  }

  // أوامر الأدمن + المساعد
  if (isAdmin || isHelper) {
    if (msg.startsWith("!حماية ")) {
      const target = msg.split(" ")[1];
      if (!protectedMembers.includes(target)) {
        protectedMembers.push(target);
        saveProtected();
        return reply(event, `🛡️ تمت حماية ${target}`);
      }
    }

    if (msg.startsWith("!الغاء_الحماية ")) {
      const target = msg.split(" ")[1];
      protectedMembers = protectedMembers.filter((id) => id !== target);
      saveProtected();
      return reply(event, `🚫 تم إلغاء حماية ${target}`);
    }

    if (msg === "!المحميين") {
      return reply(event, "🛡️ الأعضاء المحميين:\n" + protectedMembers.join("\n"));
    }
  }
}

function reply(event, text) {
  return client.replyMessage(event.replyToken, { type: "text", text });
}

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
