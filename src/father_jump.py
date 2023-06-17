import pygetwindow as gw
import cv2
import numpy as np
import pyautogui
import time
import json

# Load the configuration file
with open("../config.json", "r") as f:
    config = json.load(f)

# Get the values for DETECTION_LENGTH and TOLERANCE
DETECTION_LENGTH = config["DETECTION_LENGTH"]
TOLERANCE = config["TOLERANCE"]

def get_game_window(title):
    try:
        return gw.getWindowsWithTitle(title)[0]
    except IndexError:
        return None

def capture_image(window):
    # 使用PyAutoGUI捕获特定窗口的图像
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    # 将图像转换为OpenCV可以处理的格式
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return img

def process_image(img):
    # 将图像转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 应用阈值
    _, thresh = cv2.threshold(gray, 169, 255, cv2.THRESH_BINARY_INV)
    return thresh

def find_platforms_backup(img, game_window):
    # 计算裁剪区域
    top = game_window.top + 555
    bottom = game_window.top + 580

    # 裁剪图像，只保留我们关心的垂直范围
    img = img[top:bottom, :]
    
    # 保存裁剪后的图片到项目根目录
    cv2.imwrite('cropped.png', img)
    
    # 使用OpenCV寻找轮廓
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 在图像上绘制所有找到的轮廓
    cv2.drawContours(img, contours, -1, (0,255,0), 3)

    # 对于每个轮廓，绘制其边界框
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

    # 保存带有轮廓和边界框的图像
    cv2.imwrite('contours_and_boxes.png', img)
    
    platforms = []
    for contour in contours:
        # 获取轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        # print(x, y, w, h)
        # 如果边界框的宽度和高度满足条件，那么它可能是一个平台 (179, 8)
        if 100 < w < 200 and 10 < h:
            print(x, y, w, h)
            platforms.append((x, x + w))

    if platforms.__len__() > 0:
        print(platforms)
    
    return platforms

def click_center(window):
    # 获取窗口的位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    # 计算中心点的坐标
    center_x = x + width // 2
    center_y = y + height // 2

    # 在中心点进行点击
    pyautogui.click(center_x, center_y)

def get_relative_position(window, screen_x):
    # 获取窗口的左上角x坐标
    window_x = window.left

    # 计算相对于窗口的x坐标
    relative_x = screen_x - window_x

    return relative_x

def find_platforms(img, game_window):
    # 计算裁剪区域
    top = game_window.top + 530
    bottom = game_window.top + 580

    # 裁剪图像，只保留我们关心的垂直范围
    img = img[top:bottom, :]
    # 保存裁剪后的图片到项目根目录
    # cv2.imwrite('cropped.png', img)
    
    # 定义平台颜色的上下界（你需要根据实际情况调整这些值）
    lower = np.array([198, 206, 86])
    upper = np.array([200, 208, 88])
    
    # 创建掩模
    mask = cv2.inRange(img, lower, upper)

    # 保存掩模
    # cv2.imwrite('mask.png', mask)

    # 使用OpenCV寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask, contours, -1, (0,255,0), 3)
    
    platforms = []
    for contour in contours:
        # 获取轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        
        # 如果边界框的宽度和高度满足条件，那么它可能是一个平台 (179, 8)
        if DETECTION_LENGTH < w:
            cv2.rectangle(mask, (x, y), (x+w, y+h), (255,0,0), 2)
            # print(x, y, w, h)
            platforms.append((x, x + w))

    cv2.imwrite('contours_and_boxes.png', mask)

    # if platforms.__len__() > 0:
    #     print(platforms)

    return platforms

def should_jump(platforms, character):
    # 判断是否应该跳跃
    should_jump = False
    for platform in platforms:
        if -50 < character[0] - platform[1] <= TOLERANCE:  # 如果平台的右边缘与角色的左边缘在误差范围内
            should_jump = True
            # print(f'命中的左跳时机：{platform[0]},{platform[1]}')
        if -50 < platform[0] - character[1] <= TOLERANCE:  # 如果平台的左边缘与角色的右边缘在误差范围内
            should_jump = True
            # print(f'命中的右跳时机：{platform[0]},{platform[1]}')
        
    
    return should_jump

def main():
    game_window = get_game_window('微信')
    if game_window is not None:
        game_window.activate()
        while True:
            img = capture_image(game_window)  # 使用game_window
            # 保存图片到项目根目录
            # cv2.imwrite('gamewindow.png', img)
            # processed = process_image(img)
            # 保存处理图片到项目根目录
            # cv2.imwrite('processed.png', processed)
            platforms = find_platforms(img, game_window)
            # 获取相对于游戏窗口的坐标
            # character_platform_left = get_relative_position(game_window, 601)
            # character_platform_right = get_relative_position(game_window, 780)
            # character_platform = (character_platform_left, character_platform_right)
            character_platform = (180, 370)
            if should_jump(platforms, character_platform):
                # 在游戏窗口的中央进行点击
                # a = 1
                click_center(game_window)
    else:
        print("Game window not found.")

if __name__ == "__main__":
    main()
