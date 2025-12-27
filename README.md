# Quantum Transport with Majorana Bound States (MBS)

## 项目概述

这是一个基于**小极化子变换框架**的量子点输运计算程序，专门用于研究**量子点-马约拉纳零能模耦合系统**的输运性质。程序采用**非平衡格林函数方法**实现电子-声子耦合系统的数值计算。

## 🎯 主要特性

- **物理模型完整**：包含量子点、马约拉纳零能模、电极耦合、磁通量相位等关键物理要素
- **计算方法先进**：基于非平衡格林函数方法，支持声子辅助跃迁计算
- **可视化功能丰富**：提供多种绘图脚本，生成高质量的学术图表
- **测试框架完善**：包含完整的参数扫描和验证测试
- **中英双语支持**：代码注释和文档支持中文和英文

## 📁 项目结构

```
quantum-transport-mbs/
├── main.f90                    # Fortran主程序 - 核心计算模块
├── plot_model_schematic.py     # 模型示意图绘制脚本
├── plot_figure3.py             # 电导分量分解图绘制
├── plot_dos.py                 # 态密度分布图绘制
├── comprehensive_plots_fixed.py # 综合图表生成脚本
├── run_tests.py                # 自动化测试框架
├── generate_data.py            # 数据生成脚本
├── test_report.md              # 测试报告文档
├── DOS_analysis_report.md      # DOS分析报告
├── Physical_Authenticity_Analysis.md # 物理真实性分析
└── README.md                   # 项目说明文档
```

## 🔬 物理模型

### 核心组件

1. **量子点 (QD)**：中心散射区域，能级 ε_d = 0
2. **马约拉纳零能模 (MBS)**：两个Majorana算符 γ₁, γ₂，耦合强度 λ₁, λ₂
3. **电极耦合**：左电极(Γₗ)和右电极(Γᵣ)耦合强度均为0.05Ω₀
4. **磁通量相位**：AB环相位 φ = π，通过磁通Φ量控制
5. **电子-声子耦合**：小极化子变换处理，耦合强度 λ₀ = 0（当前关闭）
6. **温度效应**：系统温度 k_BT = 0.1Ω₀

### 关键方程

- **推迟格林函数**：Gʳ(ω) = [ω - H_eff - Σʳ(ω)]⁻¹
- **有效哈密顿量**：H_eff = ε_d d^†d + E_M γ₁γ₂ + λ₁(d^† - d)γ₁ + λ₂(d^† + d)γ₂
- **自能计算**：Σʳ(ω) = -i(Γₗ + Γᵣ)/2
- **态密度**：DOS(ω) = -Im Gʳ₁₁(ω)/π
- **电流公式**：I = (e/h)∫dω[fₗ(ω) - fᵣ(ω)]T(ω)

## 🚀 快速开始

### 环境要求

- **Fortran编译器**：gfortran 或 Intel Fortran
- **Python 3.7+**：用于数据可视化和分析
- **Python依赖**：numpy, matplotlib, scipy

### 安装依赖

```bash
pip install numpy matplotlib scipy
```

### 编译和运行

1. **编译Fortran程序**：
```bash
gfortran -O3 main.f90 -o quantum_transport.exe
```

2. **运行计算**：
```bash
./quantum_transport.exe
```

3. **生成可视化图表**：
```bash
python plot_model_schematic.py
python plot_dos.py
python plot_figure3.py
```

## 📊 输出文件

程序运行后生成以下数据文件：

- `DOS_data_origin.txt`：态密度数据
- `Current_data_origin.txt`：电流数据
- `Conductance_data_origin.txt`：电导数据
- `G_tilde_values.txt`：格林函数数据
- `Ln_data_origin.txt`：声子展开系数

## 🔍 测试和验证

项目包含完整的测试框架：

```bash
python run_tests.py
```

测试内容包括：
- 态密度随磁通量相位变化
- 电导分量分解分析
- 参数敏感性测试
- 数值稳定性验证

## 📈 可视化示例

### 模型示意图
![模型示意图](model_schematic.png)

### 态密度分布
![态密度分布](DOS_plot.png)

### 电导分量分解
![电导分量分解](figure3.png)

## 📚 技术细节

### 小极化子变换

程序采用小极化子变换处理电子-声子耦合：

```fortran
! 小极化子变换因子
real(8) function Ln(n, lambda_0, Omega_0)
    implicit none
    integer :: n
    real(8) :: lambda_0, Omega_0
    Ln = exp(-(lambda_0/Omega_0)**2/2) * (lambda_0/Omega_0)**n / sqrt(factorial(n))
end function Ln
```

### 非平衡格林函数方法

采用非平衡格林函数方法计算输运性质：

1. **推迟格林函数**：Gʳ(ω) = [ω - H_eff - Σʳ(ω)]⁻¹
2. **超前格林函数**：Gᵃ(ω) = [Gʳ(ω)]†
3. **谱函数**：A(ω) = i[Gʳ(ω) - Gᵃ(ω)]
4. **透射系数**：T(ω) = Tr[ΓₗGʳΓᵣGᵃ]

## 🤝 贡献指南

欢迎贡献代码和文档！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至项目维护者

## 🙏 致谢

感谢以下开源项目的启发和参考：

- [Quantum Transport Toolkit](https://github.com/quantum-toolkit)
- [Non-equilibrium Green's Function Methods](https://github.com/NEGF-methods)
- [Majorana Physics Simulations](https://github.com/majorana-simulations)

---

**注意**：本项目为学术研究用途，计算结果需结合具体物理背景进行解释。