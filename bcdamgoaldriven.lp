benefitrealized(0,0).
costincurred(0,0).

action(construct(X)):-epic(X).
action(produce(X)):-epic(X).
0 {occurs(A,T) : action(A)} 1 :- T = 0..h-1.

% not possible to move to construction unless in backlog earlier
:- occurs(construct(X),T+1), not holds(inbacklog(X),T).

%change state to inconstruction for X
holds(inconstruction(X),T) :- occurs(construct(X),T).

% can't be in backlog when in construction
-holds(inbacklog(X),T) :-  holds(inconstruction(X),T).

%not possible to move to construction if already in construction
-occurs(construct(X),T+1):- holds(inconstruction(X),T).


% not possible to move to production unless in construction earlier
:- occurs(produce(X),T+1), not holds(inconstruction(X),T).

%change state to in production for X
holds(inproduction(X),T) :- occurs(produce(X),T).

% can't be in construction when in production
 -holds(inconstruction(X),T) :- holds(inproduction(X),T).

%not possible to move to production if already in production
-occurs(produce(X),T+1) :-  holds(inproduction(X),T).

% can't be in backlog when in production
-holds(inbacklog(X),T) :- holds(inproduction(X),T).


%Update capacity.
holds(capacity(P-TX),T+1) :- occurs(construct(X),T+1), holds(capacity(P),T), time(X,TX).

%Update capacity.
holds(capacity(P+CX),T+1) :- occurs(produce(X),T+1), holds(capacity(P),T), time(X,CX).

% can only move to construction when enough capacity
:- occurs(construct(X),T), holds(capacity(P),T), P<TX, time(X,TX).

% can only move to production when finished
:- occurs(produce(X),T), start(X,ST), T<ST+TX, time(X,TX).

%Register start time for constructing X
start(X,T+1) :- occurs(construct(X),T).



%inertia
{holds(inbacklog(X),T+1)} :- holds(inbacklog(X),T), T = 0..h-1.
{holds(inconstruction(X),T+1)} :- holds(inconstruction(X),T), T = 0..h-1.
{holds(inproduction(X),T+1)} :- holds(inproduction(X),T), T = 0..h-1.

benefitrealized(BX,T) :- benefit(X,BX), occurs(produce(X),T).
costincurred(CX,T) :- cost(X,CX), occurs(produce(X),T).


%{benefitrealized(BR,T+1)} :- benefitrealized(BR,T), T = 0..h-1.
%{costincurred(CI,T+1)} :- costincurred(CI,T), T = 0..h-1.
%:-#count{BR : benefitrealized(BR,T)} <1, T=0..h.
%:-#count{CI : costincurred(CI,T)} <1, T=0..h.

%The most benefit/cost-worthy product element.
%holds(first(X),T) :-  holds(inbacklog(X),T),benefit(X,BX),cost(X,CX),BX/CX=#max{BY/CY : benefit(Y,BY), cost(Y,CY),holds(inbacklog(Y),T)}.

%Send X into construction if first and enough capacity.
%occurs(construct(X),T+1) :- holds(inbacklog(X),T),  time(X,TX), holds(capacity(P),T), P>TX.

%:- occurs(construct(X),T), occurs(construct(Y),T), X!=Y.

%:- holds(capacity(P),T), P>p.

%Send X into production when finished.
%occurs(produce(X),T+1) :- holds(inconstruction(X),T),  start(X,TS),time(X,TX), T=TS+TX.

%bci(BR,CI,T) :- benefitrealized(BR,T), costincurred(CI,T).

%occurs(move(a,c),3; move(b,a),4).

%initial state
%init(backlog(a,b);loc(b,table);loc(c,table)).
%occurs(move(a,c),3; move(b,a),4).

%effect of action on state
%holds(loc(B,L),T+1) :- occurs(move(B,L),T).

%two blocks can’t be located on top of the same block
%B1 = B2 :- holds(loc(B1,B),T), holds(loc(B2,B),T), block(B).
%:- occurs(move(_,L),T), holds(loc(_,L),T), block(L).

%a block can’t be moved unless it is clear
%:- occurs(move(B,L),T), holds(loc(_,B),T).

% a block can’t be moved to its current location
%:- occurs(move(B,L),T), holds(loc(B,L),T).

% existence and uniqueness of value
%:- #count{L : holds(loc(B,L),T)} != 1, block(B), T = 0..h.

% relationship between holds/2, init/1, and final/1
holds(C,0) :- init(C).
final(C) :- holds(C,h).
:- goal(C), not holds(C,h).

sumbenefitrealized(SBR) :- SBR=#sum{BR : benefitrealized(BR,T), T = 0..h}.
sumcostincurred(SCI) :- SCI=#sum{CI : costincurred(CI,T), T = 0..h}.

%finalmaxbenefitrealized(MBR) :- maxbenefitrealized(MBR,h).
%finalmaxcostincurred(MCI) :- maxcostincurred(MCI,h).
%finalbenefitcost(MBR/MCI):- finalmaxbenefitrealized(MBR), finalmaxcostincurred(MCI).

%#maximize{BR/CI : benefitealized(BR), costincurred(CI)}.

%#maximize{SBR:sumbenefitrealized(SBR)}.
%#minimize{SCI : sumcostincurred(SCI)}.
%#maximize{SBR/SCI:sumbenefitrealized(SBR),sumcostincurred(SCI)}.
#maximize{(SBR/SCI)/T:sumbenefitrealized(SBR),sumcostincurred(SCI),T=1..h}.


#show occurs/2.
#show holds/2.
%#show start/2.

#show final/1.

#show sumbenefitrealized/1.
#show sumcostincurred/1.
%#show finalbenefitcost/1.
#show benefitrealized/2.
#show costincurred/2.
%#show bci/3.