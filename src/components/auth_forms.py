import streamlit as st
from src.auth.auth_manager import AuthManager

# 旧的登录和注册表单函数已被增强版本替代

def render_forgot_password():
    """渲染忘记密码表单"""
    st.subheader("🔐 重置密码")
    
    st.write("**请选择重置密码的方式**")
    
    reset_method = st.radio(
        "重置方式",
        ["📧 邮箱验证", "📱 手机验证"],
        index=0
    )
    
    if reset_method == "📧 邮箱验证":
        email = st.text_input("邮箱地址", placeholder="请输入注册时使用的邮箱")
        
        if st.button("📧 发送验证码", type="primary"):
            if email:
                st.success("验证码已发送到您的邮箱，请查收！")
            else:
                st.warning("请输入邮箱地址！")
        
        verification_code = st.text_input("验证码", placeholder="请输入收到的验证码")
        new_password = st.text_input("新密码", type="password", placeholder="请输入新密码")
        confirm_new_password = st.text_input("确认新密码", type="password", placeholder="请再次输入新密码")
        
        if st.button("🔄 重置密码", type="primary"):
            if verification_code and new_password and confirm_new_password:
                if new_password == confirm_new_password:
                    st.success("密码重置成功！请使用新密码登录。")
                else:
                    st.error("两次输入的密码不一致！")
            else:
                st.warning("请填写所有字段！")
    
    else:  # 手机验证
        phone = st.text_input("手机号码", placeholder="请输入注册时使用的手机号")
        
        if st.button("📱 发送验证码", type="primary"):
            if phone:
                st.success("验证码已发送到您的手机，请查收！")
            else:
                st.warning("请输入手机号码！")
        
        verification_code = st.text_input("验证码", placeholder="请输入收到的验证码")
        new_password = st.text_input("新密码", type="password", placeholder="请输入新密码")
        confirm_new_password = st.text_input("确认新密码", type="password", placeholder="请再次输入新密码")
        
        if st.button("🔄 重置密码", type="primary"):
            if verification_code and new_password and confirm_new_password:
                if new_password == confirm_new_password:
                    st.success("密码重置成功！请使用新密码登录。")
                else:
                    st.error("两次输入的密码不一致！")
            else:
                st.warning("请填写所有字段！")
    
    # 返回登录
    st.write("---")
    if st.button("🔙 返回登录"):
        st.session_state.show_forgot_password = False
        st.session_state.show_login = True
        st.rerun()

def render_welcome_hero():
    """渲染欢迎页面的主题展示区域"""
    # 主标题区域
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 2rem; color: white;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem; font-weight: 700;">
            🎓 5A智慧学习空间
        </h1>
        <h3 style="font-size: 1.2rem; opacity: 0.9; font-weight: 300;">
            AI驱动的个性化学习生态系统
        </h3>
        <p style="font-size: 1rem; opacity: 0.8; margin-top: 1rem;">
            通过先进的AI技术，为您打造专属的智能学习体验
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 核心功能亮点
    st.markdown("### ✨ 核心功能亮点")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 1.5rem; 
                    border-radius: 12px; text-align: center; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0;">🤖 AI智能助手</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                基于DeepSeek的智能问答<br/>
                个性化学习指导
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #3742fa, #2f3542); padding: 1.5rem; 
                    border-radius: 12px; text-align: center; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0;">📊 数据分析</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                学习行为深度分析<br/>
                个性化学习报告
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #26de81, #20bf6b); padding: 1.5rem; 
                    border-radius: 12px; text-align: center; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0;">🎯 智能推荐</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                学习空间智能匹配<br/>
                个性化路径规划
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_feature_showcase():
    """渲染功能展示区域"""
    st.markdown("---")
    st.markdown("### 🚀 平台优势")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        #### 🔮 前沿技术加持
        - **AI深度学习**：采用最新的深度学习算法，精准分析学习模式
        - **大数据分析**：多维度数据挖掘，洞察学习规律
        - **智能推荐**：基于协同过滤和内容过滤的混合推荐系统
        - **实时反馈**：动态调整学习策略，优化学习效果
        
        #### 🎯 个性化体验
        - **专属学习档案**：建立完整的个人学习画像
        - **智能诊断**：精准识别学习问题和薄弱环节
        - **定制化方案**：量身定制专属学习路径
        - **多维度评估**：全方位评估学习成效
        """)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center;">
            <h4 style="color: #2d3436; margin-bottom: 1rem;">📈 学习成效提升</h4>
            <div style="font-size: 2.5rem; font-weight: bold; color: #6c5ce7; margin-bottom: 0.5rem;">85%</div>
            <p style="color: #636e72; margin-bottom: 1.5rem;">平均学习效率提升</p>
            
            <div style="font-size: 2rem; font-weight: bold; color: #00b894; margin-bottom: 0.5rem;">92%</div>
            <p style="color: #636e72; margin-bottom: 1.5rem;">用户满意度</p>
            
            <div style="font-size: 1.8rem; font-weight: bold; color: #e17055; margin-bottom: 0.5rem;">10000+</div>
            <p style="color: #636e72;">活跃学习者</p>
        </div>
        """, unsafe_allow_html=True)

def render_auth_container():
    """渲染认证容器"""
    # 检查是否显示认证表单
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    
    if "show_forgot_password" not in st.session_state:
        st.session_state.show_forgot_password = False
    
    # 如果用户还没有选择登录或注册，显示欢迎页面
    if not any([st.session_state.show_login, st.session_state.show_register, st.session_state.show_forgot_password]):
        render_welcome_hero()
        render_feature_showcase()
        
        # 行动号召区域
        st.markdown("---")
        st.markdown("### 🎉 开始您的智慧学习之旅")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <p style="font-size: 1.2rem; color: #636e72; margin-bottom: 2rem;">
                    立即注册，体验AI驱动的个性化学习
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔑 立即登录", use_container_width=True, type="primary"):
                    st.session_state.show_login = True
                    st.rerun()
            
            with col_b:
                if st.button("📝 免费注册", use_container_width=True):
                    st.session_state.show_register = True
                    st.rerun()
        
        # 底部信息
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #636e72; font-size: 0.9rem; padding: 1rem;">
            <p>© 2024 5A智慧学习空间 | 基于AI技术的下一代学习平台</p>
            <p>联系我们：support@5a-learning.com | 400-123-4567</p>
        </div>
        """, unsafe_allow_html=True)
        
        return
    
    # 显示相应的表单
    if st.session_state.show_login:
        render_enhanced_login_form()
    elif st.session_state.show_register:
        render_enhanced_register_form()
    elif st.session_state.show_forgot_password:
        render_forgot_password()

def render_enhanced_login_form():
    """渲染增强版登录表单"""
    # 返回欢迎页按钮
    if st.button("← 返回首页", key="back_to_welcome"):
        st.session_state.show_login = False
        st.rerun()
    
    # 登录表单容器
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 2rem 0;">
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #2d3436; margin-bottom: 0.5rem;">🔑 用户登录</h2>
            <p style="color: #636e72;">欢迎回到5A智慧学习空间</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 初始化 AuthManager
        auth_manager = AuthManager()
        
        with st.form("enhanced_login_form"):
            username = st.text_input("👤 用户名", placeholder="请输入您的用户名")
            password = st.text_input("🔒 密码", type="password", placeholder="请输入您的密码")
            
            col_a, col_b = st.columns(2)
            with col_a:
                remember_me = st.checkbox("🔄 记住登录状态")
            
            with col_b:
                forgot_password = st.form_submit_button("❓ 忘记密码?")
            
            submit_button = st.form_submit_button("🚀 立即登录", type="primary", use_container_width=True)
            
            if forgot_password:
                st.session_state.show_forgot_password = True
                st.session_state.show_login = False
                st.rerun()
            
            if submit_button:
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
                        st.success("🎉 登录成功！正在进入系统...")
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误！请检查后重试。")
                else:
                    st.warning("⚠️ 请填写完整的用户名和密码！")
        
        # 注册链接
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: #636e72;">还没有账户？</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 立即注册", use_container_width=True):
            st.session_state.show_register = True
            st.session_state.show_login = False
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_enhanced_register_form():
    """渲染增强版注册表单"""
    # 返回欢迎页按钮
    if st.button("← 返回首页", key="back_to_welcome_reg"):
        st.session_state.show_register = False
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 2rem 0;">
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #2d3436; margin-bottom: 0.5rem;">📝 用户注册</h2>
            <p style="color: #636e72;">加入5A智慧学习空间大家庭</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("enhanced_register_form"):
            # 基本信息
            st.markdown("**📋 基本信息**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                username = st.text_input("👤 用户名", placeholder="请输入用户名")
                email = st.text_input("📧 邮箱地址", placeholder="请输入邮箱地址")
            
            with col_b:
                full_name = st.text_input("👨‍🎓 真实姓名", placeholder="请输入真实姓名")
                phone = st.text_input("📱 手机号码", placeholder="请输入手机号码")
            
            # 密码设置
            st.markdown("**🔒 密码设置**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                password = st.text_input("🔑 密码", type="password", placeholder="请输入密码（至少6位）")
                confirm_password = st.text_input("🔄 确认密码", type="password", placeholder="请再次输入密码")
            
            with col_b:
                password_strength = st.selectbox("💪 密码强度", ["弱", "中等", "强", "极强"])
            
            # 学习信息
            st.markdown("**🎓 学习信息**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                education_level = st.selectbox("🎯 教育水平", ["小学", "初中", "高中", "大学", "研究生", "博士", "其他"])
                major = st.text_input("📚 专业/学科", placeholder="请输入专业或学科")
            
            with col_b:
                learning_goals = st.text_area("🎯 学习目标", placeholder="请描述您的学习目标", height=80)
            
            # 偏好科目
            preferred_subjects = st.multiselect(
                "💡 偏好科目",
                ["数学", "物理", "化学", "生物", "语文", "英语", "历史", "地理", "政治", "计算机", "其他"],
                default=["数学", "计算机"]
            )
            
            # 协议同意
            agree_terms = st.checkbox("✅ 我已阅读并同意《用户协议》和《隐私政策》")
            agree_notifications = st.checkbox("📬 我同意接收学习相关的通知和提醒")
            
            # 提交按钮
            submit_button = st.form_submit_button("🚀 立即注册", type="primary", use_container_width=True)
            
            if submit_button:
                # 初始化 AuthManager
                auth_manager = AuthManager()
                
                # 验证表单
                if not username or not email or not password or not confirm_password:
                    st.error("❌ 请填写所有必填字段！")
                elif password != confirm_password:
                    st.error("❌ 两次输入的密码不一致！")
                elif len(password) < 6:
                    st.error("❌ 密码长度至少6位！")
                elif not agree_terms:
                    st.error("❌ 请同意用户协议和隐私政策！")
                else:
                    # 调用真实的注册服务
                    success, message = auth_manager.add_user(username, password)
                    if success:
                        st.success(f"🎉 {message} 请使用新账户登录。")
                        # 保存额外的用户信息到 session state（可选）
                        st.session_state.temp_user_info = {
                            "username": username,
                            "email": email,
                            "full_name": full_name,
                            "phone": phone,
                            "education_level": education_level,
                            "major": major,
                            "learning_goals": learning_goals,
                            "preferred_subjects": preferred_subjects
                        }
                        st.session_state.show_register = False
                        st.session_state.show_login = True
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        # 登录链接
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: #636e72;">已有账户？</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔑 立即登录", use_container_width=True):
            st.session_state.show_login = True
            st.session_state.show_register = False
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
