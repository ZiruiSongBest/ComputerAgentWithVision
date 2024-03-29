import os
import pandas as pd

def read_file_content(filename):
    try:
        # 打开文件并读取内容
        with open(filename, 'r', encoding='utf-8') as file:
            # 使用列表推导式读取非空行并去除行尾空白
            lines = [line.strip() for line in file if line.strip()]
            # 将非空行合并为一个字符串
            content = '\n'.join(lines)
        return content
    except Exception as e:
        # 发生任何异常时返回空字符串
        print(f"Error reading file: {e}")  # Optional: Print error message
        return ""
    
class ExcelWriter:
    def __init__(self, filename):
        self.filename = filename
        # 检查文件是否存在并且不为空
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            try:
                # 试图读取现有 Excel 文件到 DataFrame
                self.df = pd.read_excel(self.filename)
            except Exception as e:
                print(f"Error reading the Excel file: {e}")
                # 如果读取失败，初始化一个空的 DataFrame
                self.df = pd.DataFrame(columns=['task_id', 'final_answer', 'my_answer'])
        else:
            # 如果文件不存在或为空，初始化一个空的 DataFrame
            self.df = pd.DataFrame(columns=['task_id', 'final_answer', 'my_answer'])

    def add_row(self, task_id, final_answer, my_answer):
        # 添加一行数据
        new_row = {'task_id': task_id, 'final_answer': final_answer, 'my_answer': my_answer}
        self.df = self.df.append(new_row, ignore_index=True)

    def save(self):
        # 将 DataFrame 写入 Excel 文件，如果文件存在，不会删除原有数据
        with pd.ExcelWriter(self.filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            self.df.to_excel(writer, index=False)