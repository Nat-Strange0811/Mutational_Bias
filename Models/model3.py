from Models.model1 import Base_Model
from Bio.Seq import Seq

class Model3(Base_Model):
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
        CG_mutations = set()
        mutations = set()
        Original_DNA = Seq(self.sequence)
        Original_Protein = Original_DNA.translate()
        sequence_length = len(self.sequence)
        for i in range(len(self.sequence)):
            codon_start = i - (i % 3)
            codon_end = codon_start + 3
            codon = self.sequence[codon_start:codon_end]
            amino_acid = self.codons.get(codon)
            for amino_acid_V in self.codons:
                if amino_acid != amino_acid_V:
                    new_sequence = self.sequence[:codon_start] + amino_acid_V + self.sequence[codon_end:(sequence_length - (sequence_length % 3))]
                    if self.CpG_sites[i] and ((self.sequence[i] == 'C' and new_sequence[i] == 'T') or (self.sequence[i] == 'G' and new_sequence[i] == 'A')):
                        New_DNA = Seq(new_sequence)
                        New_Protein = New_DNA.translate()
                        if New_Protein != Original_Protein and '*' not in New_Protein:
                            CG_mutations.add(str(New_Protein))
                            mutations.add(str(New_Protein))
                    else:
                        DNA = Seq(new_sequence)
                        New_Protein = DNA.translate()
                        if New_Protein != Original_Protein and '*' not in New_Protein:
                            mutations.add(str(New_Protein))

        mutations = list(mutations)
        CG_mutations = list(CG_mutations)
        return CG_mutations, mutations