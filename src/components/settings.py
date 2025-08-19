import streamlit as st

def render_settings():
    """渲染设置页面"""
    st.title("⚙️ 系统设置")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 个人设置", 
        "🎨 界面设置", 
        "🔒 安全设置", 
        "📊 数据设置"
    ])
    
    with tab1:
        render_personal_settings()
    
    with tab2:
        render_interface_settings()
    
    with tab3:
        render_security_settings()
    
    with tab4:
        render_data_settings()

def render_personal_settings():
    """个人设置"""
    st.subheader("👤 个人设置")
    
    # 基本信息
    st.write("**基本信息**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("用户名", value="user123")
        email = st.text_input("邮箱地址", value="user@example.com")
        full_name = st.text_input("真实姓名", value="张三")
    
    with col2:
        age = st.number_input("年龄", min_value=10, max_value=100, value=20)
        education_level = st.selectbox("教育水平", ["小学", "初中", "高中", "大学", "研究生", "博士", "其他"])
        major = st.text_input("专业/学科", value="计算机科学")
    
    # 学习偏好
    st.write("**学习偏好**")
    
    learning_goals = st.text_area("学习目标", value="提升专业技能", height=100)
    preferred_subjects = st.multiselect("偏好科目", ["数学", "物理", "化学", "生物", "语文", "英语", "计算机"], default=["数学", "物理", "计算机"])
    daily_study_time = st.selectbox("每日学习时间", ["1小时以下", "1-2小时", "2-4小时", "4-6小时", "6小时以上"])
    notification_enabled = st.checkbox("启用学习提醒", value=True)
    
    # 保存设置
    if st.button("💾 保存个人设置", type="primary"):
        st.success("个人设置已保存！")

def render_interface_settings():
    """界面设置"""
    st.subheader("🎨 界面设置")
    
    # 主题和外观
    st.write("**主题和外观**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox("主题模式", ["浅色", "深色", "自动"])
        font_size = st.selectbox("字体大小", ["小", "中等", "大", "超大"])
        color_scheme = st.selectbox("配色方案", ["默认", "蓝色", "绿色", "紫色", "橙色"])
    
    with col2:
        language = st.selectbox("界面语言", ["中文", "English", "日本語", "한국어"])
        sidebar_collapsed = st.checkbox("默认收起侧边栏", value=False)
        show_animations = st.checkbox("显示动画效果", value=True)
    
    # 功能设置
    st.write("**功能设置**")
    
    compact_mode = st.checkbox("紧凑模式", value=False)
    auto_refresh = st.checkbox("自动刷新", value=True)
    
    if auto_refresh:
        refresh_interval = st.number_input("刷新间隔（秒）", min_value=10, max_value=300, value=30, step=10)
    
    # 保存设置
    if st.button("💾 保存界面设置", type="primary"):
        st.success("界面设置已保存！")

def render_security_settings():
    """安全设置"""
    st.subheader("🔒 安全设置")
    
    # 密码设置
    st.write("**密码设置**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_password = st.text_input("当前密码", type="password")
        new_password = st.text_input("新密码", type="password")
    
    with col2:
        confirm_password = st.text_input("确认新密码", type="password")
        password_strength = st.selectbox("密码强度要求", ["弱", "中等", "强", "极强"])
    
    # 安全选项
    st.write("**安全选项**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        two_factor_enabled = st.checkbox("启用双因素认证", value=False)
        login_notifications = st.checkbox("登录通知", value=True)
        auto_logout = st.checkbox("自动登出", value=True)
    
    with col2:
        session_timeout = st.number_input("会话超时时间（分钟）", min_value=5, max_value=120, value=30)
        max_login_attempts = st.number_input("最大登录尝试次数", min_value=3, max_value=10, value=5)
        data_encryption = st.checkbox("数据加密", value=True)
    
    # 保存设置
    if st.button("💾 保存安全设置", type="primary"):
        st.success("安全设置已保存！")

def render_data_settings():
    """数据设置"""
    st.subheader("📊 数据设置")
    
    # 数据保留
    st.write("**数据保留设置**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_retention_days = st.number_input("数据保留天数", min_value=30, max_value=3650, value=365)
        auto_backup = st.checkbox("自动备份", value=True)
    
    with col2:
        if auto_backup:
            backup_frequency = st.selectbox("备份频率", ["每天", "每周", "每月"])
        export_format = st.selectbox("导出格式", ["Excel", "CSV", "JSON", "PDF"])
    
    # 数据隐私
    st.write("**数据隐私设置**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_anonymization = st.checkbox("数据匿名化", value=False)
        usage_analytics = st.checkbox("使用分析", value=True)
    
    with col2:
        data_sync = st.checkbox("数据同步", value=True)
        storage_optimization = st.checkbox("存储优化", value=True)
    
    # 数据操作
    st.write("**数据操作**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 导入数据"):
            st.info("数据导入功能开发中...")
    
    with col2:
        if st.button("📤 导出数据"):
            st.info("数据导出功能开发中...")
    
    with col3:
        if st.button("🗑️ 清除数据"):
            st.warning("此操作将清除所有学习数据，无法恢复！")
    
    # 保存设置
    if st.button("💾 保存数据设置", type="primary"):
        st.success("数据设置已保存！")
    
    # 数据统计
    st.subheader("📈 数据统计")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("学习记录", "156条")
    
    with col2:
        st.metric("学习时长", "89.5小时")
    
    with col3:
        st.metric("存储空间", "2.3MB")
    
    with col4:
        st.metric("最后备份", "2天前")
