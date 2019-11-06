import decimal

R_VOTE = 160  # reward of vote for every block
R_BlOCK = 16  # reward of block for every block
SR_NUMBER = 27  # total number of SR
BLOCK_PRODUCED = 28792  # total number of blocks produced one day

D_R_VOTE = decimal.Decimal(str(R_VOTE))
D_R_BlOCK = decimal.Decimal(str(R_BlOCK))
D_SR_NUMBER = decimal.Decimal(str(SR_NUMBER))
D_BLOCK_PRODUCED = decimal.Decimal(str(BLOCK_PRODUCED))

# calculate user's one vote reward for specific SR.
def calc_vote_profit(total_vote, sr_vote, ratio):
    if total_vote < sr_vote or total_vote <= 0 or sr_vote <=0 or ratio > 100 or ratio < 0:
        raise Exception("bad parameters")
    d_ratio = decimal.Decimal(str(ratio / 100.0))
    return (D_R_BlOCK / D_SR_NUMBER / sr_vote + D_R_VOTE / total_vote) * D_BLOCK_PRODUCED * d_ratio