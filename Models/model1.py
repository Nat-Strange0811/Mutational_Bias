from Models.base_model import Base_Model

class Model1(Base_Model):
    def __init__(self, sequence, splice_site):
        self.sequence = sequence
        self.splice_site = splice_site
        super().__init__()
    
    def get_expected_frequency(self):
        if self.protein == "Error: Sequence contains a stop codon":
            return "Error: Sequence contains a stop codon"

        CG_count = self.CpG_sites.count(True)
        CG_ratio = CG_count/ len(self.sequence) * 100

        return CG_ratio