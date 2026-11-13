# 射电望远镜 3D 模型

根据单张参考图制作的可打印简化模型，保留了抛物面反射面、焦点馈源、背部桁架、俯仰转轴、锥形转台和四脚底座。

## 文件

- `generated/radio_telescope.3mf`：推荐使用，Bambu Studio 可直接打开；包含反射面、桁架和底座三个分色对象。
- `generated/radio_telescope_A1_190pct.3mf`：为 Bambu Lab A1 热床准备的 190% 大尺寸版，约 233 × 212 × 230 mm。
- `generated/radio_telescope_A1_190pct_supported.3mf`：已在 Bambu Studio 中开启“树状（自动）”支撑并完成切片验证的项目版，推荐直接使用。
- `generated/radio_telescope_plate1_base_A1.3mf`：两盘打印版的第一盘，底座四脚直接接触热床。
- `generated/radio_telescope_plate2_dish_A1.3mf`：两盘打印版的第二盘，碟口朝上、连接环直接接触热床。
- `generated/radio_telescope.stl`：通用单文件备份格式。
- `generated/radio_telescope_preview.png`：模型预览。

模型包围尺寸约为 123 × 111 × 121 mm。它是基于单视角图片的摆件级重建，不是天线工程模型。结构按 0.4 mm 喷嘴的 FDM 打印能力做了加粗，但整体姿态仍需要支撑；建议使用树状支撑，并在 Bambu Studio 中先检查薄壁和悬空区域。

两盘打印版为 190% 尺寸。第一盘约 127 × 127 × 139 mm；第二盘约 233 × 233 × 90 mm。第二盘已经把天线轴线旋转为竖直方向，让连接环直接落在热床上；打印完成后，将底座插接柱插入天线背部连接环，并用瞬干胶或环氧胶固定。

重新生成：

```bash
uv run labs/radio-telescope-model/generate_radio_telescope.py
```
