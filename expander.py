from expand_NSWs import *

func_expand_dict = {
    'LWRD':LWRD2words,
    'LSEQ':LSEQ2words,
    'LABB':LABB2words,
    'NTIM':NTIM2words,
    'NDAT':NDAT2words,
    'NDAY':NDAY2words,
    'NMON':NMON2words,
    'NNUM':NNUM2words,
    'NTEL':NTEL2words,
    'NDIG':NDIG2words,
    'NSCR':NSCR2words,
    'NRNG':NRNG2words,
    'NPER':NPER2words,
    'NFRC':NFRC2words,
    'NADD':NADD2words,
    'URLE':URLE2words,
    'PUNC':PUNC2words,
    'CSEQ':CSEQ2words,
    'MONY':MONY2words,
    'DURA':DURA2words,
    'NONE':NONE2words,
}

def expand(classified_dic, list_tokens):
    out = {}
    for ind, (nsw, tag, class_) in classified_dic.items():
        func_expand = func_expand_dict[class_]
        fulltext = func_expand(nsw)
        out.update({ind: (nsw, tag, class_, fulltext)})
    return out

