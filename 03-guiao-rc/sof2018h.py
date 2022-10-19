from bayes_net import *



""" 	
    #https://dreampuf.github.io/GraphvizOnline/	


    digraph G {	    assert len(sof2018h.bn.dependencies['sc']) == 1
    node [shape=record];	    assert len(sof2018h.bn.dependencies['pt']) == 1
    "sc" [label="Sobre Carregado\n|0.6"];	    assert len(sof2018h.bn.dependencies['cp']) == 4
    "pt" [label="Processador Texto\n|0.05"];	    assert len(sof2018h.bn.dependencies['fr']) == 4
    "cp" [label="Cara Preocupada\n|{{~sc^~pa = 0.01}|{~sc^pa = 0.011}|{sc^~pa = 0.01}|{sc^pa = 0.02}}"];	    assert len(sof2018h.bn.dependencies['pa']) == 2
    "fr" [label="Frequência Rato\n|{{~pt^~pa=0.01}|{~pt^pa=0.10}|{pt^~pa=0.90}|{pt^pa=0.90}}"];	    assert len(sof2018h.bn.dependencies['cnl']) == 2
    "pa" [label="Precisa Ajuda\n|{{~pt = 0.004}|{pt = 0.25}}"];	
    "cnl" [label="Correio Não Lido\n|{{sc = 0.90}|{~sc = 0.001}}"];	


    "pt" -> "fr";	    assert sof2018h.bn.jointProb([(v,True) for v in sof2018h.bn.dependencies]) == 0.0001215
    "pa" -> "fr";	
    "pt" -> "pa";	    assert sof2018h.bn.jointProb([('sc', True)]) == round(sof2018h.bn.individualProb('sc', True),5)
    "pa" -> "cp";	    assert sof2018h.bn.jointProb([('pt', False)]) == round(sof2018h.bn.individualProb('pt', False),5)
    "sc" -> "cnl";	
    "sc" -> "cp";	
    } 	
    """	


bn = BayesNet()

bn.add('sc',[],0.6)	
bn.add('pt',[],0.05)	

bn.add('cp',[('sc',True ),('pa',True )],0.02)	
bn.add('cp',[('sc',True ),('pa',False)],0.01)	
bn.add('cp',[('sc',False),('pa',True )],0.011)	
bn.add('cp',[('sc',False),('pa',False)],0.001)	

bn.add('fr',[('pt',True ),('pa',True )],0.90)	
bn.add('fr',[('pt',True ),('pa',False)],0.90)	
bn.add('fr',[('pt',False),('pa',True )],0.10)	
bn.add('fr',[('pt',False),('pa',False)],0.01)	

bn.add('pa',[('pt',True )],0.25)	
bn.add('pa',[('pt',False)],0.004)	

bn.add('cnl',[('sc',True )],0.90)	
bn.add('cnl',[('sc',False)],0.001)


bn2 = BayesNet()

#variables = ['sc', 'pt', 'cp', 'fr', 'pa', 'cnl']

bn2.add('r', [], 0.001)
bn2.add('t', [], 0.002)

bn2.add('a', [('r', True ),('t', True )], 0.950)
bn2.add('a', [('r', True ),('t', False)], 0.940)
bn2.add('a', [('r', False),('t', True )], 0.290)
bn2.add('a', [('r', False),('t', False)], 0.001)

bn2.add('j', [('a', True )], 0.900)
bn2.add('j', [('a', False)], 0.050)

bn2.add('m', [('a', True )], 0.700)
bn2.add('m', [('a', False)], 0.100)

conjunction = [('j',True),('m',True),('a',True),('r',False),('t',False)]

print(bn2.jointProb(conjunction))

#import printt
#printt.print(bn2.conjuctions(['a','b','c']))
