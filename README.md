\# CSV to JSONL 数据清洗流水线



一个轻量级的数据转换工具，将CSV文件转换为JSONL格式，支持缺失值填充、字段筛选和字段统计。  

项目使用 Docker 封装，确保环境一致性；通过 Git 进行版本管理。



\## ✨ 功能



\- 将任意CSV转换为JSONL（每行一个JSON对象）

\- 可选填充缺失值（如 `--fillna 0` 或 `--fillna "unknown"`）

\- 可选只保留指定列（`--columns name,age`）

\- 输出指定列的统计分布（数值列：均值/中位数/极值；分类列：频次占比）

\- 示例数据一键生成（`--generate-sample`）

\- Docker 一键运行



\## 🚀 快速开始



\### 本地运行（需要Python 3.9+）



```bash

pip install -r requirements.txt

python csv\_to\_jsonl.py --generate-sample

python csv\_to\_jsonl.py --input sample\_data.csv --output output/data.jsonl --fillna 0 --columns id,name,age,score,category --stats age

