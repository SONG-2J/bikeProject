# 读取hdfs文件内容,将每行存入数组返回
def read_hdfs_file(client, file_path):
    lines = []
    with client.read(file_path, encoding='utf-8', delimiter='\n') as reader:
        for line in reader:
            lines.append(line.strip())
    return lines


# 向文件追加数据
def append2hdfs(client, file_path, data):
    client.write(file_path, data.encode('UTF-8'), overwrite=False, append=True)


# 覆盖数据写到hdfs文件
def write2hdfs(client, file_path, data):
    client.write(file_path, data.encode('UTF-8'), overwrite=True, append=False)
