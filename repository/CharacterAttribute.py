class CharacterAttribute:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 0
        self.hp_max = 0
        self.mp = 0
        self.mp_max = 0
        self.exp = 0
        self.next_exp = 0
        # 判断人物是否读取了游戏信息flag，防止使用的时候出现判断异常
        self.init_flag = False
