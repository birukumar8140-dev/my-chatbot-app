import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
messages = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Mera Chatbot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #1a1a2e; color: white; margin: 0; padding: 20px; }
        h2 { text-align: center; color: #00d4ff; }
        #chat { height: 70vh; overflow-y: auto; background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .user { text-align: right; margin: 10px 0; }
        .bot { text-align: left; margin: 10px 0; }
        .user span { background: #0f3460; padding: 10px 15px; border-radius: 15px; display: inline-block; }
        .bot span { background: #533483; padding: 10px 15px; border-radius: 15px; display: inline-block; }
        #input-area { display: flex; gap: 10px; }
        #msg { flex: 1; padding: 12px; border-radius: 10px; border: none; background: #16213e; color: white; font-size: 16px; }
        button { padding: 12px 20px; background: #00d4ff; color: black; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h2>🤖 Mera AI Chatbot</h2>
    <div id="chat"></div>
    <div id="input-area">
        <input id="msg" placeholder="Kuch poocho..." onkeypress="if(event.key==='Enter') send()">
        <button onclick="send()">Send</button>
    </div>
    <script>
        async function send() {
            const msg = document.getElementById("msg").value;
            if (!msg) return;
            document.getElementById("chat").innerHTML += `<div class="user"><span>${msg}</span></div>`;
            document.getElementById("msg").value = "";
            const res = await fetch("/chat", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({message: msg})});
            const data = await res.json();
            document.getElementById("chat").innerHTML += `<div class="bot"><span>${data.reply}</span></div>`;
            document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    messages.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages)
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)