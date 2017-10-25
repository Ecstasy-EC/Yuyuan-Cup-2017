# Yuyuan-Cup-2017
Repository for Yuyuan Cup in 2017

##上位机方块识别使用说明
1.连接上wifcar的摄像头，并将窗口调置最大化
2.在python中打开CubeRecog.py，按F5运行
3.调整各窗口位置，保证wifcar的显示框不被其他窗口遮挡，点击显示的实时录像框，按'y'键
4.在5秒后将显示出识别框，查看方块踪是否对准
5.在python中打开TaskExecution，设置波特率和通讯端口（默认为COM12和9600，此操作不需要保证不挡住wifcar的显示框）
6.运行TaskExecution，在7秒内迅速调整窗口位置，不遮挡wifcar显示框

