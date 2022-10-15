__author__ = 'Miaokai Le'

# 导入基本模块
import os, sys
# pip install moviepy
# import moviepy.editor as mp
from moviepy.editor import VideoFileClip, AudioFileClip

# 调用tkinter模块
from tkinter import *
from tkinter import messagebox, filedialog

# 调用多线程模块
from threading import Thread

# 全局变量设定：
# 获取当前程序所在的目录，
g_curr_path = os.path.dirname(os.path.realpath(sys.argv[0]))
# 用于存储Mp3的存储路径，因为mp3_filepath 会因为选择框中没有输入内容而清空，所以还需要另外一个变量，来保存路径参数
g_mp3_path = g_curr_path
g_mp4_path = g_curr_path

# 用于存放添加到列表框中的文件名
g_mp4_file_list = []


# 下载选中的视频
def threading_convert():
    # 调用下载列表中的视频的函数
    v_l = Thread(target=mp4_convert_to_mp3)
    v_l.start()


# 将提取mp4格式文件中的音频并转为mp3文件
def mp4_convert_to_mp3():
    global g_mp3_path, g_mp4_path, g_mp4_file_list

    # 对列表中选中的文件进行转换
    list_selected = list_box.curselection()
    if len(list_selected) == 0:
        messagebox.showinfo("提示：", "请选择列表框中需要转换的MP4文件！")
    else:
        for i in list_selected:
            mp4_filename = g_mp4_file_list[i]
            # 生成完整的MP4文件路径
            mp4_file = os.path.join(g_mp4_path, mp4_filename)
            # 通过替换文件后缀，生成Mp3文件名
            # 生成Mp3的存放目录以及完整路径
            mp3_file = os.path.join(g_mp3_path, mp4_filename.replace('.mp4', '.mp3'))
            list_box_color_set(i, "正在转换...")

            # 判断文件是否已经存在
            if os.path.exists(mp3_file):
                # print(mp4_file_name)
                list_box_color_set(i, "未作转换")
                status_info["text"] = f"Mp3文件已经存在，如需继续转换请先从MP3保存目录中移除，或更改保存目录"
            else:
                try:
                    # 正常情况下，应该使用VideoFileClip来读取Mp4文件，并重新生成Mp3文件，代码如下：
                    VideoFileClip(mp4_file).audio.write_audiofile(mp3_file)
                    # 但是由于从Youtube下载的仅包含音频的文件，其实并不是MP4文件，会出现 self.fps = infos['video_fps'] 的关键错误，
                    # 所以不能采用这种方式读取，应该考虑用音频的方式读取
                except:
                    # 用音频的方式读取从Youtube下载的Mp4文件，并输出为mp3 音频文件。
                    AudioFileClip(mp4_file).write_audiofile(mp3_file)

                status_info["text"] = f"所选的MP4文件已经成功转换为Mp3"
                list_box_color_set(i, "转换完成")

                # 完成转换后，将列表中的内容清空,表示访序号的文件已经完成了转换。
                g_mp4_file_list[i] == ''


# 设置列表框中第i行信息内容的显示颜色
def list_box_color_set(i, status):
    global g_mp4_file_list
    list_box.delete(i)
    list_box.insert(i, f"{str(i + 1).zfill(3)} . |{status}|{g_mp4_file_list[i]}")

    if "转换完成" in status:
        list_box.itemconfigure(i, background="yellowgreen", fg="black")
    elif "正在转换..." in status:
        list_box.itemconfigure(i, background="greenyellow")
    elif "未作转换" in status:
        list_box.itemconfigure(i, background="yellow", fg="black")


# 选择转换后的Mp3文件的保存路径
def choose_mp3_filepath():
    global g_mp3_path
    # 由于在select_dir中不能添加与目录选择无关的语句，所以需要这个一个函数，来审核选择内容的情况
    # 如果从目录选择框中获取的内容为空，则重新设定为g_save_path,否则就更新g_save_path.
    Mp3_Browse()
    if mp3_filepath.get() == '':
        mp3_filepath.set(g_mp3_path)
    else:
        g_mp3_path = mp3_filepath.get()


# download_Path.set() 会在状态栏显示，当前的路径
# print(g_save_path)

# 弹出目录选择框
def Mp3_Browse():
    download_Directory = filedialog.askdirectory(initialdir='', title="选择用于保存转换后的Mp3的文件夹")
    # 设置选中的目录位置
    mp3_filepath.set(download_Directory)


# 添加单个链接到listbox中
def add_filename_to_listbox():
    global g_mp4_path, g_mp4_file_list
    # 每次添加前，先清空
    list_box.delete(0, 'end')
    # 同时清空用于存放添加到列表框中的文件名
    g_mp4_file_list = []
    for mp4_filename in os.listdir(g_mp4_path):
        if '.mp4' in mp4_filename:
            # 输出的序号，需要 list_box.size() + 1。
            g_mp4_file_list.append(mp4_filename)
            list_box.insert(END, f"{str(list_box.size() + 1).zfill(3)} . {mp4_filename}")


# 选择MP4文件所在的目录路径
def choose_mp4_filepath():
    global g_mp4_path
    # 由于在select_dir中不能添加与目录选择无关的语句，所以需要这个一个函数，来审核选择内容的情况
    # 如果从目录选择框中获取的内容为空，则重新设定为g_save_path,否则就更新g_save_path.
    Mp4_Browse()
    if mp4_filepath.get() == '':
        mp4_filepath.set(g_mp4_path)
    else:
        g_mp4_path = mp4_filepath.get()
    # 将当前选定目录中的Mp4文件添加到列表框中
    add_filename_to_listbox()
    status_info["text"] = f"目录中的MP4文件已添加。"


# 弹出目录选择框
def Mp4_Browse():
    download_Directory = filedialog.askdirectory(initialdir='', title="选择需要转换的MP4文件所在目录")
    # 设置选中的目录位置
    mp4_filepath.set(download_Directory)


# 创建窗口
root = Tk()
# 设置窗口尺寸
root.geometry('900x550')
root.title("Mp3提取工具")
bg_color = 'snow'  # 'lemon chiffon' #"black"  #"whitesmoke"  # "floralwhite"
fg_color = "greenyellow"
root.configure(background=bg_color)

# 设置目录选择变量
mp3_filepath = StringVar()
mp3_filepath.set(g_mp3_path)

mp4_filepath = StringVar()
mp4_filepath.set(g_curr_path)

# 添加窗口中组件：
# 添加输入及操作区域
inputframe = Frame(root, bg=bg_color)
inputframe.pack(side=TOP, pady=0)

# 添加输入框 Mp4
inputframe_mp4 = Frame(inputframe, bg=bg_color)
inputframe_mp4.pack(side=TOP, pady=0)

# 添加提示标签
Label(inputframe_mp4, text="Mp4文件目录 :", font="Calibri 12", bg=bg_color).pack(side=LEFT)
# 添加输入框， 默认内容为当前文件夹目录
Mp4_filepath_input = Entry(inputframe_mp4, textvariable=mp4_filepath, width=90, font="Calibri 12", bg=bg_color)
Mp4_filepath_input.pack(side=LEFT, padx=3, pady=8)
# 添加选择MP4文件目录的按钮
convert_BT = Button(inputframe_mp4, text="浏览", command=choose_mp4_filepath, font="Calibri 11", bg=bg_color)
convert_BT.pack(side=LEFT, padx=3, pady=8)

# 设定程序起动后的焦点为输入框
Mp4_filepath_input.focus_set()

# 添加输入框 Mp3
inputframe_mp3 = Frame(inputframe, bg=bg_color)
inputframe_mp3.pack(side=TOP, pady=0)

Label(inputframe_mp3, text="Mp3保存目录 :", font="Calibri 12", bg=bg_color).pack(side=LEFT)
# 添加输入框， 默认内容为当前文件夹目录
Mp3_filepath_input = Entry(inputframe_mp3, textvariable=mp3_filepath, width=90, font="Calibri 12", bg=bg_color)
Mp3_filepath_input.pack(side=LEFT, padx=3, pady=8)

# 添加选择MP3文件目录的按钮
convert_BT = Button(inputframe_mp3, text="浏览", command=choose_mp3_filepath, font="Calibri 11", bg=bg_color)
convert_BT.pack(side=LEFT, padx=3, pady=8)

# 开始转换
more_BT = Button(root, text="开 始 转 换", font="Calibri 11 bold", command=threading_convert, bg="greenyellow",
                 fg="black")
more_BT.pack(fill=X)

# 滚动条和列表框设定
listboxframe = Frame(root, bg=bg_color, bd=1)
listboxframe.pack(expand=YES, fill=BOTH, padx=2, pady=2)

scrollbar = Scrollbar(listboxframe, bg=bg_color)
scrollbar.pack(side=RIGHT, fill=BOTH)
list_box = Listbox(listboxframe, selectmode="multiple", font="Arial 11", bg=bg_color)
list_box.pack(expand=YES, fill="both")
list_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=list_box.yview)


# 清空下载列表
# 删除列表中的全部内容
def clean_listbox():
    global g_mp4_file_list
    list_box.delete(0, 'end')
    # 清空下载列表
    g_mp4_file_list = []
    # 在状态样栏中显示状态
    status_info["text"] = f"列表已经清空，请再次选择MP4文件所在目录 "


clean_list_BT = Button(listboxframe, text="清空列表", command=clean_listbox, background="greenyellow", fg="black",
                       font="Arial 10")
clean_list_BT.pack(side=RIGHT, padx=8, pady=8)


# 删除已经完成的项目
def delete_finished():
    global g_mp4_file_list
    # 遍历字典中的全部数据
    for i in range(len(g_mp4_file_list)):
        # 如果列表中的文件名为'' 表示该文件已经完成了转换
        if g_mp4_file_list[i] == '':
            # 根据URL获取编号 i
            g_mp4_file_list.pop(i)
            list_box.delete(i)

    # 删除后，对列表中的内容重新排序号
    # list_box_sort()
    # 在状态样栏中显示目前已经下载完成的数量
    status_info["text"] = f"已经转换过的MP4文件已经从列表框中清除"


# 删除已经完成下载的内容

select_all_BT = Button(listboxframe, text="删除已完成", command=delete_finished, background="greenyellow", fg="black",
                       font="Arial 10")
select_all_BT.pack(side=RIGHT, padx=8, pady=8)


# 删除选中的项目
def delete_selected():
    global g_mp4_file_list
    select_list = list(list_box.curselection())
    select_list.sort(reverse=True)
    for i in select_list:
        g_mp4_file_list.pop(i)
        list_box.delete(i)

    # 删除后，对列表中的内容重新排序号
    # list_box_sort()

    # 在状态样栏中显示目前已经下载完成的数量
    status_info["text"] = f"选中的文件已经从列表框中清除 "


# 删除选中记录
select_all_BT = Button(listboxframe, text="删除已选", command=delete_selected, background="greenyellow", fg="black",
                       font="Arial 10")
select_all_BT.pack(side=RIGHT, padx=8, pady=8)


# 对列表中的内容进行反向选择
def list_box_inverse():
    # 先将当前选中的内容保存
    selected_list = list_box.curselection()
    # 选择全部列表
    select_all()
    # 将之前选中过的内容清空
    for i in selected_list:
        list_box.selection_clear(i, i)


# 反向选择
sort_list_BT = Button(listboxframe, text="反向选择", command=list_box_inverse, background="greenyellow", fg="black",
                      font="Arial 10")
sort_list_BT.pack(side=RIGHT, padx=8, pady=8)


# 清空所有选中的项目
def select_none():
    # 清空选中的列表中的内容
    list_box.selection_clear(0, END)


# 全部不选
select_all_BT = Button(listboxframe, text="全部不选", command=select_none, background="greenyellow", fg="black",
                       font="Arial 10")
select_all_BT.pack(side=RIGHT, padx=8, pady=8)


# 选中列表中的全部
def select_all():
    # 选中全部列表中的内容
    list_box.select_set(0, END)


# 全部选中
select_all_BT = Button(listboxframe, text="全部选中", command=select_all, background="greenyellow", fg="black",
                       font="Arial 10")
select_all_BT.pack(side=RIGHT, padx=8, pady=8)

# 向列表框中添加当前目录中的MP4文件
add_filename_to_listbox()
# 选中全部内容
select_all()

# 状态栏设定
statusframe = Frame(root, bd=1, relief=SUNKEN, bg=bg_color)
statusframe.pack(side=BOTTOM, fill=X)

status_label = Label(statusframe, text='>>>', anchor=W, bg=bg_color, font="Calibri 11 bold")
status_label.pack(side=LEFT)

status_info = Label(statusframe, text='', anchor=W, bg=bg_color, font="Calibri 11 bold")
status_info.pack(side=LEFT, fill=X)

status_author = Label(statusframe, text='|Author Email: LeMiaokai@gmail.com', anchor=W, bg=bg_color,
                      font="Calibri 11 bold")
status_author.pack(side=RIGHT)


def main():
    # 打开窗口显示
    root.mainloop()


if __name__ == '__main__':
    main()
