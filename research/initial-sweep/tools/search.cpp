// Original bounded sweep engine. Search scores are untrusted until Python verification.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U=uint64_t;
using Clock=chrono::steady_clock;
struct Model {
 int v,k,t,N,M,Q; vector<U> blocks,sets; vector<vector<int>> inc,rev;
 static void enumerate(int v,int k,int at,U mask,vector<U>& out){
  if(!k){out.push_back(mask);return;}
  for(int i=at;i<=v-k;i++)enumerate(v,k-1,i+1,mask|(U(1)<<i),out);
 }
 Model(int vv,int kk,int tt):v(vv),k(kk),t(tt){
  if(!(1<=t&&t<=k&&k<=v&&v<=63))throw runtime_error("bad parameters");
  enumerate(v,t,0,0,sets);enumerate(v,k,0,0,blocks);
  N=blocks.size();M=sets.size();if(N>150000||M>50000)throw runtime_error("pool cap");
  unordered_map<U,int> ids; for(int i=0;i<M;i++)ids[sets[i]]=i;
  inc.resize(N);rev.resize(M);
  for(int i=0;i<N;i++){
   vector<int> points;for(int j=0;j<v;j++)if(blocks[i]>>j&1)points.push_back(j);
   vector<U> small;enumerate(k,t,0,0,small);
   for(U x:small){U mask=0;for(int j=0;j<k;j++)if(x>>j&1)mask|=U(1)<<points[j];
    int u=ids.at(mask);inc[i].push_back(u);rev[u].push_back(i);}
  }
  Q=inc[0].size();if((long long)N*Q>5000000)throw runtime_error("incidence cap");
 }
 vector<int> greedy(mt19937_64& rng){
  vector<int> gain(N,Q),pos(N),covered(M);vector<vector<int>> bucket(Q+1);
  for(int i=0;i<N;i++){pos[i]=i;bucket[Q].push_back(i);}
  int remain=M,top=Q;vector<int> chosen;
  while(remain){
   while(top>0&&bucket[top].empty())top--;
   if(!top)throw runtime_error("greedy stalled");
   int b=bucket[top][rng()%bucket[top].size()];chosen.push_back(b);
   for(int u:inc[b])if(!covered[u]){
    covered[u]=1;remain--;
    for(int a:rev[u]){int g=gain[a],p=pos[a],last=bucket[g].back();
     bucket[g][p]=last;pos[last]=p;bucket[g].pop_back();gain[a]--;pos[a]=bucket[g-1].size();bucket[g-1].push_back(a);}
   }
  }
  prune(chosen,rng);return chosen;
 }
 void prune(vector<int>& chosen,mt19937_64& rng){
  vector<int> counts(M);for(int b:chosen)for(int u:inc[b])counts[u]++;
  shuffle(chosen.begin(),chosen.end(),rng);vector<int> keep;
  for(int b:chosen){bool redundant=true;for(int u:inc[b])if(counts[u]==1){redundant=false;break;}
   if(redundant){for(int u:inc[b])counts[u]--;}else keep.push_back(b);}
  chosen=keep;
 }
 vector<int> load(const string& path){
  ifstream f(path);if(!f)throw runtime_error("cannot read start blocks");
  unordered_map<U,int> ids;for(int i=0;i<N;i++)ids[blocks[i]]=i;
  vector<int> chosen;int x;U mask=0;int count=0;
  while(f>>x){if(x<1||x>v)throw runtime_error("bad label");mask|=U(1)<<(x-1);count++;
   if(count==k){chosen.push_back(ids.at(mask));mask=0;count=0;}}
  if(count)throw runtime_error("incomplete block");return chosen;
 }
 void save(const vector<int>& chosen,const string& out,U seed,const string& method){
  ofstream f(out);if(!f)throw runtime_error("output unavailable");
  vector<U> sorted;for(int b:chosen)sorted.push_back(blocks[b]);sort(sorted.begin(),sorted.end());
  f<<"{\"v\":"<<v<<",\"k\":"<<k<<",\"t\":"<<t<<",\"blocks\":[";
  for(size_t i=0;i<sorted.size();i++){if(i)f<<',';f<<'[';bool first=true;for(int p=0;p<v;p++)if(sorted[i]>>p&1){if(!first)f<<',';f<<p+1;first=false;}f<<']';}
  f<<"],\"provenance\":{\"method\":\""<<method<<"\",\"seed\":\""<<seed<<"\"}}\n";
 }
};
struct State {
 Model& m;vector<int> chosen,selected,count,missing,position;
 State(Model& mm,vector<int> c):m(mm),chosen(c),selected(m.N,-1),count(m.M),position(m.M,-1){
  for(int i=0;i<(int)chosen.size();i++){selected[chosen[i]]=i;for(int u:m.inc[chosen[i]])count[u]++;}
  for(int u=0;u<m.M;u++)if(!count[u]){position[u]=missing.size();missing.push_back(u);}
 }
 State& operator=(State&& o){chosen=move(o.chosen);selected=move(o.selected);count=move(o.count);missing=move(o.missing);position=move(o.position);return *this;}
 void add(int b){for(int u:m.inc[b]){if(!count[u]){int p=position[u],last=missing.back();missing[p]=last;position[last]=p;missing.pop_back();position[u]=-1;}count[u]++;}}
 void remove(int b){for(int u:m.inc[b]){count[u]--;if(!count[u]){position[u]=missing.size();missing.push_back(u);}}}
 void swapblock(int slot,int b){int old=chosen[slot];remove(old);selected[old]=-1;add(b);chosen[slot]=b;selected[b]=slot;}
};
int main(int argc,char** argv){try{
 if(argc<10)throw runtime_error("usage: v k t seed restarts seconds output initial-or-dash mode");
 int v=stoi(argv[1]),k=stoi(argv[2]),t=stoi(argv[3]);U seed=stoull(argv[4]);int restarts=stoi(argv[5]);double seconds=stod(argv[6]);string out=argv[7],initial=argv[8],mode=argv[9];
 auto begin=Clock::now();auto elapsed=[&](){return chrono::duration<double>(Clock::now()-begin).count();};
 Model m(v,k,t);mt19937_64 rng(seed);vector<int> best;vector<int> sizes;
 if(initial!="-"){best=m.load(initial);State control(m,best);if(!control.missing.empty())throw runtime_error("initial is incomplete");}
 for(int r=0;r<restarts;r++){auto c=m.greedy(rng);sizes.push_back(c.size());if(best.empty()||c.size()<best.size())best=c;if(elapsed()>=seconds)break;}
 if(best.empty())throw runtime_error("need greedy or initial witness");
 m.save(best,out,seed,initial=="-"?"incremental-greedy-v1":"archive-initial-control");
 int initial_size=best.size(),target=initial_size-1,best_defect=m.M;uint64_t moves=0,accepted=0;vector<int> progress;
 if(mode=="repair"&&elapsed()<seconds&&target>0){
  auto c=best;shuffle(c.begin(),c.end(),rng);c.pop_back();State state(m,c);best_defect=state.missing.size();
  vector<int> tabu(m.N);uint64_t last_improvement=0;int local_best=best_defect;
  while(elapsed()<seconds){
   moves++;
   if(state.missing.empty()){
    best=state.chosen;m.prune(best,rng);progress.push_back(best.size());m.save(best,out,seed,"greedy-or-archive-delete-repair-v1");
    target=best.size()-1;if(target<=0)break;
    auto next=best;shuffle(next.begin(),next.end(),rng);next.pop_back();state=State(m,next);
    best_defect=state.missing.size();local_best=best_defect;last_improvement=moves;fill(tabu.begin(),tabu.end(),0);
   }
   int u=state.missing[rng()%state.missing.size()];auto& options=m.rev[u];
   vector<int> victims;vector<vector<int>> unique;
   int samples=min(16,(int)state.chosen.size());
   for(int i=0;i<samples;i++){int slot=rng()%state.chosen.size();victims.push_back(slot);vector<int> list;
    for(int z:m.inc[state.chosen[slot]])if(state.count[z]==1)list.push_back(z);unique.push_back(move(list));}
   int best_delta=numeric_limits<int>::max(),best_slot=-1,best_add=-1,ties=0;
   int nc=min(24,(int)options.size());
   for(int j=0;j<nc;j++){
    int b=options[rng()%options.size()];if(state.selected[b]>=0)continue;
    int gain=0;for(int z:m.inc[b])gain+=state.count[z]==0;
    for(int h=0;h<samples;h++){
     int delta=(int)unique[h].size()-gain;
     for(int z:unique[h])if((m.sets[z]&m.blocks[b])==m.sets[z])delta--;
     bool aspiration=(int)state.missing.size()+delta<local_best;
     if((uint64_t)tabu[b]>moves&&!aspiration)continue;
     if(delta<best_delta){best_delta=delta;best_slot=victims[h];best_add=b;ties=1;}
     else if(delta==best_delta&&rng()%++ties==0){best_slot=victims[h];best_add=b;}
    }
   }
   double heat=0.3+min(1.2,double(moves-last_improvement)/20000.0);
   if(best_slot>=0&&(best_delta<=0||generate_canonical<double,53>(rng)<exp(-best_delta/heat))){
    int old=state.chosen[best_slot];state.swapblock(best_slot,best_add);tabu[old]=moves+7+rng()%11;accepted++;
    if((int)state.missing.size()<local_best){local_best=state.missing.size();best_defect=local_best;last_improvement=moves;}
   }
   if(moves-last_improvement>60000){
    auto next=best;shuffle(next.begin(),next.end(),rng);next.pop_back();state=State(m,next);fill(tabu.begin(),tabu.end(),0);last_improvement=moves;local_best=state.missing.size();
   }
  }
  // Accept success reached by the last move even if the time budget just expired.
  if(state.missing.empty()&&state.chosen.size()<best.size()){best=state.chosen;m.prune(best,rng);progress.push_back(best.size());m.save(best,out,seed,"greedy-or-archive-delete-repair-v1");}
 }
 cout<<"{\"v\":"<<v<<",\"k\":"<<k<<",\"t\":"<<t<<",\"blocks\":"<<best.size()<<",\"initial_blocks\":"<<initial_size<<",\"seconds\":"<<elapsed()<<",\"moves\":"<<moves<<",\"accepted\":"<<accepted<<",\"last_target\":"<<target<<",\"best_defect_at_last_target\":"<<best_defect<<",\"restart_sizes\":[";
 for(size_t i=0;i<sizes.size();i++){if(i)cout<<',';cout<<sizes[i];}cout<<"],\"improvement_chain\":[";for(size_t i=0;i<progress.size();i++){if(i)cout<<',';cout<<progress[i];}cout<<"]}\n";
}catch(const exception& e){cerr<<e.what()<<'\n';return 1;}}
