import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 생성
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_schedule(user_input):
    """ChatGPT API를 호출하여 시간표를 생성"""
    if not client.api_key:
        return "Error: OpenAI API Key is missing. Please check your .env file."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates optimized university timetables based on user preferences."},
                {"role": "user", "content": f"Generate an optimized timetable based on the following input: {json.dumps(user_input)}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
def main():
    st.title("📅 Timetable Builder")
    
    # 캠퍼스 선택
    campus = st.selectbox("당신의 캠퍼스는 어디입니까?", ["Malaysia", "Australia"])
    
    # 과목 개수 선택
    num_subjects = st.number_input("당신은 몇 가지의 과목을 듣습니까?", min_value=1, max_value=8, step=1)
    
    subjects = []
    for i in range(int(num_subjects)):
        st.subheader(f"📘 과목 {i+1}")
        subject_name = st.text_input(f"과목 이름 {i+1}")

        forum_times = []
        tutorial_times = []

        # Forum 입력
        forum_count = st.number_input(f"Forum 개수 (1~10)", min_value=0, max_value=10, step=1, key=f"forum_count_{i}")
        for j in range(int(forum_count)):
            with st.expander(f"📚 Forum {j+1}"):
                day = st.selectbox(f"요일 {j+1}", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key=f"forum_day_{i}_{j}")
                start_time = st.time_input(f"시작 시간 {j+1}", key=f"forum_start_{i}_{j}")
                end_time = st.time_input(f"종료 시간 {j+1}", key=f"forum_end_{i}_{j}")
                forum_times.append({"day": day, "start": str(start_time), "end": str(end_time)})

        # Tutorial 입력
        tutorial_count = st.number_input(f"Tutorial 개수 (1~10)", min_value=0, max_value=10, step=1, key=f"tutorial_count_{i}")
        for j in range(int(tutorial_count)):
            with st.expander(f"📝 Tutorial {j+1}"):
                day = st.selectbox(f"요일 {j+1}", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key=f"tutorial_day_{i}_{j}")
                start_time = st.time_input(f"시작 시간 {j+1}", key=f"tutorial_start_{i}_{j}")
                end_time = st.time_input(f"종료 시간 {j+1}", key=f"tutorial_end_{i}_{j}")
                tutorial_times.append({"day": day, "start": str(start_time), "end": str(end_time)})

        subjects.append({
            "subject": subject_name,
            "forum": forum_times,
            "tutorial": tutorial_times
        })
    
    # 시간표 최적화 방식 선택
    schedule_type = st.radio("⏳ 시간표 최적화 방식", [
        "균형형 (Balanced)", "압축형 (Compact)", "아침형 (Morning Focus)", "저녁형 (Evening Focus)", "맞춤형 (Custom)"
    ])
    
    # 특정 요일 및 시간 선호
    include_weekend = st.checkbox("✅ 주말 포함 가능 여부")
    free_day = st.multiselect("🌿 공강 요일 설정", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]) 
    max_consecutive_classes = st.slider("📌 최대 연강 개수 제한", 1, 5, 3)
    
    # 추가 옵션
    more_free_days = st.checkbox("📅 한 주에 최대한 몰아넣어 공강일을 늘리기")
    extend_weekend = st.checkbox("🌙 주말과 이어붙여 연속된 휴일을 최대한 많이 만들기")
    compress_classes = st.checkbox("⏭ 최대한 연강 배치하여 하루에 몰아서 듣기")
    minimize_breaks = st.checkbox("🎯 쉬는 시간 최소화 (수업 간 공백 시간 최소화)")
    
    user_input = {
        "campus": campus,
        "subjects": subjects,
        "schedule_type": schedule_type,
        "preferences": {
            "include_weekend": include_weekend,
            "free_day": free_day,
            "max_consecutive_classes": max_consecutive_classes,
            "more_free_days": more_free_days,
            "extend_weekend": extend_weekend,
            "compress_classes": compress_classes,
            "minimize_breaks": minimize_breaks
        }
    }
    
    if st.button("🚀 시간표 생성 요청"): 
        with st.spinner("시간표를 생성 중입니다..."):
            generated_schedule = generate_schedule(user_input)
            st.write("### 📌 생성된 시간표")
            
            try:
                # JSON 형식으로 출력
                schedule_data = json.loads(generated_schedule)
                st.json(schedule_data)
            except json.JSONDecodeError:
                st.write(generated_schedule)  # 일반 텍스트로 출력

if __name__ == "__main__":
    main()