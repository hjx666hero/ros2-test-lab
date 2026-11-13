# ros2-test-lab

一个从零搭起来的 ROS 2 测试实验台：把"看起来正常"变成"跑得过 / 跑不过"。

## 这个仓库在做什么

机器人测试和 Web 测试最大的区别是：**被测对象输出的是连续信号，不是一次请求的响应**。
所以测试重点从"返回值对不对"，变成"频率对不对、延迟多大、丢没丢帧"。

这个仓库是这条思路的最小实现：

- 发布者节点 `talker`：固定周期发消息
- 订阅者节点 `listener`：接收并打印
- 两条 pytest 用例：
  - `test_publish_and_receive` —— 能不能收到
  - `test_talker_rate` —— **到达间隔是否落在 0.4 ~ 0.6 秒**

第二条是关键：它把 `ros2 topic hz` 的人眼观察，变成了 CI 里会自动变红的断言。

## 环境

- Ubuntu 22.04（WSL2）
- ROS 2 Humble
- Python 3.10 / colcon / pytest

## 快速开始

```bash
# 编译
colcon build --symlink-install
source install/setup.bash

# 运行
ros2 run demo_py talker
ros2 run demo_py listener

# 测试
colcon test --packages-select demo_py
colcon test-result --verbose
```

## 目录结构

```
src/demo_py/
├── demo_py/talker.py      # 0.5s 周期发布
├── demo_py/listener.py    # 订阅并打印
├── test/test_talker.py    # 2 条用例
├── package.xml
└── setup.py
```

## 验证过的事

- 把 `talker.py` 里的周期改成 `0.2`，`test_talker_rate` 会失败：
  `AssertionError: 期望间隔约 0.5 秒，实际 0.20 秒`
- 改回 `0.5` 后恢复通过

这条"故意弄坏 → 看到红 → 修好 → 回到绿"的记录，比一句"测试通过"更能说明用例是有效的。

## 接下来

- [ ] Gazebo 场景化回归：批量跑起点 / 障碍组合，统计到达率与碰撞率
- [ ] rosbag2 数据校验：话题频率、时间戳单调性、TF 连续性
- [ ] 故障注入：杀节点、加网络延迟、QoS 不匹配，验证系统降级
