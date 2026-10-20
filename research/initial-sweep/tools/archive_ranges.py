"""Read selected public archive witnesses with bounded HTTP Range requests.

Never execute downloaded code. Preserve exact byte offsets and source payload hashes.
"""
import hashlib
import json
import re
import urllib.request
import urllib.error
import time
from pathlib import Path

URL='https://zenodo.org/records/19735294/files/covers.json'
TOKEN=re.compile(rb'"C\((\d+),(\d+),(\d+)\)"\s*:')


def order(key):
    v,k,t=key
    return t,k,v


class Archive:
    def __init__(self, cache, byte_budget=128*1024*1024):
        self.cache=Path(cache);self.cache.mkdir(parents=True,exist_ok=True)
        self.budget=byte_budget;self.downloaded=0;self.total=None;self.regions=[]
        self.logs=[]

    def add_cached(self,path,start):
        data=Path(path).read_bytes();self.regions.append((start,data))

    def fetch(self,start,length=65536):
        for attempt in range(3):
            try:return self._fetch(start,length)
            except (TimeoutError, urllib.error.URLError) as e:
                if isinstance(e,urllib.error.HTTPError) or attempt==2:raise
                print(f'RETRY public archive range {start}+{length}: {type(e).__name__}',flush=True)
                time.sleep(2**attempt)

    def _fetch(self,start,length=65536):
        if self.downloaded+length>self.budget:raise RuntimeError('archive download budget exceeded')
        path=self.cache/f'{start}-{length}.bin'
        if path.exists():
            data=path.read_bytes();meta=json.loads(path.with_suffix('.json').read_text());self.total=meta['total']
        else:
            req=urllib.request.Request(URL,headers={'Range':f'bytes={start}-{start+length-1}'})
            with urllib.request.urlopen(req,timeout=30) as r:
                header=r.headers.get('Content-Range','')
                match=re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)',header)
                if r.status!=206 or not match or int(match[1])!=start:
                    raise RuntimeError('server did not honor requested byte range')
                data=r.read(length+1);self.total=int(match[3])
                if len(data)>length:raise RuntimeError('unexpected response length')
            self.downloaded+=len(data);path.write_bytes(data)
            meta={'start':start,'length':len(data),'total':self.total,'sha256':hashlib.sha256(data).hexdigest()}
            path.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
            self.logs.append(meta)
        self.regions.append((start,data));return data

    def extract(self,key):
        token=f'"C({key[0]},{key[1]},{key[2]})"'.encode()
        def within(offset,data):
            at=data.find(token)
            if at<0:return None
            start=data.index(b'[',at)
            try:blocks,end=json.JSONDecoder().raw_decode(data[start:].decode('ascii'))
            except json.JSONDecodeError:
                offset+=start;start=0;length=1024*1024
                while True:
                    data=self.fetch(offset,length)
                    try:blocks,end=json.JSONDecoder().raw_decode(data.decode('ascii'));break
                    except json.JSONDecodeError:
                        length*=2
                        if length>16*1024*1024:raise RuntimeError('selected block payload exceeds extraction cap')
            raw=data[start:start+end]
            return {'blocks':blocks,'source':URL,'byte_range':[offset+start,offset+start+end-1],'source_payload_sha256':hashlib.sha256(raw).hexdigest()}
        for offset,data in self.regions[:]:
            result=within(offset,data)
            if result:return result
        if self.total is None:self.fetch(0)
        low,high=0,self.total
        for offset,data in self.regions:
            for token_match in TOKEN.finditer(data):
                other=tuple(map(int,token_match.groups()));point=offset+token_match.start()
                if order(other)<order(key):low=max(low,point+1)
                elif order(other)>order(key):high=min(high,point)
        for _ in range(40):
            at=(low+high)//2;length=min(65536,self.total-at)
            data=self.fetch(at,length);matches=list(TOKEN.finditer(data))
            while not matches:
                length=min(length*4,8*1024*1024,self.total-at)
                if length==len(data):raise RuntimeError('no archive key in bounded window')
                data=self.fetch(at,length);matches=list(TOKEN.finditer(data))
            result=within(at,data)
            if result:return result
            first=tuple(map(int,matches[0].groups()));last=tuple(map(int,matches[-1].groups()))
            if order(key)<order(first):high=at
            elif order(key)>order(last):low=at+matches[-1].end()
            else:raise RuntimeError(f'target absent between archive keys: {key}')
            if low>=high:break
        raise RuntimeError(f'archive key not located: {key}')
