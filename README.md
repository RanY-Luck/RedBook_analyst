# 小红书笔记数据处理工具

这个项目用于处理小红书笔记数据,主要功能包括:
1. 读取Excel中的笔记URL
2. 爬取笔记内容和话题标签
3. 将数据保存到新的Excel文件

## 依赖安装

```
pip install -r requirements.txt
```

## 使用说明

1. 准备包含笔记URL的Excel文件
2. 修改spider.py中的cookie信息
3. 运行程序:

```
python spider.py
```

## 注意事项

1. 需要有效的小红书cookie
2. 请遵守小红书的使用条款
3. 建议控制爬取频率,避免被封禁
