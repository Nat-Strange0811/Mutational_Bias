from Models.base_model import Base_Model

class Model2(Base_Model):
    def __init__(self, sequence, splice_site):
        self.sequence = sequence
        super().__init__()
        self.splice_site = splice_site

    def get_expected_frequency(self):

        if self.protein == "Error: Sequence contains a stop codon":
            return "Error: Sequence contains a stop codon"
        
        CpG_mutations, mutations = self.get_mutations()
        CpG_ratio = len(CpG_mutations) / len(mutations) * 100

        return CpG_ratio

    def get_mutations(self):
        mutations = []
        CG_mutations = []
        for i in range(len(self.sequence)):
            codon_start = i - (i % 3)
            codon_end = codon_start + 3
            codon = self.sequence[codon_start:codon_end]
            amino_acid = self.codons.get(codon)
            for base in ['A', 'C', 'G', 'T']:
                if base != self.sequence[i]:
                    new_sequence = self.sequence[:i] + base + self.sequence[i+1:]
                    new_codon_start = i - (i % 3)
                    new_codon_end = new_codon_start + 3
                    new_codon = new_sequence[new_codon_start:new_codon_end]
                    new_amino_acid = self.codons.get(new_codon)
                    if new_amino_acid != amino_acid and new_amino_acid != '*':
                        if self.CpG_sites[i]:
                            CG_mutations.append(new_sequence)
                            mutations.append(new_sequence)
                        else:
                            mutations.append(new_sequence)
        return CG_mutations, mutations



