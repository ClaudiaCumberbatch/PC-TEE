import tensorflow as tf
import pandas as pd
import sys

# 从CSV文件中加载数据
def load_data(file_path):
    df = pd.read_csv(file_path)
    X = df[['Name_Length', 'Age', 'Income']].values
    y = df['Label'].values
    return X, y

def main():
    if len(sys.argv) != 2:
        print("Usage: python train.py <path_to_train_data.csv>")
        sys.exit(1)

    train_data_path = sys.argv[1]

    # 加载训练数据
    X_train, y_train = load_data(train_data_path)

    # 构建简单的神经网络模型
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(3,)),  # 输入层有3个特征
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')  # 输出层为二分类问题
    ])

    # 编译模型
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # 训练模型
    model.fit(X_train, y_train, epochs=10, batch_size=32)

    # 保存模型
    model.save('trained_model.h5')
    print("模型已保存为 trained_model.h5")

if __name__ == "__main__":
    main()