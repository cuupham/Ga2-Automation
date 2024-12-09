import pygetwindow as gw
from pygetwindow import Win32Window
import time
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui

# from time import sleep
from typing import Callable, Optional
import os


class Ga2:
    def __init__(self):
        self.ga2_window: Win32Window = gw.getWindowsWithTitle("GETAMPED 2")[0]

        # Button in game
        self.btn_left = "j"
        self.btn_right = "l"
        self.btn_up = "i"
        self.btn_down = "k"

        self.btn_aim = "z"
        self.btn_strong_attack = "x"
        self.btn_weak_attack = "c"
        self.btn_jump = "v"
        self.btn_weapon = "space"

        # Image Path
        self.all_area_btn = r"img\all_area_btn.png"

        self.running = True

    def focus_window(self):
        self.ga2_window.activate()

    def move_top_left(self):
        self.ga2_window.moveTo(0, 0)

    def activate_ga2(self):
        self.focus_window()
        self.move_top_left()
        pyautogui.move(30, 30)

    def waiting(self, sleep_delay):
        start_time = time.perf_counter()
        while self.running:
            elapsed_time = time.perf_counter() - start_time
            if elapsed_time >= sleep_delay:

                break
            time.sleep(0.05)

    def click_coordinate(self, coordinate: tuple, time_delay=0.5):
        if self.running:
            try:
                pyautogui.mouseDown(x=coordinate[0], y=coordinate[1])
                self.waiting(time_delay)
            finally:
                pyautogui.mouseUp(x=coordinate[0], y=coordinate[1])
                pyautogui.move(20, 20, 0.1)

    def press_key(self, keyword: str, time_delay=0.0):
        if self.running:
            try:
                pyautogui.keyDown(key=keyword)
                self.waiting(time_delay)
            finally:
                pyautogui.keyUp(key=keyword)

    def find_image(
        self,
        image_path: str,
        timeout=5.0,
        threshold=0.8,
        search_region=(0, 0, 850, 650),
    ):
        template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if template.shape[2] == 4:  # Kiểm tra xem ảnh có kênh alpha không
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        else:
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]

        start_time = time.perf_counter()
        # image_found = False
        while time.perf_counter() - start_time < timeout and self.running:
            screen = np.array(ImageGrab.grab(bbox=search_region))
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(gray_screen, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                print(
                    f"=> Found {image_path} at location: {max_loc} in {timeout} sec(s)!"
                )
                center_x = max_loc[0] + w // 2 + search_region[0]
                center_y = max_loc[1] + h // 2 + search_region[1]
                # image_found = True
                return center_x, center_y
        print(f"No {image_path} found in {timeout} sec(s).")
        return None

    def find_and_click_image(
        self,
        image_path: str,
        timeout=5.0,
        threshold=0.8,
        search_region=(0, 0, 850, 650),
    ):
        coor = self.find_image(
            image_path=image_path,
            timeout=timeout,
            threshold=threshold,
            search_region=search_region,
        )
        if coor:
            self.click_coordinate(coor)
            return True
        return False

    def find_images(
        self,
        image_paths: list,
        timeout=5.0,
        threshold=0.8,
        search_region=(0, 0, 850, 650),
    ):
        templates = []
        for image_path in image_paths:
            template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if template.shape[2] == 4:  # Kiểm tra xem ảnh có kênh alpha không
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
            else:
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            templates.append(template_gray)

        start_time = time.perf_counter()
        while time.perf_counter() - start_time < timeout and self.running:
            screen = np.array(ImageGrab.grab(bbox=search_region))
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            for template in templates:
                # So sánh ảnh màn hình với từng template
                result = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                # Nếu giá trị tương đồng cao hơn threshold, có thể coi là tìm thấy template
                if max_val >= threshold:
                    print(
                        f"=> Found {image_paths} at location: {max_loc} with score {max_val} in {timeout} sec(s)."
                    )
                    # Tính toán tọa độ trung tâm của khu vực trùng khớp
                    w, h = template.shape[::-1]
                    center_x = max_loc[0] + w // 2 + search_region[0]
                    center_y = max_loc[1] + h // 2 + search_region[1]

                    return center_x, center_y

        print(f"No match found in {timeout} sec(s).")
        return None


class Gat(Ga2):
    def __init__(self):
        super().__init__()

        # Image Path
        self.ready_1_btn = r"img\gat\ready_1.png"
        self.ready_2_btn = r"img\gat\ready_2.png"
        self.reject_1_btn = r"img\gat\reject_1.png"
        self.reject_2_btn = r"img\gat\reject_2.png"
        self.start_time = r"img\gat\start_time.png"
        self.end_time = r"img\gat\end_time.png"
        self.close_point_gat = r"img\gat\close_point.png"
        self.close_reward = r"img\gat\close_reward.png"
        self.close_event_reward = r"img\gat\close_reward.png"

    def ready(self, func: Optional[Callable] = None):
        self.activate_ga2()
        ready_btn = self.find_images([self.ready_1_btn, self.ready_2_btn], 1)
        point = self.find_image(self.close_point_gat, 1)

        if ready_btn:
            if point:
                self.get_reward(point)
            self.click_coordinate(ready_btn)
            if self.find_images([self.reject_1_btn, self.reject_2_btn], 1):
                if func:
                    func()
        elif self.find_images([self.reject_1_btn, self.reject_2_btn], 2):
            if func:
                func()
            else:
                self.waiting(10)

    def get_reward(self, coor: tuple):
        self.activate_ga2()
        self.click_coordinate(coor)
        i = 1
        while i <= 4 and self.running:
            self.press_key("enter", 0.5)
            i += 1

        self.find_and_click_image(self.close_event_reward, 1)

    def start_game(self):
        self.activate_ga2()
        pyautogui.keyUp(self.btn_right)
        pyautogui.keyUp(self.btn_up)
        pyautogui.keyUp(self.btn_aim)

        # Di chuyen len truoc
        i = 1
        while i <= 8 and self.running:
            # for _ in range(6):
            self.press_key(self.btn_up)
            self.waiting(0.6)
            i += 1

        # Di chuyen cheo
        i = 1
        while i <= 20 and self.running:
            # for _ in range(20):
            self.press_key(self.btn_up)
            self.press_key(self.btn_right)
            self.press_key(self.btn_aim)
            i += 1

        pyautogui.keyDown(self.btn_aim)
        pyautogui.keyDown(self.btn_up)
        pyautogui.keyDown(self.btn_right)
        # pyautogui.keyUp(self.btn_right)
        # pyautogui.keyUp(self.btn_up)
        # pyautogui.keyUp(self.btn_aim)

    def attack_opponent_near_fall(self, num=18):
        self.attack_opponent_after(num)
        # pyautogui.keyUp(self.btn_right)
        # pyautogui.keyUp(self.btn_up)

    def attack_opponent(self, num=30):
        try:
            self.activate_ga2()
            # pyautogui.keyDown(self.btn_aim)
            i = 1
            while i <= num and self.running:
                # for _ in range(num):
                self.press_key(self.btn_strong_attack)
                self.waiting(0.8)
                i += 1
        finally:
            pyautogui.keyUp(self.btn_right)
            pyautogui.keyUp(self.btn_up)
            pyautogui.keyUp(self.btn_aim)

    def attack_opponent_after(self, num=30):
        # try:
        self.activate_ga2()
        # pyautogui.keyDown(self.btn_aim)
        i = 1
        while i <= num and self.running:
            # for _ in range(num):
            self.press_key(self.btn_strong_attack)
            self.waiting(0.8)
            i += 1

    def finish_hits(self, number=10):
        self.attack_opponent_after(number)
        pyautogui.keyUp(self.btn_right)
        pyautogui.keyUp(self.btn_up)
        pyautogui.keyUp(self.btn_aim)

    def farm_400(self):
        self.activate_ga2()
        if self.find_image(self.start_time, 100):
            self.start_game()
            self.attack_opponent_near_fall()
            print("Sleep 50s")
            self.waiting(50)
            if self.find_image(self.end_time, 30):
                self.finish_hits()
                self.waiting(10)

    def farm_gold(self):
        self.activate_ga2()
        if self.find_image(self.start_time, 100):
            self.start_game()
            self.attack_opponent()
            self.waiting(10)


class KhuOChuot(Ga2):
    def __init__(self):
        super().__init__()

        # Image Path
        self.khu_o_chuot_area = r"img\khu_o_chuot\khu_o_chuot_area.png"
        self.exit_1 = r"img\khu_o_chuot\exit_1.png"
        self.exit_2 = r"img\khu_o_chuot\exit_2.png"
        self.room = r"img\khu_o_chuot\room.png"
        self.start = r"img\khu_o_chuot\start.png"
        self.close_point = r"img\khu_o_chuot\close_point.png"

    def go_to_area(self, area_coor):
        self.click_coordinate(area_coor)
        khu_o_chuot_area = self.find_image(self.khu_o_chuot_area)
        if khu_o_chuot_area:
            # self.find_and_click_image(self.khu_o_chuot_area)
            self.click_coordinate(khu_o_chuot_area)
            self.waiting(2)
            self.find_and_click_image(self.room)
        # self.find_and_click_image(self.start, 8)

    def exit_area(self):
        self.find_and_click_image(self.exit_1)
        self.waiting(6)

        i = 1
        while i <= 2 and self.running:
            # for _ in range(3):
            self.find_and_click_image(self.exit_2, 2)
            point = self.find_image(self.close_point, 3)
            if point:
                self.click_coordinate(point)
                self.click_coordinate(point)
                # self.press_key("enter")
                return True
            # pyautogui.move(0, 30)
            i += 1
        return False

    def self_destruct(self):
        i = 1
        while i <= 2 and self.running:
            # for _ in range(2):
            self.press_key(self.btn_right)
            i += 1

        self.waiting(1)
        self.press_key(self.btn_weapon)

        self.waiting(1)
        i = 1
        while i <= 5 and self.running:
            # for _ in range(5):
            self.press_key(self.btn_right)
            i += 1

    def farm_10_exp_for_awaken(self):
        i = 1
        while i <= 9 and self.running:
            self.activate_ga2()
            all_area_btn = self.find_image(self.all_area_btn, 8)
            if all_area_btn:
                self.go_to_area(all_area_btn)
                start_khu_o_chuot = self.find_image(self.start, 11)
                if start_khu_o_chuot:
                    self.click_coordinate(start_khu_o_chuot)
                    self.waiting(2.5)
                    self.self_destruct()
                    result = self.exit_area()
                    if result:
                        print(f"[LOGGING]: Đã hoàn thành {i}/10 trận - Awaken Skill\n")
                        i += 1
            else:
                print("[ERROR]: Cửa sổ GA2 chưa ở vị trí hiển thị nút All Area.")
            self.waiting(2)
        else:
            print("Exiting...")


class PhongThiNghiem(Ga2):
    def __init__(self):
        super().__init__()

        # Image Path
        self.phong_thi_nghiem_area = r"img\phong_thi_nghiem\phong_thi_nghiem_area.png"
        self.agree_btn_1 = r"img\phong_thi_nghiem\agree_btn_1.png"
        self.agree_btn_2 = r"img\phong_thi_nghiem\agree_btn_2.png"
        self.awaken_btn = r"img\phong_thi_nghiem\awaken_btn.png"
        self.close_btn = r"img\phong_thi_nghiem\close_btn.png"
        self.price_250w = r"img\phong_thi_nghiem\price_250w.png"
        self.skip_btn = r"img\phong_thi_nghiem\skip_btn.png"
        self.level_up_awaken_btn = r"img\phong_thi_nghiem\level_up_awaken_btn.png"
        self.awaken_option = r"img\phong_thi_nghiem\awaken_option.png"
        self.next_page = r"img\phong_thi_nghiem\next_page.png"
        self.exit_option = r"img\phong_thi_nghiem\exit_option.png"
        self.awaken_skill_level_20 = r"img\phong_thi_nghiem\awaken_skill_level_20.png"

    def go_to_awaken_section(self, coor):
        self.click_coordinate(coor)
        phong_thi_nghiem_area = self.find_image(self.phong_thi_nghiem_area)
        if phong_thi_nghiem_area:
            # self.find_and_click_image(self.phong_thi_nghiem_area)
            self.click_coordinate(phong_thi_nghiem_area)
            self.find_and_click_image(self.skip_btn)
            self.find_and_click_image(self.awaken_option)
            self.find_and_click_image(self.skip_btn)

    def process_awaken(self):
        self.find_and_click_image(self.awaken_btn)
        price_250w_btn = self.find_image(self.price_250w, 3)
        if price_250w_btn:
            self.waiting(1)
            self.find_and_click_image(self.next_page)
            self.waiting(1)
            self.find_and_click_image(self.agree_btn_1)
            self.waiting(1)
            self.find_and_click_image(self.skip_btn)
            self.waiting(1)
            self.find_and_click_image(self.agree_btn_2)
            self.waiting(4)
            self.find_and_click_image(self.close_btn)
            self.waiting(2)
            self.find_and_click_image(self.skip_btn)
            self.waiting(1)
            self.find_and_click_image(self.exit_option)
            self.waiting(1)
            self.find_and_click_image(self.skip_btn)
        else:
            print(f"[ERROR]: Có lỗi xảy ra khi thức tỉnh trang bị")

    def level_up_awaken(self):
        if self.find_image(self.awaken_skill_level_20, 1.5):
            print("Trang bị đã thức tỉnh full lv20")
            self.running = False
        else:
            awaken_btn = self.find_image(self.level_up_awaken_btn)
            if awaken_btn:
                self.click_coordinate(awaken_btn)
                i = 1
                while i <= 3 and self.running:
                    # for _ in range(3):
                    self.find_and_click_image(self.next_page)
                    # pyautogui.move(20, 20)
                    i += 1

                self.waiting(1.5)
                self.press_key("enter")
                self.waiting(1.5)
                self.find_and_click_image(self.agree_btn_1)
                self.waiting(1.5)
                self.find_and_click_image(self.skip_btn)
                self.waiting(1.5)
                self.find_and_click_image(self.agree_btn_2)
                self.waiting(3)
                self.find_and_click_image(self.close_btn)
                self.waiting(1.5)
                self.find_and_click_image(self.skip_btn)
                self.waiting(1.5)
                self.find_and_click_image(self.exit_option)
                self.waiting(1.5)
                self.find_and_click_image(self.skip_btn)

    def awakening_accessory(self):
        self.activate_ga2()
        all_area_visible = self.find_image(self.all_area_btn, 8)
        if all_area_visible:
            self.go_to_awaken_section(all_area_visible)
            self.process_awaken()
        else:
            print("[ERROR]")

    def upgrade_awaken(self):
        self.activate_ga2()
        all_area_visible = self.find_image(self.all_area_btn, 8)
        if all_area_visible:
            self.go_to_awaken_section(all_area_visible)
            self.level_up_awaken()
        else:
            print("[ERROR]")


class AutoGa2(KhuOChuot, PhongThiNghiem, Gat):
    def __init__(self):
        super().__init__()

    # Auto Awaken
    def auto_farm_10_exp_awaken(self):
        self.farm_10_exp_for_awaken()
        self.awakening_accessory()

    def auto_farm_lv10_to_lv20_awaken(self):
        i = 1
        # for i in range(10):
        while i <= 10 and self.running:
            self.farm_10_exp_for_awaken()
            self.upgrade_awaken()
            # print(f"Up Awaken Skill Lv{i+10}/20")
            i += 1

    # Auto Gat
    def run_auto_task(self, task_function):
        try:
            while self.running:
                task_function()
                self.waiting(1)
            else:
                print("Stop loop")
        except Exception as e:
            print(f"[ERROR]: {e}")
            os.system("pause")

    def auto_ready(self):
        self.run_auto_task(self.ready)

    def auto_farm_400(self):
        self.run_auto_task(lambda: self.ready(self.farm_400))

    def auto_farm_gold(self):
        self.run_auto_task(lambda: self.ready(self.farm_gold))
