
import pytest
import sof2018h

def test_exercicio15():
    assert all([k in ['sc', 'pt', 'cp', 'fr', 'pa', 'cnl'] for k in sof2018h.bn2.dependencies.keys()])

    assert len(sof2018h.bn2.dependencies['sc']) == 1
    assert len(sof2018h.bn2.dependencies['pt']) == 1
    assert len(sof2018h.bn2.dependencies['cp']) == 4
    assert len(sof2018h.bn2.dependencies['fr']) == 4
    assert len(sof2018h.bn2.dependencies['pa']) == 2
    assert len(sof2018h.bn2.dependencies['cnl']) == 2

    assert sof2018h.bn2.jointProb([(v,True) for v in sof2018h.bn2.dependencies]) == 0.0001215
    
    assert sof2018h.bn2.jointProb([('sc', True)]) == round(sof2018h.bn2.individualProb('sc', True),5)
    assert sof2018h.bn2.jointProb([('pt', False)]) == round(sof2018h.bn2.individualProb('pt', False),5)

    assert round(sof2018h.bn2.individualProb('pa', True),5) == 0.0163

