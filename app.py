from dotenv import load_dotenv
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

load_dotenv()

st.set_page_config(page_title="主夫の味方")
st.title("主夫の味方")

# 会話履歴をセッションで保持
if "history" not in st.session_state:
	st.session_state["history"] = []

category = st.radio("悩みの種を選んでください", ("掃除", "洗濯", "料理"))


# 会話履歴表示（履歴がある場合のみ）
if st.session_state["history"]:
	st.markdown("### これまでの会話履歴")
	for h in st.session_state["history"]:
		st.markdown(f"**Q:** {h['question']}")
		st.markdown(f"**A:** {h['answer']}")
	# 最新の回答表示（履歴がある場合のみ、入力スペースの上）
	last_answer = st.session_state["history"][-1]["answer"]
	st.markdown("### 回答")
	st.write(last_answer)

user_input = st.text_area("悩みを入力してください（「quit」と入力で終了）", "")
if st.button("実行"):
	if user_input.strip().lower() == "quit":
		st.session_state["quit"] = True
		st.success("頑張ってください")
	elif not user_input.strip():
		st.warning("悩みを入力してください")
	else:
		# カテゴリごとにプロンプトテンプレートを用意
		if category == "掃除":
			template = "あなたは掃除のプロです。会話履歴: {history}\n新しい悩み: {question}"
		elif category == "洗濯":
			template = "あなたは洗濯の専門家です。会話履歴: {history}\n新しい悩み: {question}"
		else:
			template = "あなたは料理の達人です。会話履歴: {history}\n新しい悩み: {question}"

		history_str = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in st.session_state["history"]])
		prompt = ChatPromptTemplate.from_template(template)
		messages = prompt.format_messages(history=history_str, question=user_input)

		openai_api_key = os.getenv("OPENAI_API_KEY")
		if not openai_api_key:
			st.error("OPENAI_API_KEYが設定されていません。環境変数に設定してください。")
		else:
			llm = ChatOpenAI(api_key=openai_api_key)
			response = llm(messages)
			# 履歴に追加
			st.session_state["history"].append({"question": user_input, "answer": response.content})

# quit入力時は以降の処理を停止
if st.session_state.get("quit"):
	st.stop()
from dotenv import load_dotenv
