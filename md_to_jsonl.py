import json
import re

def parse_markdown_to_jsonl(md_file, jsonl_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取任务背景
    bg_match = re.search(r'## 任务背景\n(.*?)\n##', content, re.DOTALL)
    task_background = bg_match.group(1).strip() if bg_match else ""

    # 提取初始代码（未用```包裹，但我们的内容没有```，按实际文本提取）
    # 简单起见，我们直接提取 "## 初始代码" 后到 "## 对话记录" 之间的内容
    init_match = re.search(r'## 初始代码\n(.*?)\n## 对话记录', content, re.DOTALL)
    initial_code = init_match.group(1).strip() if init_match else ""

    # 提取对话记录
    dialog_match = re.search(r'## 对话记录\n(.*?)\n## 代码变更', content, re.DOTALL)
    dialog_text = dialog_match.group(1).strip() if dialog_match else ""
    # 简单解析：按行分割，识别“用户：”和“AI：”
    interaction = []
    lines = dialog_text.split('\n')
    for line in lines:
        if line.startswith('用户：'):
            interaction.append({"role": "user", "content": line[3:].strip()})
        elif line.startswith('AI：'):
            interaction.append({"role": "assistant", "content": line[3:].strip()})

    # 提取 UnifiedDiff
    diff_match = re.search(r'## 代码变更.*?\n(.*?)\n## 验证步骤', content, re.DOTALL)
    unified_diff = diff_match.group(1).strip() if diff_match else ""

    # 构造 JSON 对象
    record = {
        "id": "001",
        "task_type": "feature_dev",
        "task_background": task_background,
        "initial_code": initial_code,
        "unified_diff": unified_diff,
        "interaction": interaction,
        "env_info": {
            "git_hash": "5088668",  # 你的初始 commit
            "os": "windows"
        },
        "metrics": {
            "timestamp": "2026-05-30"
        }
    }

    with open(jsonl_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"✅ JSONL 文件已生成: {jsonl_file}")

if __name__ == "__main__":
    parse_markdown_to_jsonl("interaction_log.md", "interaction_log.jsonl")