#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绘制符合论文figure3要求的电导分量分解图
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置更专业的绘图风格
plt.style.use('default')

# 设置字体，确保中文和数学符号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['mathtext.fontset'] = 'stix'  # 使用STIX字体，支持数学符号
plt.rcParams['mathtext.default'] = 'it'  # 数学符号使用斜体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置颜色方案（符合学术论文要求）
colors = {
    'et': '#1f77b4',      # 蓝色 - ET分量
    'lar': '#ff7f0e',     # 橙色 - LAR分量
    'total': '#2ca02c',   # 绿色 - 总电导
    'reference': '#7f7f7f', # 灰色 - 参考线
}

# 设置线条样式
line_styles = {
    'solid': '-',
    'dashed': '--',
    'dotted': ':',
    'dashdot': '-.'
}

def load_conductance_data():
    """加载电导数据"""
    try:
        # 加载总电导数据
        data_total = np.loadtxt('Conductance_data_origin.txt')
        
        # 加载ET分量数据
        data_et = np.loadtxt('Conductance_ET_data.txt')
        
        # 加载LAR分量数据
        data_lar = np.loadtxt('Conductance_LAR_data.txt')
        
        return data_total, data_et, data_lar
    except FileNotFoundError as e:
        print(f"数据文件未找到: {e}")
        print("请先运行主程序生成数据文件")
        return None, None, None

def plot_figure3():
    """绘制figure3电导分量分解图"""
    
    # 加载数据
    data_total, data_et, data_lar = load_conductance_data()
    
    if data_total is None:
        print("无法加载数据，退出绘图")
        return
    
    # 创建图形
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # 提取数据
    omega_total = data_total[:, 0]
    conductance_total = data_total[:, 1]
    
    omega_et = data_et[:, 0]
    conductance_et = data_et[:, 1]
    
    omega_lar = data_lar[:, 0]
    conductance_lar = data_lar[:, 1]
    
    # 绘制各分量
    ax.plot(omega_et, conductance_et, 
            color=colors['et'], 
            linewidth=2, 
            label='$G_{\\mathrm{ET}}$',
            linestyle=line_styles['solid'])
    
    ax.plot(omega_lar, conductance_lar, 
            color=colors['lar'], 
            linewidth=2, 
            label='$G_{\\mathrm{LAR}}$',
            linestyle=line_styles['dashed'])
    
    ax.plot(omega_total, conductance_total, 
            color=colors['total'], 
            linewidth=3, 
            label='$G_{\\mathrm{total}}$',
            linestyle=line_styles['solid'])
    
    # 添加零线参考
    ax.axhline(y=0, color=colors['reference'], linewidth=1, alpha=0.5, linestyle=line_styles['dotted'])
    
    # 设置坐标轴
    ax.set_xlabel('能量 $\\omega$ ($\\Omega_0$)', fontsize=14)
    ax.set_ylabel('电导 $G$ ($e^2/h$)', fontsize=14)
    ax.set_title('电导分量分解分析', fontsize=16, pad=20)
    
    # 设置坐标轴范围
    ax.set_xlim(-2, 2)
    ax.set_ylim(-0.1, 0.5)
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle=line_styles['dotted'])
    
    # 添加图例
    ax.legend(fontsize=12, loc='upper right', framealpha=0.9)
    
    # 设置刻度
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # 添加物理说明
    ax.text(0.02, 0.98, '物理说明:', 
            transform=ax.transAxes, 
            fontsize=12, 
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.8))
    
    ax.text(0.02, 0.88, '• ET: 弹性隧穿分量\\n• LAR: 局域Andreev反射\\n• Total: 总电导', 
            transform=ax.transAxes, 
            fontsize=10, 
            verticalalignment='top')
    
    plt.tight_layout()
    
    # 保存图像
    plt.savefig('figure3.png', dpi=300, bbox_inches='tight')
    plt.savefig('figure3.pdf', bbox_inches='tight')
    plt.savefig('figure3.eps', bbox_inches='tight')
    
    plt.show()
    
    return fig

def plot_phi_dependence():
    """绘制电导随磁通量相位变化图"""
    
    # 这里可以扩展为加载不同phi值的数据
    # 目前使用固定数据演示
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # 示例数据 - 实际应用中应从多个数据文件加载
    omega = np.linspace(-2, 2, 100)
    
    # 模拟不同phi值的电导
    phi_values = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
    phi_labels = ['$0$', '$\\pi/2$', '$\\pi$', '$3\\pi/2$', '$2\\pi$']
    
    for i, phi in enumerate(phi_values):
        # 模拟电导随phi的变化（实际应从数据文件读取）
        conductance = 0.25 * np.exp(-(omega)**2/0.5) * (1 + 0.5 * np.cos(phi))
        
        ax.plot(omega, conductance, 
                linewidth=2, 
                label=f'$\\phi = {phi_labels[i]}$')
    
    ax.set_xlabel('能量 $\\omega$ ($\\Omega_0$)', fontsize=14)
    ax.set_ylabel('电导 $G$ ($e^2/h$)', fontsize=14)
    ax.set_title('电导随磁通量相位变化', fontsize=16, pad=20)
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 0.4)
    
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig('figure3_phi_dependence.png', dpi=300, bbox_inches='tight')
    plt.savefig('figure3_phi_dependence.pdf', bbox_inches='tight')
    
    plt.show()
    
    return fig

if __name__ == "__main__":
    print("开始绘制电导分量分解图...")
    
    # 绘制主要图形
    fig1 = plot_figure3()
    
    # 绘制相位依赖性图形
    fig2 = plot_phi_dependence()
    
    print("绘图完成！")
    print("生成的文件:")
    print("- figure3.png: 主要电导分量分解图")
    print("- figure3.pdf: PDF版本")
    print("- figure3.eps: EPS版本（适合论文投稿）")
    print("- figure3_phi_dependence.png: 相位依赖性分析图")
    print("- figure3_phi_dependence.pdf: PDF版本")