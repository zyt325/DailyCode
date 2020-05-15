PYTHONPATH=PYTHONPATH:project_root

## backend
### 初始化

1. 把backend路径加入到PYTHONPATH，
1. cd backend;
1. 安装python相关库   pip install -r requirement.txt
1. 配置数据库    db/config.py
1. 查看管理方法  python manage.py
1. 创建数据库address_book   python manage.py create_db
1. 创建相关表    python manage.py init_table
1. 删除表book_view  python manage.py drop_table_book_view
1. 创建视图      python manage.py create_book_view
1. 同步数据      python manage.py sync_data_db
1. 启动服务      gunicorn -c gunicore.conf.py  main:app


* 删除表book_view,手动创建book_view视图

```sql
CREATE VIEW book_view AS SELECT p.*,
d.code AS dep_code,d.english_name AS dep_english_name,d.chinese_name AS dep_chinese_name,
o.code AS office_code,o.english_name AS office_english_name,
t.wiki_title AS title,t.wiki_title_cn AS title_cn,
l.code 
FROM people p 
LEFT JOIN department d ON p.department_id=d.id 
LEFT JOIN office o ON p.office_id=o.id 
LEFT JOIN title t ON p.title_id=t.id
LEFT JOIN logical_company l ON p.logical_company_id=l.id
```