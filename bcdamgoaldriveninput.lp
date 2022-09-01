#const h=25.
#const p=50.
epic (e1; e2; e3; e4).
benefit (e1, 3; e2, 3; e3, 3; e4, 21).
cost (e1, 3; e2, 4; e3, 3; e4, 13).
time (e1, 3; e2, 4; e3, 3; e4, 13).
init( inbacklog (e1; e2; e3; e4); capacity(p) ).
goal( inproduction (e1; e2; e3; e4) ).
