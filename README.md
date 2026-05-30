# CSV to JSONL 数据清洗流水线

一个轻量级的数据转换工具，将CSV文件转换为JSONL格式，支持缺失值填充、字段筛选和字段统计。  
项目使用 Docker 封装，确保环境一致性；通过 Git 进行版本管理。

## ✨ 功能

- 将任意CSV转换为JSONL（每行一个JSON对象）
- 可选填充缺失值（如 \`--fillna 0\` 或 \`--fillna "unknown"\`）
- 可选只保留指定列（\`--columns name,age\`）
- 输出指定列的统计分布（数值列：均值/中位数/极值；分类列：频次占比）
- 示例数据一键生成（\`--generate-sample\`）
- Docker 一键运行

## 🚀 快速开始

### 本地运行（需要Python 3.9+）

```bash
pip install -r requirements.txt
python csv_to_jsonl.py --generate-sample
python csv_to_jsonl.py --input sample_data.csv --output output/data.jsonl --fillna 0 --columns id,name,age,score,category --stats age
```

### Docker 运行

```bash
docker build -t csv-to-jsonl .
docker run --rm -v $(pwd):/data csv-to-jsonl --generate-sample
docker run --rm -v $(pwd):/data csv-to-jsonl --input /data/sample_data.csv --output /data/output/docker_out.jsonl --fillna 0 --stats age
```

## 📊 数据采集与可复现性验证

本项目同时用作 AI 训练数据采集的示例，展示了如何记录 AI 编程助手的交互轨迹并验证代码变更的可复现性。

### 交互轨迹记录

在 `data-agent` 分支中，我们记录了为 `math_utils.py` 添加除法函数的完整过程：
- 任务背景与初始代码
- 用户与 AI 助手的对话
- 代码变更的 UnifiedDiff
- 通过 \`git apply\` 验证补丁的可行性

详见 [\`interaction_log.md\`](https://github.com/RXH99/csv-to-jsonl-tool/blob/data-agent/interaction_log.md) 和 [\`add_divide_function.patch\`](https://github.com/RXH99/csv-to-jsonl-tool/blob/data-agent/add_divide_function.patch)。

### 可复现性验证命令

在 `data-agent` 分支下执行以下命令可重现代码变更：

```bash
 恢复初始状态（仅 add 和 multiply）
git checkout math_utils.py

 应用补丁
git apply add_divide_function.patch

 检查文件，应包含 divide 函数
cat math_utils.py
```

### JSONL 格式化

我们还提供了将交互日志转换为 JSONL 的脚本 [`md_to_jsonl.py\`](https://github.com/RXH99/csv-to-jsonl-tool/blob/data-agent/md_to_jsonl.py)，输出示例见 [`interaction_log.jsonl\`](https://github.com/RXH99/csv-to-jsonl-tool/blob/data-agent/interaction_log.jsonl)，满足标准化数据采集的需要。

