from django.test import TestCase

# Create your tests here.

import random
import requests
numberran = random.sample(range(1,100),5)
print(numberran)
randomselect = random.sample(range(0,5),2)
l={"val":numberran,"choice":randomselect}
x=requests.post("http://localhost:8000/bet/addbet/",data={"val":numberran[0],"rr":numberran[1],"kkk":numberran[2],"kk":numberran[3],"k":numberran[4],
"e":randomselect[0],"ee":randomselect[1]})
print(x.status_code)