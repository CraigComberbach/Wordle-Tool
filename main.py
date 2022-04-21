from wordle import Wordle

qourdle_top_left = Wordle()
qourdle_top_left.add_bad_letters("")
qourdle_top_left.add_good_letters({0:[""],1:[""],2:[""],3:[""],4:[""]})
qourdle_top_left.add_known_letters({0:"",1:"",2:"",3:"",4:""})
qourdle_top_left.solve()
print(f"Top Left\t{len(qourdle_top_left):6d}\t{qourdle_top_left}")

qourdle_top_right = Wordle()
qourdle_top_right.add_bad_letters("")
qourdle_top_right.add_good_letters({0:[""],1:[""],2:[""],3:[""],4:[""]})
qourdle_top_right.add_known_letters({0:"",1:"",2:"",3:"",4:""})
qourdle_top_right.solve()
print(f"Top Right\t{len(qourdle_top_right):6d}\t{qourdle_top_right}")

qourdle_bottom_left = Wordle()
qourdle_bottom_left.add_bad_letters("")
qourdle_bottom_left.add_good_letters({0:[""],1:[""],2:[""],3:[""],4:[""]})
qourdle_bottom_left.add_known_letters({0:"",1:"",2:"",3:"",4:""})
qourdle_bottom_left.solve()
print(f"Bottom Left\t{len(qourdle_bottom_left):6d}\t{qourdle_bottom_left}")

qourdle_bottom_right = Wordle()
qourdle_bottom_right.add_bad_letters("")
qourdle_bottom_right.add_good_letters({0:[""],1:[""],2:[""],3:[""],4:[""]})
qourdle_bottom_right.add_known_letters({0:"",1:"",2:"",3:"",4:""})
qourdle_bottom_right.solve()
print(f"Bottom Right{len(qourdle_bottom_right):6d}\t{qourdle_bottom_right}")
