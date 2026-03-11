from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # === 背景資訊與控制變數 ===
    age = models.IntegerField(label='請問您的年齡為？ ( 請輸入阿拉伯數字 )', min=15, max=100)
    male = models.IntegerField(
        choices=[
            [1, '男'],
            [0, '女']
        ],
        label='請問您的性別為何？',
        widget=widgets.RadioSelectHorizontal
    )
    econ_or_bz = models.IntegerField(
        label='請問您是否有「經濟或商管」領域相關知識？',
        choices=[[1, '是'], [0, '否']],
        widget=widgets.RadioSelectHorizontal
    )
    env = models.IntegerField(
        label='請問您是否有「環境科學」領域相關知識？',
        choices=[[1, '是'], [0, '否']],
        widget=widgets.RadioSelectHorizontal
    )

    # 價值觀與偏好
    main_goal = models.StringField(
        label='請問在整個實驗中，您決定生產量時，最主要考慮的目標是？',
        choices=['利潤最大化',  '綜合考慮利潤與碳排（多考慮利潤）', '綜合考慮利潤與碳排（多考慮碳排）','碳排最少'],
        widget=widgets.RadioSelectHorizontal
    )

    respond_to_high_others = models.IntegerField(
        label='當您看到其他受試者碳排放（或生產量）很多時，您通常會怎麼做？',
        choices=[
            [-2, '排放（生產）少很多'],
            [-1, '排放（生產）少一點'],
            [0, '不受影響，維持原策略'],
            [1, '排放（生產）多一點'],
            [2, '排放（生產）多很多']
        ],
        widget=widgets.RadioSelectHorizontal
    )

    # carbon_trade 專屬題目
    carbon_trade_fairness = models.IntegerField(
        label='請問您認為第二部分碳權交易制度在「公平性」方面的表現如何？',
        choices=[[1, '非常不公平'], [2, '不太公平'], [3, '普通'], [4, '公平'], [5, '非常公平']],
        widget=widgets.RadioSelectHorizontal
    )
    carbon_trade_efficiency = models.IntegerField(
        label='請問您認為第二部分碳權交易制度在「經濟效率」方面的表現如何？',
        choices=[[1, '非常沒效率'], [2, '沒效率'], [3, '普通'], [4, '有效率'], [5, '非常有效率']],
        widget=widgets.RadioSelectHorizontal
    )
    carbon_trade_environment = models.IntegerField(
        label='請問您認為第二部分碳權交易制度在「減碳／改善環境」方面的效果',
        choices=[[1, '完全沒幫助'], [2, '幫助很小'], [3, '普通'], [4, '有幫助'], [5, '非常有效']],
        widget=widgets.RadioSelectHorizontal
    )
    carbon_trade_mkt_power = models.IntegerField(
        label='請問在第二部分碳權交易制度中，若您是產量上限高的大廠商，您是否會嘗試壓低碳權的價格？',
        choices=[[1, '不會'], [2, '可能不會'], [3, '不確定'], [4, '可能會'], [5, '會']],
        widget=widgets.RadioSelectHorizontal
    )
    
    env_job_type = models.StringField(
        label='您的相關工作主要屬於下列哪一類？（可依您目前或最主要的工作經驗勾選一項）',
        choices=[
            '企業內部永續、ESG、環安衛或環境管理人員',
            '顧問、查證、會計師事務所或其他專業服務人員',
            'NGO、倡議、研究或政策推動相關人員',
            '綠能、節能或環境技術解決方案公司人員',
            '其他與減碳、碳資訊或環境管理有關的工作者',
            '其他'
        ],
        widget=widgets.RadioSelect
    )

    env_job_type_other = models.StringField(
        label='若選擇「其他」，請填寫：',
        blank=True
    )
    

    work_experience = models.IntegerField(label='您從事上述相關工作的累計年資約為多久？(請填入阿拉伯數字)', min=0, max=80)
    
    ind_risk = models.IntegerField(
        label='在涉及財務的決策中，我個人較傾向選擇風險較低、結果較穩定的方案。（請根據敘述與實際情況的符合程度作出選擇)',
        choices=[[1, '非常不同意'], [2, '不同意'], [3, '普通'], [4, '同意'], [5, '非常同意']],
        widget=widgets.RadioSelectHorizontal
    )
    prevention_climate = models.IntegerField(
        label='在我的工作環境中，工作決策著重於「避免造成金錢或資源上的損失」。（請根據敘述與實際情況的符合程度作出選擇)',
        choices=[[1, '非常不同意'], [2, '不同意'], [3, '普通'], [4, '同意'], [5, '非常同意']],
        widget=widgets.RadioSelectHorizontal
    )
    performance_pressure = models.IntegerField(
        label='在我的工作環境中，為了創造良好收益而承受的工作壓力很高。（請根據敘述與實際情況的符合程度作出選擇)',
        choices=[[1, '非常不同意'], [2, '不同意'], [3, '普通'], [4, '同意'], [5, '非常同意']],
        widget=widgets.RadioSelectHorizontal
    )
    emission_experience = models.IntegerField(
        label='請問您是否有涉及碳排放相關的工作經驗？您的相關經驗年數為？( 請輸入阿拉伯數字，若無請填寫 0 )', min=0, max=80)

    ipas = models.IntegerField(
        label='請問您是否有過iPAS淨零碳規劃師的證照嗎？',
        choices=[[1, '是'], [2, '否']],
        widget=widgets.RadioSelectHorizontal
    )
    trade_experience = models.IntegerField(label='請問您在「工作上」是否有任何形式的市場交易經驗（如金融商品等即時交易）？您的交易年數為？( 請輸入阿拉伯數字，若無請填寫 0 )', min=0, max=80)

# === 頁面設定 ===
class Survey(Page):
    
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        return [
            'age', 'male', 'econ_or_bz', 'env',
            'main_goal', 'respond_to_high_others',
            'carbon_trade_fairness', 'carbon_trade_efficiency', 'carbon_trade_environment',
            'carbon_trade_mkt_power',
            'env_job_type', 'env_job_type_other','work_experience',
            'ind_risk','prevention_climate','performance_pressure',
            'emission_experience','ipas',
            'trade_experience'
        ]

    ##############################0301#新增(0301只是方便統一尋找修改的地方，正確更新時間是3/12)
    @staticmethod
    def error_message(player, values):
        env_job_type = values.get('env_job_type')
        env_job_type_other = values.get('env_job_type_other')

        if env_job_type_other:
            env_job_type_other = env_job_type_other.strip()

        # 把錯誤掛在「其他說明」欄位，而不是整頁最上方
        if env_job_type == '其他' and not env_job_type_other:
            return {'env_job_type_other': '您勾選了「其他」，請填寫具體工作類別。'}

        if env_job_type != '其他' and env_job_type_other:
            return {'env_job_type_other': '只有在勾選「其他」時才能填寫說明。'}

        return None
    #######################################
    
class ByePage(Page):
    def is_displayed(player):
        return True

page_sequence = [Survey, ByePage]