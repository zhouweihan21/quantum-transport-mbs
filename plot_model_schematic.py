#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量子输运模型示意图绘制脚本
展示小极化子变换框架下的量子点-马约拉纳零能模耦合系统
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Arc
import matplotlib.font_manager as fm

# 设置中文字体和数学符号
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['mathtext.fontset'] = 'stix'  # 使用STIX字体，支持数学符号
plt.rcParams['mathtext.default'] = 'it'  # 数学符号使用斜体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置绘图参数
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

def draw_model_schematic():
    """绘制量子输运模型示意图"""
    fig = plt.figure(figsize=(16, 10))
    
    # 创建网格布局：左侧示意图，右侧参数和方程
    gs = fig.add_gridspec(2, 2, width_ratios=[1.2, 0.8], height_ratios=[1, 1], 
                          hspace=0.3, wspace=.03)
    
    # 左侧：模型示意图
    ax_schematic = fig.add_subplot(gs[:, 0])
    ax_schematic.set_xlim(-2, 12)
    ax_schematic.set_ylim(-2, 8)
    ax_schematic.set_aspect('equal')
    ax_schematic.axis('off')
    ax_schematic.set_title('量子输运模型示意图', fontsize=16, pad=20)
    
    # 左侧电极（绘制左导线）
    left_electrode = patches.Rectangle((-1.5, 2), 1, 4, linewidth=2,
                                       edgecolor='darkblue', facecolor='lightblue', alpha=0.6)
    ax_schematic.add_patch(left_electrode)
    ax_schematic.text(-1, 4, '左电极\n(L)', ha='center', va='center', fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.8))
    
    # 右侧电极（绘制右导线）
    right_electrode = patches.Rectangle((10.5, 2), 1, 4, linewidth=2,
                                        edgecolor='darkblue', facecolor='lightblue', alpha=0.6)
    ax_schematic.add_patch(right_electrode)
    ax_schematic.text(11, 4, '右电极\n(R)', ha='center', va='center', fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.8))
    
    # 绘制量子点（中心）
    quantum_dot = Circle((4.5, 4), 1.2, linewidth=3, edgecolor='darkgreen', 
                         facecolor='lightgreen', alpha=0.8, zorder=5)
    ax_schematic.add_patch(quantum_dot)
    ax_schematic.text(4.5, 4, '量子点\n(QD)', ha='center', va='center', fontsize=12,
                      bbox=dict(boxstyle='circle,pad=0.5', facecolor='lightgreen', alpha=0.9))
    
    # 绘制马约拉纳零能模（两个小红圈）
    mbs1 = Circle((2., 6.55), 0.5, linewidth=2, edgecolor='darkred', 
                  facecolor='red', alpha=0.7, zorder=4)
    mbs2 = Circle((6.5, 6.5), 0.5, linewidth=2, edgecolor='darkred', 
                  facecolor='red', alpha=0.7, zorder=4)
    ax_schematic.add_patch(mbs1)
    ax_schematic.add_patch(mbs2)
    ax_schematic.text(2., 7.2, '$\\gamma_1$', ha='center', va='center', fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.8))
    ax_schematic.text(6.5, 7.2, '$\\gamma_2$', ha='center', va='center', fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.8))
    
    # 绘制耦合箭头
    # QD-左电极耦合
    arrow_l_qd = FancyArrowPatch((-0.5, 4), (3.3, 4), 
                                 arrowstyle='->', mutation_scale=20, 
                                 color='blue', linewidth=2, alpha=0.8)
    ax_schematic.add_patch(arrow_l_qd)
    ax_schematic.text(1.5, 4.5, '$\\Gamma_L$', ha='center', va='bottom', fontsize=10,
                      color='blue', fontweight='bold')
    
    # QD-右电极耦合
    arrow_qd_r = FancyArrowPatch((5.7, 4), (10.5, 4), 
                                 arrowstyle='->', mutation_scale=20, 
                                 color='blue', linewidth=2, alpha=0.8)
    ax_schematic.add_patch(arrow_qd_r)
    ax_schematic.text(8, 4.5, '$\\Gamma_R$', ha='center', va='bottom', fontsize=10,
                      color='blue', fontweight='bold')
    
    # QD-MBS1耦合
    arrow_qd_mbs1 = FancyArrowPatch((3.5, 4.8), (1.5, 6.1), 
                                    arrowstyle='->', mutation_scale=15, 
                                    color='red', linewidth=2, alpha=0.8)
    ax_schematic.add_patch(arrow_qd_mbs1)
    ax_schematic.text(2.5, 5.2, '$\\lambda_1$', ha='center', va='center', fontsize=10,
                      color='red', fontweight='bold')
    
    # QD-MBS2耦合
    arrow_qd_mbs2 = FancyArrowPatch((5.5, 4.8), (6., 6.), 
                                    arrowstyle='->', mutation_scale=15, 
                                    color='red', linewidth=2, alpha=0.8)
    ax_schematic.add_patch(arrow_qd_mbs2)
    ax_schematic.text(5.8, 5.2, '$\\lambda_2$', ha='center', va='center', fontsize=10,
                      color='red', fontweight='bold')
    
    # MBS1-MBS2耦合（虚线表示拓扑超导）
    arrow_mbs1_mbs2 = FancyArrowPatch((2.5, 6.5), (6., 6.5), 
                                      arrowstyle='<->', mutation_scale=15, 
                                      color='purple', linewidth=2, alpha=0.7, linestyle='--')
    ax_schematic.add_patch(arrow_mbs1_mbs2)
    ax_schematic.text(4.25, 6.8, '$E_M$', ha='center', va='center', fontsize=10,
                      color='purple', fontweight='bold')
    
    # 绘制磁通量（AB环）
    flux_ring = Arc((4.5, 2), 6, 3, theta1=0, theta2=360, 
                    linewidth=2, edgecolor='orange', facecolor='none', alpha=0.6)
    ax_schematic.add_patch(flux_ring)
    ax_schematic.text(4.5, 0.5, '磁通量 $\\Phi$', ha='center', va='center', fontsize=10,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='orange', alpha=0.8))
    ax_schematic.text(4.5, 1.2, '$\\phi = 2\\pi\\Phi/\\Phi_0$', ha='center', va='center', fontsize=9,
                      color='orange')
    
    # 右侧上方：参数表格
    ax_params = fig.add_subplot(gs[0, 1])
    ax_params.axis('off')
    ax_params.set_title('物理参数设置', fontsize=14, pad=10)
    
    # 创建参数表格
    parameters = [
        ['参数', '符号', '数值', '单位'],
        ['特征声子能量', '$\\Omega_0$', '1.0', '$E_0$'],
        ['左电极耦合', '$\\Gamma_L$', '0.05', '$\\Omega_0$'],
        ['右电极耦合', '$\\Gamma_R$', '0.05', '$\\Omega_0$'],
        ['磁通量相位', '$\\phi$', '$\\pi$', 'rad'],
        ['QD-MBS耦合1', '$\\lambda_1$', '1.0', '$\\Omega_0$'],
        ['QD-MBS耦合2', '$\\lambda_2$', '1.0', '$\\Omega_0$'],
        ['Majorana能级', '$E_M$', '0.0', '$\\Omega_0$'],
        ['温度', '$k_BT$', '0.1', '$\\Omega_0$'],
        ['电声耦合', '$\\lambda_0$', '0.0', '$\\Omega_0$']
    ]
    
    # 绘制表格
    table = ax_params.table(cellText=parameters, 
                           loc='center', 
                           cellLoc='center',
                           colWidths=[0.25, 0.2, 0.2, 0.15])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    # 设置表格样式
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # 表头
            cell.set_facecolor('#4CAF50')
            cell.set_text_props(weight='bold', color='white')
        elif i % 2 == 1:  # 奇数行
            cell.set_facecolor('#E8F5E8')
        else:  # 偶数行
            cell.set_facecolor('#F5F5F5')
    
    # 右侧下方：关键方程
    ax_equations = fig.add_subplot(gs[1, 1])
    ax_equations.axis('off')
    ax_equations.set_title('关键方程', fontsize=14, pad=10)
    
    # 显示关键方程
    equations = [
        r'$H_{\text{eff}} = \varepsilon_d d^\dagger d + E_M \gamma_1\gamma_2$',
        r'$\quad + \lambda_1(d^\dagger - d)\gamma_1 + \lambda_2(d^\dagger + d)\gamma_2$',
        '',
        r'$G^r(\omega) = [\omega - H_{\text{eff}} - \Sigma^r(\omega)]^{-1}$',
        '',
        r'$\text{DOS}(\omega) = -\frac{1}{\pi}\text{Im}[G^r_{11}(\omega)]$',
        '',
        r'$I = \frac{e}{h}\int d\omega[f_L(\omega) - f_R(\omega)]T(\omega)$',
        '',
        r'$T(\omega) = \text{Tr}[\Gamma_L G^r \Gamma_R G^a]$'
    ]
    
    for i, eq in enumerate(equations):
        ax_equations.text(0.1, 0.9 - i*0.1, eq, fontsize=11, 
                         transform=ax_equations.transAxes, 
                         verticalalignment='top')
    
    # 添加模型说明
    ax_schematic.text(0.02, 0.98, '模型说明:', transform=ax_schematic.transAxes, 
                     fontsize=12, fontweight='bold', verticalalignment='top')
    
    notes = [
        '• 量子点(QD)作为中心散射区域',
        '• 马约拉纳零能模(MBS)提供拓扑保护',
        '• 电极耦合实现电子输运',
        '• 磁通量相位控制AB效应',
        '• 小极化子变换处理电声耦合'
    ]
    
    for i, note in enumerate(notes):
        ax_schematic.text(0.05, 0.90 - i*0.05, note, transform=ax_schematic.transAxes, 
                         fontsize=10, verticalalignment='top')
    
    plt.tight_layout()
    
    # 保存图像
    plt.savefig('model_schematic.png', dpi=300, bbox_inches='tight')
    plt.savefig('model_schematic.pdf', bbox_inches='tight')
    
    plt.show()
    
    return fig

if __name__ == "__main__":
    print("开始绘制量子输运模型示意图...")
    fig = draw_model_schematic()
    print("示意图绘制完成！已保存为 model_schematic.png 和 model_schematic.pdf")
    
    # 输出模型信息
    print("\n模型特征:")
    print("- 量子点能级: ε_d = 0")
    print("- 马约拉纳零能模: γ₁, γ₂")
    print("- 电极耦合强度: Γ_L = Γ_R = 0.05Ω₀")
    print("- 磁通量相位: φ = π")
    print("- QD-MBS耦合: λ₁ = λ₂ = 1.0Ω₀")
    print("- 温度: k_BT = 0.1Ω₀")