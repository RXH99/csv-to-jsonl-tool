#!/usr/bin/env python3
"""
CSV to JSONL Converter with statistics and missing value handling.
Usage: python csv_to_jsonl.py --input input.csv --output output.jsonl
       --fillna 0 --columns Name,Age --stats Age
"""
import argparse
import json
import sys
import pandas as pd
from pathlib import Path

def generate_sample_csv(filename="sample_data.csv"):
    """生成一个示例CSV文件，包含缺失值和多种数据类型"""
    import numpy as np
    data = {
        "id": range(1, 101),
        "name": [f"user_{i}" for i in range(1, 101)],
        "age": np.random.randint(18, 70, 100),
        "score": np.random.uniform(50, 100, 100).round(2),
        "category": np.random.choice(["A", "B", "C", None], 100, p=[0.4, 0.3, 0.2, 0.1]),
    }
    df = pd.DataFrame(data)
    df.loc[5, "age"] = None
    df.loc[12, "score"] = None
    df.loc[23, "category"] = None
    df.to_csv(filename, index=False)
    print(f"✅ 生成示例CSV文件: {filename}")
    return filename

def convert_csv_to_jsonl(input_path, output_path, fillna=None, columns=None, stats_col=None):
    df = pd.read_csv(input_path)
    print(f"📄 读取CSV: {input_path}, 形状 {df.shape}")

    if fillna is not None:
        df = df.fillna(fillna)
        print(f"🔧 缺失值已填充为: {fillna}")

    if columns:
        selected = [col.strip() for col in columns.split(",")]
        df = df[selected]
        print(f"📌 保留列: {selected}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            for k, v in row_dict.items():
                if pd.isna(v):
                    row_dict[k] = None
            f.write(json.dumps(row_dict, ensure_ascii=False) + '\n')
    print(f"✅ 写入JSONL: {output_path}，共 {len(df)} 行")

    if stats_col and stats_col in df.columns:
        col_data = df[stats_col].dropna()
        if not col_data.empty:
            print(f"\n📊 列 '{stats_col}' 的分布统计:")
            if col_data.dtype in ['int64', 'float64']:
                print(f"  均值: {col_data.mean():.2f}")
                print(f"  中位数: {col_data.median()}")
                print(f"  最小/最大: {col_data.min()} / {col_data.max()}")
            else:
                counts = col_data.value_counts()
                for val, cnt in counts.items():
                    print(f"  {val}: {cnt} ({cnt/len(df)*100:.1f}%)")
        else:
            print(f"⚠️ 列 '{stats_col}' 全部为缺失值，无法统计")
    elif stats_col:
        print(f"❌ 列 '{stats_col}' 不存在于数据中，可用列: {list(df.columns)}")

    return len(df)

def main():
    parser = argparse.ArgumentParser(description="CSV to JSONL converter with optional statistics")
    parser.add_argument("--input", "-i", help="输入CSV文件路径")
    parser.add_argument("--output", "-o", default="output/data.jsonl", help="输出JSONL文件路径 (默认: output/data.jsonl)")
    parser.add_argument("--fillna", help="缺失值填充内容，例如 0 或 'missing'")
    parser.add_argument("--columns", help="需要保留的列名，逗号分隔，例如 'id,name,age'")
    parser.add_argument("--stats", help="需要统计分布的列名")
    parser.add_argument("--generate-sample", action="store_true", help="生成一个示例CSV文件 (sample_data.csv) 并退出")
    args = parser.parse_args()

    if args.generate_sample:
        generate_sample_csv()
        return

    if not args.input:
        print("❌ 请指定 --input 参数，或使用 --generate-sample 生成示例数据")
        sys.exit(1)

    convert_csv_to_jsonl(
        input_path=args.input,
        output_path=args.output,
        fillna=args.fillna,
        columns=args.columns,
        stats_col=args.stats
    )

if __name__ == "__main__":
    main()