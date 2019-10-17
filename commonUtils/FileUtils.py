import os


def list_all_file_abs_path(path):
    # 列出该目录下的所有文件名
    file_list = os.listdir(path)
    return_list = []
    for f in file_list:
        # 将文件名映射成绝对路径
        filepath = os.path.join(path, f)
        return_list.append(filepath)
    return return_list


def del_file_from_dir(path):
    file_list = list_all_file_abs_path(path)
    for i in file_list:
        os.remove(i)
    print(path + "文件夹删除完毕")

