const { Bot } = require("grammy");
const fs = require("fs");
const path = require("path");

// Read BOT_TOKEN from api_key.py (simple regex to find it)
const apiKeyPath = path.join(__dirname, "api_key.py");
if (!fs.existsSync(apiKeyPath)) {
    console.error("❌ Error: api_key.py not found.");
    process.exit(1);
}

const content = fs.readFileSync(apiKeyPath, "utf8");
const match = content.match(/BOT_TOKEN\s*=\s*["']([^"']+)["']/);
if (!match || match[1] === "YOUR_BOT_TOKEN_HERE") {
    console.error("❌ Error: Please set your BOT_TOKEN in api_key.py first.");
    process.exit(1);
}

const BOT_TOKEN = match[1];
const bot = new Bot(BOT_TOKEN);

const verificationCode = Math.floor(100000 + Math.random() * 900000).toString();

console.log("\n" + "=".repeat(50));
console.log("🤖 TELEGRAM BOT VERIFICATION");
console.log(`Please send this 6-digit code to your bot: ${verificationCode}`);
console.log("Waiting for verification...");
console.log("=".repeat(50) + "\n");

bot.on("message:text", async (ctx) => {
    if (ctx.message.text === verificationCode) {
        const chatId = ctx.chat.id.toString();
        fs.writeFileSync(path.join(__dirname, "chat_id.txt"), chatId);
        console.log(`✅ Success! Verified chat ID: ${chatId}`);
        console.log("Chat ID saved to chat_id.txt");
        await ctx.reply("Verification successful! You will now receive LinkedIn activity alerts here.");
        process.exit(0);
    } else {
        console.log(`Received incorrect code: ${ctx.message.text}`);
        await ctx.reply("Incorrect verification code. Please try again.");
    }
});

bot.catch((err) => {
    console.error("❌ Bot Error:", err);
    process.exit(1);
});

bot.start();
