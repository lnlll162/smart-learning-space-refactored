import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_analysis():
    """渲染数据分析页面"""
    st.title("📊 数据分析中心")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 学习趋势分析", 
        "🎯 知识点分析", 
        "⏰ 时间分布分析", 
        "📚 科目对比分析",
        "🔍 深度洞察"
    ])
    
    with tab1:
        render_trend_analysis()
    
    with tab2:
        render_knowledge_analysis()
    
    with tab3:
        render_time_analysis()
    
    with tab4:
        render_subject_comparison()
    
    with tab5:
        render_deep_insights()

def render_trend_analysis():
    """学习趋势分析"""
    st.subheader("📈 学习趋势分析")
    
    # 时间范围选择
    col1, col2 = st.columns(2)
    with col1:
        time_range = st.selectbox(
            "选择时间范围",
            ["最近7天", "最近30天", "最近90天", "本学期"],
            index=1
        )
    
    with col2:
        metric = st.selectbox(
            "选择分析指标",
            ["学习时长", "做题数量", "正确率", "学习效率"],
            index=0
        )
    
    # 生成模拟数据
    if time_range == "最近7天":
        days = 7
    elif time_range == "最近30天":
        days = 30
    elif time_range == "最近90天":
        days = 90
    else:
        days = 120
    
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                         end=datetime.now(), freq='D')
    
    # 根据指标生成数据
    if metric == "学习时长":
        data = [random.randint(2, 8) for _ in range(days)]
        y_label = "小时"
    elif metric == "做题数量":
        data = [random.randint(20, 100) for _ in range(days)]
        y_label = "题目数"
    elif metric == "正确率":
        data = [random.randint(70, 95) for _ in range(days)]
        y_label = "百分比"
    else:  # 学习效率
        data = [random.uniform(0.5, 2.0) for _ in range(days)]
        y_label = "效率指数"
    
    # 创建趋势图
    fig = go.Figure()
    
    # 主趋势线
    fig.add_trace(go.Scatter(
        x=dates, y=data,
        mode='lines+markers',
        name=metric,
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # 添加移动平均线
    if len(data) > 7:
        window_size = min(7, len(data) // 4)
        moving_avg = pd.Series(data).rolling(window=window_size).mean()
        fig.add_trace(go.Scatter(
            x=dates, y=moving_avg,
            mode='lines',
            name=f'{window_size}天移动平均',
            line=dict(color='red', width=2, dash='dash')
        ))
    
    fig.update_layout(
        title=f"{metric}趋势分析 ({time_range})",
        xaxis_title="日期",
        yaxis_title=y_label,
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 统计摘要
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("平均值", f"{np.mean(data):.2f}")
    
    with col2:
        st.metric("最大值", f"{np.max(data):.2f}")
    
    with col3:
        st.metric("最小值", f"{np.min(data):.2f}")
    
    with col4:
        st.metric("标准差", f"{np.std(data):.2f}")

def render_knowledge_analysis():
    """知识点分析"""
    st.subheader("🎯 知识点掌握分析")
    
    # 科目选择
    subject = st.selectbox(
        "选择科目",
        ["数学", "物理", "化学", "生物", "语文", "英语"],
        index=0
    )
    
    # 模拟知识点数据
    knowledge_points = {
        "数学": ["函数", "导数", "积分", "概率", "统计", "几何", "代数"],
        "物理": ["力学", "热学", "电磁学", "光学", "原子物理", "波动"],
        "化学": ["无机化学", "有机化学", "物理化学", "分析化学", "生物化学"],
        "生物": ["细胞生物学", "遗传学", "生态学", "进化论", "生理学"],
        "语文": ["现代文阅读", "古文阅读", "写作", "语言运用", "文学常识"],
        "英语": ["词汇", "语法", "阅读", "写作", "听力", "口语"]
    }
    
    selected_points = knowledge_points[subject]
    
    # 生成掌握程度数据
    mastery_data = []
    for point in selected_points:
        mastery_data.append({
            "知识点": point,
            "掌握程度": random.randint(30, 95),
            "练习次数": random.randint(10, 100),
            "错误率": random.randint(5, 40)
        })
    
    df = pd.DataFrame(mastery_data)
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("掌握程度", "练习次数", "错误率", "综合评估"),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # 掌握程度
    fig.add_trace(
        go.Bar(x=df["知识点"], y=df["掌握程度"], name="掌握程度"),
        row=1, col=1
    )
    
    # 练习次数
    fig.add_trace(
        go.Bar(x=df["知识点"], y=df["练习次数"], name="练习次数"),
        row=1, col=2
    )
    
    # 错误率
    fig.add_trace(
        go.Bar(x=df["知识点"], y=df["错误率"], name="错误率"),
        row=2, col=1
    )
    
    # 综合评估散点图
    fig.add_trace(
        go.Scatter(
            x=df["掌握程度"], 
            y=df["练习次数"],
            mode="markers",
            marker=dict(
                size=df["错误率"],
                color=df["掌握程度"],
                colorscale="RdYlGn",
                showscale=True
            ),
            text=df["知识点"],
            name="综合评估"
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # 知识点建议
    st.subheader("💡 知识点学习建议")
    
    # 找出薄弱知识点
    weak_points = df[df["掌握程度"] < 60].sort_values("掌握程度")
    
    if not weak_points.empty:
        st.warning("**需要重点加强的知识点：**")
        for _, row in weak_points.iterrows():
            st.write(f"- **{row['知识点']}**: 掌握程度 {row['掌握程度']}%，建议增加练习次数")
    
    # 找出优势知识点
    strong_points = df[df["掌握程度"] > 80].sort_values("掌握程度", ascending=False)
    
    if not strong_points.empty:
        st.success("**掌握较好的知识点：**")
        for _, row in strong_points.iterrows():
            st.write(f"- **{row['知识点']}**: 掌握程度 {row['掌握程度']}%，可以适当减少练习时间")

def render_time_analysis():
    """时间分布分析"""
    st.subheader("⏰ 学习时间分布分析")
    
    # 时间维度选择
    time_dimension = st.selectbox(
        "选择时间维度",
        ["每日分布", "每周分布", "每月分布", "时段分布"],
        index=0
    )
    
    if time_dimension == "每日分布":
        # 一周内每天的学习时间
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        study_hours = [random.randint(3, 8) for _ in range(7)]
        
        fig = px.bar(
            x=days, y=study_hours,
            title="一周内每日学习时间分布",
            color=study_hours,
            color_continuous_scale="Blues"
        )
        
    elif time_dimension == "每周分布":
        # 一个月内每周的学习时间
        weeks = [f"第{i}周" for i in range(1, 5)]
        study_hours = [random.randint(20, 40) for _ in range(4)]
        
        fig = px.line(
            x=weeks, y=study_hours,
            title="月度学习时间趋势",
            markers=True
        )
        
    elif time_dimension == "每月分布":
        # 一年内每月的学习时间
        months = ["1月", "2月", "3月", "4月", "5月", "6月", 
                 "7月", "8月", "9月", "10月", "11月", "12月"]
        study_hours = [random.randint(80, 200) for _ in range(12)]
        
        fig = px.area(
            x=months, y=study_hours,
            title="年度学习时间分布",
            fill="tonexty"
        )
        
    else:  # 时段分布
        # 一天内不同时段的学习效率
        time_slots = ["6-9点", "9-12点", "12-15点", "15-18点", "18-21点", "21-24点"]
        efficiency = [random.randint(60, 95) for _ in range(6)]
        
        fig = px.pie(
            values=efficiency, names=time_slots,
            title="不同时段学习效率分布"
        )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # 时间管理建议
    st.subheader("⏰ 时间管理建议")
    
    if time_dimension == "每日分布":
        best_day = days[study_hours.index(max(study_hours))]
        worst_day = days[study_hours.index(min(study_hours))]
        
        st.info(f"**最佳学习日**: {best_day} ({max(study_hours)}小时)")
        st.warning(f"**需要改进**: {worst_day} ({min(study_hours)}小时)")
        
        if worst_day in ["周六", "周日"]:
            st.write("建议：周末时间充足，可以适当增加学习时间")
        else:
            st.write("建议：工作日学习时间较少，可以调整作息安排")
    
    elif time_dimension == "时段分布":
        best_time = time_slots[efficiency.index(max(efficiency))]
        worst_time = time_slots[efficiency.index(min(efficiency))]
        
        st.info(f"**最佳学习时段**: {best_time} (效率: {max(efficiency)}%)")
        st.warning(f"**效率较低时段**: {worst_time} (效率: {min(efficiency)}%)")
        
        st.write("建议：")
        st.write(f"- 在{best_time}安排重要学习任务")
        st.write(f"- 在{worst_time}安排复习或轻松的学习内容")

def render_subject_comparison():
    """科目对比分析"""
    st.subheader("📚 科目对比分析")
    
    # 选择对比科目
    col1, col2 = st.columns(2)
    with col1:
        subject1 = st.selectbox("选择科目1", ["数学", "物理", "化学", "生物", "语文", "英语"], index=0)
    with col2:
        subject2 = st.selectbox("选择科目2", ["数学", "物理", "化学", "生物", "语文", "英语"], index=1)
    
    # 生成对比数据
    metrics = ["学习时长", "做题数量", "正确率", "学习效率", "知识点掌握"]
    
    subject1_data = [random.randint(60, 95) for _ in metrics]
    subject2_data = [random.randint(60, 95) for _ in metrics]
    
    # 雷达图对比
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=subject1_data,
        theta=metrics,
        fill='toself',
        name=subject1,
        line_color='blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=subject2_data,
        theta=metrics,
        fill='toself',
        name=subject2,
        line_color='red'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"{subject1} vs {subject2} 综合对比",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 详细对比表格
    st.subheader("📊 详细数据对比")
    
    comparison_data = {
        "指标": metrics,
        subject1: subject1_data,
        subject2: subject2_data,
        "差异": [s1 - s2 for s1, s2 in zip(subject1_data, subject2_data)]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    # 分析结论
    st.subheader("🔍 对比分析结论")
    
    total_score1 = sum(subject1_data)
    total_score2 = sum(subject2_data)
    
    if total_score1 > total_score2:
        st.success(f"**{subject1}整体表现更好**，总分: {total_score1} vs {total_score2}")
        st.write(f"建议：保持{subject1}的优势，重点提升{subject2}")
    elif total_score2 > total_score1:
        st.success(f"**{subject2}整体表现更好**，总分: {total_score2} vs {total_score1}")
        st.write(f"建议：保持{subject2}的优势，重点提升{subject1}")
    else:
        st.info(f"**两科目表现相当**，总分: {total_score1}")
        st.write("建议：均衡发展，可以适当调整学习重点")

def render_deep_insights():
    """深度洞察"""
    st.subheader("🔍 深度洞察分析")
    
    # 学习模式识别
    st.subheader("🎯 学习模式识别")
    
    # 模拟学习模式数据
    patterns = {
        "模式类型": ["晨型学习者", "夜型学习者", "碎片化学习", "集中式学习", "循环复习型"],
        "适用人群": ["早起人群", "夜猫子", "忙碌工作者", "学生", "记忆困难者"],
        "推荐指数": [random.randint(70, 95) for _ in range(5)]
    }
    
    patterns_df = pd.DataFrame(patterns)
    
    # 找出最适合的学习模式
    best_pattern_idx = patterns_df["推荐指数"].idxmax()
    best_pattern = patterns_df.loc[best_pattern_idx]
    
    st.success(f"**最适合你的学习模式**: {best_pattern['模式类型']}")
    st.write(f"**适用人群**: {best_pattern['适用人群']}")
    st.write(f"**推荐指数**: {best_pattern['推荐指数']}%")
    
    # 学习效率预测
    st.subheader("📈 学习效率预测")
    
    # 基于历史数据的简单预测
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("下周预测学习时长", f"{random.randint(25, 45)}小时", f"+{random.randint(1, 8)}小时")
        st.metric("下周预测做题数量", f"{random.randint(150, 350)}题", f"+{random.randint(10, 50)}题")
    
    with col2:
        st.metric("下周预测正确率", f"{random.randint(75, 95)}%", f"+{random.randint(1, 5)}%")
        st.metric("下周预测学习效率", f"{random.randint(80, 95)}%", f"+{random.randint(1, 10)}%")
    
    # 个性化建议
    st.subheader("💡 个性化学习建议")
    
    st.info("**基于你的学习数据分析，我们为你提供以下建议：**")
    
    recommendations = [
        "📚 **知识巩固**: 重点复习最近错误率较高的知识点",
        "⏰ **时间管理**: 在效率最高的时段安排重要学习任务",
        "🎯 **目标设定**: 设定每周具体的学习目标，并定期检查进度",
        "🔄 **复习策略**: 采用间隔重复的方法，提高记忆效果",
        "📊 **数据监控**: 每周回顾学习数据，及时调整学习策略"
    ]
    
    for rec in recommendations:
        st.write(rec)
    
    # 学习路径推荐
    st.subheader("🛤️ 推荐学习路径")
    
    path_data = {
        "阶段": ["基础巩固", "能力提升", "综合应用", "创新突破"],
        "预计时长": ["2-3周", "3-4周", "2-3周", "持续进行"],
        "重点内容": ["核心概念", "解题技巧", "综合题目", "创新思维"],
        "预期效果": ["基础扎实", "能力提升", "应用熟练", "思维创新"]
    }
    
    path_df = pd.DataFrame(path_data)
    st.dataframe(path_df, use_container_width=True)
    
    st.write("**建议**: 按照推荐路径循序渐进，每个阶段完成后进行自我评估，确保达到预期效果后再进入下一阶段。")
