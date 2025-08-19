"""
数据分析工具
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px


class DataAnalyzer:
    """数据分析器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scaler = StandardScaler()
    
    def analyze_space_usage(self, usage_data: pd.DataFrame) -> Dict[str, Any]:
        """分析空间使用情况"""
        try:
            analysis = {}
            
            # 基本统计
            analysis['basic_stats'] = {
                'total_records': len(usage_data),
                'date_range': {
                    'start': usage_data['date'].min().strftime('%Y-%m-%d'),
                    'end': usage_data['date'].max().strftime('%Y-%m-%d')
                },
                'unique_spaces': usage_data['space'].nunique(),
                'space_list': usage_data['space'].unique().tolist()
            }
            
            # 使用率统计
            analysis['usage_stats'] = {
                'avg_usage_rate': float(usage_data['usage_rate'].mean()),
                'peak_usage_rate': float(usage_data['usage_rate'].max()),
                'low_usage_rate': float(usage_data['usage_rate'].min()),
                'usage_variance': float(usage_data['usage_rate'].var())
            }
            
            # 按空间分析
            space_analysis = usage_data.groupby('space').agg({
                'usage_rate': ['mean', 'max', 'std'],
                'users': ['mean', 'max', 'sum']
            }).round(3)
            
            analysis['by_space'] = space_analysis.to_dict()
            
            # 时间模式分析
            hourly_pattern = usage_data.groupby('hour')['usage_rate'].mean()
            analysis['hourly_pattern'] = {
                'peak_hours': hourly_pattern.nlargest(3).index.tolist(),
                'low_hours': hourly_pattern.nsmallest(3).index.tolist(),
                'pattern_data': hourly_pattern.to_dict()
            }
            
            # 工作日vs周末
            weekday_weekend = usage_data.groupby('is_weekend')['usage_rate'].mean()
            analysis['weekday_vs_weekend'] = {
                'weekday_avg': float(weekday_weekend.get(False, 0)),
                'weekend_avg': float(weekday_weekend.get(True, 0)),
                'difference': float(weekday_weekend.get(False, 0) - weekday_weekend.get(True, 0))
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing space usage: {str(e)}")
            return {"error": str(e)}
    
    def analyze_learning_behavior(self, behavior_data: pd.DataFrame) -> Dict[str, Any]:
        """分析学习行为"""
        try:
            analysis = {}
            
            # 基本统计
            analysis['basic_stats'] = {
                'total_sessions': len(behavior_data),
                'unique_users': behavior_data['user_id'].nunique(),
                'avg_session_duration': float(behavior_data['duration_minutes'].mean()),
                'total_learning_time': float(behavior_data['duration_minutes'].sum())
            }
            
            # 学习模式分析
            user_patterns = behavior_data.groupby('user_id').agg({
                'duration_minutes': ['sum', 'mean', 'count'],
                'focus_level': 'mean',
                'satisfaction': 'mean'
            }).round(3)
            
            analysis['user_patterns'] = {
                'avg_total_time': float(user_patterns[('duration_minutes', 'sum')].mean()),
                'avg_session_length': float(user_patterns[('duration_minutes', 'mean')].mean()),
                'avg_sessions_per_user': float(user_patterns[('duration_minutes', 'count')].mean()),
                'avg_focus_level': float(user_patterns[('focus_level', 'mean')].mean()),
                'avg_satisfaction': float(user_patterns[('satisfaction', 'mean')].mean())
            }
            
            # 活动类型分析
            activity_analysis = behavior_data.groupby('activity_type').agg({
                'duration_minutes': ['mean', 'count'],
                'focus_level': 'mean',
                'satisfaction': 'mean'
            }).round(3)
            
            analysis['activity_analysis'] = activity_analysis.to_dict()
            
            # 时间分布分析
            behavior_data['hour'] = pd.to_datetime(behavior_data['start_time']).dt.hour
            hourly_distribution = behavior_data.groupby('hour').size()
            
            analysis['time_distribution'] = {
                'peak_learning_hours': hourly_distribution.nlargest(3).index.tolist(),
                'hourly_counts': hourly_distribution.to_dict()
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing learning behavior: {str(e)}")
            return {"error": str(e)}
    
    def cluster_users(self, user_data: pd.DataFrame, n_clusters: int = 4) -> Dict[str, Any]:
        """用户聚类分析"""
        try:
            # 准备特征数据
            features = ['total_time', 'avg_session_length', 'session_count', 'avg_focus', 'avg_satisfaction']
            
            if not all(feature in user_data.columns for feature in features):
                return {"error": "缺少必要的特征列"}
            
            # 数据标准化
            feature_data = user_data[features]
            scaled_data = self.scaler.fit_transform(feature_data)
            
            # K-means聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(scaled_data)
            
            # 添加聚类标签
            user_data_clustered = user_data.copy()
            user_data_clustered['cluster'] = clusters
            
            # 聚类统计
            cluster_stats = user_data_clustered.groupby('cluster').agg({
                'total_time': 'mean',
                'avg_session_length': 'mean',
                'session_count': 'mean',
                'avg_focus': 'mean',
                'avg_satisfaction': 'mean'
            }).round(3)
            
            # 聚类标签
            cluster_labels = self._generate_cluster_labels(cluster_stats)
            
            return {
                'cluster_count': n_clusters,
                'cluster_stats': cluster_stats.to_dict(),
                'cluster_labels': cluster_labels,
                'user_clusters': user_data_clustered[['user_id', 'cluster']].to_dict('records')
            }
            
        except Exception as e:
            self.logger.error(f"Error clustering users: {str(e)}")
            return {"error": str(e)}
    
    def predict_space_demand(self, usage_data: pd.DataFrame, forecast_days: int = 7) -> Dict[str, Any]:
        """预测空间需求"""
        try:
            predictions = {}
            
            for space in usage_data['space'].unique():
                space_data = usage_data[usage_data['space'] == space]
                
                # 按日期聚合
                daily_usage = space_data.groupby('date')['users'].sum().reset_index()
                daily_usage['date'] = pd.to_datetime(daily_usage['date'])
                daily_usage = daily_usage.sort_values('date')
                
                # 简单的移动平均预测
                window_size = min(7, len(daily_usage))
                if window_size > 0:
                    recent_avg = daily_usage['users'].tail(window_size).mean()
                    
                    # 考虑趋势
                    if len(daily_usage) >= 2:
                        trend = (daily_usage['users'].iloc[-1] - daily_usage['users'].iloc[0]) / len(daily_usage)
                    else:
                        trend = 0
                    
                    # 生成预测
                    future_dates = []
                    future_predictions = []
                    
                    last_date = daily_usage['date'].max()
                    for i in range(1, forecast_days + 1):
                        future_date = last_date + timedelta(days=i)
                        prediction = recent_avg + trend * i
                        prediction = max(0, prediction)  # 不能为负
                        
                        future_dates.append(future_date.strftime('%Y-%m-%d'))
                        future_predictions.append(float(prediction))
                    
                    predictions[space] = {
                        'future_dates': future_dates,
                        'predictions': future_predictions,
                        'avg_recent_usage': float(recent_avg),
                        'trend': float(trend)
                    }
            
            return predictions
            
        except Exception as e:
            self.logger.error(f"Error predicting space demand: {str(e)}")
            return {"error": str(e)}
    
    def analyze_performance_trends(self, performance_data: pd.DataFrame) -> Dict[str, Any]:
        """分析学习表现趋势"""
        try:
            analysis = {}
            
            # 整体趋势
            performance_data['date'] = pd.to_datetime(performance_data['date'])
            performance_data = performance_data.sort_values('date')
            
            # 按日期聚合
            daily_performance = performance_data.groupby('date').agg({
                'completion_rate': 'mean',
                'accuracy': 'mean',
                'learning_time': 'mean',
                'engagement_score': 'mean'
            }).round(3)
            
            # 计算趋势
            metrics = ['completion_rate', 'accuracy', 'learning_time', 'engagement_score']
            trends = {}
            
            for metric in metrics:
                if len(daily_performance) >= 2:
                    # 简单线性趋势
                    x = np.arange(len(daily_performance))
                    y = daily_performance[metric].values
                    
                    # 计算相关系数
                    correlation = np.corrcoef(x, y)[0, 1] if len(x) > 1 else 0
                    
                    # 计算变化率
                    if daily_performance[metric].iloc[0] != 0:
                        change_rate = (daily_performance[metric].iloc[-1] - daily_performance[metric].iloc[0]) / daily_performance[metric].iloc[0]
                    else:
                        change_rate = 0
                    
                    trends[metric] = {
                        'correlation': float(correlation),
                        'change_rate': float(change_rate),
                        'trend_direction': 'up' if correlation > 0.1 else 'down' if correlation < -0.1 else 'stable'
                    }
            
            analysis['trends'] = trends
            analysis['daily_performance'] = daily_performance.to_dict()
            
            # 用户表现分布
            user_performance = performance_data.groupby('user_id').agg({
                'completion_rate': 'mean',
                'accuracy': 'mean',
                'learning_time': 'sum',
                'engagement_score': 'mean'
            }).round(3)
            
            analysis['user_distribution'] = {
                'high_performers': int((user_performance['completion_rate'] > 0.8).sum()),
                'medium_performers': int(((user_performance['completion_rate'] >= 0.6) & 
                                       (user_performance['completion_rate'] <= 0.8)).sum()),
                'low_performers': int((user_performance['completion_rate'] < 0.6).sum())
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance trends: {str(e)}")
            return {"error": str(e)}
    
    def _generate_cluster_labels(self, cluster_stats: pd.DataFrame) -> Dict[int, str]:
        """生成聚类标签"""
        labels = {}
        
        for cluster_id in cluster_stats.index:
            stats = cluster_stats.loc[cluster_id]
            
            # 基于特征值生成标签
            if stats['total_time'] > cluster_stats['total_time'].mean() * 1.2:
                if stats['avg_focus'] > cluster_stats['avg_focus'].mean():
                    label = "高投入专注型"
                else:
                    label = "高投入普通型"
            elif stats['avg_session_length'] > cluster_stats['avg_session_length'].mean() * 1.2:
                label = "长时间学习型"
            elif stats['session_count'] > cluster_stats['session_count'].mean() * 1.2:
                label = "高频率学习型"
            elif stats['avg_satisfaction'] > cluster_stats['avg_satisfaction'].mean() * 1.1:
                label = "高满意度型"
            else:
                label = "均衡学习型"
            
            labels[cluster_id] = label
        
        return labels


class LearningAnalytics:
    """学习分析专用工具"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_learning_insights(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """生成学习洞察"""
        insights = {}
        
        try:
            # 空间使用洞察
            if 'usage_data' in data:
                usage_insights = self._analyze_space_usage_patterns(data['usage_data'])
                insights['space_usage'] = usage_insights
            
            # 学习行为洞察
            if 'behavior_data' in data:
                behavior_insights = self._analyze_learning_patterns(data['behavior_data'])
                insights['learning_behavior'] = behavior_insights
            
            # 表现洞察
            if 'performance_data' in data:
                performance_insights = self._analyze_performance_patterns(data['performance_data'])
                insights['performance'] = performance_insights
            
            # 综合建议
            recommendations = self._generate_recommendations(insights)
            insights['recommendations'] = recommendations
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating learning insights: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_space_usage_patterns(self, usage_data: pd.DataFrame) -> Dict[str, Any]:
        """分析空间使用模式"""
        patterns = {}
        
        # 高峰时段分析
        hourly_usage = usage_data.groupby('hour')['usage_rate'].mean()
        peak_hours = hourly_usage.nlargest(3).index.tolist()
        
        patterns['peak_patterns'] = {
            'peak_hours': peak_hours,
            'peak_description': self._describe_peak_hours(peak_hours)
        }
        
        # 空间偏好分析
        space_popularity = usage_data.groupby('space')['users'].sum().sort_values(ascending=False)
        patterns['space_preferences'] = {
            'most_popular': space_popularity.index[0] if len(space_popularity) > 0 else None,
            'least_popular': space_popularity.index[-1] if len(space_popularity) > 0 else None,
            'popularity_ranking': space_popularity.to_dict()
        }
        
        return patterns
    
    def _analyze_learning_patterns(self, behavior_data: pd.DataFrame) -> Dict[str, Any]:
        """分析学习模式"""
        patterns = {}
        
        # 学习时间模式
        behavior_data['hour'] = pd.to_datetime(behavior_data['start_time']).dt.hour
        learning_hours = behavior_data.groupby('hour').size()
        peak_learning_time = learning_hours.idxmax()
        
        patterns['time_patterns'] = {
            'peak_learning_hour': int(peak_learning_time),
            'learning_time_description': self._describe_learning_time(peak_learning_time)
        }
        
        # 专注度分析
        avg_focus = behavior_data['focus_level'].mean()
        patterns['focus_patterns'] = {
            'avg_focus_level': float(avg_focus),
            'focus_description': self._describe_focus_level(avg_focus)
        }
        
        return patterns
    
    def _analyze_performance_patterns(self, performance_data: pd.DataFrame) -> Dict[str, Any]:
        """分析表现模式"""
        patterns = {}
        
        # 完成率趋势
        performance_data['date'] = pd.to_datetime(performance_data['date'])
        recent_data = performance_data.tail(100)  # 最近数据
        
        completion_trend = recent_data['completion_rate'].rolling(window=10).mean()
        is_improving = completion_trend.iloc[-1] > completion_trend.iloc[0]
        
        patterns['performance_trends'] = {
            'is_improving': bool(is_improving),
            'avg_completion_rate': float(recent_data['completion_rate'].mean()),
            'trend_description': "学习表现呈上升趋势" if is_improving else "学习表现需要改进"
        }
        
        return patterns
    
    def _generate_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于空间使用模式的建议
        if 'space_usage' in insights:
            space_insights = insights['space_usage']
            if 'peak_patterns' in space_insights:
                peak_hours = space_insights['peak_patterns']['peak_hours']
                if 9 in peak_hours or 10 in peak_hours:
                    recommendations.append("建议在上午高峰期预约热门学习空间")
        
        # 基于学习行为的建议
        if 'learning_behavior' in insights:
            behavior_insights = insights['learning_behavior']
            if 'focus_patterns' in behavior_insights:
                avg_focus = behavior_insights['focus_patterns']['avg_focus_level']
                if avg_focus < 0.6:
                    recommendations.append("建议选择更安静的学习环境以提高专注度")
                elif avg_focus > 0.8:
                    recommendations.append("您的专注度很好，可以尝试更具挑战性的学习任务")
        
        # 基于表现的建议
        if 'performance' in insights:
            performance_insights = insights['performance']
            if 'performance_trends' in performance_insights:
                if not performance_insights['performance_trends']['is_improving']:
                    recommendations.append("建议调整学习方法或寻求额外的学习支持")
                else:
                    recommendations.append("学习表现良好，继续保持当前的学习策略")
        
        # 通用建议
        recommendations.append("定期回顾学习数据，持续优化学习策略")
        
        return recommendations
    
    def _describe_peak_hours(self, peak_hours: List[int]) -> str:
        """描述高峰时段"""
        if not peak_hours:
            return "无明显高峰时段"
        
        if all(hour < 12 for hour in peak_hours):
            return "主要集中在上午时段"
        elif all(hour >= 12 and hour < 18 for hour in peak_hours):
            return "主要集中在下午时段"
        elif all(hour >= 18 for hour in peak_hours):
            return "主要集中在晚上时段"
        else:
            return "分布在多个时段"
    
    def _describe_learning_time(self, peak_hour: int) -> str:
        """描述学习时间特征"""
        if 6 <= peak_hour <= 9:
            return "您是早鸟型学习者，适合在清晨学习"
        elif 10 <= peak_hour <= 12:
            return "您在上午学习效率最高"
        elif 13 <= peak_hour <= 17:
            return "您偏好在下午进行学习"
        elif 18 <= peak_hour <= 22:
            return "您习惯在晚上学习"
        else:
            return "您的学习时间比较特殊"
    
    def _describe_focus_level(self, avg_focus: float) -> str:
        """描述专注度水平"""
        if avg_focus >= 0.8:
            return "专注度很高，学习效率优秀"
        elif avg_focus >= 0.6:
            return "专注度良好，有进一步提升空间"
        elif avg_focus >= 0.4:
            return "专注度一般，建议优化学习环境"
        else:
            return "专注度较低，需要重点改进"
