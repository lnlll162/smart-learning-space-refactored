import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_learning_path():
    """渲染学习路径页面"""
    st.title("🛤️ 智能学习路径")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 路径规划", 
        "📊 进度跟踪", 
        "🔄 路径调整", 
        "📈 学习报告"
    ])
    
    with tab1:
        render_path_planning()
    
    with tab2:
        render_progress_tracking()
    
    with tab3:
        render_path_adjustment()
    
    with tab4:
        render_learning_report()

def render_path_planning():
    """学习路径规划"""
    st.subheader("🎯 个性化学习路径规划")
    
    # 用户信息输入
    col1, col2 = st.columns(2)
    
    with col1:
        current_level = st.selectbox(
            "当前学习水平",
            ["初学者", "基础", "进阶", "高级", "专家"],
            index=1
        )
        
        target_level = st.selectbox(
            "目标学习水平",
            ["基础", "进阶", "高级", "专家", "大师"],
            index=2
        )
        
        available_time = st.selectbox(
            "每日可用时间",
            ["1小时以下", "1-2小时", "2-4小时", "4-6小时", "6小时以上"],
            index=2
        )
    
    with col2:
        learning_style = st.selectbox(
            "学习风格偏好",
            ["视觉型", "听觉型", "动手型", "阅读型", "混合型"],
            index=0
        )
        
        focus_subject = st.selectbox(
            "重点学习科目",
            ["数学", "物理", "化学", "生物", "语文", "英语", "综合"],
            index=0
        )
        
        deadline = st.date_input(
            "目标完成时间",
            value=datetime.now() + timedelta(days=90)
        )
    
    # 生成学习路径
    if st.button("🚀 生成学习路径", type="primary"):
        with st.spinner("正在分析您的需求，生成个性化学习路径..."):
            learning_path = generate_learning_path(
                current_level, target_level, available_time,
                learning_style, focus_subject, deadline
            )
            
            # 显示学习路径
            st.subheader("✨ 您的个性化学习路径")
            
            # 路径概览
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("总阶段数", len(learning_path["stages"]))
            
            with col2:
                st.metric("预计总时长", f"{learning_path['total_duration']}天")
            
            with col3:
                st.metric("难度提升", f"{learning_path['difficulty_increase']}")
            
            # 详细路径
            for i, stage in enumerate(learning_path["stages"], 1):
                with st.expander(f"📚 阶段 {i}: {stage['name']} ({stage['duration']}天)", expanded=i==1):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**学习目标**: {stage['objective']}")
                        st.write(f"**核心内容**: {', '.join(stage['core_content'])}")
                        st.write(f"**学习方式**: {stage['learning_method']}")
                        st.write(f"**预期成果**: {stage['expected_outcome']}")
                    
                    with col2:
                        # 进度条
                        progress = random.randint(0, 100)
                        st.progress(progress / 100)
                        st.write(f"当前进度: {progress}%")
                        
                        # 难度指示器
                        difficulty_colors = {
                            "简单": "green",
                            "中等": "orange",
                            "困难": "red"
                        }
                        st.write(f"**难度**: :{difficulty_colors.get(stage['difficulty'], 'blue')}[{stage['difficulty']}]")
                    
                    # 学习资源
                    st.write("**推荐学习资源**:")
                    for resource in stage['resources']:
                        st.write(f"- 📖 {resource}")
                    
                    # 学习任务
                    st.write("**具体学习任务**:")
                    for j, task in enumerate(stage['tasks'], 1):
                        if st.checkbox(f"☐ {task}", key=f"task_{i}_{j}"):
                            st.success(f"✅ {task}")
            
            # 保存路径
            if st.button("💾 保存学习路径"):
                st.success("学习路径已保存！")
                st.session_state.saved_path = learning_path

def generate_learning_path(current_level, target_level, available_time, learning_style, focus_subject, deadline):
    """生成学习路径"""
    stages = [
        {
            "name": "基础巩固",
            "objective": f"巩固{current_level}水平的基础知识",
            "duration": random.randint(7, 14),
            "core_content": ["基础概念", "基本技能", "简单应用"],
            "learning_method": "系统学习",
            "expected_outcome": "基础知识扎实",
            "difficulty": "简单",
            "resources": ["教材", "在线课程", "练习题"],
            "tasks": ["阅读教材", "完成练习", "总结笔记"]
        },
        {
            "name": "能力提升",
            "objective": f"提升到{target_level}水平",
            "duration": random.randint(14, 28),
            "core_content": ["进阶概念", "复杂技能", "综合应用"],
            "learning_method": "深度练习",
            "expected_outcome": "能力显著提升",
            "difficulty": "中等",
            "resources": ["进阶教材", "实战项目", "专家指导"],
            "tasks": ["深入学习", "项目实践", "技能训练"]
        },
        {
            "name": "综合应用",
            "objective": "综合运用所学知识",
            "duration": random.randint(14, 21),
            "core_content": ["综合应用", "创新思维", "实际问题"],
            "learning_method": "项目实践",
            "expected_outcome": "综合能力突出",
            "difficulty": "困难",
            "resources": ["项目案例", "创新平台", "实践机会"],
            "tasks": ["项目开发", "创新实践", "成果展示"]
        }
    ]
    
    total_duration = sum(stage["duration"] for stage in stages)
    
    return {
        "stages": stages,
        "total_duration": total_duration,
        "difficulty_increase": f"{current_level} → {target_level}",
        "focus_subject": focus_subject,
        "learning_style": learning_style
    }

def render_progress_tracking():
    """进度跟踪"""
    st.subheader("📊 学习进度跟踪")
    
    if "saved_path" not in st.session_state:
        st.warning("您还没有创建学习路径，请先在'路径规划'选项卡中创建。")
        return
    
    saved_path = st.session_state.saved_path
    
    # 总体进度
    st.write("**总体学习进度**")
    
    total_stages = len(saved_path["stages"])
    completed_stages = random.randint(0, total_stages)
    current_progress = (completed_stages / total_stages) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("已完成阶段", completed_stages, f"+{random.randint(0, 2)}")
    
    with col2:
        st.metric("总阶段数", total_stages)
    
    with col3:
        st.metric("完成进度", f"{current_progress:.1f}%", f"+{random.randint(1, 5)}%")
    
    with col4:
        remaining_days = max(0, saved_path["total_duration"] - random.randint(0, 30))
        st.metric("剩余天数", remaining_days, f"-{random.randint(1, 5)}天")
    
    # 进度可视化
    st.subheader("📈 进度可视化")
    
    stage_names = [stage["name"] for stage in saved_path["stages"]]
    stage_progress = [random.randint(0, 100) for _ in stage_names]
    
    fig_progress = px.bar(
        x=stage_names, y=stage_progress,
        title="各阶段完成进度",
        color=stage_progress,
        color_continuous_scale="RdYlGn"
    )
    
    fig_progress.update_layout(height=400)
    st.plotly_chart(fig_progress, use_container_width=True)

def render_path_adjustment():
    """路径调整"""
    st.subheader("🔄 学习路径调整")
    
    if "saved_path" not in st.session_state:
        st.warning("您还没有创建学习路径，请先在'路径规划'选项卡中创建。")
        return
    
    saved_path = st.session_state.saved_path
    
    st.write("**当前学习路径概览**")
    
    for i, stage in enumerate(saved_path["stages"]):
        st.write(f"**阶段 {i+1}**: {stage['name']} ({stage['duration']}天)")
        st.write(f"目标: {stage['objective']}")
        st.write("---")
    
    # 调整选项
    st.subheader("🔧 路径调整选项")
    
    adjustment_type = st.selectbox(
        "选择调整类型",
        ["调整学习时长", "修改学习内容", "重新规划路径"],
        index=0
    )
    
    if adjustment_type == "调整学习时长":
        st.write("**调整各阶段学习时长**")
        
        for i, stage in enumerate(saved_path["stages"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{stage['name']}**")
            with col2:
                new_duration = st.number_input(
                    f"天数", 
                    min_value=1, 
                    max_value=30, 
                    value=stage['duration'],
                    key=f"duration_{i}"
                )
                saved_path["stages"][i]["duration"] = new_duration
        
        if st.button("💾 保存时长调整"):
            st.success("学习时长已调整！")
    
    elif adjustment_type == "修改学习内容":
        st.write("**修改学习内容**")
        
        selected_stage = st.selectbox(
            "选择要修改的阶段",
            [f"阶段 {i+1}: {stage['name']}" for i, stage in enumerate(saved_path["stages"])],
            index=0
        )
        
        stage_index = int(selected_stage.split(":")[0].split()[1]) - 1
        stage = saved_path["stages"][stage_index]
        
        st.write(f"**当前内容**: {stage['objective']}")
        
        new_objective = st.text_area(
            "修改学习目标",
            value=stage['objective'],
            key=f"objective_{stage_index}"
        )
        
        if st.button("💾 保存内容修改"):
            saved_path["stages"][stage_index]["objective"] = new_objective
            st.success("学习内容已修改！")
    
    elif adjustment_type == "重新规划路径":
        st.write("**重新规划学习路径**")
        
        st.warning("重新规划将清除当前进度，确定要继续吗？")
        
        if st.button("🔄 重新规划"):
            del st.session_state.saved_path
            st.success("已清除当前路径，请重新创建！")
            st.rerun()

def render_learning_report():
    """学习报告"""
    st.subheader("📈 学习报告")
    
    if "saved_path" not in st.session_state:
        st.warning("您还没有创建学习路径，请先在'路径规划'选项卡中创建。")
        return
    
    saved_path = st.session_state.saved_path
    
    # 报告时间范围
    col1, col2 = st.columns(2)
    
    with col1:
        report_start = st.date_input(
            "报告开始时间",
            value=datetime.now() - timedelta(days=30)
        )
    
    with col2:
        report_end = st.date_input(
            "报告结束时间",
            value=datetime.now()
        )
    
    # 生成报告
    if st.button("📊 生成学习报告"):
        with st.spinner("正在生成学习报告..."):
            report = generate_learning_report(saved_path, report_start, report_end)
            
            # 显示报告
            st.subheader("📋 学习报告")
            
            # 学习概览
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**学习概览**")
                st.write(f"- 报告期间: {report_start} 至 {report_end}")
                st.write(f"- 学习天数: {report['study_days']}天")
                st.write(f"- 总学习时长: {report['total_study_time']}小时")
                st.write(f"- 平均每日时长: {report['avg_daily_time']:.1f}小时")
            
            with col2:
                st.write("**学习成果**")
                st.write(f"- 完成阶段: {report['completed_stages']}个")
                st.write(f"- 学习效率: {report['learning_efficiency']:.1f}%")
                st.write(f"- 知识掌握: {report['knowledge_mastery']:.1f}%")
                st.write(f"- 学习评分: {report['learning_score']:.1f}/10")
            
            # 学习趋势分析
            st.subheader("📈 学习趋势分析")
            
            fig_trend = px.line(
                x=report['dates'], y=report['daily_study_time'],
                title="学习时长趋势",
                markers=True
            )
            
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # 学习建议
            st.subheader("💡 学习建议")
            
            for suggestion in report['suggestions']:
                st.write(f"- {suggestion}")

def generate_learning_report(saved_path, start_date, end_date):
    """生成学习报告"""
    days_diff = (end_date - start_date).days
    
    return {
        "study_days": random.randint(days_diff//2, days_diff),
        "total_study_time": random.randint(20, 80),
        "avg_daily_time": random.uniform(1.5, 4.0),
        "completed_stages": random.randint(0, len(saved_path["stages"])),
        "learning_efficiency": random.uniform(70, 95),
        "knowledge_mastery": random.uniform(60, 90),
        "learning_score": random.uniform(7.0, 9.5),
        "dates": pd.date_range(start=start_date, end=end_date, freq='D'),
        "daily_study_time": [random.randint(1, 6) for _ in range(days_diff + 1)],
        "suggestions": [
            "建议增加每日学习时间，提高学习效率",
            "重点复习薄弱知识点，巩固基础",
            "多进行实践练习，提升应用能力",
            "保持学习连续性，避免知识遗忘"
        ]
    }
