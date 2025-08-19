import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_learning_space():
    """渲染学习空间页面"""
    st.title("🏠 智能学习空间")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 空间推荐", 
        "📊 空间分析", 
        "⚙️ 空间设置", 
        "📈 使用统计"
    ])
    
    with tab1:
        render_space_recommendation()
    
    with tab2:
        render_space_analysis()
    
    with tab3:
        render_space_settings()
    
    with tab4:
        render_usage_statistics()

def render_space_recommendation():
    """学习空间推荐"""
    st.subheader("🎯 个性化学习空间推荐")
    
    # 用户偏好设置
    st.write("**请设置您的学习偏好：**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        preferred_subject = st.selectbox(
            "主要学习科目",
            ["数学", "物理", "化学", "生物", "语文", "英语", "综合"],
            index=0
        )
        
        study_time = st.selectbox(
            "每日学习时间",
            ["1-2小时", "2-4小时", "4-6小时", "6小时以上"],
            index=1
        )
        
        noise_level = st.selectbox(
            "噪音容忍度",
            ["需要绝对安静", "轻微背景音", "适度环境音", "不介意噪音"],
            index=1
        )
    
    with col2:
        study_style = st.selectbox(
            "学习风格",
            ["独立学习", "小组讨论", "混合模式"],
            index=0
        )
        
        temperature = st.selectbox(
            "温度偏好",
            ["凉爽(18-22°C)", "适中(22-26°C)", "温暖(26-30°C)"],
            index=1
        )
        
        lighting = st.selectbox(
            "照明偏好",
            ["自然光", "柔和灯光", "明亮灯光", "可调节"],
            index=0
        )
    
    # 生成推荐
    if st.button("🚀 生成推荐", type="primary"):
        with st.spinner("正在分析您的偏好，生成个性化推荐..."):
            recommendations = generate_space_recommendations(
                preferred_subject, study_time, noise_level,
                study_style, temperature, lighting
            )
            
            # 显示推荐结果
            st.subheader("✨ 为您推荐的学习空间")
            
            for i, space in enumerate(recommendations, 1):
                with st.expander(f"🏆 推荐 {i}: {space['name']} (匹配度: {space['match_score']}%)", expanded=i==1):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**空间类型**: {space['type']}")
                        st.write(f"**适合科目**: {', '.join(space['suitable_subjects'])}")
                        st.write(f"**学习风格**: {space['study_style']}")
                        st.write(f"**环境特点**: {space['environment']}")
                        st.write(f"**推荐理由**: {space['reason']}")
                    
                    with col2:
                        # 显示匹配度图表
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number+delta",
                            value=space['match_score'],
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "匹配度"},
                            delta={'reference': 80},
                            gauge={
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 80], 'color': "gray"},
                                    {'range': [80, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 90
                                }
                            }
                        ))
                        fig.update_layout(height=200)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # 操作按钮
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📍 查看详情", key=f"detail_{i}"):
                            show_space_details(space)
                    
                    with col2:
                        if st.button(f"💾 收藏空间", key=f"favorite_{i}"):
                            st.success(f"已收藏 {space['name']}")
                    
                    with col3:
                        if st.button(f"📱 预约使用", key=f"book_{i}"):
                            show_booking_form(space)

def generate_space_recommendations(subject, study_time, noise_level, study_style, temperature, lighting):
    """生成学习空间推荐"""
    spaces = [
        {
            "name": "安静自习室A",
            "type": "独立学习",
            "suitable_subjects": ["数学", "物理", "化学"],
            "study_style": "独立学习",
            "environment": "安静、温度适中、自然光充足",
            "reason": "符合您的独立学习偏好，环境安静适合深度思考",
            "match_score": random.randint(85, 98)
        },
        {
            "name": "小组讨论室B",
            "type": "协作学习",
            "suitable_subjects": ["语文", "英语", "综合"],
            "study_style": "小组讨论",
            "environment": "适度环境音、温度可调、照明充足",
            "reason": "适合需要讨论和交流的学习内容",
            "match_score": random.randint(75, 90)
        },
        {
            "name": "多媒体教室C",
            "type": "综合学习",
            "suitable_subjects": ["所有科目"],
            "study_style": "混合模式",
            "environment": "设备齐全、温度适中、照明可调",
            "reason": "功能全面，适合多种学习需求",
            "match_score": random.randint(80, 95)
        }
    ]
    
    # 根据用户偏好调整匹配度
    for space in spaces:
        if space["study_style"] == study_style:
            space["match_score"] += 10
        if subject in space["suitable_subjects"]:
            space["match_score"] += 5
    
    # 按匹配度排序
    spaces.sort(key=lambda x: x["match_score"], reverse=True)
    
    return spaces

def show_space_details(space):
    """显示空间详情"""
    st.info(f"**{space['name']} 详细信息**")
    st.write(f"**空间类型**: {space['type']}")
    st.write(f"**适合科目**: {', '.join(space['suitable_subjects'])}")
    st.write(f"**学习风格**: {space['study_style']}")
    st.write(f"**环境特点**: {space['environment']}")
    st.write(f"**推荐理由**: {space['reason']}")
    st.write(f"**匹配度**: {space['match_score']}%")

def show_booking_form(space):
    """显示预约表单"""
    st.info(f"**预约 {space['name']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("选择日期")
        start_time = st.time_input("开始时间")
    
    with col2:
        duration = st.selectbox("使用时长", ["1小时", "2小时", "3小时", "4小时"])
        purpose = st.text_input("使用目的")
    
    if st.button("确认预约"):
        st.success(f"已成功预约 {space['name']}！")

def render_space_analysis():
    """学习空间分析"""
    st.subheader("📊 学习空间使用分析")
    
    # 时间范围选择
    col1, col2 = st.columns(2)
    with col1:
        time_range = st.selectbox(
            "选择时间范围",
            ["最近7天", "最近30天", "最近90天", "本学期"],
            index=1
        )
    
    with col2:
        analysis_type = st.selectbox(
            "分析类型",
            ["使用频率", "学习效果", "用户满意度", "空间利用率"],
            index=0
        )
    
    # 生成分析数据
    if time_range == "最近7天":
        days = 7
    elif time_range == "最近30天":
        days = 30
    elif time_range == "最近90天":
        days = 90
    else:
        days = 120
    
    # 模拟空间使用数据
    spaces = ["安静自习室", "小组讨论室", "多媒体教室", "户外学习区", "实验室"]
    
    if analysis_type == "使用频率":
        # 使用频率分析
        usage_data = []
        for space in spaces:
            for day in range(days):
                usage_data.append({
                    "空间": space,
                    "日期": datetime.now() - timedelta(days=day),
                    "使用次数": random.randint(5, 25),
                    "使用时长": random.randint(2, 8)
                })
        
        df = pd.DataFrame(usage_data)
        
        # 使用频率热力图
        pivot_df = df.pivot_table(
            values="使用次数", 
            index="空间", 
            columns=df["日期"].dt.strftime("%m-%d"),
            aggfunc="sum"
        ).fillna(0)
        
        fig = px.imshow(
            pivot_df,
            title="学习空间使用频率热力图",
            color_continuous_scale="Blues",
            aspect="auto"
        )
        
    elif analysis_type == "学习效果":
        # 学习效果分析
        effect_data = []
        for space in spaces:
            effect_data.append({
                "空间": space,
                "平均学习时长": random.randint(3, 8),
                "知识掌握度": random.randint(70, 95),
                "用户满意度": random.randint(80, 98),
                "学习效率": random.randint(75, 95)
            })
        
        df = pd.DataFrame(effect_data)
        
        # 雷达图
        fig = go.Figure()
        
        for _, row in df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row["平均学习时长"], row["知识掌握度"], 
                   row["用户满意度"], row["学习效率"]],
                theta=["学习时长", "知识掌握", "满意度", "学习效率"],
                fill='toself',
                name=row["空间"]
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="各空间学习效果对比"
        )
    
    elif analysis_type == "用户满意度":
        # 用户满意度分析
        satisfaction_data = []
        for space in spaces:
            for rating in range(1, 6):
                count = random.randint(10, 50)
                satisfaction_data.append({
                    "空间": space,
                    "评分": rating,
                    "用户数": count
                })
        
        df = pd.DataFrame(satisfaction_data)
        
        # 满意度柱状图
        fig = px.bar(
            df, x="空间", y="用户数", color="评分",
            title="各空间用户满意度分布",
            color_continuous_scale="RdYlGn"
        )
    
    else:  # 空间利用率
        # 空间利用率分析
        utilization_data = []
        for space in spaces:
            for hour in range(24):
                utilization_data.append({
                    "空间": space,
                    "小时": hour,
                    "利用率": random.randint(20, 90)
                })
        
        df = pd.DataFrame(utilization_data)
        
        # 利用率热力图
        pivot_df = df.pivot_table(
            values="利用率", 
            index="空间", 
            columns="小时",
            aggfunc="mean"
        )
        
        fig = px.imshow(
            pivot_df,
            title="24小时空间利用率热力图",
            color_continuous_scale="RdYlGn",
            aspect="auto",
            labels=dict(x="小时", y="空间", color="利用率(%)")
        )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def render_space_settings():
    """学习空间设置"""
    st.subheader("⚙️ 学习空间个性化设置")
    
    # 个人偏好设置
    st.write("**个人学习偏好设置**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**环境设置**")
        temperature_pref = st.slider("温度偏好 (°C)", 18, 30, 24)
        humidity_pref = st.slider("湿度偏好 (%)", 30, 80, 50)
        lighting_pref = st.selectbox("照明强度", ["柔和", "适中", "明亮"], index=1)
        noise_pref = st.selectbox("噪音控制", ["绝对安静", "轻微背景音", "适度环境音"], index=1)
    
    with col2:
        st.write("**学习设置**")
        study_duration = st.slider("单次学习时长 (小时)", 0.5, 4.0, 2.0, 0.5)
        break_interval = st.slider("休息间隔 (分钟)", 15, 60, 30, 15)
        reminder_enabled = st.checkbox("启用学习提醒", value=True)
        auto_save = st.checkbox("自动保存学习记录", value=True)
    
    # 保存设置
    if st.button("💾 保存设置", type="primary"):
        st.success("设置已保存！")

def render_usage_statistics():
    """使用统计"""
    st.subheader("📈 学习空间使用统计")
    
    # 统计概览
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("本月使用次数", "156", "+23")
    
    with col2:
        st.metric("累计学习时长", "89.5小时", "+12.3小时")
    
    with col3:
        st.metric("平均每次时长", "2.1小时", "+0.2小时")
    
    with col4:
        st.metric("空间满意度", "4.6/5.0", "+0.1")
    
    # 详细统计图表
    st.subheader("📊 详细使用统计")
    
    # 使用趋势图
    dates = pd.date_range(start=datetime.now() - timedelta(days=29), end=datetime.now(), freq='D')
    usage_trend = [random.randint(3, 8) for _ in range(30)]
    
    fig_trend = px.line(
        x=dates, y=usage_trend,
        title="30天使用趋势",
        labels={"x": "日期", "y": "使用次数"},
        markers=True
    )
    
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)
