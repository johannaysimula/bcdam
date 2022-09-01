% time step horizon
#const h=11.
% personhours capacity
#const p=17.
epic (a; b; c).
cost(a,4;b,3;c,8).
time(a,4;b,3;c,8).
benefit(a,6;b,7;c,2).
init(inbacklog(a;b;c);capacity(p)).


%goal(inconstruction(a;b;c)).
goal(inproduction(a;b;c)).