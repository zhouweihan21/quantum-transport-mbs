#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量子点输运计算结果可视化脚本
用于绘制DOS曲线，复现PRB论文Figure 2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import argparse
from matplotlib.ticker import AutoMinorLocator

# 设置字体支持，避免符号乱码
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False  # 禁用外部LaTeX，使用Matplotlib内置渲染
plt.rcParams['mathtext.fontset'] = 'stix'  # 使用STIX字体渲染数学符号


def read_data_file(file_path):
    """读取数据文件，返回能量和DOS数据"""
    print(f"读取数据文件: {file_path}")
    
    try:
        # 读取文件，跳过中文标题行
        data = np.loadtxt(file_path, skiprows=1, encoding='gbk')
        
        energy = data[:, 0]
        dos = data[:, 1]
        
        return energy, dos
        
    except UnicodeDecodeError:
        # 如果GBK编码失败，尝试其他编码
        try:
            data = np.loadtxt(file_path, skiprows=1, encoding='utf-8')
            energy = data[:, 0]
            dos = data[:, 1]
            return energy, dos
        except:
            # 最后尝试无编码读取
            data = np.loadtxt(file_path, skiprows=1)
            energy = data[:, 0]
            dos = data[:, 1]
            return energy, dos
    except Exception as e:
        print(f"读取文件错误: {e}")
        return None, None


def plot_dos_single(energy, dos, output_file='DOS_plot.png', title='量子点态密度分布'):
    """绘制单个DOS图像"""
    
    # 创建图形
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # 绘制DOS曲线
    ax.plot(energy, dos, linewidth=2, color='#1f77b4', label='DOS')
    
    # 设置坐标轴标签和标题
    ax.set_xlabel('能量 $\\omega$ ($\\Omega_0$)', fontsize=14)
    ax.set_ylabel('态密度 DOS($\\omega$)', fontsize=14)
    ax.set_title(title, fontsize=16)
    
    # 设置坐标轴范围
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, max(dos) * 1.1)
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 添加图例
    ax.legend(fontsize=12)
    
    # 添加次要刻度
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    # 设置刻度标签大小
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=8)
    
    # 添加零线
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
    
    # 添加物理参数说明
    ax.text(0.02, 0.98, '物理参数:', 
            transform=ax.transAxes, 
            fontsize=12, 
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.8))
    
    ax.text(0.02, 0.88, '• $\\Gamma_L = \\Gamma_R = 0.05\\Omega_0$\\n• $\\phi = \\pi$\\n• $\\lambda_1 = \\lambda_2 = 1.0\\Omega_0$', 
            transform=ax.transAxes, 
            fontsize=10, 
            verticalalignment='top')
    
    plt.tight_layout()
    
    # 保存图像
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.savefig(output_file.replace('.png', '.pdf'), bbox_inches='tight')
    
    plt.show()
    
    return fig


def plot_dos_multiple(energy_list, dos_list, labels, output_file='DOS_plots.png'):
    """绘制多个DOS曲线对比"""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # 定义颜色方案
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (energy, dos, label) in enumerate(zip(energy_list, dos_list, labels)):
        color = colors[i % len(colors)]
        ax.plot(energy, dos, linewidth=2, color=color, label=label)
    
    ax.set_xlabel('能量 $\\omega$ ($\\Omega_0$)', fontsize=14)
    ax.set_ylabel('态密度 DOS($\\omega$)', fontsize=14)
    ax.set_title('不同参数下的态密度分布', fontsize=16)
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, max([max(dos) for dos in dos_list]) * 1.1)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=12)
    
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=8)
    
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
    
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.savefig(output_file.replace('.png', '.pdf'), bbox_inches='tight')
    
    plt.show()
    
    return fig


def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(description='量子点输运计算结果可视化')
    parser.add_argument('--data_file', default='DOS_data_origin.txt', 
                       help='数据文件路径 (默认: DOS_data_origin.txt)')
    parser.add_argument('--output', default='DOS_plot.png', 
                       help='输出图像文件名 (默认: DOS_plot.png)')
    parser.add_argument('--title', default='量子点态密度分布', 
                       help='图像标题 (默认: 量子点态密度分布)')
    
    args = parser.parse_args()
    
    print("开始绘制DOS曲线...")
    
    # 读取数据
    energy, dos = read_data_file(args.data_file)
    
    if energy is None or dos is None:
        print("无法读取数据文件，退出")
        return
    
    print(f"数据范围: 能量 [{min(energy):.2f}, {max(energy):.2f}], DOS [{min(dos):.4f}, {max(dos):.4f}]")
    
    # 绘制图像
    fig = plot_dos_single(energy, dos, args.output, args.title)
    
    print(f"绘图完成！图像已保存为: {args.output}")
    print(f"同时生成了PDF版本: {args.output.replace('.png', '.pdf')}")
    
    # 输出统计信息
    print("\n统计信息:")
    print(f"- 峰值位置: {energy[np.argmax(dos)]:.4f}")
    print(f"- 峰值高度: {max(dos):.4f}")
    print(f"- 半高全宽: {calculate_fwhm(energy, dos):.4f}")


def calculate_fwhm(energy, dos):
    """计算半高全宽"""
    max_dos = max(dos)
    half_max = max_dos / 2
    
    # 找到半高位置
    above_half = dos > half_max
    indices = np.where(above_half)[0]
    
    if len(indices) > 0:
        left_idx = indices[0]
        right_idx = indices[-1]
        fwhm = energy[right_idx] - energy[left_idx]
        return fwhm
    else:
        return 0


if __name__ == "__main__":
    main()