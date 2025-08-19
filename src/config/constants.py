"""
系统常量定义
"""

# 国际化支持
LANGUAGES = {
    "中文": {
        "title": "5A智慧学习空间数据大屏",
        "login": "登录",
        "username": "用户名",
        "password": "密码",
        "logout": "注销",
        "register": "注册",
        "reset_password": "重置密码",
        "dashboard": "数据大屏",
        "data_analysis": "数据分析",
        "settings": "设置"
    },
    "English": {
        "title": "5A Smart Learning Space Dashboard",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "logout": "Logout",
        "register": "Register",
        "reset_password": "Reset Password",
        "dashboard": "Dashboard",
        "data_analysis": "Analysis",
        "settings": "Settings"
    }
}

# 文本映射
TEXT_MAP = {
    "title": {
        "en": "5A Smart Learning Space Dashboard",
        "zh": "5A智慧学习交互系统数据大屏"
    },
    "dashboard": {
        "en": "Data Dashboard",
        "zh": "数据大屏"
    },
    "analysis": {
        "en": "Data Analysis",
        "zh": "数据分析"
    },
    "ai_assistant": {
        "en": "AI Assistant",
        "zh": "AI助手"
    },
    "learning_space": {
        "en": "Learning Space Recommendation",
        "zh": "学习空间推荐"
    },
    "learning_path": {
        "en": "Learning Path Planning",
        "zh": "学习路径规划"
    },
    "learning_behavior": {
        "en": "Learning Behavior Analysis",
        "zh": "学习行为分析"
    },
    "learning_diagnosis": {
        "en": "Learning Diagnosis",
        "zh": "学习诊断"
    },
    "learning_tracker": {
        "en": "Learning Records",
        "zh": "学习记录"
    },
    "help": {
        "en": "Help Center",
        "zh": "帮助中心"
    },
    "settings": {
        "en": "Settings",
        "zh": "设置"
    },
    "logout": {
        "en": "Logout",
        "zh": "注销"
    }
}

# 主题配置
THEMES = {
    "Default": {
        "primary_color": "#1E88E5",
        "background_color": "#FFFFFF",
        "secondary_background_color": "#F0F2F6",
        "text_color": "#262730"
    },
    "Dark": {
        "primary_color": "#FF6B6B",
        "background_color": "#0E1117",
        "secondary_background_color": "#262730",
        "text_color": "#FAFAFA"
    }
}

# 数据可视化配置
CHART_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

# 系统状态常量
SYSTEM_STATUS = {
    "ONLINE": "在线",
    "OFFLINE": "离线",
    "MAINTENANCE": "维护中",
    "ERROR": "错误"
}

# 学习空间类型
SPACE_TYPES = {
    "PHYSICAL": "物理空间",
    "VIRTUAL": "虚拟空间",
    "UBIQUITOUS": "泛在空间"
}

# API状态码
API_STATUS = {
    200: "成功",
    400: "请求错误",
    401: "未授权",
    403: "禁止访问",
    404: "未找到",
    500: "服务器错误"
}

# 数据导出格式
EXPORT_FORMATS = ["CSV", "JSON", "PDF", "Excel"]

# 默认用户配置
DEFAULT_USERS = {
    "admin": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
    "user": "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",   # user123
    "demo": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"    # hello
}
