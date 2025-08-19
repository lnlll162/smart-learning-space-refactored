import streamlit as st

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("🏠 大创智慧学习空间")
        
        # 用户信息
        st.write("---")
        st.write(f"👤 **{st.session_state.get('username', '用户')}**")
        st.write(f"📧 {st.session_state.get('email', 'user@example.com')}")
        
        # 用户状态和快捷操作
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚙️ 设置"):
                st.session_state.current_page = "settings"
                st.rerun()
        
        with col2:
            if st.button("🚪 退出"):
                st.session_state.user_logged_in = False
                st.session_state.username = None
                st.session_state.email = None
                st.session_state.app_state = "welcome"
                st.session_state.show_login = False
                st.session_state.show_register = False
                st.session_state.show_forgot_password = False
                st.rerun()
        
        st.write("---")
        
        # 导航菜单
        st.write("**📚 主要功能**")
        
        # 仪表板
        if st.sidebar.button("📊 仪表板", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        # 数据分析
        if st.sidebar.button("📈 数据分析", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()
        
        # AI助手
        if st.sidebar.button("🤖 AI助手", use_container_width=True):
            st.session_state.current_page = "ai_assistant"
            st.rerun()
        
        # 学习空间
        if st.sidebar.button("🏠 学习空间", use_container_width=True):
            st.session_state.current_page = "learning_space"
            st.rerun()
        
        # 学习路径
        if st.sidebar.button("🛤️ 学习路径", use_container_width=True):
            st.session_state.current_page = "learning_path"
            st.rerun()
        
        # 学习行为分析
        if st.sidebar.button("🔍 学习行为分析", use_container_width=True):
            st.session_state.current_page = "learning_behavior"
            st.rerun()
        
        # 学习诊断
        if st.sidebar.button("🔬 学习诊断", use_container_width=True):
            st.session_state.current_page = "learning_diagnosis"
            st.rerun()
        
        # 学习追踪器
        if st.sidebar.button("📊 学习追踪器", use_container_width=True):
            st.session_state.current_page = "learning_tracker"
            st.rerun()
        
        st.write("---")
        
        # 辅助功能
        st.write("**🔧 辅助功能**")
        
        # 设置
        if st.sidebar.button("⚙️ 设置", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        
        # 帮助
        if st.sidebar.button("❓ 帮助", use_container_width=True):
            st.session_state.current_page = "help"
            st.rerun()
        
        st.write("---")
        
        # 快速操作
        st.write("**⚡ 快速操作**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 记录学习", use_container_width=True):
                st.session_state.current_page = "learning_tracker"
                st.rerun()
        
        with col2:
            if st.button("🎯 设置目标", use_container_width=True):
                st.session_state.current_page = "learning_path"
                st.rerun()
        
        # 学习统计
        if st.sidebar.button("📊 查看统计", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.write("---")
        
        # 系统信息
        st.write("**ℹ️ 系统信息**")
        st.write("版本: v2.0.0")
        st.write("更新时间: 2024-01-15")
        
        # 在线状态
        st.write("🟢 系统在线")
        
        # 帮助链接
        st.write("---")
        st.write("**🔗 快速链接**")
        
        if st.button("📖 使用指南", use_container_width=True):
            st.session_state.current_page = "help"
            st.rerun()
        
        if st.button("🐛 报告问题", use_container_width=True):
            st.session_state.current_page = "help"
            st.rerun()
        
        if st.button("💡 功能建议", use_container_width=True):
            st.session_state.current_page = "help"
            st.rerun()
        
        # 底部信息
        st.write("---")
        st.write("© 2024 大创智慧学习空间")
        st.write("让学习更智能，让成长更高效")
