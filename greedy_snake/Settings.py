"""定数宣言用のファイル
"""


#mapのvalueが同じときこの優先順位で動く
MOVES = ["down", "left", "right", "up"]
#場外
OUTSIDE_THE_FRAME_VALUE = -128
#body
NEG_INF = -100
#foodの周囲
AROUND_FOOD_VALUE = -1
#food
FOOD_VALUE = -5
#餌が食べられないパス
CANNOT_EAT_FOOD_VALUE = -50
