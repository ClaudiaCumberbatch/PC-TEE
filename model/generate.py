import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# 生成模拟数据
def generate_data(num_samples=1000):
    np.random.seed(42)
    # 模拟特征：姓名长度、年龄、收入（随机生成）
    name_length = np.random.randint(3, 10, num_samples)  # 姓名长度（字符数）
    age = np.random.randint(18, 70, num_samples)  # 年龄
    income = np.random.randint(20000, 120000, num_samples)  # 收入

    # 目标标签（例如是否为高收入群体，1表示高收入，0表示低收入）
    label = (income > 80000).astype(int)

    data = np.stack([name_length, age, income], axis=1)
    return data, label

# 加载并分割数据
data, labels = generate_data()
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# 保存训练数据
train_data = pd.DataFrame(X_train, columns=['Name_Length', 'Age', 'Income'])
train_data['Label'] = y_train
train_data.to_csv('train_data.csv', index=False)

# 保存测试数据
test_data = pd.DataFrame(X_test, columns=['Name_Length', 'Age', 'Income'])
test_data['Label'] = y_test
test_data.to_csv('test_data.csv', index=False)

print("训练数据已保存为 'train_data.csv'")
print("测试数据已保存为 'test_data.csv'")