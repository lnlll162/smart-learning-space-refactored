import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_dashboard():
    """渲染仪表板页面"""
    st.title("📊 学习空间仪表板")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 学习进度概览")
        
        # 模拟学习数据
        subjects = ["数学", "物理", "化学", "生物", "语文", "英语"]
        progress_data = {
            "subject": subjects,
            "progress": [random.randint(60, 95) for _ in subjects],
            "time_spent": [random.randint(2, 8) for _ in subjects],
            "difficulty": [random.randint(1, 5) for _ in subjects]
        }
        
        df = pd.DataFrame(progress_data)
        
        # 学习进度柱状图
        fig_progress = px.bar(
            df, x="subject", y="progress",
            title="各科目学习进度",
            color="progress",
            color_continuous_scale="RdYlGn"
        )
        fig_progress.update_layout(height=400)
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # 学习时间分布
        fig_time = px.pie(
            df, values="time_spent", names="subject",
            title="学习时间分布"
        )
        fig_time.update_layout(height=300)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.subheader("🎯 今日目标")
        
        # 今日学习目标
        today_goals = [
            "完成数学第三章练习",
            "复习物理公式",
            "背诵英语单词50个",
            "阅读语文课文"
        ]
        
        for i, goal in enumerate(today_goals):
            if st.checkbox(f"☐ {goal}", key=f"goal_{i}"):
                st.success(f"✅ {goal}")
        
        st.subheader("📅 学习日历")
        
        # 简单的日历显示
        today = datetime.now()
        calendar_data = []
        
        for i in range(7):
            date = today - timedelta(days=i)
            study_hours = random.randint(1, 6)
            calendar_data.append({
                "date": date.strftime("%m-%d"),
                "hours": study_hours
            })
        
        calendar_df = pd.DataFrame(calendar_data)
        fig_calendar = px.line(
            calendar_df, x="date", y="hours",
            title="近7天学习时长",
            markers=True
        )
        fig_calendar.update_layout(height=200)
        st.plotly_chart(fig_calendar, use_container_width=True)
    
    # 学习统计卡片
    st.subheader("📊 学习统计")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="本周学习时长",
            value=f"{random.randint(20, 40)}小时",
            delta=f"+{random.randint(1, 5)}小时"
        )
    
    with col2:
        st.metric(
            label="完成题目数",
            value=f"{random.randint(100, 300)}题",
            delta=f"+{random.randint(10, 30)}题"
        )
    
    with col3:
        st.metric(
            label="平均正确率",
            value=f"{random.randint(75, 95)}%",
            delta=f"+{random.randint(1, 5)}%"
        )
    
    with col4:
        st.metric(
            label="连续学习天数",
            value=f"{random.randint(5, 15)}天",
            delta="+1天"
        )
    
    # 学习趋势图
    st.subheader("📈 学习趋势分析")
    
    # 生成30天的学习数据
    dates = pd.date_range(start=today - timedelta(days=30), end=today, freq='D')
    study_data = []
    
    for date in dates:
        study_data.append({
            "date": date,
            "hours": random.randint(2, 8),
            "questions": random.randint(20, 100),
            "accuracy": random.randint(70, 95)
        })
    
    study_df = pd.DataFrame(study_data)
    
    # 创建子图
    fig_trends = make_subplots(
        rows=2, cols=2,
        subplot_titles=("学习时长趋势", "做题数量趋势", "正确率趋势", "学习效率分析"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 学习时长趋势
    fig_trends.add_trace(
        go.Scatter(x=study_df["date"], y=study_df["hours"], 
                  mode="lines+markers", name="学习时长"),
        row=1, col=1
    )
    
    # 做题数量趋势
    fig_trends.add_trace(
        go.Scatter(x=study_df["date"], y=study_df["questions"], 
                  mode="lines+markers", name="做题数量"),
        row=1, col=2
    )
    
    # 正确率趋势
    fig_trends.add_trace(
        go.Scatter(x=study_df["date"], y=study_df["accuracy"], 
                  mode="lines+markers", name="正确率"),
        row=2, col=1
    )
    
    # 学习效率分析（时长/题目数的比值）
    efficiency = study_df["hours"] / study_df["questions"]
    fig_trends.add_trace(
        go.Scatter(x=study_df["date"], y=efficiency, 
                  mode="lines+markers", name="学习效率"),
        row=2, col=2
    )
    
    fig_trends.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # 学习建议
    st.subheader("💡 学习建议")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**数学学习建议**\n\n根据你的学习数据，建议：\n- 重点复习第三章薄弱知识点\n- 每天保持2小时练习时间\n- 错题本要及时整理")
        
        st.info("**物理学习建议**\n\n当前状态良好，建议：\n- 继续巩固公式记忆\n- 多做实验题\n- 关注解题思路")
    
    with col2:
        st.warning("**英语学习建议**\n\n需要加强的方面：\n- 词汇量积累\n- 语法规则理解\n- 听力训练")
        
        st.success("**语文学习建议**\n\n表现优秀，建议：\n- 保持阅读习惯\n- 多写作文\n- 背诵经典段落")
