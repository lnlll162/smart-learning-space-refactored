import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_learning_tracker():
    """渲染学习追踪器页面"""
    st.title("📊 学习追踪器")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 学习记录", 
        "📈 进度追踪", 
        "🎯 目标管理", 
        "📋 学习日志"
    ])
    
    with tab1:
        render_study_records()
    
    with tab2:
        render_progress_tracking()
    
    with tab3:
        render_goal_management()
    
    with tab4:
        render_study_log()

def render_study_records():
    """学习记录"""
    st.subheader("📝 学习记录管理")
    
    # 初始化学习记录
    if "study_records" not in st.session_state:
        st.session_state.study_records = []
    
    # 添加新记录
    st.write("**添加新的学习记录**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox(
            "学习科目",
            ["数学", "物理", "化学", "生物", "语文", "英语", "其他"],
            index=0
        )
        
        study_date = st.date_input(
            "学习日期",
            value=datetime.now()
        )
        
        study_duration = st.number_input(
            "学习时长（小时）",
            min_value=0.5,
            max_value=12.0,
            value=2.0,
            step=0.5
        )
    
    with col2:
        study_type = st.selectbox(
            "学习类型",
            ["理论学习", "实践练习", "复习巩固", "考试准备", "项目实践"],
            index=0
        )
        
        efficiency_rating = st.slider(
            "学习效率评分",
            min_value=1,
            max_value=10,
            value=7
        )
        
        difficulty_level = st.selectbox(
            "难度等级",
            ["简单", "中等", "困难", "极难"],
            index=1
        )
    
    # 学习内容描述
    study_content = st.text_area(
        "学习内容描述",
        placeholder="请描述今天学习的具体内容...",
        height=100
    )
    
    # 学习成果
    achievements = st.text_area(
        "学习成果",
        placeholder="请记录今天的学习收获...",
        height=100
    )
    
    # 添加记录
    if st.button("💾 添加学习记录", type="primary"):
        if study_content.strip():
            new_record = {
                "id": len(st.session_state.study_records) + 1,
                "subject": subject,
                "date": study_date,
                "duration": study_duration,
                "type": study_type,
                "efficiency": efficiency_rating,
                "difficulty": difficulty_level,
                "content": study_content,
                "achievements": achievements,
                "timestamp": datetime.now()
            }
            
            st.session_state.study_records.append(new_record)
            st.success("学习记录已添加！")
            st.rerun()
        else:
            st.warning("请填写学习内容描述！")
    
    # 显示学习记录
    st.subheader("📋 学习记录列表")
    
    if not st.session_state.study_records:
        st.info("暂无学习记录，请添加第一条记录。")
        return
    
    # 记录筛选
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_subject = st.selectbox(
            "按科目筛选",
            ["全部"] + list(set([record["subject"] for record in st.session_state.study_records])),
            index=0
        )
    
    with col2:
        filter_date_start = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30)
        )
    
    with col3:
        filter_date_end = st.date_input(
            "结束日期",
            value=datetime.now()
        )
    
    # 筛选记录
    filtered_records = st.session_state.study_records
    
    if filter_subject != "全部":
        filtered_records = [r for r in filtered_records if r["subject"] == filter_subject]
    
    filtered_records = [r for r in filtered_records if filter_date_start <= r["date"] <= filter_date_end]
    
    # 显示筛选后的记录
    if filtered_records:
        # 按日期排序
        filtered_records.sort(key=lambda x: x["date"], reverse=True)
        
        for record in filtered_records:
            with st.expander(f"📚 {record['subject']} - {record['date']} ({record['duration']}小时)", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**学习类型**: {record['type']}")
                    st.write(f"**学习内容**: {record['content']}")
                    st.write(f"**学习成果**: {record['achievements']}")
                
                with col2:
                    st.write(f"**效率评分**: {record['efficiency']}/10")
                    st.write(f"**难度等级**: {record['difficulty']}")
                    
                    # 删除按钮
                    if st.button(f"🗑️ 删除", key=f"delete_{record['id']}"):
                        st.session_state.study_records = [r for r in st.session_state.study_records if r["id"] != record["id"]]
                        st.success("记录已删除！")
                        st.rerun()
    else:
        st.info("没有找到符合条件的记录。")

def render_progress_tracking():
    """进度追踪"""
    st.subheader("📈 学习进度追踪")
    
    if "study_records" not in st.session_state or not st.session_state.study_records:
        st.warning("请先添加学习记录！")
        return
    
    records = st.session_state.study_records
    
    # 总体统计
    st.write("**总体学习统计**")
    
    total_records = len(records)
    total_hours = sum(record["duration"] for record in records)
    avg_efficiency = np.mean([record["efficiency"] for record in records])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总记录数", total_records)
    
    with col2:
        st.metric("总学习时长", f"{total_hours:.1f}小时")
    
    with col3:
        st.metric("平均效率", f"{avg_efficiency:.1f}/10")
    
    with col4:
        study_days = len(set(record["date"] for record in records))
        st.metric("学习天数", study_days)
    
    # 进度可视化
    st.subheader("📊 进度可视化")
    
    # 按科目统计
    subject_stats = {}
    for record in records:
        subject = record["subject"]
        if subject not in subject_stats:
            subject_stats[subject] = {"hours": 0, "records": 0, "efficiency": []}
        
        subject_stats[subject]["hours"] += record["duration"]
        subject_stats[subject]["records"] += 1
        subject_stats[subject]["efficiency"].append(record["efficiency"])
    
    # 学习时长分布
    subjects = list(subject_stats.keys())
    hours = [subject_stats[s]["hours"] for s in subjects]
    
    fig_hours = px.pie(
        values=hours, names=subjects,
        title="各科目学习时长分布"
    )
    
    fig_hours.update_layout(height=400)
    st.plotly_chart(fig_hours, use_container_width=True)
    
    # 学习效率趋势
    st.subheader("📈 学习效率趋势")
    
    # 按日期统计效率
    date_efficiency = {}
    for record in records:
        date = record["date"]
        if date not in date_efficiency:
            date_efficiency[date] = []
        date_efficiency[date].append(record["efficiency"])
    
    # 计算每日平均效率
    dates = sorted(date_efficiency.keys())
    avg_efficiencies = [np.mean(date_efficiency[date]) for date in dates]
    
    fig_efficiency = px.line(
        x=dates, y=avg_efficiencies,
        title="学习效率趋势变化",
        markers=True
    )
    
    fig_efficiency.update_layout(height=400)
    st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # 学习时长趋势
    st.subheader("⏰ 学习时长趋势")
    
    # 按日期统计时长
    date_duration = {}
    for record in records:
        date = record["date"]
        if date not in date_duration:
            date_duration[date] = 0
        date_duration[date] += record["duration"]
    
    # 按日期排序
    sorted_dates = sorted(date_duration.keys())
    durations = [date_duration[date] for date in sorted_dates]
    
    fig_duration = px.bar(
        x=sorted_dates, y=durations,
        title="每日学习时长变化",
        color=durations,
        color_continuous_scale="Blues"
    )
    
    fig_duration.update_layout(height=400)
    st.plotly_chart(fig_duration, use_container_width=True)

def render_goal_management():
    """目标管理"""
    st.subheader("🎯 学习目标管理")
    
    # 初始化学习目标
    if "learning_goals" not in st.session_state:
        st.session_state.learning_goals = []
    
    # 添加新目标
    st.write("**设置新的学习目标**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        goal_subject = st.selectbox(
            "目标科目",
            ["数学", "物理", "化学", "生物", "语文", "英语", "综合"],
            index=0
        )
        
        goal_type = st.selectbox(
            "目标类型",
            ["知识掌握", "技能提升", "考试通过", "项目完成", "时间投入"],
            index=0
        )
    
    with col2:
        goal_deadline = st.date_input(
            "目标截止日期",
            value=datetime.now() + timedelta(days=30)
        )
        
        goal_priority = st.selectbox(
            "优先级",
            ["低", "中", "高", "紧急"],
            index=1
        )
    
    goal_description = st.text_area(
        "目标描述",
        placeholder="请详细描述您的学习目标...",
        height=100
    )
    
    goal_metrics = st.text_area(
        "成功指标",
        placeholder="请描述如何衡量目标是否达成...",
        height=100
    )
    
    # 添加目标
    if st.button("🎯 添加学习目标", type="primary"):
        if goal_description.strip() and goal_metrics.strip():
            new_goal = {
                "id": len(st.session_state.learning_goals) + 1,
                "subject": goal_subject,
                "type": goal_type,
                "deadline": goal_deadline,
                "priority": goal_priority,
                "description": goal_description,
                "metrics": goal_metrics,
                "status": "进行中",
                "progress": 0,
                "created_at": datetime.now()
            }
            
            st.session_state.learning_goals.append(new_goal)
            st.success("学习目标已添加！")
            st.rerun()
        else:
            st.warning("请填写目标描述和成功指标！")
    
    # 显示学习目标
    st.subheader("📋 学习目标列表")
    
    if not st.session_state.learning_goals:
        st.info("暂无学习目标，请设置第一个目标。")
        return
    
    # 目标筛选
    col1, col2 = st.columns(2)
    
    with col1:
        filter_goal_subject = st.selectbox(
            "按科目筛选",
            ["全部"] + list(set([goal["subject"] for goal in st.session_state.learning_goals])),
            index=0
        )
    
    with col2:
        filter_goal_status = st.selectbox(
            "按状态筛选",
            ["全部", "进行中", "已完成", "已暂停"],
            index=0
        )
    
    # 筛选目标
    filtered_goals = st.session_state.learning_goals
    
    if filter_goal_subject != "全部":
        filtered_goals = [g for g in filtered_goals if g["subject"] == filter_goal_subject]
    
    if filter_goal_status != "全部":
        filtered_goals = [g for g in filtered_goals if g["status"] == filter_goal_status]
    
    # 显示筛选后的目标
    if filtered_goals:
        for goal in filtered_goals:
            with st.expander(f"🎯 {goal['subject']} - {goal['type']} ({goal['priority']}优先级)", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**目标描述**: {goal['description']}")
                    st.write(f"**成功指标**: {goal['metrics']}")
                    st.write(f"**截止日期**: {goal['deadline']}")
                    st.write(f"**当前状态**: {goal['status']}")
                
                with col2:
                    # 进度更新
                    new_progress = st.slider(
                        "更新进度",
                        min_value=0,
                        max_value=100,
                        value=goal["progress"],
                        key=f"progress_{goal['id']}"
                    )
                    
                    if new_progress != goal["progress"]:
                        goal["progress"] = new_progress
                        if new_progress >= 100:
                            goal["status"] = "已完成"
                        st.success("进度已更新！")
                    
                    # 状态更新
                    new_status = st.selectbox(
                        "更新状态",
                        ["进行中", "已完成", "已暂停"],
                        index=["进行中", "已完成", "已暂停"].index(goal["status"]),
                        key=f"status_{goal['id']}"
                    )
                    
                    if new_status != goal["status"]:
                        goal["status"] = new_status
                        st.success("状态已更新！")
                    
                    # 删除按钮
                    if st.button(f"🗑️ 删除", key=f"delete_goal_{goal['id']}"):
                        st.session_state.learning_goals = [g for g in st.session_state.learning_goals if g["id"] != goal["id"]]
                        st.success("目标已删除！")
                        st.rerun()
    else:
        st.info("没有找到符合条件的目标。")

def render_study_log():
    """学习日志"""
    st.subheader("📋 学习日志")
    
    if "study_records" not in st.session_state or not st.session_state.study_records:
        st.warning("请先添加学习记录！")
        return
    
    records = st.session_state.study_records
    
    # 日志时间范围选择
    col1, col2 = st.columns(2)
    
    with col1:
        log_start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=7)
        )
    
    with col2:
        log_end_date = st.date_input(
            "结束日期",
            value=datetime.now()
        )
    
    # 筛选指定时间范围的记录
    filtered_records = [r for r in records if log_start_date <= r["date"] <= log_end_date]
    
    if not filtered_records:
        st.info("指定时间范围内没有学习记录。")
        return
    
    # 按日期排序
    filtered_records.sort(key=lambda x: x["date"])
    
    # 生成学习日志
    st.write("**学习日志摘要**")
    
    # 统计信息
    total_days = len(set(r["date"] for r in filtered_records))
    total_hours = sum(r["duration"] for r in filtered_records)
    avg_efficiency = np.mean([r["efficiency"] for r in filtered_records])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("学习天数", total_days)
    
    with col2:
        st.metric("总学习时长", f"{total_hours:.1f}小时")
    
    with col3:
        st.metric("平均效率", f"{avg_efficiency:.1f}/10")
    
    # 详细日志
    st.subheader("📝 详细学习日志")
    
    # 按日期分组显示
    current_date = None
    for record in filtered_records:
        if record["date"] != current_date:
            current_date = record["date"]
            st.write(f"## 📅 {current_date}")
        
        with st.expander(f"📚 {record['subject']} - {record['type']} ({record['duration']}小时)", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**学习内容**: {record['content']}")
                st.write(f"**学习成果**: {record['achievements']}")
            
            with col2:
                st.write(f"**效率评分**: {record['efficiency']}/10")
                st.write(f"**难度等级**: {record['difficulty']}")
                st.write(f"**记录时间**: {record['timestamp'].strftime('%H:%M')}")
    
    # 导出日志
    if st.button("📥 导出学习日志"):
        st.success("日志导出功能开发中...")
        st.info("您可以将此页面保存为PDF或截图保存。")
