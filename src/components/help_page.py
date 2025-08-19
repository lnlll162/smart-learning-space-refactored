import streamlit as st

def render_help_page():
    """渲染帮助页面"""
    st.title("❓ 帮助中心")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 使用指南", 
        "🔧 常见问题", 
        "📞 联系我们", 
        "📚 更新日志"
    ])
    
    with tab1:
        render_user_guide()
    
    with tab2:
        render_faq()
    
    with tab3:
        render_contact()
    
    with tab4:
        render_changelog()

def render_user_guide():
    """使用指南"""
    st.subheader("📖 使用指南")
    
    st.write("**欢迎使用大创智慧学习空间！本指南将帮助您快速上手使用系统。**")
    
    # 快速开始
    with st.expander("🚀 快速开始", expanded=True):
        st.write("**第一步：注册和登录**")
        st.write("1. 点击右上角的'登录'按钮")
        st.write("2. 如果是新用户，点击'注册新账户'")
        st.write("3. 填写必要信息并完成注册")
        st.write("4. 使用注册的账户登录系统")
        
        st.write("**第二步：探索主要功能**")
        st.write("1. **仪表板**: 查看学习概览和统计数据")
        st.write("2. **数据分析**: 深入分析学习数据和趋势")
        st.write("3. **AI助手**: 获取智能学习建议和帮助")
        st.write("4. **学习空间**: 发现适合的学习环境")
        st.write("5. **学习路径**: 规划个性化学习路线")
        
        st.write("**第三步：开始学习**")
        st.write("1. 设置学习目标")
        st.write("2. 记录学习过程")
        st.write("3. 跟踪学习进度")
        st.write("4. 分析学习效果")
    
    # 功能详解
    with st.expander("🔍 功能详解", expanded=True):
        st.write("**📊 仪表板功能**")
        st.write("- 学习进度概览：查看各科目学习进度")
        st.write("- 学习统计：学习时长、做题数量、正确率等")
        st.write("- 学习趋势：分析学习数据变化趋势")
        st.write("- 学习建议：基于数据提供个性化建议")
        
        st.write("**📈 数据分析功能**")
        st.write("- 学习趋势分析：多维度分析学习趋势")
        st.write("- 知识点分析：评估知识点掌握程度")
        st.write("- 时间分布分析：了解学习时间模式")
        st.write("- 科目对比分析：比较不同科目表现")
        st.write("- 深度洞察：识别学习模式和问题")
        
        st.write("**🤖 AI助手功能**")
        st.write("- 智能对话：与AI进行学习相关对话")
        st.write("- 学习辅导：获取个性化学习指导")
        st.write("- 题目解析：AI辅助解题和思路分析")
        st.write("- 知识问答：快速获取知识答案")
        
        st.write("**🏠 学习空间功能**")
        st.write("- 空间推荐：基于偏好推荐学习环境")
        st.write("- 空间分析：分析空间使用情况")
        st.write("- 空间设置：个性化空间配置")
        st.write("- 使用统计：统计空间使用数据")
        
        st.write("**🛤️ 学习路径功能**")
        st.write("- 路径规划：制定个性化学习计划")
        st.write("- 进度跟踪：监控学习目标完成情况")
        st.write("- 路径调整：根据情况调整学习计划")
        st.write("- 学习报告：生成详细学习报告")
        
        st.write("**🔍 学习行为分析功能**")
        st.write("- 行为概览：学习行为整体分析")
        st.write("- 时间模式：学习时间分布分析")
        st.write("- 学习模式：识别学习行为模式")
        st.write("- 行为建议：提供改进建议")
        
        st.write("**🔬 学习诊断功能**")
        st.write("- 诊断测试：评估学习能力水平")
        st.write("- 问题分析：深度分析学习问题")
        st.write("- 解决方案：提供个性化改进方案")
        st.write("- 诊断报告：生成完整诊断报告")
        
        st.write("**📊 学习追踪器功能**")
        st.write("- 学习记录：记录详细学习过程")
        st.write("- 进度追踪：可视化学习进度")
        st.write("- 目标管理：设置和管理学习目标")
        st.write("- 学习日志：生成学习日志报告")
    
    # 使用技巧
    with st.expander("💡 使用技巧", expanded=True):
        st.write("**提高使用效率的技巧**")
        st.write("1. **定期更新数据**: 建议每天记录学习情况，保持数据新鲜")
        st.write("2. **设置学习提醒**: 利用系统提醒功能，保持学习连续性")
        st.write("3. **多维度分析**: 结合不同分析工具，全面了解学习状况")
        st.write("4. **个性化设置**: 根据个人偏好调整系统设置")
        st.write("5. **定期回顾**: 每周回顾学习数据，及时调整学习策略")
        
        st.write("**数据安全建议**")
        st.write("1. **定期备份**: 重要数据建议定期导出备份")
        st.write("2. **隐私保护**: 不要在记录中填写敏感个人信息")
        st.write("3. **账户安全**: 使用强密码，定期更换")
        st.write("4. **设备安全**: 在个人设备上使用，避免在公共设备登录")

def render_faq():
    """常见问题"""
    st.subheader("🔧 常见问题")
    
    # 系统使用问题
    with st.expander("❓ 系统使用问题", expanded=True):
        st.write("**Q: 如何重置密码？**")
        st.write("A: 在登录页面点击'忘记密码'，按照提示操作即可重置密码。")
        
        st.write("**Q: 可以同时登录多个设备吗？**")
        st.write("A: 为了账户安全，系统不支持同时登录多个设备。")
        
        st.write("**Q: 学习数据会丢失吗？**")
        st.write("A: 系统会自动保存您的学习数据，但建议定期导出备份重要数据。")
        
        st.write("**Q: 如何导出学习报告？**")
        st.write("A: 在各个功能页面都有导出按钮，点击即可导出相应报告。")
    
    # 功能相关问题
    with st.expander("❓ 功能相关问题", expanded=True):
        st.write("**Q: AI助手回答不准确怎么办？**")
        st.write("A: AI助手基于训练数据回答，可能存在不准确情况。建议结合其他学习资源验证。")
        
        st.write("**Q: 学习路径规划不合理怎么办？**")
        st.write("A: 系统会根据您的设置生成路径，您可以在'路径调整'中手动修改。")
        
        st.write("**Q: 数据统计不准确怎么办？**")
        st.write("A: 请检查是否正确记录了学习数据，数据统计基于您的输入。")
        
        st.write("**Q: 如何获得更好的学习建议？**")
        st.write("A: 提供更详细的学习数据，系统会生成更精准的建议。")
    
    # 技术问题
    with st.expander("❓ 技术问题", expanded=True):
        st.write("**Q: 页面加载缓慢怎么办？**")
        st.write("A: 请检查网络连接，或尝试刷新页面。如果问题持续，请联系技术支持。")
        
        st.write("**Q: 图表显示异常怎么办？**")
        st.write("A: 尝试刷新页面或清除浏览器缓存。建议使用Chrome或Edge浏览器。")
        
        st.write("**Q: 无法保存数据怎么办？**")
        st.write("A: 检查网络连接，确保填写了必要信息。如果问题持续，请联系技术支持。")
        
        st.write("**Q: 系统支持哪些浏览器？**")
        st.write("A: 建议使用Chrome、Edge、Firefox等现代浏览器，不支持IE浏览器。")

def render_contact():
    """联系我们"""
    st.subheader("📞 联系我们")
    
    st.write("**如果您在使用过程中遇到问题，或有任何建议和反馈，欢迎联系我们！**")
    
    # 联系方式
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📧 邮箱联系**")
        st.write("技术支持: support@example.com")
        st.write("功能建议: feedback@example.com")
        st.write("商务合作: business@example.com")
        
        st.write("**📱 在线客服**")
        st.write("工作时间: 周一至周五 9:00-18:00")
        st.write("响应时间: 24小时内回复")
    
    with col2:
        st.write("**🏢 公司信息**")
        st.write("公司名称: 大创智慧学习科技有限公司")
        st.write("地址: 北京市海淀区中关村大街1号")
        st.write("电话: 400-123-4567")
        
        st.write("**🌐 官方网站**")
        st.write("官网: www.example.com")
        st.write("论坛: forum.example.com")
    
    # 反馈表单
    st.subheader("📝 在线反馈")
    
    feedback_type = st.selectbox(
        "反馈类型",
        ["功能建议", "问题报告", "使用咨询", "其他"],
        index=0
    )
    
    feedback_title = st.text_input(
        "反馈标题",
        placeholder="请简要描述您的反馈..."
    )
    
    feedback_content = st.text_area(
        "反馈内容",
        placeholder="请详细描述您的反馈内容...",
        height=150
    )
    
    contact_info = st.text_input(
        "联系方式（可选）",
        placeholder="邮箱或电话，方便我们回复您..."
    )
    
    if st.button("📤 提交反馈", type="primary"):
        if feedback_title.strip() and feedback_content.strip():
            st.success("感谢您的反馈！我们会在24小时内回复您。")
        else:
            st.warning("请填写反馈标题和内容！")
    
    # 常见问题快速入口
    st.subheader("🔗 快速入口")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 查看使用指南"):
            st.info("请查看'使用指南'选项卡获取详细使用说明。")
    
    with col2:
        if st.button("🔧 常见问题"):
            st.info("请查看'常见问题'选项卡获取问题解答。")
    
    with col3:
        if st.button("📚 更新日志"):
            st.info("请查看'更新日志'选项卡了解系统更新情况。")

def render_changelog():
    """更新日志"""
    st.subheader("📚 更新日志")
    
    st.write("**了解系统的最新更新和改进内容**")
    
    # 最新版本
    with st.expander("🚀 最新版本 v2.0.0 (2024-01-15)", expanded=True):
        st.write("**✨ 新功能**")
        st.write("- 全新的模块化架构，提升系统性能")
        st.write("- 增强的AI助手功能，支持更多学习场景")
        st.write("- 新增学习行为分析模块")
        st.write("- 新增学习诊断中心")
        st.write("- 新增学习追踪器")
        st.write("- 优化学习路径规划算法")
        
        st.write("**🔧 功能改进**")
        st.write("- 重新设计用户界面，提升用户体验")
        st.write("- 优化数据可视化图表，支持更多图表类型")
        st.write("- 改进数据统计算法，提高准确性")
        st.write("- 增强数据导出功能")
        
        st.write("**🐛 问题修复**")
        st.write("- 修复了数据保存偶尔失败的问题")
        st.write("- 修复了图表在某些浏览器显示异常的问题")
        st.write("- 修复了移动端适配问题")
        st.write("- 修复了数据同步问题")
    
    # 历史版本
    with st.expander("📋 历史版本", expanded=True):
        st.write("**v1.5.0 (2023-12-01)**")
        st.write("- 新增学习空间推荐功能")
        st.write("- 优化数据分析模块")
        st.write("- 修复已知问题")
        
        st.write("**v1.4.0 (2023-10-15)**")
        st.write("- 新增AI助手功能")
        st.write("- 改进学习路径规划")
        st.write("- 优化用户界面")
        
        st.write("**v1.3.0 (2023-08-01)**")
        st.write("- 新增学习行为分析")
        st.write("- 优化数据统计功能")
        st.write("- 修复性能问题")
        
        st.write("**v1.2.0 (2023-06-15)**")
        st.write("- 新增学习诊断功能")
        st.write("- 改进数据可视化")
        st.write("- 优化用户体验")
        
        st.write("**v1.1.0 (2023-04-01)**")
        st.write("- 新增学习追踪器")
        st.write("- 优化仪表板功能")
        st.write("- 修复已知问题")
        
        st.write("**v1.0.0 (2023-01-01)**")
        st.write("- 系统正式发布")
        st.write("- 基础功能完整")
        st.write("- 支持用户注册和登录")
    
    # 即将推出
    with st.expander("🔮 即将推出", expanded=True):
        st.write("**v2.1.0 (预计2024-03-01)**")
        st.write("- 移动端APP开发")
        st.write("- 社交学习功能")
        st.write("- 更多AI模型支持")
        st.write("- 离线学习模式")
        
        st.write("**v2.2.0 (预计2024-06-01)**")
        st.write("- 多语言支持")
        st.write("- 高级数据分析")
        st.write("- 学习游戏化")
        st.write("- 智能推荐系统")
        
        st.write("**v3.0.0 (预计2024-12-01)**")
        st.write("- 完全重构架构")
        st.write("- 云端数据同步")
        st.write("- 多平台支持")
        st.write("- 企业级功能")
    
    # 反馈渠道
    st.subheader("💬 版本反馈")
    
    st.write("**如果您对新版本有任何建议或发现问题，欢迎反馈！**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐛 报告问题"):
            st.info("请使用'联系我们'选项卡中的反馈表单报告问题。")
    
    with col2:
        if st.button("💡 功能建议"):
            st.info("请使用'联系我们'选项卡中的反馈表单提出功能建议。")
