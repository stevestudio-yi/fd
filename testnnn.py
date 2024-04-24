class IDM:
    def __init__(self, max_velocity, desired_time_headway, minimum_spacing, acceleration, comfortable_deceleration):
        self.max_velocity = max_velocity  # 最大速度
        self.desired_time_headway = desired_time_headway  # 期望时间间隔
        self.minimum_spacing = minimum_spacing  # 最小间隔
        self.acceleration = acceleration  # 加速度
        self.comfortable_deceleration = comfortable_deceleration  # 舒适减速度

    def calculate_acceleration(self, delta_v, s_star, current_spacing):
        """
        计算加速度
        :param delta_v: 相对速度
        :param s_star: 期望间隔
        :param current_spacing: 当前间隔
        :return: 加速度
        """
        term1 = self.acceleration * (1 - (delta_v / self.max_velocity)**4)
        term2 = (self.acceleration * (s_star / current_spacing)**2)
        return term1 - term2

    def update_velocity(self, current_velocity, acceleration, time_step):
        """
        更新速度
        :param current_velocity: 当前速度
        :param acceleration: 加速度
        :param time_step: 时间步长
        :return: 新的速度
        """
        return max(0, current_velocity + acceleration * time_step)

    def update_position(self, current_position, current_velocity, time_step):
        """
        更新位置
        :param current_position: 当前位置
        :param current_velocity: 当前速度
        :param time_step: 时间步长
        :return: 新的位置
        """
        return current_position + current_velocity * time_step

    def desired_gap(self, current_velocity, delta_v):
        """
        计算期望间隔
        :param current_velocity: 当前速度
        :param delta_v: 相对速度
        :return: 期望间隔
        """
        s0 = self.minimum_spacing
        T = self.desired_time_headway
        a = self.acceleration
        b = self.comfortable_deceleration
        term1 = s0 + current_velocity * T
        term2 = (current_velocity * delta_v) / (2 * (a * b)**0.5)
        return term1 + term2

# 示例使用
if __name__ == "__main__":
    # 初始化参数
    max_velocity = 33.33  # 最大速度 (120 km/h)
    desired_time_headway = 1.5  # 期望时间间隔 (s)
    minimum_spacing = 2.0  # 最小间隔 (m)
    acceleration = 0.3  # 加速度 (m/s^2)
    comfortable_deceleration = 0.2  # 舒适减速度 (m/s^2)

    # 创建IDM实例
    idm = IDM(max_velocity, desired_time_headway, minimum_spacing, acceleration, comfortable_deceleration)

    # 模拟参数
    time_step = 0.1  # 时间步长 (s)
    simulation_time = 60  # 模拟时间 (s)
    current_velocity = 0  # 当前速度 (m/s)
    current_position = 0  # 当前位置 (m)

    # 模拟循环
    for t in range(int(simulation_time / time_step)):
        # 假设前车速度为最大速度，当前车与前车间隔为50米
        lead_vehicle_velocity = max_velocity
        current_spacing = 50

        # 计算相对速度和期望间隔
        delta_v = lead_vehicle_velocity - current_velocity
        s_star = idm.desired_gap(current_velocity, delta_v)

        # 计算加速度
        acceleration = idm.calculate_acceleration(delta_v, s_star, current_spacing)

        # 更新速度和位置
        current_velocity = idm.update_velocity(current_velocity, acceleration, time_step)
        current_position = idm.update_position(current_position, current_velocity, time_step)

        # 打印结果
        print(f"Time: {t * time_step:.1f}s, Position: {current_position:.2f}m, Velocity: {current_velocity:.2f}m/s")

