# ROS 2 机器人测试环境 · 使用说明

> 搭建时间：2026-11-10 晚 ｜ 位置：**F 盘**（C 盘只占了几 MB 注册表项）

---

## 1. 装了什么东西

| 组件 | 版本 | 位置 |
|---|---|---|
| WSL2 发行版 `ROS2-Humble` | Ubuntu 22.04 LTS | `F:\WSL\ROS2-Humble\ext4.vhdx`（约 7.8 GB） |
| ROS 2 Humble Desktop | 0.10.0 | `/opt/ros/humble` |
| Gazebo（新版，gz sim / Fortress） | 6.18.0 | 命令 `ign gazebo` |
| Gazebo Classic | 11.10.2 | 命令 `gazebo` |
| Nav2 / nav2_bringup | Humble | `/opt/ros/humble` |
| slam_toolbox | Humble | `/opt/ros/humble` |
| ros_gz_bridge / ros_gz_sim | Humble（桥接 Fortress） | `/opt/ros/humble` |
| 工作区 | — | `F:\ros_workspace` ↔ `/mnt/f/ros_workspace` |

Python 3.10.12，已装 colcon、rosdep、pytest。

**你原来那个 Ubuntu 发行版没动**，还在 C 盘（3.4 GB），随时可切回去。

---

## 2. 怎么进来

**方式一（推荐）**：双击 `F:\ros_workspace\start_ros2.bat`

**方式二**：任意 PowerShell / Windows Terminal 输入

```powershell
wsl            # 默认发行版已改成 ROS2-Humble
```

进来后：

- 用户 `hjx`，密码 `hjx123456`，`sudo` 免密
- 已自动 `source /opt/ros/humble/setup.bash`，并 `cd` 到 `/mnt/f/ros_workspace`
- 想回到原来的 Ubuntu：`wsl -d Ubuntu`

---

## 3. 已验证跑通的东西（不是"应该能跑"，是真跑过）

| 验证项 | 结果 |
|---|---|
| `talker` / `listener` 收发 | ✅ 收到 `Hello World: 6` |
| `colcon build --symlink-install` | ✅ demo_py 编译通过 |
| `colcon test`（pytest 集成用例） | ✅ 1 passed |
| `rviz2` 图形界面 | ✅ 弹窗正常，OpenGL 4.1（WSLg） |
| Gazebo Fortress 无界面跑 300 帧 | ✅ exit 0 |
| gz 仿真 → ROS 2 `/clock` 桥接 | ✅ 收到仿真时间 sec=9 |

---

## 4. 立刻可以敲的命令

```bash
# 1) 官方 demo：两个窗口，先 talker 再 listener
ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_cpp listener

# 2) 自己的包（等价于 14 周计划 W2 的产物）
ros2 run demo_py talker
ros2 run demo_py listener
ros2 pkg executables demo_py

# 3) 仿真：无界面（快，适合 CI）
ign gazebo -s -r /usr/share/ignition/ignition-gazebo6/worlds/shapes.sdf

# 4) 仿真：有界面（会弹一个 3D 窗口）
ign gazebo /usr/share/ignition/ignition-gazebo6/worlds/shapes.sdf

# 5) 经典 Gazebo（教程最多，TurtleBot3 那套用它）
gazebo --verbose

# 6) 可视化
rviz2
```

**看话题**：`ros2 topic list`、`ros2 topic hz /clock`、`ros2 topic echo /clock --once`

---

## 5. 工作区与常用命令

```
/mnt/f/ros_workspace/
├── src/demo_py/        # 示例包：talker / listener / pytest 集成测试
├── build/  install/  log/   # colcon 产物（可随时删了重编）
├── start_ros2.bat      # 一键进入环境
└── 机器人测试岗_14周学习与投递计划.xlsx
```

```bash
cd /mnt/f/ros_workspace
colcon build --symlink-install     # 编译全部
source install/setup.bash          # 让当前终端找到新包
colcon test --packages-select demo_py
colcon test-result --verbose
```

新建包：`ros2 pkg create --build-type ament_python my_test_pkg --dependencies rclpy std_msgs`

---

## 6. 几个坑，先记住

1. **别用 Windows 记事本 / 带 BOM 的编辑器保存 `.sh`、`.py`**，CRLF 会让 Linux 报 `bad interpreter`。VS Code 右下角切成 `LF`。
2. **`/mnt/f` 是跨系统挂载，编译大 C++ 包会明显变慢**；纯 Python 包无感。真要编译大包，把源码放 `~/` 下。
3. **不要同时开太多 Gazebo 实例**，16 GB 内存会吃紧。
4. 图形窗口靠 WSLg，关掉窗口 = 关掉进程；卡住了用 `pkill -f rviz2` / `pkill -f gazebo`。
5. C 盘那个 36 MB 的 `swap.vhdx` 是本次会话的临时文件；已经写了 `C:\Users\pc\.wslconfig`，**下次 `wsl --shutdown` 或重启后** swap 会落到 `F:\WSL\swap.vhdx`。

---

## 7. 不想要了怎么删

```powershell
wsl --unregister ROS2-Humble        # 删除发行版（数据全没，谨慎）
wsl --set-default Ubuntu            # 恢复原来的默认发行版
```

然后手动删 `F:\WSL` 目录即可。

---

## 8. 下一步（对应 14 周计划的 W1→W2）

- [ ] 用 `ros2 topic hz /clock` 观察仿真频率，理解"仿真时间 ≠ 墙上时间"
- [ ] 照着 `src/demo_py` 改一个自己的包：发布一个 `sensor_msgs/LaserScan` 假数据
- [ ] 把 `test/test_talker.py` 改成"启动节点 → 收 3 帧 → 断言频率"，这就是 W2 的验收物
- [ ] 把仓库 `git init` 提交，作为 `ros2-test-lab` 的第一版

做完这四步，W2 的产出就齐了，可以开始投第一批实习。
