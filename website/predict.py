import pandas as pd
import tensorflow as tf
import sys

def main():
    # 从命令行参数读取输入文件路径
    if len(sys.argv) != 2:
        print("Usage: python predict.py <input_csv>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    # 读取 CSV 数据
    try:
        data = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)

    # 检查所需的列是否存在
    required_columns = ['Name_Length', 'Age', 'Income']
    if not all(column in data.columns for column in required_columns):
        print(f"CSV file must contain the following columns: {', '.join(required_columns)}", file=sys.stderr)
        sys.exit(1)

    # 加载训练好的模型
    try:
        model = tf.keras.models.load_model('../model/trained_model.h5')
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)

    # 进行预测
    X = data[required_columns].values
    predictions = model.predict(X)

    # 将预测结果添加到数据中
    data['prediction'] = predictions

    # 输出结果
    print(data.to_csv(index=False))

if __name__ == "__main__":
    main()