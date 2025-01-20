import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
from pynput import mouse, keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动点击器-vv出现")
        # 重复次数
        self.repeat_count = 9999999
        
        # 是否运行中
        self.running = False

        # 复选框：窗口是否置顶
        self.sticky_checkbox = tk.BooleanVar(value=True)  # 默认置顶
        self.sticky_checkbox_label = tk.Checkbutton(root, text="窗口置顶", variable=self.sticky_checkbox, command=self.update_sticky)
        self.sticky_checkbox_label.pack()

        # 按钮：开始录制
        self.start_record_button = tk.Button(root, text="开始录制", command=self.toggle_recording)
        self.start_record_button.pack()

        # 按钮：开始运行
        self.start_run_button = tk.Button(root, text="开始运行(重复%s次,按空格取消)" % self.repeat_count, command=self.start_run)
        self.start_run_button.pack()

        # 初始化录制数据
        self.clicks = []
        self.recording = False
        self.listener = None
        self.pretime = 0
        self.keyboard_listener = None
        # 快捷键
        print('开始监听')   
        self.keyboard_listener = keyboard.Listener(on_press=self.end_run)
        # 启动监听器
        self.keyboard_listener.start()

        # 初始化窗口置顶
        self.update_sticky()

    def toggle_recording(self):
        if self.recording:
            self.recording = False
            self.start_record_button.config(text="开始录制")
            self.start_run_button['state'] = 'normal'
            
            if self.listener:
                self.listener.stop()
        else:
            self.pretime = time.time()
            self.recording = True
            self.start_record_button.config(text="停止录制")
            self.clicks = []  # 清空之前的记录
            self.start_run_button['state'] = 'disabled'
            self.listener = mouse.Listener(on_click=self.on_mouse_click)
            self.listener.start()

    def start_run(self):
        # 定义结束监听的函数
        print('start 了')
        self.start_run_button.config(text="运行中，按空格结束")
        self.start_run_button['state'] = 'disabled'
        self.running = True
        self.root.after(0, self.doRun)
    # 监听键盘，点击后暂停
    def doRun(self):
        cur_count = 0
        for _ in range(self.repeat_count):
            if not self.running:
                break
            # 或者如果超过当天的23:59分，则break
            if time.localtime().tm_hour >= 23 and time.localtime().tm_min >= 59:
                break
            for x, y, interval in self.clicks:
                if not self.running:
                    break
                pyautogui.click(x, y)
                time.sleep(0.1)
            cur_count += 1
            print('当前次数: %s, 剩余次数：%s' % (cur_count, self.repeat_count-cur_count))
        print('end 了')
        # 重置状态
        self.running = False
        self.start_run_button.config(text="开始运行(重复%s次或23:59结束,按空格取消)" % self.repeat_count)
        self.start_run_button['state'] = 'normal'
        
    # mgh 这里的监听有问题！
    def end_run(self, key):
        try:
            print(f'{key} pressed')
            if(key == keyboard.Key.space):
                self.running = False
                print('空壳被按下了')    
        except AttributeError:
                pass
        self.running = False


    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            # 判断是否在录制按钮中
            if self.start_record_button.winfo_rootx() <= x <= self.start_record_button.winfo_rootx() + self.start_record_button.winfo_width() and \
               self.start_record_button.winfo_rooty() <= y <= self.start_record_button.winfo_rooty() + self.start_record_button.winfo_height():
                return
            current_time = time.time()
            # 计算两次点击的间隔
            interval = current_time - self.pretime
            self.clicks.append((x, y, interval))
            self.pretime = time.time()

    def update_sticky(self):
        self.root.attributes('-topmost', self.sticky_checkbox.get())

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300") 
    app = AutoClickerApp(root)
    root.mainloop()