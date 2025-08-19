"""
数据存储管理
"""

import os
import json
import pandas as pd
import sqlite3
from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime
from contextlib import contextmanager

from ..config.settings import DatabaseConfig


class DataStorage:
    """数据存储管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.use_json = DatabaseConfig.USE_JSON_STORAGE
        self.data_dir = DatabaseConfig.DATA_DIR
        self.db_url = DatabaseConfig.DATABASE_URL
        
        # 确保数据目录存在
        if self.use_json:
            os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化数据库（如果使用数据库）
        if not self.use_json:
            self._init_database()
    
    def save_data(self, data: Union[Dict, pd.DataFrame], table_name: str, file_format: str = "json") -> bool:
        """保存数据"""
        try:
            if self.use_json:
                return self._save_to_file(data, table_name, file_format)
            else:
                return self._save_to_database(data, table_name)
        except Exception as e:
            self.logger.error(f"Error saving data to {table_name}: {str(e)}")
            return False
    
    def load_data(self, table_name: str, file_format: str = "json") -> Optional[Union[Dict, pd.DataFrame]]:
        """加载数据"""
        try:
            if self.use_json:
                return self._load_from_file(table_name, file_format)
            else:
                return self._load_from_database(table_name)
        except Exception as e:
            self.logger.error(f"Error loading data from {table_name}: {str(e)}")
            return None
    
    def delete_data(self, table_name: str, condition: Optional[Dict] = None) -> bool:
        """删除数据"""
        try:
            if self.use_json:
                return self._delete_from_file(table_name)
            else:
                return self._delete_from_database(table_name, condition)
        except Exception as e:
            self.logger.error(f"Error deleting data from {table_name}: {str(e)}")
            return False
    
    def query_data(self, table_name: str, filters: Optional[Dict] = None, limit: Optional[int] = None) -> Optional[pd.DataFrame]:
        """查询数据"""
        try:
            if self.use_json:
                data = self._load_from_file(table_name, "json")
                if data is None:
                    return None
                
                # 转换为DataFrame（如果需要）
                if isinstance(data, dict):
                    df = pd.DataFrame(data)
                else:
                    df = data
                
                # 应用过滤器
                if filters:
                    for column, value in filters.items():
                        if column in df.columns:
                            df = df[df[column] == value]
                
                # 应用限制
                if limit:
                    df = df.head(limit)
                
                return df
            else:
                return self._query_from_database(table_name, filters, limit)
        except Exception as e:
            self.logger.error(f"Error querying data from {table_name}: {str(e)}")
            return None
    
    def list_tables(self) -> List[str]:
        """列出所有表/文件"""
        try:
            if self.use_json:
                files = os.listdir(self.data_dir)
                tables = [f.split('.')[0] for f in files if f.endswith('.json') or f.endswith('.csv')]
                return tables
            else:
                return self._list_database_tables()
        except Exception as e:
            self.logger.error(f"Error listing tables: {str(e)}")
            return []
    
    def backup_data(self, backup_dir: str) -> bool:
        """备份数据"""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            if self.use_json:
                # 复制所有JSON和CSV文件
                import shutil
                for filename in os.listdir(self.data_dir):
                    if filename.endswith(('.json', '.csv')):
                        src = os.path.join(self.data_dir, filename)
                        dst = os.path.join(backup_dir, filename)
                        shutil.copy2(src, dst)
            else:
                # 导出数据库数据
                tables = self.list_tables()
                for table in tables:
                    data = self.load_data(table)
                    if data is not None:
                        backup_file = os.path.join(backup_dir, f"{table}.csv")
                        if isinstance(data, pd.DataFrame):
                            data.to_csv(backup_file, index=False)
                        else:
                            pd.DataFrame(data).to_csv(backup_file, index=False)
            
            self.logger.info(f"Data backup completed to {backup_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error backing up data: {str(e)}")
            return False
    
    def restore_data(self, backup_dir: str) -> bool:
        """恢复数据"""
        try:
            if not os.path.exists(backup_dir):
                self.logger.error(f"Backup directory {backup_dir} does not exist")
                return False
            
            for filename in os.listdir(backup_dir):
                if filename.endswith('.csv'):
                    table_name = filename.replace('.csv', '')
                    file_path = os.path.join(backup_dir, filename)
                    data = pd.read_csv(file_path)
                    self.save_data(data, table_name, "csv")
                elif filename.endswith('.json'):
                    table_name = filename.replace('.json', '')
                    file_path = os.path.join(backup_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.save_data(data, table_name, "json")
            
            self.logger.info(f"Data restore completed from {backup_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring data: {str(e)}")
            return False
    
    # JSON文件存储方法
    def _save_to_file(self, data: Union[Dict, pd.DataFrame], table_name: str, file_format: str) -> bool:
        """保存数据到文件"""
        filename = f"{table_name}.{file_format}"
        filepath = os.path.join(self.data_dir, filename)
        
        if file_format == "json":
            if isinstance(data, pd.DataFrame):
                data_dict = data.to_dict('records')
            else:
                data_dict = data
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=2, default=str)
        
        elif file_format == "csv":
            if isinstance(data, pd.DataFrame):
                data.to_csv(filepath, index=False, encoding='utf-8')
            else:
                pd.DataFrame(data).to_csv(filepath, index=False, encoding='utf-8')
        
        return True
    
    def _load_from_file(self, table_name: str, file_format: str) -> Optional[Union[Dict, pd.DataFrame]]:
        """从文件加载数据"""
        filename = f"{table_name}.{file_format}"
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        if file_format == "json":
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        elif file_format == "csv":
            return pd.read_csv(filepath, encoding='utf-8')
        
        return None
    
    def _delete_from_file(self, table_name: str) -> bool:
        """删除文件"""
        for ext in ['.json', '.csv']:
            filepath = os.path.join(self.data_dir, f"{table_name}{ext}")
            if os.path.exists(filepath):
                os.remove(filepath)
        return True
    
    # 数据库存储方法
    def _init_database(self):
        """初始化数据库"""
        if self.db_url.startswith('sqlite'):
            # SQLite数据库
            db_path = self.db_url.replace('sqlite:///', '')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 这里可以添加其他数据库的初始化逻辑
    
    @contextmanager
    def _get_db_connection(self):
        """获取数据库连接"""
        if self.db_url.startswith('sqlite'):
            db_path = self.db_url.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            try:
                yield conn
            finally:
                conn.close()
        else:
            # 可以添加其他数据库的连接逻辑
            raise NotImplementedError("Only SQLite is currently supported")
    
    def _save_to_database(self, data: Union[Dict, pd.DataFrame], table_name: str) -> bool:
        """保存数据到数据库"""
        try:
            with self._get_db_connection() as conn:
                if isinstance(data, pd.DataFrame):
                    data.to_sql(table_name, conn, if_exists='replace', index=False)
                else:
                    df = pd.DataFrame(data)
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
            return True
        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}")
            return False
    
    def _load_from_database(self, table_name: str) -> Optional[pd.DataFrame]:
        """从数据库加载数据"""
        try:
            with self._get_db_connection() as conn:
                query = f"SELECT * FROM {table_name}"
                return pd.read_sql_query(query, conn)
        except Exception as e:
            self.logger.error(f"Error loading from database: {str(e)}")
            return None
    
    def _delete_from_database(self, table_name: str, condition: Optional[Dict] = None) -> bool:
        """从数据库删除数据"""
        try:
            with self._get_db_connection() as conn:
                if condition:
                    # 构建WHERE子句
                    where_clause = " AND ".join([f"{k} = ?" for k in condition.keys()])
                    query = f"DELETE FROM {table_name} WHERE {where_clause}"
                    conn.execute(query, list(condition.values()))
                else:
                    # 删除整个表
                    query = f"DROP TABLE IF EXISTS {table_name}"
                    conn.execute(query)
                conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting from database: {str(e)}")
            return False
    
    def _query_from_database(self, table_name: str, filters: Optional[Dict] = None, limit: Optional[int] = None) -> Optional[pd.DataFrame]:
        """从数据库查询数据"""
        try:
            with self._get_db_connection() as conn:
                query = f"SELECT * FROM {table_name}"
                params = []
                
                if filters:
                    where_clause = " AND ".join([f"{k} = ?" for k in filters.keys()])
                    query += f" WHERE {where_clause}"
                    params.extend(filters.values())
                
                if limit:
                    query += f" LIMIT {limit}"
                
                return pd.read_sql_query(query, conn, params=params if params else None)
        except Exception as e:
            self.logger.error(f"Error querying database: {str(e)}")
            return None
    
    def _list_database_tables(self) -> List[str]:
        """列出数据库中的所有表"""
        try:
            with self._get_db_connection() as conn:
                if self.db_url.startswith('sqlite'):
                    query = "SELECT name FROM sqlite_master WHERE type='table'"
                    cursor = conn.execute(query)
                    return [row[0] for row in cursor.fetchall()]
                else:
                    return []
        except Exception as e:
            self.logger.error(f"Error listing database tables: {str(e)}")
            return []
    
    def get_storage_info(self) -> Dict[str, Any]:
        """获取存储信息"""
        info = {
            "storage_type": "JSON Files" if self.use_json else "Database",
            "data_directory": self.data_dir if self.use_json else None,
            "database_url": self.db_url if not self.use_json else None,
            "tables_count": len(self.list_tables()),
            "tables": self.list_tables()
        }
        
        if self.use_json:
            # 计算存储大小
            total_size = 0
            for filename in os.listdir(self.data_dir):
                filepath = os.path.join(self.data_dir, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)
            
            info["storage_size_bytes"] = total_size
            info["storage_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        return info
