import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_learning_behavior():
    """渲染学习行为分析页面"""
    st.title("🔍 学习行为分析")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 行为概览", 
        "⏰ 时间模式", 
        "🎯 学习模式", 
        "💡 行为建议"
    ])
    
    with tab1:
        render_behavior_overview()
    
    with tab2:
        render_time_patterns()
    
    with tab3:
        render_learning_patterns()
    
    with tab4:
        render_behavior_suggestions()

def render_behavior_overview():
    """行为概览"""
    st.subheader("📊 学习行为概览")
    
    # 行为统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("平均学习时长", "3.2小时", "+0.3小时")
    
    with col2:
        st.metric("学习频率", "5.8天/周", "+0.5天")
    
    with col3:
        st.metric("专注度", "78%", "+5%")
    
    with col4:
        st.metric("学习效率", "82%", "+3%")
    
    # 行为趋势图
    st.subheader("📈 行为趋势分析")
    
    # 生成30天的行为数据
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    behavior_data = []
    for date in dates:
        behavior_data.append({
            "日期": date,
            "学习时长": random.randint(2, 6),
            "专注度": random.randint(60, 90),
            "学习效率": random.randint(70, 95),
            "休息次数": random.randint(2, 8)
        })
    
    df = pd.DataFrame(behavior_data)
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("学习时长趋势", "专注度变化", "学习效率趋势", "休息频率"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 学习时长趋势
    fig.add_trace(
        go.Scatter(x=df["日期"], y=df["学习时长"], mode="lines+markers", name="学习时长"),
        row=1, col=1
    )
    
    # 专注度变化
    fig.add_trace(
        go.Scatter(x=df["日期"], y=df["专注度"], mode="lines+markers", name="专注度"),
        row=1, col=2
    )
    
    # 学习效率趋势
    fig.add_trace(
        go.Scatter(x=df["日期"], y=df["学习效率"], mode="lines+markers", name="学习效率"),
        row=2, col=1
    )
    
    # 休息频率
    fig.add_trace(
        go.Scatter(x=df["日期"], y=df["休息次数"], mode="lines+markers", name="休息次数"),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def render_time_patterns():
    """时间模式分析"""
    st.subheader("⏰ 学习时间模式分析")
    
    # 时间维度选择
    time_dimension = st.selectbox(
        "选择时间维度",
        ["每日分布", "每周分布", "时段分析", "季节变化"],
        index=0
    )
    
    if time_dimension == "每日分布":
        # 一周内每天的学习行为
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            study_hours = [random.randint(2, 6) for _ in range(7)]
            fig_hours = px.bar(
                x=days, y=study_hours,
                title="一周内每日学习时长",
                color=study_hours,
                color_continuous_scale="Blues"
            )
            fig_hours.update_layout(height=400)
            st.plotly_chart(fig_hours, use_container_width=True)
        
        with col2:
            focus_scores = [random.randint(60, 90) for _ in range(7)]
            fig_focus = px.line(
                x=days, y=focus_scores,
                title="一周内每日专注度",
                markers=True
            )
            fig_focus.update_layout(height=400)
            st.plotly_chart(fig_focus, use_container_width=True)
    
    elif time_dimension == "每周分布":
        # 一个月内每周的学习行为
        weeks = [f"第{i}周" for i in range(1, 5)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            weekly_hours = [random.randint(15, 35) for _ in range(4)]
            fig_weekly = px.bar(
                x=weeks, y=weekly_hours,
                title="月度学习时长分布",
                color=weekly_hours,
                color_continuous_scale="Greens"
            )
            fig_weekly.update_layout(height=400)
            st.plotly_chart(fig_weekly, use_container_width=True)
        
        with col2:
            weekly_efficiency = [random.randint(70, 95) for _ in range(4)]
            fig_efficiency = px.line(
                x=weeks, y=weekly_efficiency,
                title="月度学习效率趋势",
                markers=True
            )
            fig_efficiency.update_layout(height=400)
            st.plotly_chart(fig_efficiency, use_container_width=True)
    
    elif time_dimension == "时段分析":
        # 一天内不同时段的学习行为
        time_slots = ["6-9点", "9-12点", "12-15点", "15-18点", "18-21点", "21-24点"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            efficiency_by_hour = [random.randint(60, 95) for _ in range(6)]
            fig_efficiency_hour = px.pie(
                values=efficiency_by_hour, names=time_slots,
                title="不同时段学习效率分布"
            )
            fig_efficiency_hour.update_layout(height=400)
            st.plotly_chart(fig_efficiency_hour, use_container_width=True)
        
        with col2:
            focus_by_hour = [random.randint(50, 90) for _ in range(6)]
            fig_focus_hour = px.bar(
                x=time_slots, y=focus_by_hour,
                title="不同时段专注度分布",
                color=focus_by_hour,
                color_continuous_scale="RdYlGn"
            )
            fig_focus_hour.update_layout(height=400)
            st.plotly_chart(fig_focus_hour, use_container_width=True)
    
    else:  # 季节变化
        # 一年内不同季节的学习行为
        seasons = ["春季", "夏季", "秋季", "冬季"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            seasonal_hours = [random.randint(80, 200) for _ in range(4)]
            fig_seasonal = px.area(
                x=seasons, y=seasonal_hours,
                title="季节性学习时长变化",
                fill="tonexty"
            )
            fig_seasonal.update_layout(height=400)
            st.plotly_chart(fig_seasonal, use_container_width=True)
        
        with col2:
            seasonal_efficiency = [random.randint(70, 95) for _ in range(4)]
            fig_seasonal_eff = px.bar(
                x=seasons, y=seasonal_efficiency,
                title="季节性学习效率",
                color=seasonal_efficiency,
                color_continuous_scale="RdYlGn"
            )
            fig_seasonal_eff.update_layout(height=400)
            st.plotly_chart(fig_seasonal_eff, use_container_width=True)

def render_learning_patterns():
    """学习模式分析"""
    st.subheader("🎯 学习模式识别")
    
    # 学习模式类型
    pattern_types = ["时间管理", "专注模式", "休息模式", "效率模式", "环境偏好"]
    
    # 创建选项卡
    pattern_tabs = st.tabs(pattern_types)
    
    with pattern_tabs[0]:  # 时间管理
        st.write("**时间管理模式分析**")
        
        # 时间分配饼图
        time_allocation = {
            "专注学习": random.randint(40, 60),
            "复习巩固": random.randint(15, 25),
            "练习应用": random.randint(15, 25),
            "休息调整": random.randint(10, 20)
        }
        
        fig_time = px.pie(
            values=list(time_allocation.values()),
            names=list(time_allocation.keys()),
            title="学习时间分配"
        )
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
        
        # 时间管理建议
        st.write("**时间管理建议**:")
        st.write("- 建议增加专注学习时间比例")
        st.write("- 合理安排休息时间，避免过度疲劳")
        st.write("- 制定详细的时间计划表")
    
    with pattern_tabs[1]:  # 专注模式
        st.write("**专注模式分析**")
        
        # 专注度分布
        focus_levels = ["低专注", "中等专注", "高专注", "超高专注"]
        focus_counts = [random.randint(5, 15) for _ in range(4)]
        
        fig_focus = px.bar(
            x=focus_levels, y=focus_counts,
            title="专注度水平分布",
            color=focus_counts,
            color_continuous_scale="RdYlGn"
        )
        fig_focus.update_layout(height=400)
        st.plotly_chart(fig_focus, use_container_width=True)
        
        # 专注模式建议
        st.write("**专注模式建议**:")
        st.write("- 采用番茄工作法提高专注度")
        st.write("- 减少外界干扰，创造专注环境")
        st.write("- 定期进行专注力训练")
    
    with pattern_tabs[2]:  # 休息模式
        st.write("**休息模式分析**")
        
        # 休息频率分析
        rest_intervals = ["15分钟", "30分钟", "45分钟", "60分钟", "90分钟"]
        rest_counts = [random.randint(10, 30) for _ in range(5)]
        
        fig_rest = px.line(
            x=rest_intervals, y=rest_counts,
            title="休息间隔频率分布",
            markers=True
        )
        fig_rest.update_layout(height=400)
        st.plotly_chart(fig_rest, use_container_width=True)
        
        # 休息模式建议
        st.write("**休息模式建议**:")
        st.write("- 建议采用25分钟工作+5分钟休息的模式")
        st.write("- 休息时进行轻度活动，避免久坐")
        st.write("- 保证充足的睡眠时间")
    
    with pattern_tabs[3]:  # 效率模式
        st.write("**学习效率模式分析**")
        
        # 效率影响因素
        efficiency_factors = ["学习环境", "时间安排", "学习方法", "身体状况", "心理状态"]
        factor_scores = [random.randint(70, 95) for _ in range(5)]
        
        fig_efficiency = px.bar(
            x=efficiency_factors, y=factor_scores,
            title="学习效率影响因素分析",
            color=factor_scores,
            color_continuous_scale="RdYlGn"
        )
        fig_efficiency.update_layout(height=400)
        st.plotly_chart(fig_efficiency, use_container_width=True)
        
        # 效率提升建议
        st.write("**效率提升建议**:")
        st.write("- 优化学习环境，减少干扰因素")
        st.write("- 采用科学的学习方法")
        st.write("- 保持良好的身心状态")
    
    with pattern_tabs[4]:  # 环境偏好
        st.write("**学习环境偏好分析**")
        
        # 环境因素评分
        environment_factors = ["噪音水平", "温度", "照明", "空间大小", "设备配置"]
        factor_ratings = [random.randint(60, 95) for _ in range(5)]
        
        fig_env = go.Figure()
        
        fig_env.add_trace(go.Scatterpolar(
            r=factor_ratings,
            theta=environment_factors,
            fill='toself',
            name='环境偏好评分'
        ))
        
        fig_env.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title="学习环境偏好雷达图",
            height=400
        )
        st.plotly_chart(fig_env, use_container_width=True)
        
        # 环境优化建议
        st.write("**环境优化建议**:")
        st.write("- 选择安静的学习环境")
        st.write("- 保持适宜的温度和照明")
        st.write("- 确保学习设备齐全")

def render_behavior_suggestions():
    """行为建议"""
    st.subheader("💡 个性化学习行为建议")
    
    # 行为评估
    st.write("**学习行为评估结果**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**优势行为**:")
        st.success("✅ 学习时间安排合理")
        st.success("✅ 专注度保持良好")
        st.success("✅ 学习效率较高")
    
    with col2:
        st.write("**需要改进**:")
        st.warning("⚠️ 休息时间不够规律")
        st.warning("⚠️ 学习环境有待优化")
        st.warning("⚠️ 学习方法可以改进")
    
    # 具体建议
    st.subheader("🎯 具体改进建议")
    
    # 时间管理建议
    with st.expander("⏰ 时间管理建议", expanded=True):
        st.write("**当前问题**: 学习时间安排不够规律")
        st.write("**改进方案**:")
        st.write("1. 制定固定的学习时间表")
        st.write("2. 采用番茄工作法（25分钟工作+5分钟休息）")
        st.write("3. 设置学习提醒和进度跟踪")
        st.write("4. 合理安排学习强度，避免过度疲劳")
    
    # 专注力提升建议
    with st.expander("🎯 专注力提升建议", expanded=True):
        st.write("**当前问题**: 专注度波动较大")
        st.write("**改进方案**:")
        st.write("1. 创造无干扰的学习环境")
        st.write("2. 使用专注力训练应用")
        st.write("3. 采用渐进式专注训练")
        st.write("4. 定期进行冥想和放松练习")
    
    # 学习方法优化建议
    with st.expander("📚 学习方法优化建议", expanded=True):
        st.write("**当前问题**: 学习方法较为传统")
        st.write("**改进方案**:")
        st.write("1. 尝试多种学习方法（如费曼学习法）")
        st.write("2. 结合视觉、听觉等多种学习方式")
        st.write("3. 定期总结和复习")
        st.write("4. 参与讨论和知识分享")
    
    # 环境优化建议
    with st.expander("🏠 学习环境优化建议", expanded=True):
        st.write("**当前问题**: 学习环境不够理想")
        st.write("**改进方案**:")
        st.write("1. 选择安静、通风良好的学习空间")
        st.write("2. 调整合适的照明和温度")
        st.write("3. 准备必要的学习工具和设备")
        st.write("4. 减少视觉和听觉干扰")
    
    # 行动计划
    st.subheader("📋 行动计划")
    
    st.write("**建议您制定以下行动计划**:")
    
    action_plan = [
        "第一周：制定详细的学习时间表",
        "第二周：优化学习环境，减少干扰",
        "第三周：尝试新的学习方法",
        "第四周：评估改进效果，调整计划"
    ]
    
    for i, action in enumerate(action_plan, 1):
        st.write(f"{i}. {action}")
    
    # 进度跟踪
    if st.button("📊 开始跟踪改进进度"):
        st.success("已开始跟踪您的改进进度！")
        st.info("建议每周回顾一次，及时调整改进计划。")

# 辅助函数已移至导入部分
