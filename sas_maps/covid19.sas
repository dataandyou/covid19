%let name=c19;
filename odsout '.';
goptions device=png;
ODS LISTING CLOSE;
ODS HTML path=odsout body="&name..htm" style=htmlblue;
goptions gunit=pct htitle=4 htext=2.0 ftitle="albany amt/bold" ftext="albany amt";
goptions ctext=gray33;
%let override  = 0;

/*----download county level data from nyt github site----*/
%if ^%sysfunc(exist(c19county)) or "&override" ^= "0" %then %do;
    filename f url 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv';
    proc import datafile=f
            out=C19COUNTY
            dbms=csv
            replace;
    getnames = yes;
    guessingrows = 100000;
    run;
    filename f clear;
%end;

proc sort data=c19county out=c192;
by state county date;
run;


/*-----keep the data for last available date----*/
data c192;
set c192;
by state county date;
keep date state county deaths;
if last.county then output;
run;

/*-----find total number of deaths, exclude 'UNKNOWN' county----*/
proc means data=c192(where=(upcase(county)="UNKNOWN")) nway noprint;
var deaths;
output out=s_u(drop=_type_ _freq_) sum=total_deaths;
run;


%let nout = 0;
data _null_;
set s_u;
nout = put(total_deaths,best.);
call symputx("nout",trim(left(nout)),'l');
put "WARNING: " total_deaths best. " deaths ommitted from analysis as they were not assigned to any county";
run;

/*---SAS Map datasets and NYT data follow different naming 
      conventions for counties.
      NYT dataset contains obs for Kansas City,MI which 
      is not a county. I add its deaths to Jackson County, MI
----*/ 



data c192;
set c192;
length ctyname $64;
length stname $64;

where upcase(county) ^= "UNKNOWN";

ctyname = county;
stname = state;

call scan(ctyname,-1,p,l);
/*----- Abc County becomes simply Abc----*/
if upcase(substrn(ctyname,p,l)) in ("COUNTY","PARISH","MUNICIPALITY") then do;
    ctyname = substrn(ctyname,1,p-1);
end;
else if upcase(substrn(ctyname,p,l)) = "CITY" then do;
/*----Abc City becomes Abc with some exceptions----*/
 if (stname ^= "Nevada" or upcase(upcase(ctyname)) ^= "CARSON CITY") and
       (stname ^= "Maryland" or upcase(ctyname) ^= "BALTIMORE CITY") and
       (stname ^= "Missouri" or upcase(ctyname) ^= "ST. LOUIS CITY") and
       (stname ^= "Virginia" or upcase(ctyname) ^= "ROANOKE CITY") and
       (stname ^= "Virginia" or upcase(ctyname) ^= "RICHMOND CITY") and
       (stname ^= "Virginia" or upcase(ctyname) ^= "FAIRFAX CITY") and
       (stname ^= "Virginia" or upcase(ctyname) ^= "BEDFORD CITY") and
       (stname ^= "Virginia" or upcase(ctyname) ^= "FRANKLIN CITY") and
       (stname ^= "Virginia" or upcase(ctyname) ^= "CHARLES CITY") and 
       (stname ^= "Virginia" or upcase(ctyname) ^= "JAMES CITY") 
    then do; 
        ctyname = substrn(ctyname,1,p-1);
    end;
end;
else if upcase(substrn(ctyname,p,l)) = "BOROUGH" then do;
/*-----Abc Borough and City becomes Abc with some exceptions---*/
    if stname ^= "Alaska" or (not (ctyname =: "Wrangell")) then do; 
        ctyname = substrn(ctyname,1,p-1);
        call scan(ctyname,-1,p,l);
        if upcase(substrn(ctyname,p,l)) = "AND" then do;
            ctyname = substrn(ctyname,1,p-1);
        end;
        call scan(ctyname,-1,p,l);
        if upcase(substrn(ctyname,p,l)) = "CITY" then do;
            ctyname = substrn(ctyname,1,p-1);
        end;
    end;
end;

/*----LaSalle is spelled La Salle in gfk maps----*/
if upcase(stname) =: "LO" and upcase(ctyname) = "LASALLE" then do;
    ctyname = "La Salle";
end;

if upcase(stname) = "ALASKA" then do;
    /*----Abc Census Area becomes Abc----*/
    call scan(ctyname,-1,p,l);
    if upcase(substrn(ctyname,p,l)) = "AREA" then do;
        call scan(ctyname,-2,p,l);
        if upcase(substrn(ctyname,p,l)) = "CENSUS" then do;
            ctyname = substrn(ctyname,1,p-1);
        end;
    end;
    
   /*----GFK data still contains some old names, revert to old names---*/
    if ctyname =: "Kusilvak" then ctyname = "Wade Hampton";
end;
    /*----GFK data still contains some old names, revert to old names---*/
if upcase(stname) = "SOUTH DAKOTA" and ctyname = "Oglala Lakota" then
 ctyname = "Shannon";

/*---Remove special characters---*/
if stname ="New Mexico" and ctyname =: "Do" then do;
    ctyname = "Dona Ana";
end;

/*----add stats of Kansas city to Jackson county since there
      is no entry for Kansas City, Mi in the county map data
---*/
if stname = "Missouri" and ctyname = "Kansas" then do;
    ctyname = "Jackson";
end;
drop p l;

county = ctyname;
state = stname;
drop ctyname stname;
run;

/*---Get Current Date and store in dt----*/
proc sql noprint;
select max(date) format=date. into :dt 
from c192;
quit;

proc sort data=c192;
by descending deaths;
run;

proc means data=c192 nway noprint;
var deaths;
output out=s(drop=_type_ _freq_) sum=total_deaths;
run;

%let total_deaths = 0;
data _null_;
set s;
t = put(total_deaths,best.);
call symputx("total_deaths",trim(left(t)),'l');
put "Total deaths attributed to counties is " total_deaths;
run;

/*----attach total deaths to data----*/
data c192_f;
retain total_deaths;
if _n_ = 1 then do;
    set s;
end;
set c192;
run;

/*----Add county id to the data set by matching state and county
      names
-----*/
proc sql noprint;
create table c192_idt as
select c192_f.*, us_counties_attr.id
from  c192_f 
left join mapsgfk.us_counties_attr
     on upcase(c192_f.county)=upcase(us_counties_attr.idname)
     and upcase(c192_f.state)=upcase(us_counties_attr.id1name)
order by us_counties_attr.id;
quit; 

proc sql;
create table dup as
select distinct id,count(id) as n,county,state
from c192_idt
group by id
having n > 1;
quit;

data _null_;
set dup;
if state ^= "Missouri" or county ^= "Jackson" then do;
    put "ERROR: FOUND UNEXPECTED REPEATED COUNTIES";
end;
if _n_ > 1 then do;
    put "ERROR: FOUND UNEXPECTED REPEATED COUNTIES";
end; 
run;

/*-----aggregate to add Kansas City Stats to Jackson County
       all other numbers should not change
----*/
data c192_id;
set c192_idt;
by id;
retain td;
if first.id then td = deaths;
else td = td + deaths;
if last.id then do;
    deaths = td;
    output;
end;
drop td;
run;

proc sort data=c192_id out=map_data2;
by descending deaths;
run;

/*---must be an integer between 1 and 100---*/
%let pct = 75;
data map_data;
set map_data2;
label deaths="Number of deaths";
sum_deaths + deaths;
prop = deaths/total_deaths;
sum_prop + prop;
if floor(100*sum_prop) <= &pct then output; 
if floor(100*sum_prop) >= &pct then stop;
run;

%if ^%sysfunc(exist(us_counties_div)) or "&override" ^= "0" %then %do;
/*---- the NY data in the NYT database 
      is actually the data for all the five boroughs
      Define a new map region to include all the following
      counties
      1. NY
      2. Kings
      3. Bronx
      4. Richmond
      5. Queens
*/

data nyc;
set mapsgfk.us_counties_attr;
where idname in ("New York","Kings","Bronx","Richmond","Queens")
and id1name in ("New York");
;
run;

proc sql;
create table nyc_data as 
select a.*
from  nyc a,mapsgfk.us_counties_attr b
where a.idname = b.idname and a.id1name = b.id1name;
run;
quit;

data us_counties_div;
length div $15;
merge nyc_data(in=in1 keep=id) mapsgfk.us_counties(in=in2);
by id;
/*---this is the id of the NY county in the original data--*/
if in1 then div = "US-36061";
else div = id;
run;
proc sort data=us_counties_div;
by div;
run;
/*----us_counties_div is identical to us_counties
      except that the entire NYC region is mapped
      to US-36061
 ----*/
proc gremove data=us_counties_div out=us_counties_div;
   by div;
   id id;
run;
/*----end creating map----*/
%end;

/*
pattern1 value=solid color='CXBF1C1C'; ****red0 redbrown****;
pattern2 value=solid color='CXD02226'; ****red1****;
pattern3 value=solid color='CXDE363C'; ****red2****;
pattern4 value=solid color='CXE45D66'; ****red3****;
pattern5 value=solid color='CXE76F77'; ****red4****;
pattern6 value=solid color='CXEA8188'; ****red5****;
pattern7 value=solid color='CXED9399'; ****red6****;
pattern8 value=solid color='CXF0A5AA'; ****red7****;
pattern9 value=solid color='CXF3B7BB'; ****lightred8****;
pattern10 value=solid color='CXF6C9CC'; ****lightred9****;
pattern11 value=solid color='CXF9DBDD'; ****lightred10****;
pattern12 value=solid color='CXFCEDEE'; ****palered11****;
pattern13 value=solid color='CXE4F1EA'; ****palegreen10****;
pattern14 value=solid color='CXCBE4DE'; ****lightgreen9****;
pattern15 value=solid color='CXB2D7D2'; ****lightgreen8****;
pattern16 value=solid color='CX99C9C7'; ****green7****;
pattern17 value=solid color='CX80BDBA'; ****green6****;
pattern18 value=solid color='CX67B0AE'; ****green5****;
pattern19 value=solid color='CX4EA3A2'; ****green4****;
pattern20 value=solid color='CX359696'; ****green3****;
pattern21 value=solid color='CX1C898A'; ****green2****;
pattern22 value=solid color='CX037C7E'; ****green1****;
*/

pattern1 value=solid color=orange;
pattern2 value=solid color=purple; ****palered11****;
pattern3 value=solid color='CXBF1C1C'; ****red0 redbrown****;

proc format;
  value deaths 0-100   = '0 - 100'
               101 - 500 = '101 - 500'
               501-2000 = '501 - 2000'
               2000 - high = '>2000'
;
run;
legend1 label =(f="albany amt/bold" position=top j=l h=12pt "Deaths")
 position=(right middle) 
 mode=reserve
 across=1
 shape=bar(0.15in,0.15in)
 ;
title "The shaded regions account for &pct.% of all Covid-19 deaths in US";
title2 "Date : &dt";
footnote j=l "Data Source:https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv";
footnote2 j=l "Total deaths attributed to counties is &total_deaths.";
footnote3 j=l "&nout deaths were ommitted from analysis as they were not attributed to any county.";
footnote4 j=l "Disclaimer: For informational purposes only. No guarantee of correctness.";
*goptions xpixels=4500 ypixels=2000;
proc gmap data=map_data(rename=(id=div)) map=us_counties_div (where=(statecode not in ('AK' 'HI'))) all density=2;
id div;
choro deaths / legend=legend1 discrete coutline = lightgray name="c19";
format deaths deaths.;
run;
quit;

title;
title2;
footnote;
footnote2;
footnote3;

quit;
goptions reset=all;
ODS HTML CLOSE;
ODS LISTING;
