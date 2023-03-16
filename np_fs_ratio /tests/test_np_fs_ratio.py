from np_fs_ratio import np_fs_ratio

#write pytest 
def test_Fundraising_Efficiency_ratio():
    EG_EIN = '131644147'
    EG_YR = 2017
    assert np_fs_ratio.fudeff(EG_EIN,EG_YR)==466.5765, 'fundraising efficiency ratio is correct!'

def test_profit_margin():
    EG_EIN = '131644147'
    EG_YR = 2017
    assert np_fs_ratio.pm(EG_EIN,EG_YR)==0.1345, 'Profit Margin is correct!'
    
def test_leverages():
    EG_EIN = '131644147'
    EG_YR = 2017
    assert np_fs_ratio.lvg(EG_EIN,EG_YR)==0.1912, 'leverage is correct!'  
