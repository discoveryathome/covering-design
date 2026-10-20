"""Two-point combination and simple induced-cover audits; arithmetic leads only."""
import argparse
import json
from math import comb
from pathlib import Path


def audit(source):
    data={tuple(map(int,key[2:-1].split(','))):x['size'] for key,x in source.items()}
    def C(v,k,t):
        if not 0<=t<=k<=v:return None
        if t==0 or k==v:return 1
        if t==1:return (v+k-1)//k
        if k==t:return comb(v,t)
        return data.get((v,k,t))
    two=[];induced=[]
    for (v,k,t),old in data.items():
        a=C(v-2,k,t);b=C(v-2,k-2,t-1)
        if a is not None and b is not None and a+b<old:
            two.append({'v':v,'k':k,'t':t,'archive_upper':old,'derived_upper':a+b,
                        'rule':'two-point-combination','parents':[(v-2,k,t),(v-2,k-2,t-1)],'parent_bounds':[a,b]})
        parent=(v+1,k+1,t+1)
        if parent in data:
            bound=(k+1)*data[parent]//(v+1)
            if bound<old:induced.append({'v':v,'k':k,'t':t,'archive_upper':old,'derived_upper':bound,
                'rule':'least-degree-point-induced-cover','parent':parent,'parent_upper':data[parent]})
        parent=(v-1,k-1,t)
        if parent in data and data[parent]<old:induced.append({'v':v,'k':k,'t':t,'archive_upper':old,'derived_upper':data[parent],
                'rule':'append-new-point-to-every-block','parent':parent,'parent_upper':data[parent]})
    return {'source_cells':len(data),'two_point_candidates':two,'induced_candidates':induced,
            'status':'Arithmetic leads conditional on source constructions; no new witness or novelty claim.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('metadata',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=audit(json.loads(a.metadata.read_text()));a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'two_point_candidates':len(result['two_point_candidates']),'induced_candidates':len(result['induced_candidates'])}))


if __name__=='__main__':main()
