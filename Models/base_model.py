from Bio.Seq import Seq

class Base_Model:
    def __init__(self):
        self.codons = {    
    "ATA":"I", "ATC":"I", "ATT":"I", "ATG":"M",
    "ACA":"T", "ACC":"T", "ACG":"T", "ACT":"T",
    "AAC":"N", "AAT":"N", "AAA":"K", "AAG":"K",
    "AGC":"S", "AGT":"S", "AGA":"R", "AGG":"R",
    "CTA":"L", "CTC":"L", "CTG":"L", "CTT":"L",
    "CCA":"P", "CCC":"P", "CCG":"P", "CCT":"P",
    "CAC":"H", "CAT":"H", "CAA":"Q", "CAG":"Q",
    "CGA":"R", "CGC":"R", "CGG":"R", "CGT":"R",
    "GTA":"V", "GTC":"V", "GTG":"V", "GTT":"V",
    "GCA":"A", "GCC":"A", "GCG":"A", "GCT":"A",
    "GAC":"D", "GAT":"D", "GAA":"E", "GAG":"E",
    "GGA":"G", "GGC":"G", "GGG":"G", "GGT":"G",
    "TCA":"S", "TCC":"S", "TCG":"S", "TCT":"S",
    "TTC":"F", "TTT":"F", "TTA":"L", "TTG":"L",
    "TAC":"Y", "TAT":"Y", "TAA":"*", "TAG":"*",
    "TGC":"C", "TGT":"C", "TGA":"*", "TGG":"W",
    }
        self.protein = None
        self.process_sequence()
        self.CpG_sites = self.find_CpG_sites()
        self.splice()
    
    def process_sequence(self):
        if self.sequence.startswith('ATG'):
              self.sequence = self.sequence[3:]
        if self.sequence.endswith('TAA') or self.sequence.endswith('TAG') or self.sequence.endswith('TGA'):
              self.sequence = self.sequence[:-3]

        self.protein = Seq(self.sequence).translate()
        if '*' in self.protein:
             self.protein = "Error: Sequence contains a stop codon"
    
    def find_CpG_sites(self):
        CpG_sites = []
        for i in range(len(self.sequence)):
            if self.sequence[i] == 'N':
                 continue
            if self.CpG_site(i):
                CpG_sites.append(True)
            else:
                CpG_sites.append(False)
        return CpG_sites
            
    def splice(self):
        self.sequence.replace('N', '')
        self.sequence = self.sequence.replace('Y', 'C')

    def CpG_site(self, i):
        if (
            self.sequence[i] == 'G' and i > 0 
                and 
            (self.sequence[i-1] == 'C' or self.sequence[i-1] =='N' or self.sequence[i-1] == 'Y')  
                or 
            self.sequence[i] == 'C' and i < (len(self.sequence) - 1) 
                and 
            (self.sequence[i+1] == 'G' or self.sequence[i+1] == 'N')
        ):
              return True
        return False
    
