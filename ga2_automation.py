import tkinter as tk
from handler import AutoGa2
import threading
import keyboard
from time import sleep


class Ga2UI:
    def __init__(self, root):
        self.root = root
        self.root.title("GA2 Automation")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 400
        x_position = int(screen_width - window_width - (screen_width * 0.05))
        y_position = int((screen_height - window_height) * 0.10)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.config(bg="#2C3E50")

        # Tạo font
        self.font_title = ("Arial", 14, "bold")
        self.font_button = ("Arial", 12, "bold")

        # Khởi tạo đối tượng của các class AutoAwaken và AutoGat
        self.auto_ga2 = AutoGa2()

        # Tạo các khu vực (Frame) cho UI
        self.create_section_awaken()
        self.create_section_gat()
        self.create_stop_section()

        # Nhóm các chức năng button vào một dictionary
        self.button_actions = {
            "Auto Awaken Accessory": self.awaken_task,
            "Level Up Awaken Skill": self.level_up_skill_task,
            "Auto Ready": self.auto_ready_task,
            "Auto Farm 400": self.farm_400_task,
            "Auto Farm Gold": self.farm_gold_task,
            "STOP": self.stop_task,
        }

    def create_button(self, parent_frame, text, command, color, state="normal"):
        """Hàm tạo nút, giúp giảm bớt sự lặp lại trong code"""
        return tk.Button(
            parent_frame,
            text=text,
            font=self.font_button,
            bg=color,
            fg="#000000",  # Màu chữ tối
            command=command,
            relief="raised",
            height=2,
            state=state,  # Thêm tham số state
        )

    def create_section_awaken(self):
        # Khu vực 1: Thức tỉnh trang bị
        frame_1 = tk.Frame(
            self.root, bg="#34495E", bd=5, relief="groove", width=280, height=250
        )
        frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        label_1 = tk.Label(
            frame_1,
            text="Auto Awaken",
            font=self.font_title,
            bg="#34495E",
            fg="#ECF0F1",  # Chữ sáng
        )
        label_1.pack(pady=10)

        # Nút bấm
        self.auto_ga2_button = self.create_button(
            frame_1,
            "Awaken Accessory",
            lambda: self.start_thread(self.button_actions["Auto Awaken Accessory"]),
            "#1ABC9C",
        )
        self.auto_ga2_button.pack(fill=tk.X, padx=10, pady=10)

        self.level_up_awaken_button = self.create_button(
            frame_1,
            "Awaken Level Up: Lv10 to Lv20",
            lambda: self.start_thread(self.button_actions["Level Up Awaken Skill"]),
            "#1ABC9C",
        )
        self.level_up_awaken_button.pack(fill=tk.X, padx=10, pady=10)

    def create_section_gat(self):
        # Khu vực 2: Auto GAT
        frame_2 = tk.Frame(
            self.root, bg="#34495E", bd=5, relief="groove", width=280, height=250
        )
        frame_2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        label_2 = tk.Label(
            frame_2, text="Auto GAT", font=self.font_title, bg="#34495E", fg="#ECF0F1"
        )
        label_2.pack(pady=10)

        # Nút bấm
        self.auto_ready_button = self.create_button(
            frame_2,
            "Auto Ready",
            lambda: self.start_thread(self.button_actions["Auto Ready"]),
            "#E74C3C",
        )
        self.auto_ready_button.pack(fill=tk.X, padx=10, pady=10)

        self.auto_farm_400_button = self.create_button(
            frame_2,
            "Auto Farm 400",
            lambda: self.start_thread(self.button_actions["Auto Farm 400"]),
            "#E74C3C",
        )
        self.auto_farm_400_button.pack(fill=tk.X, padx=10, pady=10)

        self.auto_farm_gold_button = self.create_button(
            frame_2,
            "Auto Farm Gold",
            lambda: self.start_thread(self.button_actions["Auto Farm Gold"]),
            "#E74C3C",
        )
        self.auto_farm_gold_button.pack(fill=tk.X, padx=10, pady=5)

    def create_stop_section(self):
        # Khu vực 3: Nút STOP
        stop_frame = tk.Frame(
            self.root, bg="#34495E", bd=5, relief="groove", width=600, height=100
        )
        stop_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Nút STOP mặc định là disabled
        self.stop_button = self.create_button(
            stop_frame,
            "STOP",
            lambda: self.start_thread(self.button_actions["STOP"]),
            "#F39C12",
            state="disabled",
        )
        self.stop_button.pack(fill=tk.X, padx=10, pady=10)

    """Method"""

    def awaken_task(self):
        self.auto_ga2.auto_farm_10_exp_awaken()
        self.on_task_complete()

    def level_up_skill_task(self):
        self.auto_ga2.auto_farm_lv10_to_lv20_awaken()
        self.on_task_complete()

    def auto_ready_task(self):
        self.auto_ga2.auto_ready()
        self.on_task_complete()

    def farm_400_task(self):
        self.auto_ga2.auto_farm_400()
        self.on_task_complete()

    def farm_gold_task(self):
        self.auto_ga2.auto_farm_gold()
        self.on_task_complete()

    def stop_task(self):
        self.auto_ga2.running = False

    # Hàm để khởi tạo một thread cho mỗi task
    def start_thread(self, task):
        self.disable_all_buttons()
        self.enable_stop_button()

        keyboard_thread = threading.Thread(target=self.monitor_f2)
        keyboard_thread.daemon = (
            True  # Đảm bảo thread này sẽ kết thúc khi chương trình chính kết thúc
        )
        keyboard_thread.start()

        thread = threading.Thread(target=task)
        thread.daemon = True
        thread.start()

    def monitor_f2(self):
        while True:
            if keyboard.is_pressed("F2"):  # Kiểm tra xem phím F2 có được nhấn không
                print("F2 pressed, stopping the task...")
                self.auto_ga2.running = False  # Dừng task chính
                break  # Thoát khỏi vòng lặp khi F2 được nhấn
            sleep(0.1)

    def enable_stop_button(self):
        self.stop_button.config(state="normal")

    def disable_stop_button(self):
        self.stop_button.config(state="disabled")

    def disable_all_buttons(self):
        self.auto_ga2_button.config(state="disabled")
        self.level_up_awaken_button.config(state="disabled")
        self.auto_ready_button.config(state="disabled")
        self.auto_farm_400_button.config(state="disabled")
        self.auto_farm_gold_button.config(state="disabled")

    def enable_all_buttons(self):
        self.auto_ga2_button.config(state="normal")
        self.level_up_awaken_button.config(state="normal")
        self.auto_ready_button.config(state="normal")
        self.auto_farm_400_button.config(state="normal")
        self.auto_farm_gold_button.config(state="normal")

    def on_task_complete(self):
        self.auto_ga2.running = True
        self.enable_all_buttons()
        self.disable_stop_button()


if __name__ == "__main__":
    # Khởi tạo cửa sổ chính
    root = tk.Tk()

    # Khởi tạo lớp AutoUI
    app = Ga2UI(root)

    # Thiết lập các tỷ lệ chiều rộng của các cột
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Thiết lập các tỷ lệ chiều cao của các hàng
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Chạy giao diện
    root.mainloop()
