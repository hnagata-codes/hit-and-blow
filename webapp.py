import streamlit as st
import random

st.title("Hit & Blow")

if "answer" not in st.session_state:
    number = random.sample("0123456789", 3)
    st.session_state.answer = "".join(number)
    st.session_state.is_cleared = False
    st.session_state.history = []
    st.session_state.round = 0
    st.session_state.is_correct = ""

# st.write(st.session_state.answer)

is_correct = st.empty()
history_table = st.empty()

if st.session_state.is_cleared == False:
    with st.form("form", clear_on_submit=True):
        player_number = st.text_input("3桁の数字を入力してください：")
        submitted = st.form_submit_button("予想する")

    if submitted:
        if len(set(player_number)) != 3 or not player_number.isdigit():
            st.write("エラー：重複しない3桁の半角数字を入力して下さい")
        else:
            st.session_state.round += 1
            hit = 0
            blow = 0
            if player_number == st.session_state.answer:
                hit = 3
                st.session_state.is_correct = "正解！"
                st.session_state.history.append(
                    {
                        "ラウンド": st.session_state.round,
                        "あなたの予想": player_number,
                        "Hit": hit,
                        "Blow": blow,
                    }
                )
                st.session_state.is_cleared = True
                st.rerun()
            else:
                st.session_state.is_correct = "ハズレ！"
                for i in range(3):
                    if player_number[i] == st.session_state.answer[i]:
                        hit += 1
                    elif player_number[i] in st.session_state.answer:
                        blow += 1
                st.session_state.history.append(
                    {
                        "ラウンド": st.session_state.round,
                        "あなたの予想": player_number,
                        "Hit": hit,
                        "Blow": blow,
                    }
                )

is_correct.write(st.session_state.is_correct)

if len(st.session_state.history) >= 1:
    history_table.dataframe(
        st.session_state.history,
        hide_index=True,
        column_config={"ラウンド": st.column_config.NumberColumn(width="small")},
    )

if st.session_state.is_cleared == True:
    if st.button("もう一度遊ぶ"):
        del st.session_state.answer
        st.rerun()
