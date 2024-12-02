import tensorflow as tf
import pandas as pd

# 从CSV文件中加载数据
def load_data(file_path):
    df = pd.read_csv(file_path)
    X = df[['Name_Length', 'Age', 'Income']].values
    y = df['Label'].values
    return X, y

# 加载训练和测试数据
X_train, y_train = load_data('train_data.csv')
X_test, y_test = load_data('test_data.csv')

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
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 评估模型
loss, accuracy = model.evaluate(X_test, y_test)
print(f"测试集上的准确率: {accuracy:.2f}")