# 父亲大跳跃自动跳跃脚本
运行脚本前请确保已安装Python解释器

## 使用

在电脑上打开游戏，横向最小窗口，然后运行 `start.bat` 脚本：

```bash
./start.bat
```

## 参数调整

在 `config.json` 中，有两个参数 `DETECTION_LENGTH` 和 `TOLERANCE` ，你可以根据实际情况调整这两个参数来优化跳跃的时机。

- `DETECTION_LENGTH`：检测长度，图像识别检测长度，越大跳跃越慢。
- `TOLERANCE`：误差范围，边缘检测误差值，越小跳跃越慢。

## 注意事项

- 运行脚本时，关闭微信聊天窗口，不要移动或最小化游戏窗口，否则脚本可能无法正常工作。
- 这个脚本可能无法在所有电脑上正常运行，因为它依赖于特定的屏幕分辨率和游戏设置。
- 请根据自己电脑情况调整脚本参数
- 启动脚本后，Ctrl+C以停止项目。

## 贡献

haocong.jin

## 联系作者

Archeruuu@gmail.com