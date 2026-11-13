# 射电望远镜 3D 模型

根据单张参考图制作的可打印简化模型，保留了抛物面反射面、焦点馈源、背部桁架、俯仰转轴、锥形转台和四脚底座。

## 文件

- `generated/radio_telescope.3mf`：推荐使用，Bambu Studio 可直接打开；包含反射面、桁架和底座三个分色对象。
- `generated/radio_telescope.stl`：通用单文件备份格式。
- `generated/radio_telescope_preview.png`：模型预览。

模型约为 120 × 121 × 123 mm。它是基于单视角图片的摆件级重建，不是天线工程模型。结构按 0.4 mm 喷嘴的 FDM 打印能力做了加粗，但整体姿态仍需要支撑；建议使用树状支撑，并在 Bambu Studio 中先检查薄壁和悬空区域。

重新生成：

```bash
uv run labs/radio-telescope-model/generate_radio_telescope.py
```
