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

    def add_row(self, task_id, final_answer, my_answer, question=None):
        # 检查是否存在给定 task_id 的行
        existing_row_index = self.df[self.df['task_id'] == task_id].index

        if not existing_row_index.empty:
            # 如果存在，更新该行
            self.df.loc[existing_row_index, 'final_answer'] = final_answer
            self.df.loc[existing_row_index, 'my_answer'] = my_answer
        else:
            # 如果不存在，添加新行
            new_row_df = pd.DataFrame([[task_id, final_answer, my_answer]], columns=['task_id', 'final_answer', 'my_answer'])
            self.df = pd.concat([self.df, new_row_df], ignore_index=True)

    def save(self):
        self.remove_duplicate_task_ids()
        # Check if the Excel file exists
        if os.path.exists(self.filename):
            # If the file exists, open in append mode
        #     mode = 'a'
        #     if_sheet_exists = 'overlay'
        # else:
            # If the file does not exist, create a new file
            mode = 'w'
            if_sheet_exists = None

        # Use the determined mode to save the DataFrame
        with pd.ExcelWriter(self.filename, engine='openpyxl', mode=mode, if_sheet_exists=if_sheet_exists) as writer:
            self.df.to_excel(writer, index=False)

    def remove_duplicate_task_ids(self):
        # 检查并保留每个 task_id 的最后一个条目
        self.df = self.df.drop_duplicates(subset=['task_id'], keep='last')
