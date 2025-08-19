"""
5A智慧学习空间系统 - 统一应用入口
"""

import streamlit as st
import asyncio
from datetime import datetime
import random

# 导入页面组件
from src.components.dashboard import render_dashboard
from src.components.analysis import render_analysis
from src.components.ai_assistant import render_ai_assistant
from src.components.learning_space import render_learning_space
from src.components.learning_path import render_learning_path
from src.components.learning_behavior import render_learning_behavior
from src.components.learning_diagnosis import render_learning_diagnosis
from src.components.learning_tracker import render_learning_tracker
from src.components.settings import render_settings
from src.components.help_page import render_help_page

# 导入认证组件（仅用于忘记密码页面）
from src.components.auth_forms import render_forgot_password

# 导入侧边栏组件
from src.components.sidebar import render_sidebar

# 导入其他模块
from src.auth.auth_manager import AuthManager
from src.auth.session_manager import SessionManager
from src.ai.ai_manager import AIManager
from src.data.data_simulator import DataSimulator
from src.utils.helpers import log_user_activity
from src.utils.decorators import login_required, performance_monitor
from src.utils.i18n import get_text, set_language
from src.config.settings import get_settings

# 初始化会话状态（在页面配置前）
if "app_state" not in st.session_state:
    st.session_state.app_state = "welcome"  # welcome, main_app

# 初始化登录相关状态（仅在首次访问时）
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "show_forgot_password" not in st.session_state:
    st.session_state.show_forgot_password = False

# 根据应用状态决定侧边栏状态
sidebar_state = "collapsed" if st.session_state.app_state == "welcome" else "expanded"

# 页面配置
st.set_page_config(
    page_title="5A智慧学习空间",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state=sidebar_state
)

# 初始化其他会话状态
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "email" not in st.session_state:
    st.session_state.email = None



# 初始化管理器
@st.cache_resource
def get_managers():
    """获取各种管理器实例"""
    return {
        "auth_manager": AuthManager(),
        "session_manager": SessionManager(),
        "ai_manager": AIManager(),
        "data_simulator": DataSimulator()
    }

managers = get_managers()

def render_welcome_app():
    """渲染欢迎应用页面"""
    # 强制隐藏侧边栏和头部，重置所有样式
    st.markdown("""
    <style>
        /* 强制隐藏所有Streamlit默认元素 */
        section[data-testid="stSidebar"] {display: none !important;}
        .css-1rs6os {display: none !important;}
        .css-17ziqus {display: none !important;}
        header[data-testid="stHeader"] {display: none !important;}
        .css-1d391kg {display: none !important;}
        
        /* 重置主容器 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        /* 强制重置页面背景 */
        .stApp {
            background: #f5f7fa !important;
        }
        
        /* 移除所有默认间距 */
        .main {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        div[data-testid="stVerticalBlock"] > div {
            margin: 0 !important;
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 检查是否已登录，如果已登录则切换到主应用
    if st.session_state.user_logged_in:
        st.session_state.app_state = "main_app"
        st.rerun()
    
    # 显示相应的页面
    if st.session_state.show_login:
        render_login_page()
    elif st.session_state.show_register:
        render_register_page()
    elif st.session_state.show_forgot_password:
        render_forgot_password_page()
    else:
        render_welcome_landing_page()

def render_welcome_landing_page():
    """渲染简洁专业的欢迎着陆页"""
    
    # 使用简单的Streamlit组件创建美观的页面
    st.markdown("""
    <style>
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        .stApp {
            background: #f0f2f6 !important;
        }
        .main {
            padding: 0 !important;
            margin: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用列布局创建居中效果
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 创建白色卡片容器
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border-top: 4px solid #1E88E5;
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
        # 标题
        st.markdown("## 🎓 5A智慧学习空间")
        st.markdown("### AI驱动的个性化学习生态系统")
        st.markdown("开启您的智慧学习之旅")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 功能列表
        with st.container():
            st.markdown("### 🎯 核心功能")
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("🤖 **AI智能助手**")
                st.markdown("24/7智能问答指导")
                
                st.markdown("📊 **智能分析**")
                st.markdown("深度学习行为分析")
            
            with col_b:
                st.markdown("🎯 **路径规划**")
                st.markdown("AI推荐个性化学习路径")
                
                st.markdown("📈 **效果提升**")
                st.markdown("实时评估优化学习效果")
        
        # 操作按钮
        st.markdown("---")
        
        if st.button("🔑 立即登录", key="welcome_login_btn", use_container_width=True):
            st.session_state.show_login = True
            st.session_state.show_register = False
            st.session_state.show_forgot_password = False
            st.session_state.app_state = "welcome"
            st.rerun()
        
        if st.button("📝 免费注册", key="welcome_register_btn", use_container_width=True):
            st.session_state.show_register = True
            st.session_state.show_login = False
            st.session_state.show_forgot_password = False
            st.session_state.app_state = "welcome"
            st.rerun()
        
        # 底部信息
        st.markdown("---")
        st.markdown("*© 2024 5A智慧学习空间 | 让学习更智能，让成长更高效*")

def render_login_page():
    """渲染统一风格的登录页面"""
    
    # 设置页面样式 - 统一浅色主题
    st.markdown("""
    <style>
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        .stApp {
            background: #f0f2f6 !important;
        }
        .main {
            padding: 0 !important;
            margin: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用列布局创建居中效果
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 创建白色卡片容器
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border-top: 4px solid #1E88E5;
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
        # 标题
        st.markdown("## 🔑 欢迎回来")
        st.markdown("### 登录您的5A智慧学习空间账户")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 初始化 AuthManager
    auth_manager = managers["auth_manager"]
    
    # 登录表单
    with st.form("modern_login_form", clear_on_submit=False):
        # 用户名输入
        username = st.text_input(
            "👤 用户名", 
            placeholder="请输入您的用户名",
            key="login_username_new"
        )
        
        # 密码输入
        password = st.text_input(
            "🔒 密码", 
            type="password", 
            placeholder="请输入您的密码",
            key="login_password_new"
        )
        
        # 登录按钮
        login_clicked = st.form_submit_button(
            "🚀 立即登录", 
            type="primary", 
            use_container_width=True
        )
        
        # 处理登录逻辑
        if login_clicked:
            if username and password:
                # 检查是否被锁定
                lockout_info = auth_manager.get_lockout_info(username)
                if lockout_info:
                    remaining_minutes = int(lockout_info["remaining_minutes"])
                    st.error(f"🔒 账户已被锁定，请在 {remaining_minutes} 分钟后重试！")
                elif auth_manager.verify_user(username, password):
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.session_state.email = f"{username}@example.com"
                    st.session_state.app_state = "main_app"
                    st.success("🎉 登录成功！正在跳转...")
                    st.rerun()
                else:
                    st.error("❌ 用户名或密码错误！")
            else:
                st.warning("⚠️ 请输入用户名和密码！")
    
    # 其他选项
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📝 注册账户", use_container_width=True):
            st.session_state.show_register = True
            st.session_state.show_login = False
            st.session_state.show_forgot_password = False
            st.rerun()
    
    with col_b:
        if st.button("← 返回首页", use_container_width=True):
            st.session_state.show_login = False
            st.session_state.show_register = False
            st.session_state.show_forgot_password = False
            st.rerun()
    
    # 快速登录提示
    st.info("💡 测试账户：admin/admin123、user/user123、demo/hello")

def render_register_page():
    """渲染统一风格的注册页面"""
    
    # 设置页面样式 - 统一浅色主题
    st.markdown("""
    <style>
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        .stApp {
            background: #f0f2f6 !important;
        }
        .main {
            padding: 0 !important;
            margin: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用列布局创建居中效果
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 创建白色卡片容器
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border-top: 4px solid #1E88E5;
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
        # 标题
        st.markdown("## 📝 加入我们")
        st.markdown("### 创建您的5A智慧学习空间账户")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
        # 注册表单
        with st.form("modern_register_form", clear_on_submit=False):
            # 基本信息
            username = st.text_input(
                "👤 用户名", 
                placeholder="请输入用户名（3-20个字符）",
                key="register_username_new"
            )
            
            email = st.text_input(
                "📧 邮箱地址", 
                placeholder="请输入邮箱地址",
                key="register_email_new"
            )
            
            # 密码设置
            password = st.text_input(
                "🔑 密码", 
                type="password", 
                placeholder="请输入密码（至少6位）",
                key="register_password_new"
            )
            
            confirm_password = st.text_input(
                "🔄 确认密码", 
                type="password", 
                placeholder="请再次输入密码",
                key="register_confirm_password_new"
            )
            
            # 协议同意
            agree_terms = st.checkbox(
                "✅ 我已阅读并同意《用户协议》和《隐私政策》",
                key="register_agree_terms"
            )
            
            # 注册按钮
            register_clicked = st.form_submit_button(
                "🚀 立即注册", 
                type="primary", 
                use_container_width=True
            )
        
        # 处理注册逻辑
        if register_clicked:
            # 初始化 AuthManager
            auth_manager = managers["auth_manager"]
            
            # 验证表单
            if not username or not email or not password or not confirm_password:
                st.error("❌ 请填写所有必填字段！")
            elif not agree_terms:
                st.error("❌ 请先同意用户协议和隐私政策！")
            elif password != confirm_password:
                st.error("❌ 两次输入的密码不一致！")
            elif len(password) < 6:
                st.error("❌ 密码长度至少需要6位！")
            else:
                # 调用真实的注册服务
                success, message = auth_manager.add_user(username, password)
                if success:
                    st.success(f"🎉 {message} 请使用新账户登录。")
                    st.session_state.show_register = False
                    st.session_state.show_login = True
                    st.session_state.show_forgot_password = False
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        # 其他选项
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔑 已有账户", use_container_width=True):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.session_state.show_forgot_password = False
                st.rerun()
        
        with col_b:
            if st.button("← 返回首页", use_container_width=True):
                st.session_state.show_login = False
                st.session_state.show_register = False
                st.session_state.show_forgot_password = False
                st.rerun()
        
        # 注册提示
        st.info("💡 注册后即可享受：AI智能学习助手、个性化学习路径、学习行为分析等高级功能")

def render_forgot_password_page():
    """渲染统一风格的忘记密码页面"""
    
    # 设置页面样式 - 统一浅色主题
    st.markdown("""
    <style>
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        .stApp {
            background: #f0f2f6 !important;
        }
        .main {
            padding: 0 !important;
            margin: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用列布局创建居中效果
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 创建白色卡片容器
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border-top: 4px solid #1E88E5;
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
        # 标题
        st.markdown("## 🔐 重置密码")
        st.markdown("### 我们将向您的邮箱发送重置链接")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 重置密码表单
        with st.form("modern_forgot_password_form", clear_on_submit=False):
            email = st.text_input(
                "📧 邮箱地址", 
                placeholder="请输入注册时使用的邮箱地址",
                key="forgot_password_email_new"
            )
            
            submit_button = st.form_submit_button(
                "📧 发送重置链接", 
                type="primary", 
                use_container_width=True
            )
            
            if submit_button:
                if email:
                    if "@" in email and "." in email:
                        st.success("🎉 重置链接已发送到您的邮箱，请查收！")
                        st.info("💡 如果没有收到邮件，请检查垃圾邮件文件夹")
                    else:
                        st.warning("⚠️ 请输入有效的邮箱地址！")
                else:
                    st.warning("⚠️ 请输入邮箱地址！")
        
        # 其他选项
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔙 返回登录", use_container_width=True):
                st.session_state.show_forgot_password = False
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
            
        with col_b:
            if st.button("← 返回首页", use_container_width=True):
                st.session_state.show_login = False
                st.session_state.show_register = False
                st.session_state.show_forgot_password = False
                st.rerun()
        
        # 安全提示
        st.info("🔒 安全提示：重置链接有效期为24小时，请及时处理")

def render_main_app():
    """渲染主应用"""
    # 显示侧边栏
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: block !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 显示欢迎信息
    if st.session_state.get('username'):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%); 
                    padding: 1rem 2rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
            <h3 style="margin: 0;">👋 欢迎回来，{st.session_state.username}！</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">享受您的智慧学习之旅</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 渲染侧边栏
    render_sidebar()
    
    # 根据当前页面渲染相应内容
    current_page = st.session_state.current_page
    
    if current_page == "dashboard":
        render_dashboard()
    elif current_page == "analysis":
        render_analysis()
    elif current_page == "ai_assistant":
        render_ai_assistant()
    elif current_page == "learning_space":
        render_learning_space()
    elif current_page == "learning_path":
        render_learning_path()
    elif current_page == "learning_behavior":
        render_learning_behavior()
    elif current_page == "learning_diagnosis":
        render_learning_diagnosis()
    elif current_page == "learning_tracker":
        render_learning_tracker()
    elif current_page == "settings":
        render_settings()
    elif current_page == "help":
        render_help_page()
    else:
        # 默认显示仪表板
        render_dashboard()
    
    # 记录用户活动
    if st.session_state.get('username'):
        log_user_activity(
            username=st.session_state.username,
            action=f"访问页面: {current_page}",
            timestamp=datetime.now()
        )

def main():
    """主应用函数"""
    # 根据应用状态渲染不同的页面
    if st.session_state.app_state == "welcome":
        render_welcome_app()
    elif st.session_state.app_state == "main_app":
        render_main_app()
    else:
        # 默认状态
        st.session_state.app_state = "welcome"
        render_welcome_app()

if __name__ == "__main__":
    main()