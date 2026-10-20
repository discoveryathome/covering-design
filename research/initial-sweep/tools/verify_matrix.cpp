// Independent exact checker for one space-separated k-block per line.
// No search engine imports, masks, heuristic state, or incidence tables.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;
using U=uint64_t;
U binom[101][9];
void mark(const vector<int>& b,int t,int at,int depth,U rank,vector<unsigned char>& covered){
 if(depth==t){if(rank>=covered.size())throw runtime_error("rank out of bounds");covered[rank]=1;return;}
 for(int i=at;i<=(int)b.size()-(t-depth);i++)mark(b,t,i+1,depth+1,rank+binom[b[i]-1][depth+1],covered);
}
int main(int argc,char** argv){try{
 if(argc!=6)throw runtime_error("usage: v k t expected_blocks matrix.txt");
 int v=stoi(argv[1]),k=stoi(argv[2]),t=stoi(argv[3]),expected=stoi(argv[4]);
 if(!(1<=t&&t<=k&&k<=v&&v<=100&&t<=8))throw runtime_error("invalid parameters");
 for(int n=0;n<=100;n++){binom[n][0]=1;for(int j=1;j<=8;j++)binom[n][j]=(j>n)?0:(j==n?1:binom[n-1][j-1]+binom[n-1][j]);}
 U total=binom[v][t];if(total>30000000)throw runtime_error("thirty-million-subset cap");
 vector<unsigned char> covered(total);unordered_set<string> seen;ifstream file(argv[5]);if(!file)throw runtime_error("cannot read matrix");
 string line;int count=0;
 while(getline(file,line)){
  istringstream input(line);vector<int> b;int x;
  while(input>>x){if(x<1||x>v)throw runtime_error("point outside universe");b.push_back(x);}
  if(!input.eof()||(int)b.size()!=k)throw runtime_error("wrong block size or malformed integer");
  sort(b.begin(),b.end());if(adjacent_find(b.begin(),b.end())!=b.end())throw runtime_error("repeated point");
  string key;for(int p:b){key+=to_string(p);key+=',';}if(!seen.insert(key).second)throw runtime_error("duplicate block");
  mark(b,t,0,0,0,covered);count++;
 }
 if(count!=expected)throw runtime_error("block count mismatch");
 U missing=std::count(covered.begin(),covered.end(),0);if(missing)throw runtime_error("uncovered "+to_string(missing));
 cout<<"{\"valid\":true,\"v\":"<<v<<",\"k\":"<<k<<",\"t\":"<<t<<",\"blocks\":"<<count<<",\"required\":"<<total<<",\"uncovered\":0}\n";
}catch(const exception& e){cerr<<"INVALID: "<<e.what()<<'\n';return 1;}}
