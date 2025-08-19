import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def render_learning_diagnosis():
    """渲染学习诊断页面"""
    st.title("🔬 学习诊断中心")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 诊断测试", 
        "🔍 问题分析", 
        "💊 解决方案", 
        "📈 诊断报告"
    ])
    
    with tab1:
        render_diagnosis_test()
    
    with tab2:
        render_problem_analysis()
    
    with tab3:
        render_solutions()
    
    with tab4:
        render_diagnosis_report()

def render_diagnosis_test():
    """诊断测试"""
    st.subheader("📋 学习能力诊断测试")
    
    st.write("**请回答以下问题，我们将为您进行全面的学习能力诊断：**")
    
    # 初始化测试结果
    if "diagnosis_results" not in st.session_state:
        st.session_state.diagnosis_results = {}
    
    # 测试问题
    questions = [
        {
            "category": "学习动机",
            "question": "您对学习新知识的兴趣程度如何？",
            "options": ["非常感兴趣", "比较感兴趣", "一般", "不太感兴趣", "完全不感兴趣"],
            "weights": [5, 4, 3, 2, 1]
        },
        {
            "category": "学习方法",
            "question": "您通常采用哪种学习方式？",
            "options": ["系统学习", "实践练习", "讨论交流", "阅读思考", "混合方式"],
            "weights": [4, 5, 4, 3, 5]
        },
        {
            "category": "时间管理",
            "question": "您如何安排学习时间？",
            "options": ["有详细计划", "大致安排", "随机安排", "很少安排", "从不安排"],
            "weights": [5, 4, 3, 2, 1]
        },
        {
            "category": "专注能力",
            "question": "您在学习时的专注程度如何？",
            "options": ["高度专注", "比较专注", "一般", "容易分心", "很难专注"],
            "weights": [5, 4, 3, 2, 1]
        },
        {
            "category": "记忆能力",
            "question": "您对新学知识的记忆效果如何？",
            "options": ["记忆深刻", "记忆较好", "记忆一般", "容易遗忘", "很难记住"],
            "weights": [5, 4, 3, 2, 1]
        },
        {
            "category": "理解能力",
            "question": "您对新概念的理解速度如何？",
            "options": ["理解很快", "理解较快", "理解一般", "理解较慢", "很难理解"],
            "weights": [5, 4, 3, 2, 1]
        },
        {
            "category": "应用能力",
            "question": "您将所学知识应用到实际问题的能力如何？",
            "options": ["应用自如", "应用较好", "应用一般", "应用较难", "很难应用"],
            "weights": [5, 4, 3, 2, 1]
        },
        {
            "category": "创新能力",
            "question": "您在学习过程中的创新思维如何？",
            "options": ["很有创新", "比较创新", "一般", "创新较少", "缺乏创新"],
            "weights": [5, 4, 3, 2, 1]
        }
    ]
    
    # 显示问题
    answers = {}
    for i, q in enumerate(questions):
        st.write(f"**{q['category']}**: {q['question']}")
        answer = st.selectbox(
            f"选择答案",
            q["options"],
            key=f"q_{i}"
        )
        answers[q["category"]] = {
            "answer": answer,
            "score": q["weights"][q["options"].index(answer)]
        }
        st.write("---")
    
    # 提交测试
    if st.button("🚀 提交诊断", type="primary"):
        # 计算诊断结果
        diagnosis_results = calculate_diagnosis_results(questions, answers)
        st.session_state.diagnosis_results = diagnosis_results
        
        st.success("诊断完成！请查看'问题分析'选项卡了解详细结果。")
        
        # 显示总体评分
        st.subheader("📊 总体诊断评分")
        
        total_score = sum(result["score"] for result in diagnosis_results.values())
        max_score = len(questions) * 5
        percentage = (total_score / max_score) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("总分", total_score, f"/{max_score}")
        
        with col2:
            st.metric("得分率", f"{percentage:.1f}%")
        
        with col3:
            if percentage >= 80:
                level = "优秀"
                color = "success"
            elif percentage >= 60:
                level = "良好"
                color = "info"
            elif percentage >= 40:
                level = "一般"
                color = "warning"
            else:
                level = "需要改进"
                color = "error"
            
            st.metric("水平评估", level)

def render_problem_analysis():
    """问题分析"""
    st.subheader("🔍 学习问题深度分析")
    
    if "diagnosis_results" not in st.session_state or not st.session_state.diagnosis_results:
        st.warning("请先完成诊断测试！")
        return
    
    diagnosis_results = st.session_state.diagnosis_results
    
    # 问题分类分析
    st.write("**问题分类分析**")
    
    # 按得分分类问题
    excellent = []
    good = []
    average = []
    poor = []
    
    for category, result in diagnosis_results.items():
        if result["score"] >= 4:
            excellent.append(category)
        elif result["score"] >= 3:
            good.append(category)
        elif result["score"] >= 2:
            average.append(category)
        else:
            poor.append(category)
    
    # 显示分类结果
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.success(f"**优秀领域** ({len(excellent)})")
        for area in excellent:
            st.write(f"✅ {area}")
    
    with col2:
        st.info(f"**良好领域** ({len(good)})")
        for area in good:
            st.write(f"👍 {area}")
    
    with col3:
        st.warning(f"**一般领域** ({len(average)})")
        for area in average:
            st.write(f"⚠️ {area}")
    
    with col4:
        st.error(f"**需要改进** ({len(poor)})")
        for area in poor:
            st.write(f"❌ {area}")
    
    # 详细问题分析
    st.subheader("📊 详细问题分析")
    
    # 雷达图显示各维度得分
    categories = list(diagnosis_results.keys())
    scores = [result["score"] for result in diagnosis_results.values()]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='当前水平',
        line_color='blue'
    ))
    
    # 添加理想水平线
    ideal_scores = [5] * len(categories)
    fig_radar.add_trace(go.Scatterpolar(
        r=ideal_scores,
        theta=categories,
        fill='toself',
        name='理想水平',
        line_color='red',
        opacity=0.3
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True,
        title="学习能力各维度分析",
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # 问题优先级排序
    st.subheader("🎯 问题优先级排序")
    
    # 按得分排序，找出最需要改进的领域
    sorted_results = sorted(diagnosis_results.items(), key=lambda x: x[1]["score"])
    
    st.write("**按优先级排序的问题领域：**")
    
    for i, (category, result) in enumerate(sorted_results, 1):
        if result["score"] < 4:  # 只显示需要改进的领域
            priority = "🔴 高优先级" if result["score"] <= 2 else "🟡 中优先级"
            st.write(f"{i}. **{category}** - {priority}")
            st.write(f"   当前得分: {result['score']}/5")
            st.write(f"   改进空间: {5 - result['score']}分")
            st.write("---")

def render_solutions():
    """解决方案"""
    st.subheader("💊 个性化解决方案")
    
    if "diagnosis_results" not in st.session_state or not st.session_state.diagnosis_results:
        st.warning("请先完成诊断测试！")
        return
    
    diagnosis_results = st.session_state.diagnosis_results
    
    # 解决方案库
    solutions_library = {
        "学习动机": [
            "设定明确的学习目标，将大目标分解为小目标",
            "找到学习的意义和价值，建立内在驱动力",
            "采用奖励机制，激励自己持续学习",
            "与志同道合的学习伙伴一起学习",
            "定期回顾学习成果，增强成就感"
        ],
        "学习方法": [
            "尝试多种学习方法，找到最适合自己的方式",
            "采用费曼学习法，通过教授他人来巩固知识",
            "使用思维导图整理知识结构",
            "结合理论与实践，提高学习效果",
            "定期总结和反思，优化学习方法"
        ],
        "时间管理": [
            "制定详细的学习计划表，合理分配时间",
            "使用番茄工作法，提高学习效率",
            "设置学习提醒和进度跟踪",
            "避免拖延，立即开始行动",
            "定期评估时间使用效果，调整计划"
        ],
        "专注能力": [
            "创造无干扰的学习环境",
            "使用专注力训练应用",
            "采用渐进式专注训练",
            "定期进行冥想和放松练习",
            "减少多任务处理，一次专注一件事"
        ],
        "记忆能力": [
            "采用间隔重复法，定期复习",
            "使用记忆宫殿等记忆技巧",
            "将新知识与已有知识建立联系",
            "通过多种感官学习，加深记忆",
            "及时复习和应用，巩固记忆"
        ],
        "理解能力": [
            "多角度思考问题，深入理解概念",
            "通过举例和类比帮助理解",
            "主动提问，澄清疑惑",
            "与他人讨论交流，加深理解",
            "实践应用，检验理解程度"
        ],
        "应用能力": [
            "多做练习题，提高应用能力",
            "参与实际项目，锻炼实践能力",
            "寻找生活中的应用场景",
            "与他人合作，学习不同视角",
            "定期反思应用效果，总结经验"
        ],
        "创新能力": [
            "培养批判性思维，质疑常规做法",
            "尝试不同的解决方案",
            "关注前沿知识，拓展视野",
            "与他人头脑风暴，激发创意",
            "勇于尝试新方法，不怕失败"
        ]
    }
    
    # 显示个性化解决方案
    st.write("**根据您的诊断结果，为您提供以下个性化解决方案：**")
    
    # 按优先级显示解决方案
    sorted_results = sorted(diagnosis_results.items(), key=lambda x: x[1]["score"])
    
    for category, result in sorted_results:
        if result["score"] < 4:  # 只显示需要改进的领域
            with st.expander(f"🔧 {category} 改进方案 (当前得分: {result['score']}/5)", expanded=True):
                st.write(f"**问题分析**: 您在{category}方面还有改进空间")
                
                st.write("**具体解决方案**:")
                solutions = solutions_library.get(category, [])
                for i, solution in enumerate(solutions, 1):
                    st.write(f"{i}. {solution}")
                
                # 个性化建议
                if result["score"] <= 2:
                    st.warning("**紧急建议**: 建议优先改进此领域，可以寻求专业指导")
                elif result["score"] == 3:
                    st.info("**改进建议**: 通过系统练习可以显著提升")
                else:
                    st.success("**优化建议**: 在现有基础上进一步优化")
    
    # 整体改进计划
    st.subheader("📋 整体改进计划")
    
    st.write("**建议的改进时间安排**:")
    
    improvement_plan = [
        "**第一周**: 重点改进最高优先级的1-2个领域",
        "**第二周**: 继续改进，同时开始中等优先级领域",
        "**第三周**: 全面改进，重点关注薄弱环节",
        "**第四周**: 巩固改进成果，评估整体提升效果"
    ]
    
    for plan in improvement_plan:
        st.write(f"- {plan}")
    
    # 跟踪改进进度
    if st.button("📊 开始跟踪改进进度"):
        st.success("已开始跟踪您的改进进度！")
        st.info("建议每周回顾一次，及时调整改进计划。")

def render_diagnosis_report():
    """诊断报告"""
    st.subheader("📈 完整诊断报告")
    
    if "diagnosis_results" not in st.session_state or not st.session_state.diagnosis_results:
        st.warning("请先完成诊断测试！")
        return
    
    diagnosis_results = st.session_state.diagnosis_results
    
    # 报告概览
    st.write("**诊断报告概览**")
    
    total_score = sum(result["score"] for result in diagnosis_results.values())
    max_score = len(diagnosis_results) * 5
    percentage = (total_score / max_score) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总体得分", f"{total_score}/{max_score}")
    
    with col2:
        st.metric("得分率", f"{percentage:.1f}%")
    
    with col3:
        if percentage >= 80:
            level = "优秀"
            color = "success"
        elif percentage >= 60:
            level = "良好"
            color = "info"
        elif percentage >= 40:
            level = "一般"
            color = "warning"
        else:
            level = "需要改进"
            color = "error"
        
        st.metric("水平评估", level)
    
    with col4:
        improvement_potential = max_score - total_score
        st.metric("改进潜力", f"+{improvement_potential}分")
    
    # 详细得分表
    st.subheader("📊 详细得分表")
    
    score_data = []
    for category, result in diagnosis_results.items():
        score_data.append({
            "能力领域": category,
            "当前得分": result["score"],
            "满分": 5,
            "得分率": f"{(result['score'] / 5) * 100:.1f}%",
            "改进空间": 5 - result["score"],
            "状态": "优秀" if result["score"] >= 4 else "良好" if result["score"] >= 3 else "一般" if result["score"] >= 2 else "需要改进"
        })
    
    score_df = pd.DataFrame(score_data)
    st.dataframe(score_df, use_container_width=True)
    
    # 可视化分析
    st.subheader("📈 可视化分析")
    
    # 柱状图显示各领域得分
    categories = list(diagnosis_results.keys())
    scores = [result["score"] for result in diagnosis_results.values()]
    
    fig_bar = px.bar(
        x=categories, y=scores,
        title="各学习能力领域得分",
        color=scores,
        color_continuous_scale="RdYlGn"
    )
    
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 改进建议总结
    st.subheader("💡 改进建议总结")
    
    # 找出最需要改进的3个领域
    sorted_results = sorted(diagnosis_results.items(), key=lambda x: x[1]["score"])[:3]
    
    st.write("**最需要改进的领域**:")
    
    for i, (category, result) in enumerate(sorted_results, 1):
        st.write(f"{i}. **{category}** (得分: {result['score']}/5)")
        st.write(f"   改进建议: 通过系统练习和专项训练提升{category}能力")
        st.write(f"   预期提升: 可提升{5 - result['score']}分")
        st.write("---")
    
    # 下载报告
    if st.button("📥 下载诊断报告"):
        st.success("报告下载功能开发中...")
        st.info("您可以将此页面保存为PDF或截图保存。")

# 辅助函数
def calculate_diagnosis_results(questions, answers):
    """计算诊断结果"""
    results = {}
    
    for question in questions:
        category = question["category"]
        if category in answers:
            results[category] = {
                "answer": answers[category]["answer"],
                "score": answers[category]["score"]
            }
    
    return results
