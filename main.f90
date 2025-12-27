! 小极化子变换框架下量子点输运计算程序
! 基于非平衡格林函数方法实现电子-声子耦合系统的输运性质计算

! 参数定义模块 
module constant 
    implicit none 
    ! 物理常数 
    double precision, parameter :: pi = 3.141592653589793d0 
    
    ! 特征声子能量（单位：能量）（1mev）（默认hbar Omega 0） 
    double precision, parameter :: OMEGA_0 = 1.0d0 
    
    ! 物理参数 - 不加电声耦合，lambda_0设为0
    double precision, parameter :: lambda_0 = 0.0d0 * OMEGA_0  ! 不加电声耦合，设为0
    
    ! 电极耦合强度 - 减小耦合强度使能级更尖锐
    double precision, parameter :: Garmma_L = 0.05d0 * OMEGA_0  ! 减小左电极耦合强度 
    double precision, parameter :: Garmma_R = 0.05d0 * OMEGA_0  ! 减小右电极耦合强度
    
    ! 化学势 - 不加电压，设为0
    double precision, parameter :: mu_electron = 0.0d0 * OMEGA_0  ! 电子化学势，不加电压设为0 
  
    ! 数值计算参数 
    integer, parameter :: Nw = 20000          ! 能量范围扩展到-20到20，增加积分点数
    integer, parameter :: Nph = 10            ! 声子截断数设置为10
    double precision, parameter :: dw = 2e-3 * OMEGA_0    ! 保持相同的能量分辨率
    double precision, parameter :: eta = 1e-6            ! 增加小虚部以提高数值稳定性
    
    ! 物理单位
    double precision, parameter :: h = 1.0d0     ! 普朗克常数
    double precision, parameter :: e = 1.0d0     ! 电子电荷
    
    ! 测试参数 - 可通过主程序配置
    double precision :: phi = 3.14159d0 ! 磁通量相位，默认值为pi
    double precision :: KT_eq = 1.0d0 * OMEGA_0 ! 温度参数
    double precision :: Beta                     ! 增加系统温度参数 1/(k_B T_eq)，运行时计算
    double precision :: E_M = 0.0d0 ! Majorana能级
    double precision :: lambda_1 = 1.0d0 * OMEGA_0 ! QD-MBS耦合强度
    double precision :: lambda_2 = 1.0d0 * OMEGA_0 ! QD-MBS耦合强度
    
end module constant

module functions
    use constant
    implicit none
    
contains
    
    ! 声子统计函数
    real(8) function Boson(kT)
        implicit none
        real(8) :: kT
        if (kT < 1e-10) then
            Boson = 0.0d0
        else
            Boson = 1.0d0 / (exp(OMEGA_0/kT) - 1.0d0)
        endif
    end function Boson
    
    ! 阶乘函数
    real(8) function factorial(n)
        implicit none
        integer :: n, i
        real(8) :: result
        result = 1.0d0
        if (n < 0) then
            factorial = 0.0d0
            return
        endif
        do i = 1, n
            result = result * i
        enddo
        factorial = result
    end function factorial
    
    ! 小极化子变换因子
    real(8) function Ln(n, lambda_0, Omega_0)
        implicit none
        integer :: n
        real(8) :: lambda_0, Omega_0
        Ln = exp(-(lambda_0/Omega_0)**2/2) * (lambda_0/Omega_0)**n / sqrt(factorial(n))
    end function Ln
    
    ! 费米-狄拉克分布函数
    real(8) function Fermi(omega, mu, kT)
        implicit none
        real(8) :: omega, mu, kT
        if (kT < 1e-10) then
            if (omega < mu) then
                Fermi = 1.0d0
            else
                Fermi = 0.0d0
            endif
        else
            Fermi = 1.0d0 / (exp((omega - mu)/kT) + 1.0d0)
        endif
    end function Fermi
    
end module functions

program main
    use constant
    use functions
    implicit none
    
    ! 变量定义
    integer :: i, j, k, m, n, p, q, r, s, t, u, v, w
    real(8) :: omega, dos, current, conductance, G_tilde
    real(8) :: G11r, G12r, G21r, G22r, G11a, G12a, G21a, G22a
    real(8) :: A11, A12, A21, A22, T_total, T_elastic, T_inelastic
    real(8) :: sum_Ln, sum_dos, sum_current, sum_conductance
    real(8) :: H_eff(2,2), Sigma_r(2,2), Sigma_a(2,2), G_r(2,2), G_a(2,2)
    real(8) :: Gamma_L(2,2), Gamma_R(2,2), Gamma_total(2,2)
    real(8) :: identity(2,2), temp_matrix(2,2)
    
    ! 文件输出
    open(unit=10, file='DOS_data_origin.txt', status='replace')
    open(unit=11, file='Current_data_origin.txt', status='replace')
    open(unit=12, file='Conductance_data_origin.txt', status='replace')
    open(unit=13, file='G_tilde_values.txt', status='replace')
    open(unit=14, file='Ln_data_origin.txt', status='replace')
    open(unit=15, file='results.txt', status='replace')
    
    ! 初始化单位矩阵
    identity = 0.0d0
    identity(1,1) = 1.0d0
    identity(2,2) = 1.0d0
    
    ! 初始化电极耦合矩阵
    Gamma_L = 0.0d0
    Gamma_L(1,1) = Garmma_L
    Gamma_R = 0.0d0
    Gamma_R(1,1) = Garmma_R
    Gamma_total = Gamma_L + Gamma_R
    
    ! 计算温度参数
    Beta = 1.0d0 / KT_eq
    
    ! 输出参数信息
    write(15,*) '量子输运计算参数设置:'
    write(15,*) '特征声子能量 Omega_0 = ', OMEGA_0
    write(15,*) '电子-声子耦合强度 lambda_0 = ', lambda_0
    write(15,*) '左电极耦合强度 Gamma_L = ', Garmma_L
    write(15,*) '右电极耦合强度 Gamma_R = ', Garmma_R
    write(15,*) '磁通量相位 phi = ', phi
    write(15,*) '温度参数 kT = ', KT_eq
    write(15,*) 'Majorana能级 E_M = ', E_M
    write(15,*) 'QD-MBS耦合强度 lambda_1 = ', lambda_1
    write(15,*) 'QD-MBS耦合强度 lambda_2 = ', lambda_2
    write(15,*) ''
    
    ! 主循环：计算不同能量下的输运性质
    do i = -Nw/2, Nw/2
        omega = i * dw
        
        ! 构建有效哈密顿量
        H_eff = 0.0d0
        H_eff(1,1) = omega  ! 量子点能级
        H_eff(2,2) = E_M    ! Majorana能级
        H_eff(1,2) = lambda_1 * cos(phi/2) - lambda_2 * sin(phi/2)  ! QD-MBS耦合
        H_eff(2,1) = H_eff(1,2)  ! 对称性
        
        ! 计算自能
        Sigma_r = -0.5d0 * cmplx(0.0d0, 1.0d0) * Gamma_total
        Sigma_a = conjg(Sigma_r)
        
        ! 计算推迟格林函数 G_r = [omega - H_eff - Sigma_r]^{-1}
        temp_matrix = (omega + cmplx(0.0d0, eta)) * identity - H_eff - Sigma_r
        call invert_2x2(temp_matrix, G_r)
        
        ! 计算超前格林函数 G_a = [G_r]^\dagger
        G_a = conjg(transpose(G_r))
        
        ! 计算谱函数 A = i(G_r - G_a)
        A11 = imag(G_r(1,1) - G_a(1,1))
        A12 = imag(G_r(1,2) - G_a(1,2))
        A21 = imag(G_r(2,1) - G_a(2,1))
        A22 = imag(G_r(2,2) - G_a(2,2))
        
        ! 计算态密度 DOS = -Im(G_r)/pi
        dos = -imag(G_r(1,1)) / pi
        
        ! 计算透射系数 T(omega) = Tr[Gamma_L G_r Gamma_R G_a]
        T_total = 0.0d0
        do j = 1, 2
            do k = 1, 2
                T_total = T_total + Gamma_L(j,j) * abs(G_r(j,k))**2 * Gamma_R(k,k)
            enddo
        enddo
        
        ! 计算电流（Landauer公式）
        current = (e/h) * T_total * (Fermi(omega, mu_electron, KT_eq) - Fermi(omega, mu_electron, KT_eq))
        
        ! 计算电导（零偏压极限）
        conductance = (e**2/h) * T_total
        
        ! 计算G_tilde值（用于声子辅助跃迁）
        G_tilde = abs(G_r(1,1))**2
        
        ! 输出数据
        write(10,*) omega, dos
        write(11,*) omega, current
        write(12,*) omega, conductance
        write(13,*) omega, G_tilde
        
        ! 计算声子展开系数
        sum_Ln = 0.0d0
        do n = 0, Nph
            sum_Ln = sum_Ln + Ln(n, lambda_0, OMEGA_0)**2
            write(14,*) omega, n, Ln(n, lambda_0, OMEGA_0)
        enddo
        
    enddo
    
    ! 关闭文件
    close(10)
    close(11)
    close(12)
    close(13)
    close(14)
    close(15)
    
    write(*,*) '计算完成！结果已保存到输出文件。'
    
contains
    
    ! 2x2矩阵求逆子程序
    subroutine invert_2x2(A, A_inv)
        implicit none
        real(8) :: A(2,2), A_inv(2,2)
        real(8) :: det
        
        det = A(1,1)*A(2,2) - A(1,2)*A(2,1)
        
        if (abs(det) < 1e-10) then
            A_inv = 0.0d0
        else
            A_inv(1,1) = A(2,2) / det
            A_inv(1,2) = -A(1,2) / det
            A_inv(2,1) = -A(2,1) / det
            A_inv(2,2) = A(1,1) / det
        endif
        
    end subroutine invert_2x2
    
end program main