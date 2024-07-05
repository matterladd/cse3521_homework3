import argparse
import csv
from itertools import chain
import math
#import matplotlib.pyplot as plt
#import numpy as np
from random import random
import sys

def check_q1():
  import prob_inf
  prob_inf.DEBUG_OUTPUT=0
  
  print('\n-------------------------------------------------------')
  print(' Checking Question 1: Joint Probability')
  print('-------------------------------------------------------')
  
  print('Loading model file burglary_alarm.csv ...')
  model=prob_inf.read_model_file('burglary_alarm.csv')

  print('\nChecking function calc_global_joint_prob() ...')
  
  error_cnt=0
  
  #Generate
  # plst=[]
  # for jptEntry in prob_inf.truefalse_combination_iterator(model.vars):
    # plst.append( prob_inf.calc_global_joint_prob(model,jptEntry) )
  # print(repr(plst))
  
  #Check
  plst=[0.9367427006189999, 0.009462047481, 0.049302247401000004, 0.0004980024990000001, 0.00133417449, 1.3476510000000001e-05, 7.021971e-05, 7.0929e-07, 5.6317140000000054e-05, 5.688600000000006e-07, 2.964060000000003e-06, 2.994000000000003e-08, 9.405000000000008e-08, 9.500000000000009e-10, 4.950000000000005e-09, 5.0000000000000054e-11, 2.991006e-05, 6.979013999999999e-05, 0.0002691905400000001, 0.00062811126, 1.73826e-05, 4.055939999999999e-05, 0.00015644340000000003, 0.0003650346, 2.8143599999999996e-05, 6.566839999999998e-05, 0.00025329240000000004, 0.0005910156, 5.6999999999999994e-08, 1.3299999999999996e-07, 5.130000000000001e-07, 1.197e-06]
  for pr,jptEntry in zip(plst,prob_inf.truefalse_combination_iterator(model.vars)):
    prStu=prob_inf.calc_global_joint_prob(model,jptEntry)
    if prStu < 0.99*pr or prStu > 1.01*pr:
      error_cnt+=1
      
      print('\nERROR calculating joint probability for:')
      print(', '.join('{0}={1}'.format(var,'T' if jptEntry[var] else 'F') for var in model.vars))
      print('Expected pr={0}'.format(pr))
      print('Got      pr={0}'.format(prStu))
    if error_cnt>=10:
      print('\nToo many errors, exiting...')
      return False
  
  if error_cnt==0:
    print('    Ok')
    return True
  return False

def generate_pquery(model):
  N=len(model.vars)
  
  for num in range(N * 2 * 3**(N-1)):
    q=num%N
    num//=N
    q=model.vars[q]

    ev={}
    for var in model.vars:
      if var==q:
        role=num%2
        num//=2
        qV=(role==0)
      else:
        role=num%3
        num//=3
        if role<2:
          ev[var]=(role==0)
    
    yield q,qV,ev

pquery_plst=[0.9999582306503488, 0.003268423587696965, 0.0020212335907746643, 0.9, 0.7, 4.176934965122598e-05, 7.04880593227508e-05, 0.0016672224074691568, 0.05000000000000001, 0.01, 0.9980606921417061, 0.0032622416021499258, 0.0020212156643445722, 0.8993613824192337, 0.6979883381924197, 0.0019393078582939554, 0.996731576412303, 0.36755386565272496, 0.9, 0.7, 0.9980668823707707, 0.9999295119406773, 0.001422244301507779, 0.049999999999999996, 0.01, 0.0019331176292293796, 0.9967377583978501, 0.24516004609766892, 0.8712755830556878, 0.6173861720067453, 0.999949344004863, 0.484785972150593, 0.23100870196889098, 0.9, 0.7, 5.0655995137024524e-05, 6.0116566021515775e-05, 0.0014222590323639196, 0.049999999999999996, 0.01, 0.5577689243027888, 0.3441995977567134, 0.17606683840507922, 0.871364353514562, 0.6176188392283065, 0.44223107569721115, 0.515214027849407, 0.9979787664092253, 0.9, 0.7, 0.7099672469001376, 0.9999398834339785, 0.9983327775925309, 0.049999999999999996, 0.01, 0.29003275309986254, 0.6558004022432867, 0.9979787843356555, 0.8992256301245064, 0.6975618374558303, 0.99994936196669, 0.37355122828183596, 0.632446134347275, 0.9, 0.7, 5.063803330996514e-05, 6.0131316971542544e-05, 0.9985777556984922, 0.05000000000000001, 0.01, 0.6657108744026019, 0.2841718353643929, 0.7548399539023312, 0.10565949485500471, 0.022212389380530977, 0.3342891255973981, 0.6264487717181639, 0.768991298031109, 0.9000000000000001, 0.7, 0.7606920388631078, 0.9999398686830285, 0.998577740967636, 0.05, 0.01, 0.23930796113689234, 0.7158281646356071, 0.8239331615949207, 0.15175640836803259, 0.0333138844276126, 0.9929078014184398, 0.003268423587696965, 0.0020212335907746643, 0.9, 0.6999999999999998, 0.007092198581560292, 7.048805932275078e-05, 0.0016672224074691564, 0.049999999999999996, 0.009999999999999998, 0.750600850434461, 0.0024727772971907254, 0.0020181943345616267, 0.8992259044678383, 0.6975626989801145, 0.249399149565539, 0.996731576412303, 0.36755386565272496, 0.8999999999999999, 0.7, 0.7512000215618058, 0.9999295119406773, 0.0014222443015077793, 0.05000000000000001, 0.010000000000000002, 0.24879997843819432, 0.9975272227028092, 0.005637035563347659, 0.13467176850196869, 0.029086739135939295, 0.9914117824318215, 0.484785972150593, 0.23100870196889095, 0.9000000000000001, 0.7, 0.008588217568178404, 6.011656602151578e-05, 0.00142225903236392, 0.05, 0.010000000000000002, 0.00732179279326395, 0.006901098482896905, 0.005612151520557885, 0.17757660008729573, 0.03997202114194967, 0.992678207206736, 0.5152140278494068, 0.9979787664092254, 0.09999999999999998, 0.7, 0.014113094727792633, 0.9999398834339785, 0.9983327775925309, 0.95, 0.01, 0.9858869052722075, 0.9930989015171032, 0.9979818056654385, 0.10063861758076632, 0.4699999999999998, 0.9914148016888648, 0.3735512282818359, 0.632446134347275, 0.09999999999999998, 0.7, 0.008585198311135215, 6.013131697154256e-05, 0.9985777556984922, 0.9500000000000001, 0.01, 0.011511683274678913, 0.006876246073421025, 0.9943629644366524, 0.1287244169443122, 0.038443496801705744, 0.9884883167253212, 0.6264487717181639, 0.768991298031109, 0.09999999999999998, 0.7, 0.01824973824500748, 0.9999398686830284, 0.998577740967636, 0.9500000000000001, 0.01, 0.9817502617549927, 0.993123753926579, 0.9943878484794422, 0.12863564648543802, 0.03853098206245491, 0.9992486851990985, 0.0032684235876969656, 0.0020212335907746643, 0.09999999999999998, 0.7, 0.0007513148009015786, 7.048805932275078e-05, 0.0016672224074691562, 0.95, 0.01, 0.9662065683008091, 0.003160688350904322, 0.0020209111925683916, 0.10077436987549346, 0.43953642384105945, 0.033793431699190864, 0.9967315764123031, 0.36755386565272496, 0.09999999999999998, 0.7, 0.9663110041347788, 0.9999295119406773, 0.0014222443015077793, 0.95, 0.01, 0.03368899586522122, 0.9968393116490958, 0.03789402298892038, 0.8943405051449953, 0.010072696623294528, 0.9990889766170664, 0.4847859721505931, 0.23100870196889098, 0.1, 0.7000000000000001, 0.0009110233829334963, 6.011656602151578e-05, 0.0014222590323639199, 0.95, 0.01, 0.06548175865294668, 0.05808830728061875, 0.03588091528645574, 0.8482435916319675, 0.010141077385993395, 0.9345182413470534, 0.515214027849407, 0.9979787664092253, 0.09999999999999998, 0.7, 0.11971342160945007, 0.9999398834339785, 0.9983327775925309, 0.95, 0.01, 0.88028657839055, 0.9419116927193814, 0.9979790888074317, 0.10077409553216163, 0.439593927793195, 0.9990892993739275, 0.373551228281836, 0.632446134347275, 0.09999999999999998, 0.7, 0.0009107006260725188, 6.013131697154256e-05, 0.9985777556984922, 0.9500000000000001, 0.010000000000000002, 0.09961384529643373, 0.05611745403891494, 0.9621059770110797, 0.8653282314980314, 0.010114774681347466, 0.9003861547035664, 0.626448771718164, 0.7689912980311089, 0.09999999999999999, 0.7000000000000001, 0.15009011774975964, 0.9999398686830284, 0.998577740967636, 0.95, 0.010000000000000002, 0.8499098822502407, 0.9438825459610851, 0.9641190847135443, 0.8224233999127044, 0.010183185607962128, 0.9904430929626411, 0.0032684235876969656, 0.0020212335907746643, 0.9000000000000001, 0.7, 0.009556907037358824, 7.04880593227508e-05, 0.0016672224074691564, 0.05000000000000001, 0.01, 0.6902023006743356, 0.00227989956557118, 0.0020171402594207116, 0.7742152466367713, 0.6654999999999998, 0.30979769932566437, 0.996731576412303, 0.3675538656527249, 0.9, 0.7000000000000001, 0.6908868195262405, 0.9999295119406774, 0.001422244301507779, 0.049999999999999996, 0.01, 0.30911318047375946, 0.9977201004344289, 0.004551641633239515, 0.14361944549943034, 0.21009999999999998, 0.9884332281808621, 0.48478597215059305, 0.23100870196889095, 0.9, 0.6999999999999998, 0.011566771819137758, 6.0116566021515775e-05, 0.0014222590323639196, 0.04999999999999999, 0.01, 0.005430355688297585, 0.005142852044040336, 0.004538640000752913, 0.14388663878377284, 0.21055539999999998, 0.9945696443117025, 0.515214027849407, 0.9979787664092253, 0.9, 0.7, 0.010485794020393492, 0.9999398834339785, 0.9983327775925309, 0.049999999999999996, 0.01, 0.9895142059796065, 0.9948571479559597, 0.9979828597405794, 0.7521089630931458, 0.6586, 0.9884372823600297, 0.37355122828183596, 0.632446134347275, 0.9, 0.7, 0.011562717639970441, 6.013131697154255e-05, 0.9985777556984923, 0.05000000000000001, 0.010000000000000002, 0.008547192182370435, 0.005129858133401301, 0.9954483583667605, 0.05025775540528248, 0.010690000000000002, 0.9914528078176297, 0.6264487717181639, 0.7689912980311089, 0.8999999999999999, 0.7, 0.013573889331307635, 0.9999398686830284, 0.9985777409676361, 0.05000000000000001, 0.01, 0.9864261106686925, 0.9948701418665987, 0.9954613599992471, 0.050500115261828245, 0.01133791, 0.37735849056603754, 0.0032684235876969656, 0.0020212335907746643, 0.9000000000000001, 0.6999999999999998, 0.6226415094339625, 7.048805932275078e-05, 0.0016672224074691562, 0.049999999999999996, 0.010000000000000002, 0.012861165931214936, 0.00011174749602380887, 0.0017852122026965744, 0.7521522838357261, 0.6586137999999999, 0.987138834068785, 0.996731576412303, 0.36755386565272496, 0.9000000000000001, 0.7, 0.012901897594550255, 0.9999295119406773, 0.0014222443015077795, 0.05000000000000002, 0.010000000000000002, 0.9870981024054498, 0.9998882525039763, 0.001440701707124981, 0.05040690206374249, 0.011088820000000001, 0.33321517192484906, 0.484785972150593, 0.23100870196889098, 0.9, 0.7, 0.6667848280751508, 6.011656602151578e-05, 0.0014222590323639203, 0.05000000000000002, 0.010000000000000004, 3.1928837008076404e-05, 9.015328226329397e-05, 0.0014407327765951661, 0.0506493132745907, 0.01173634498, 0.9999680711629919, 0.515214027849407, 0.9979787664092253, 0.09999999999999998, 0.30000000000000004, 6.196639996757423e-05, 0.9999398834339785, 0.9983327775925308, 0.9500000000000001, 0.9899999999999999, 0.9999380336000324, 0.9999098467177366, 0.9982147877973034, 0.22578475336322876, 0.30201166180758027, 0.3332939771159549, 0.373551228281836, 0.632446134347275, 0.09999999999999998, 0.30000000000000004, 0.6667060228840451, 6.013131697154257e-05, 0.9985777556984923, 0.95, 0.99, 5.041194079081136e-05, 9.018439375484354e-05, 0.9985592982928752, 0.8563805545005697, 0.38261382799325466, 0.9999495880592093, 0.626448771718164, 0.7689912980311091, 0.09999999999999998, 0.30000000000000004, 8.046530968883622e-05, 0.9999398686830284, 0.9985777409676361, 0.95, 0.9899999999999999, 0.9999195346903111, 0.999909815606245, 0.9985592672234048, 0.8561133612162273, 0.3823811607716933, 0.8520179372197307, 0.003268423587696965, 0.0020212335907746643, 0.09999999999999998, 0.30000000000000004, 0.14798206278026912, 7.048805932275078e-05, 0.0016672224074691562, 0.95, 0.99, 0.11014052411697685, 0.0004237156096830609, 0.0019596574202472156, 0.2478910369068542, 0.3024381625441697, 0.8898594758830232, 0.996731576412303, 0.3675538656527249, 0.09999999999999996, 0.3000000000000001, 0.11045486915737979, 0.9999295119406773, 0.0014222443015077797, 0.9500000000000001, 0.99, 0.8895451308426203, 0.9995762843903171, 0.0015975145513068226, 0.9497422445947176, 0.9777876106194691, 0.8260105448154655, 0.484785972150593, 0.23100870196889095, 0.09999999999999996, 0.30000000000000004, 0.17398945518453438, 6.011656602151579e-05, 0.0014222590323639203, 0.9500000000000001, 0.99, 0.00030324165327349383, 0.0003453151521163314, 0.0015976396500871493, 0.9494998847381718, 0.9666861155723874, 0.9996967583467266, 0.515214027849407, 0.9979787664092254, 0.09999999999999998, 0.30000000000000004, 0.0005883708962685119, 0.9999398834339785, 0.9983327775925308, 0.95, 0.9899999999999999, 0.9994116291037315, 0.9996546848478836, 0.9980403425797529, 0.24784771616427387, 0.30243730101988536, 0.8260615103949719, 0.3735512282818359, 0.632446134347275, 0.09999999999999998, 0.3000000000000001, 0.1739384896050281, 6.013131697154258e-05, 0.9985777556984923, 0.9500000000000001, 0.9900000000000001, 0.00047870831028525766, 0.000345440407795925, 0.9984024854486933, 0.9495930979362576, 0.9709132608640607, 0.9995212916897149, 0.6264487717181639, 0.768991298031109, 0.09999999999999996, 0.30000000000000004, 0.0007638979701066943, 0.9999398686830285, 0.9985777409676362, 0.9500000000000001, 0.9900000000000001, 0.9992361020298933, 0.999654559592204, 0.9984023603499129, 0.9493506867254093, 0.9600279788580504, 0.9970845481049563, 0.003268423587696965, 0.0020212335907746643, 0.9, 0.30000000000000004, 0.0029154518950437348, 7.04880593227508e-05, 0.0016672224074691564, 0.05000000000000001, 0.99, 0.8802698145025294, 0.0028866125139281155, 0.0020199831098788364, 0.8574999999999999, 0.5300000000000002, 0.11973018549747047, 0.9967315764123029, 0.36755386565272496, 0.9, 0.30000000000000004, 0.8806070133743574, 0.9999295119406773, 0.0014222443015077793, 0.049999999999999996, 0.99, 0.11939298662564252, 0.9971133874860719, 0.011550155527810945, 0.29650000000000004, 0.9615565031982942, 0.9964664310954063, 0.48478597215059305, 0.23100870196889098, 0.9, 0.3, 0.0035335689045936434, 6.0116566021515775e-05, 0.0014222590323639199, 0.049999999999999996, 0.9899999999999999, 0.01769911504424779, 0.01643814928511476, 0.011394968773811184, 0.297061, 0.9614690179375449, 0.9823008849557522, 0.515214027849407, 0.9979787664092253, 0.9, 0.30000000000000004, 0.033788238300887834, 0.9999398834339785, 0.9983327775925308, 0.05, 0.9900000000000001, 0.9662117616991122, 0.9835618507148852, 0.9979800168901211, 0.849, 0.5604635761589406, 0.9964676796813255, 0.37355122828183596, 0.6324461343472751, 0.9, 0.3, 0.003532320318674423, 6.0131316971542564e-05, 0.9985777556984923, 0.05000000000000001, 0.99, 0.027661940776723615, 0.016283729946769937, 0.9884498444721891, 0.05085000000000002, 0.9899273033767055, 0.9723380592232764, 0.6264487717181638, 0.7689912980311089, 0.9, 0.30000000000000004, 0.043437711799927066, 0.9999398686830285, 0.9985777409676362, 0.05000000000000001, 0.99, 0.9565622882000729, 0.98371627005323, 0.9886050312261889, 0.05164815000000002, 0.9898589226140067, 0.6666666666666664, 0.003268423587696965, 0.0020212335907746643, 0.8999999999999999, 0.30000000000000004, 0.3333333333333336, 7.048805932275078e-05, 0.0016672224074691564, 0.05, 0.9900000000000001, 0.04122245913290688, 0.00020272029294149277, 0.0018876297331487648, 0.849017, 0.5604060722068049, 0.9587775408670931, 0.996731576412303, 0.36755386565272496, 0.9, 0.30000000000000004, 0.04134924936587669, 0.9999295119406771, 0.0014222443015077795, 0.05000000000000001, 0.99, 0.9586507506341233, 0.9997972797070585, 0.0014831466785683834, 0.05134130000000001, 0.9898852253186525, 0.6225165562913905, 0.48478597215059305, 0.23100870196889103, 0.9000000000000001, 0.30000000000000004, 0.37748344370860953, 6.011656602151578e-05, 0.0014222590323639203, 0.05000000000000001, 0.99, 0.00010535742506453144, 0.00015922360461467972, 0.0014832111079134708, 0.05213897570000001, 0.9898168143920378, 0.9998946425749355, 0.515214027849407, 0.9979787664092253, 0.09999999999999998, 0.30000000000000004, 0.00020445997970057212, 0.9999398834339785, 0.9983327775925309, 0.95, 0.9899999999999999, 0.9997955400202995, 0.9998407763953853, 0.9981123702668512, 0.1425, 0.3345, 0.6225998953524565, 0.373551228281836, 0.6324461343472751, 0.09999999999999998, 0.30000000000000004, 0.3774001046475433, 6.0131316971542564e-05, 0.9985777556984922, 0.9500000000000001, 0.99, 0.00016634011789487622, 0.00015928811938596351, 0.9985168533214316, 0.7035, 0.7898999999999999, 0.9998336598821053, 0.626448771718164, 0.7689912980311091, 0.09999999999999998, 0.3, 0.0002654863883509088, 0.9999398686830285, 0.9985777409676361, 0.9500000000000001, 0.99, 0.9997345136116491, 0.999840711880614, 0.9985167888920865, 0.7029390000000001, 0.7894445999999999, 0.9499999999999998, 0.003268423587696965, 0.0020212335907746643, 0.09999999999999998, 0.30000000000000004, 0.05000000000000004, 7.048805932275078e-05, 0.0016672224074691564, 0.95, 0.99, 0.29, 0.0010000000000000002, 0.0020000000000000005, 0.15100000000000002, 0.3414000000000001, 0.71, 0.9967315764123028, 0.36755386565272496, 0.09999999999999999, 0.3000000000000001, 0.29066000000000003, 0.9999295119406773, 0.0014222443015077795, 0.9500000000000001, 0.99, 0.70934, 0.9990000000000001, 0.002000000000000001, 0.94915, 0.98931, 0.94, 0.48478597215059305, 0.231008701968891, 0.09999999999999998, 0.3000000000000001, 0.06000000000000006, 6.011656602151578e-05, 0.0014222590323639203, 0.95, 0.99, 0.0010000000000000005, 0.0010000000000000002, 0.0020000000000000005, 0.94835185, 0.98866209, 0.9990000000000001, 0.515214027849407, 0.9979787664092252, 0.09999999999999996, 0.3, 0.0019390000000000004, 0.9999398834339784, 0.9983327775925309, 0.95, 0.9900000000000001, 0.9980610000000001, 0.999, 0.998, 0.15098300000000003, 0.3413862000000001, 0.9400200000000001, 0.373551228281836, 0.632446134347275, 0.09999999999999998, 0.30000000000000004, 0.059980000000000054, 6.013131697154257e-05, 0.9985777556984923, 0.9500000000000001, 0.99, 0.0015780000000000006, 0.0010000000000000002, 0.9980000000000001, 0.9486587000000001, 0.98891118, 0.9984220000000001, 0.6264487717181639, 0.768991298031109, 0.09999999999999996, 0.30000000000000004, 0.0025164420000000007, 0.9999398686830285, 0.9985777409676362, 0.9500000000000001, 0.99, 0.997483558, 0.9989999999999999, 0.998, 0.9478610243000001, 0.98826365502]
def check_q2():
  import prob_inf
  prob_inf.DEBUG_OUTPUT=0
  
  print('\n-------------------------------------------------------')
  print(' Checking Question 2: Table (Brute force) Inference')
  print('-------------------------------------------------------')
  
  print('Loading model file burglary_alarm.csv ...')
  model=prob_inf.read_model_file('burglary_alarm.csv')

  print('\nChecking function calc_query_exact_brute() ...')
  
  error_cnt=0
  
  #Generate
  # plst=[]
  # for q,qV,ev in generate_pquery(model):
    # plst.append( prob_inf.calc_query_exact_brute(model,q,qV,ev) )
  # print(repr(plst))

  #Check
  for pr,(q,qV,ev) in zip(pquery_plst,generate_pquery(model)):
    prStu=prob_inf.calc_query_exact_brute(model,q,qV,ev)
    if prStu < 0.99*pr or prStu > 1.01*pr:
      error_cnt+=1
      
      if error_cnt==1:
        print('\nERROR calculating joint probability for:')
      else:
        print()
      print('Query: {0}={1}'.format(q,'T' if qV else 'F'))
      print('Evidence:',', '.join('{0}={1}'.format(var,'T' if ev[var] else 'F') for var in model.vars if var in ev))
      print('Expected pr={0}'.format(pr))
      print('Got      pr={0}'.format(prStu))
    # if error_cnt>=10:
      # print('\nToo many errors, exiting...')
      # return False
  
  if error_cnt==0:
    print('    Ok')
    return True
  return False

#####################################################################

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="CSE3521 Homework 3 - Auto checker")
  parser.add_argument('--questions', '-q', type=str, action='store', default='1,2,3', help='Comma-separated list of integers, which questions to check')
  args = parser.parse_args()
  
  qq=args.questions.split(',')
  for q in qq:
    if q=='1':
      r=check_q1()
    elif q=='2':
      r=check_q2()
    else:
      print("ERROR: '{0}' is not a valid question number".format(q))
      r=False
    if not r:
      break
