import logging
import os
import requests
import pymongo
import gradio as gr
from bson.objectid import ObjectId
from questions import QUESTIONS

MONGO_URI = os.environ.get('MONGO_URI')
LLM_API_KEY = os.environ.get('LLM_API_KEY')

# MongoDB connection
client = pymongo.MongoClient(MONGO_URI)
db = client['main']
user_collection = db['user']

_DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

if _DEBUG:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.getLogger().setLevel(logging.WARNING)

title = "Instruction Following Game!"
requirement_ph = """<h2 style="color: #498FC8;">歡迎來到 Instruction Following Game!</h2>
<h4>Prompt Engineering 在人類與LLM溝通的過程中扮演非常重要的角色，精準的Prompt可以讓LLM產生更加符合你要求的回答，進而提升你操控AI的能力。<br>
你將通過這個遊戲，對大型語言模型(LLM)產生更深刻的理解。你需要根據題目來產生對LLM的問題(prompt)，使它的回復符合題目要求。點擊\"下一題\" 即可開始遊戲。</h4><p>Made by 0x.Yuan@CPSD.3rd</p>"""

def call_llm(prompt):
    endpoint = 'https://api.together.xyz/v1/chat/completions'
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}"
    }
    payload = {
        "model": "Qwen/Qwen1.5-72B-Chat",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|im_end|>"],
        "messages": [{"content": prompt, "role": "user"}]
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']

def login(user_id):
    if not user_id:
        return "請輸入User ID", None
    user = user_collection.find_one({"name": user_id})
    if not user:
        user_collection.insert_one({"name": user_id, "finished": [], "history": []})
        user = user_collection.find_one({"name": user_id})
    return "已登入", str(user["_id"])

def load_question(q_name, user_id):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    finished = user.get("finished", [])
    for q in QUESTIONS:
        if q.__name__ == q_name:
            question_text = q.question
            if q_name in finished:
                question_text += "（已完成）"
            return question_text

def check_answer(q_name, user_text, user_id):
    for q in QUESTIONS:
        if q.__name__ == q_name:
            ai_answer = call_llm(user_text)
            correct, explanation = q.check_result(user_text, ai_answer)
            feedback = "正確" if correct else "錯誤"

            # Update user history and finished status
            user_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"history": [q_name, user_text, ai_answer]}, "$addToSet": {"finished": q_name} if correct else {}}
            )

            return ai_answer, feedback, explanation

def get_leaderboard():
    users = user_collection.find()
    leaderboard = [{"User": user['name'], "Correct Answers": len(user['finished']), "Entries": len(user['history'])} for user in users]
    leaderboard.sort(key=lambda x: -x["Correct Answers"])  # Sort by number of correct answers, descending
    return leaderboard

def format_leaderboard(data):
    table = "| User | Correct Answers | Entries |\n"
    table += "|------|----------------|---------|\n"
    for row in data:
        table += f"| {row['User']} | {row['Correct Answers']} | {row['Entries']} |\n"
    return table

if __name__ == '__main__':
    with gr.Blocks(title=title, theme='ParityError/Interstellar') as demo:

        gr.Markdown('<div align="center"><img src="https://svgur.com/i/163T.svg" width=60% alt="Banner Image"></div>')
        gr.Markdown(requirement_ph)

        with gr.Row():
            gr_user_id = gr.Textbox(placeholder="User ID", label="用戶ID")
            gr_send = gr.Button("Send")
            gr_login_status = gr.Label(label="登錄狀態")
            gr_user_oid = gr.Textbox(visible=False)

        gr_send.click(login, inputs=[gr_user_id], outputs=[gr_login_status, gr_user_oid])

        with gr.Row():
            with gr.Column():
                gr_question_list = gr.Dropdown(choices=[q.__name__ for q in QUESTIONS], label="選擇題目")
                gr_question_text = gr.Textbox(label="題目", interactive=False)
                gr_user_input = gr.Textbox(label="你的回答")
                gr_submit = gr.Button("提交")

            with gr.Column():
                gr_answer_text = gr.Textbox(label="AI 回答", interactive=False)
                gr_feedback = gr.Label(label="結果")
                gr_explanation = gr.Textbox(label="詳細解釋", interactive=False)

        with gr.Row():
            gr_leaderboard = gr.Markdown(label="排行榜")

        def update_leaderboard():
            leaderboard_data = get_leaderboard()
            leaderboard_markdown = format_leaderboard(leaderboard_data)
            return leaderboard_markdown

        gr_question_list.change(load_question, inputs=[gr_question_list, gr_user_oid], outputs=[gr_question_text])
        gr_submit.click(check_answer, inputs=[gr_question_list, gr_user_input, gr_user_oid], outputs=[gr_answer_text, gr_feedback, gr_explanation])
        gr_submit.click(update_leaderboard, outputs=[gr_leaderboard])
        demo.load(update_leaderboard, outputs=[gr_leaderboard])

    demo.launch(share=True)
