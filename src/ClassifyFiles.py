import os
import shutil


def get_files():
    num = 0
    for filepath, dirnames, filenames  in os.walk(r'/Users/carotpa/PaperCode/00_Enron_DataSet/00_maildir'):
        num = num + len(filenames)
        # for filename in filenames:
        #     print(filename)
    print(num)


def select_files():
    i = 16533
    # 选择遍历的文件夹（文件夹中可以包含文件夹和文件，同一目录下可以既有文件夹又有文件）
    for filepath, dirnames, filenames  in os.walk(r'/Users/carotpa/PaperCode/01_Newsgroups_Dataset/00_20_newsgroups'):
        for filename in filenames:
            src = os.path.join(filepath, filename)
            if src.find('DS_Store') != -1:
                continue
            dst = '/Users/carotpa/PaperCode/01_Newsgroups_Dataset/01_SelectedFiles/09_Smaller_Than_1KB' + '/' + str(i) + '.txt'
            # 选择文件大小，单位为字节Byte
            if 0 < os.path.getsize(src) <= 1000:
                # 重命名后移动到目标文件夹
                shutil.copyfile(src, dst)
                i = i + 1
    print(i)


if __name__ == '__main__':
    get_files()
