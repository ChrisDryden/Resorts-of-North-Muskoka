#!/usr/bin/perl
#

#Make sure that the above line is at the very first line, not
#several lines down, and that it is completely flush with 
#the left margin, or your script will not work.

use CGI;
$query = new CGI;

#You need to modify this script at all parts of Step B

#Depending on where Perl is on your server, the above location
#may not be correct.  To find where Perl is, telnet to your
#server and at the prompt type: which perl  This will tell you
#the correct path to Perl on your server.  Or, contact your
#server administrator

#Script Description
  #Unique script ID: 37f3-5b2d
  #Created on:       12/19/2001
  #Last edited on:   12/19/2001
  #Script class:     D

#STEP A================================

#A1. The following lines get and process data passed 
#through the URL, do not modify
$stringpassed=$ENV{'QUERY_STRING'};

#A2. Replace all plusses with spaces for data passed via URL
$stringpassed=~s/\+/ /g;

#STEP B================================
######################################################
# START OF CONFIGURATION
######################################################

#B1. REQUIRED: The location of event data file on your server.  This must
#be the PATH to your data file, not the URL of your data file!
#If this file is placed in the SAME folder as this script, just type the filename below.
#If this file is located in DIFFERENT folder as this script, use the FULL PATH (NOT URL).
#This file will be automatically created when you add your first event.

  $data="eventpublisher.txt";

#B1b. REQUIRED: The location of your TEMPORARY event data file on your server.
#Must be the PATH to your temporary data data file, not the URL.  Use a file
#extension other than .tmp to avoid possible conflicts within script.
#If this file is placed in the SAME folder as this script, just type the filename below.
#If this file is located in DIFFERENT folder as this script, use the FULL PATH (NOT URL).
#This file will be automatically created when a user add the first temporary event.

  $tempdata="eventpublisher.tempdata";

#B1c. OPTIONAL: You can format the opening and closing HTML
#of your admin mode in a separate file that can be written in
#regular HTML and saved on your server. For ease of configuration,
#place it in the same directory as your icon images.
#Note: this file must have three plusses +++
#where you want your search results inserted.

  $openinghtml="/var/www/html/domains/haliburtonatv/eventpublisher/icons/template.htm";

#B2. REQUIRED: The URL of this file in your cgi-bin directory.  You must
#provide the full URL, beginning with http://

  $thisurl="http://www.north-muskoka.com/bondi/eventpublisher.cgi";

#B4. REQUIRED TO ADD, DELETE, OR MODIFY.
#Change password to any combination of letters (A-Z, a-z) and
#numbers 0-1.  USE ONLY LETTERS AND NUMBERS

  $adminpassword="upoint";

#B5. URL to send users to after posting, editing, or getting errors.
#This is usually:
# (1) the admin form (if events are added by you most of the time) OR
# (2) the user submit form (if events are submitted by users most of the time)OR
# (3) this script itself (if you want to show the existing events after posting).

 $forwardingURL="http://www.north-muskoka.com/bondi/eventpublisher.cgi";
 $forwardingURL1="http://www.north-muskoka.com/bondi/eventpublisher_admin.htm";


#B16. URL to the base ICON images directory for field:
#The URL should end with a forwardslash.

  $baseurltoIcon="http://www.randdwebhosting.com/domains/haliburtonatv/eventpublisher/icons/";

#B17. Maximum number of events to display (sorted according to event date - event on
#December 01, 2001 will be displayed on top of event on December 31, 2001).

  $maximumpage=100;

#B18. Font settings of the event display

 $fontface ="";   ### Recommended: "Verdana, Arial"
 $fontsize= "3";                ### Used for event title and description only ###
 $fonttitlecolor = "#800000";
 $fontsubtitlecolor ="#800000"; ### Used for event sub titles such as "Venue", "Date" ....

#B19. ****** REMEMBER THIS: IMPORTANT ****
#Open up all the *.htm forms that come with this script. Replace the form action URL
#under the tags "<FORM ACTION="http://....." to the URL of this script.

######################################################
# END OF CONFIGURATION
######################################################

$maximum=100;

@variablenames = $query->param;
foreach $variable (@variablenames){
$value=$query->param($variable);
$tempapprove{$variable}="$value";}

#STEP D================================
#You should not need to modify this section at all

#D1. Check to see if opening html file is on server
if (-e "$openinghtml"){

#D2. If so, open it and write opening and closing text to different strings
#to be used throughout the script
$problem="Can't open template file.  Make sure you are referencing the file and not just a directory.";
open(OPENING, "$openinghtml") || &security;
@wholefile=<OPENING>;
close(OPENING);
$fulltemplate=join("\n",@wholefile);
($templatestart,$templateend)=split(/\+\+\+/,$fulltemplate);}
else{

#D3. If template file not found, use this for now
$templatestart="<!-- \"Start of Specials Publisher Output\" -->";
$templateend="<!-- \"End of Specials Publisher Output\" -->";}
  $delimiter="\t";

#D6. Get Password Entered by User
  $checkpassword=$query->param('checkpassword');

#D7. Figure out what action user wants to take.
  $actiontotake=$query->param('actiontotake');

  $linenumberpass=$query->param('linenumberpass');

#D8. If user wants to delete record, and has already
#verified password, then go to the makechange subroutine
if ($actiontotake eq "Delete Record"){
$recordaction="Deleted";
&makechange;
exit;}

#D9. If user wants to edit record, and has already
#verified password, then go to the makechange subroutine
if ($actiontotake eq "Edit Record"){
$recordaction="Edited";
&makechange;
exit;}

#D10. If user wants to edit record, to go subroutine to verify
if ($actiontotake eq "Edit"){
&edit;
exit;}

#D11. If user wants to delete record, to go subroutine to verify
if ($actiontotake eq "Delete"){
&delete;
exit;}

#D12. If user wants to add record, go to add subroutine
if ($actiontotake eq "Add"){
&addrecord;
exit;}

#D13. If user wants to add record to temporary file
if ($actiontotake eq "Addtemp"){
&addtemp;
exit;}

#D14. If owner wants to evaluate records in temp file
if ($actiontotake eq "Scrolltemp"){
&scrolltemp;
exit;}

#D15. If user wants to update temp file
if ($actiontotake eq "Updatetemp"){
&updatetemp;
exit;}

#STEP E================================
#E1. Get the data passed from user
  $Event=$query->param('Event');
  $Eventwork=lc($Event);
if ($Eventwork eq "select"){
$Eventwork="";
$Event="";}
  $Eventpass="$Event";

#E1. Get the data passed from user
  $Description=$query->param('Description');
  $Descriptionwork=lc($Description);
if ($Descriptionwork eq "select"){
$Descriptionwork="";
$Description="";}
  $Descriptionpass="$Description";

#E1. Get the data passed from user
  $Venue=$query->param('Venue');
  $Venuework=lc($Venue);
if ($Venuework eq "select"){
$Venuework="";
$Venue="";}
  $Venuepass="$Venue";

#E1. Get the data passed from user
  $Month=$query->param('Month');
  $Monthwork=lc($Month);
if ($Monthwork eq "select"){
$Monthwork="";
$Month="";}
  $Monthpass="$Month";

#E1. Get the data passed from user
  $Year=$query->param('Year');
  $Yearwork=lc($Year);
if ($Yearwork eq "select"){
$Yearwork="";
$Year="";}
  $Yearpass="$Year";

#E6. Get number of records already displayed
  $startitem=$query->param('startitem');

#E7. Figure the last record to display on this page
  $enditem=$startitem+$maximumpage;

#F4a.  Support for European characters.  Uncomment and replace with your
#character set in brackets for all non-English Characters.  See help files.
#$Eventwork=~tr/[»… ÀÈÍÎË]/e/;
#$Eventwork=~tr/[¿¡¬√ƒ≈∆‡·‚„‰ÂÊ]/a/;
#$Eventwork=~tr/[Á«]/c/;
#$Eventwork=~tr/[ÏÌÓÔÕŒœÃ]/i/;
#$Eventwork=~tr/[“”‘’÷ÚÛÙıˆÙ]/o/;
#$Eventwork=~tr/[Ÿ⁄€‹˘˙˚¸]/u/;
($Eventone, $Eventtwo, $Eventthree, $Eventfour, $Eventfive, $Specialsix, $Specialseven)=split(/ /, $Eventwork);
#F4a.  Support for European characters.  Uncomment and replace with your
#character set in brackets for all non-English Characters.  See help files.
$Lo1="P"; $Lo2="is";
#$Descriptionwork=~tr/[»… ÀÈÍÎË]/e/;
#$Descriptionwork=~tr/[¿¡¬√ƒ≈∆‡·‚„‰ÂÊ]/a/;
#$Descriptionwork=~tr/[Á«]/c/;
#$Descriptionwork=~tr/[ÏÌÓÔÕŒœÃ]/i/;
#$Descriptionwork=~tr/[“”‘’÷ÚÛÙıˆÙ]/o/;
#$Descriptionwork=~tr/[Ÿ⁄€‹˘˙˚¸]/u/;
($Descriptionone, $Descriptiontwo, $Descriptionthree, $Descriptionfour, $Descriptionfive, $Descriptionsix, $Descriptionseven)=split(/ /, $Descriptionwork); $Text1="Fr"; $Text2="Ev"; $Text3="her";
#F4a.  Support for European characters.  Uncomment and replace with your
#character set in brackets for all non-English Characters.  See help files.
$Hi1="ee"; $Hi2="ent"; $Hi3="ubl";
#$Venuework=~tr/[»… ÀÈÍÎË]/e/;
#$Venuework=~tr/[¿¡¬√ƒ≈∆‡·‚„‰ÂÊ]/a/;
#$Venuework=~tr/[Á«]/c/;
#$Venuework=~tr/[ÏÌÓÔÕŒœÃ]/i/;
#$Venuework=~tr/[“”‘’÷ÚÛÙıˆÙ]/o/;
#$Venuework=~tr/[Ÿ⁄€‹˘˙˚¸]/u/;
($Venueone, $Venuetwo, $Venuethree, $Venuefour, $Venuefive, $Venuesix, $Venueseven)=split(/ /, $Venuework);
#F4a.  Support for European characters.  Uncomment and replace with your
#character set in brackets for all non-English Characters.  See help files.
#$Monthwork=~tr/[»… ÀÈÍÎË]/e/;
#$Monthwork=~tr/[¿¡¬√ƒ≈∆‡·‚„‰ÂÊ]/a/;
#$Monthwork=~tr/[Á«]/c/;
#$Monthwork=~tr/[ÏÌÓÔÕŒœÃ]/i/;
#$Monthwork=~tr/[“”‘’÷ÚÛÙıˆÙ]/o/;
#$Monthwork=~tr/[Ÿ⁄€‹˘˙˚¸]/u/;
($Monthone, $Monthtwo, $Monththree, $Monthfour, $Monthfive, $Monthsix, $Monthseven)=split(/ /, $Monthwork);
#F4a.  Support for European characters.  Uncomment and replace with your
#character set in brackets for all non-English Characters.  See help files.
#$Yearwork=~tr/[»… ÀÈÍÎË]/e/;
#$Yearwork=~tr/[¿¡¬√ƒ≈∆‡·‚„‰ÂÊ]/a/;
#$Yearwork=~tr/[Á«]/c/;
#$Yearwork=~tr/[ÏÌÓÔÕŒœÃ]/i/;
#$Yearwork=~tr/[“”‘’÷ÚÛÙıˆÙ]/o/;
#$Yearwork=~tr/[Ÿ⁄€‹˘˙˚¸]/u/;
$comp1="INT"; $comp2="O"; $comp3="U"; $lcomp1="int"; $lcomp2="po"; $lcomp3="u";
$and1="b"; $and2="y";
($Yearone, $Yeartwo, $Yearthree, $Yearfour, $Yearfive, $Yearsix, $Yearseven)=split(/ /, $Yearwork);


#STEP G================================
#Do not modify this section

#G1. Open datafile and write contents to an array, if can't open report the problem at the security subroutine
$problem="You do not have a file to search on the server.  Please ADD test records before trying to search your test data file.";
open (FILE, "$data") || &security;
@all=<FILE>;
close (FILE);

#G2.  The line below is required, do not modify
print "Content-type: text/html\n\n";

#G3. Display HTML Header
if ($adminpassword eq $checkpassword){
print "$templatestart\n";}
else {
print "<!-- \"Start of \@1 Event Publisher Output\" -->";}

#STEP H================================
#H1. Read each line of the data file, compare with search words

foreach $line (@all){
$line=~s/\n//g;
$loopsaround++;

$checkleng=length($line);
if ($checkleng<2){next};

$linetemp1=lc($line);

#H1a.  Support for European characters.  Uncomment and replace with your
#character set in brackets for all non-English Characters.  See help files.
#$linetemp1=~tr/[»… ÀÈÍÎË]/e/;
#$linetemp1=~tr/[¿¡¬√ƒ≈∆‡·‚„‰ÂÊ]/a/;
#$linetemp1=~tr/[Á«]/c/;
#$linetemp1=~tr/[ÏÌÓÔÕŒœÃ]/i/;
#$linetemp1=~tr/[“”‘’÷ÚÛÙıˆÙ]/o/;
#$linetemp1=~tr/[Ÿ⁄€‹˘˙˚¸]/u/;

($Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$linetemp1);

#H9. This line specifies the fields to sort results by
#See help databases for patches to allow various kinds of sorts
$line="$Year$Month$Day$delimiter$loopsaround$delimiter$line";

#H9.5 This line removes stray leading spaces before sorting your results
$line=~s/^ +//;

$increcount=0;
#H12. Look for matches in field named Event
if (($Event =~/\b$Eventone/ && $Event =~/\b$Eventtwo/ && $Event =~/\b$Eventthree/ && $Event =~/\b$Eventfour/  && $Event =~/\b$Eventfive/ && $Event=~/\b$Specialsix/ && $Event=~/\b$Specialseven/) || !$Eventwork) {
$increcount++;}

#H12. Look for matches in field named Description
if (($Description =~/\b$Descriptionone/ && $Description =~/\b$Descriptiontwo/ && $Description =~/\b$Descriptionthree/ && $Description =~/\b$Descriptionfour/  && $Description =~/\b$Descriptionfive/ && $Description=~/\b$Descriptionsix/ && $Description=~/\b$Descriptionseven/) || !$Descriptionwork) {
$increcount++;}

#H12. Look for matches in field named Venue
if (($Venue =~/\b$Venueone/ && $Venue =~/\b$Venuetwo/ && $Venue =~/\b$Venuethree/ && $Venue =~/\b$Venuefour/  && $Venue =~/\b$Venuefive/ && $Venue=~/\b$Venuesix/ && $Venue=~/\b$Venueseven/) || !$Venuework) {
$increcount++;}

#H12. Look for matches in field named Month
if (($Month =~/\b$Monthone/ && $Month =~/\b$Monthtwo/ && $Month =~/\b$Monththree/ && $Month =~/\b$Monthfour/  && $Month =~/\b$Monthfive/ && $Month=~/\b$Monthsix/ && $Month=~/\b$Monthseven/) || !$Monthwork) {
$increcount++;}

#H12. Look for matches in field named Year
if (($Year =~/\b$Yearone/ && $Year =~/\b$Yeartwo/ && $Year =~/\b$Yearthree/ && $Year =~/\b$Yearfour/  && $Year =~/\b$Yearfive/ && $Year=~/\b$Yearsix/ && $Year=~/\b$Yearseven/) || !$Yearwork) {
$increcount++;}

if ($line=~/markedtoedit/ && $actiontotake eq "markedtoedit"){
$line=~s/markedtoedit//g;
push (@keepers2,$line);}
$line=~s/markedtoedit//g;
if ($increcount==5){
push (@keepers,$line);}}

#STEP J================================
if ($actiontotake eq "markedtoedit"){
@keepers=@keepers2;}
#J1. Sort matches stored in array. 
@keepers=sort(@keepers);

#J2. Get and display number of matches found
$length1=@keepers;

#J3. If the number of matches is less than enditem, adjust
if ($length1<$enditem){
$enditem=$length1;
$displaystat="Y";}

#J4. The first field about to display
$disstart=$startitem+1;

#J5. Show user total number of matches found
if ($length1){
print "";
} else {
print "No event.<P>\n";}

#STEP K================================
#K1. Do some HTML formatting before showing results
print "<BODY BACKGROUND=\"../seamback1.jpg\"><table>\n";
#K4. Keep track of results processed on this page
foreach $line (@keepers){

#K5. Delete stray hard returns
$line=~s/\n//g;

#K6. Keep track of records displayed

$countline1++;

#K7. Decide whether or not this record goes on this page
if ($countline1>$startitem && $countline1<=$enditem){

#K8. Open each line of sorted array for displaying

($sortfield,$loopsaround,$Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$line);


#K15. Formatting for field Event.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Icon){

print "<tr valign=top><td colspan=2><img src=\"$baseurltoIcon$Icon.gif\"><hr width=\"95%\" align=center><font face=\"$fontface\" color=\"$fonttitlecolor\" size=\"$fontsize\"><b>$Event</b></font></td></tr>\n";}
else {
print "<tr valign=top><td colspan=2><hr width=\"95%\" align=center><font face=\"$fontface\" color=\"$fonttitlecolor\" size=\"$fontsize\"><b>$Event</b></font></td></tr>\n";}

#K15. Formatting for field Description.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Description){
print "<tr valign=top><td colspan=2><font face=\"$fontface\" size=\"$fontsize\">$Description</font></td></tr>\n";}

#K15. Formatting for field Venue.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Venue){
print "<tr valign=top><td><font face=\"$fontface\" color=\"$fontsubtitlecolor\" size=\"2\"><b>Location:</b></font></td><td><font face=\"$fontface\" size=\"2\">$Venue</font></td></tr>\n";}

if ($Month eq "01"){
 $Month2 = "January";}
if ($Month eq "02"){
 $Month2 = "February";}
if ($Month eq "03"){
 $Month2 = "March";}
if ($Month eq "04"){
 $Month2 = "April";}
if ($Month eq "05"){
 $Month2 = "May";}
if ($Month eq "06"){
 $Month2 = "June";}
if ($Month eq "07"){
 $Month2 = "July";}
if ($Month eq "08"){
 $Month2 = "August";}
if ($Month eq "08"){
 $Month2 = "September";}
if ($Month eq "10"){
 $Month2 = "October";}
if ($Month eq "11"){
 $Month2 = "November";}
if ($Month eq "12"){
 $Month2 = "December";}

#K15. Formatting for field Day.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
#if ($Day){
#print "<tr valign=top><td><font face=\"$fontface\" color=\"$fontsubtitlecolor\" size=\"1\"><b>Date:</b></font</td><td><font face=\"$fontface\" size=\"2\">$Month2 $Day, $Year</font></td></tr>\n";}

#K15. Formatting for field Time.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Time){
print "<tr valign=top><td><font face=\"$fontface\" color=\"$fontsubtitlecolor\" size=\"2\"><b>Time:</b></font></td><td><font face=\"$fontface\" size=\"2\">$Time</font></td></tr>\n";}

#K15. Formatting for field Website.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Website){
print "<tr valign=top><td><font face=\"$fontface\" color=\"$fontsubtitlecolor\" size=\"2\"><b>Web:</font></td><td><a href=\"$Website\" target=\"_blank\"><font face=\"$fontface\" size=\"2\">$Website</a></font></td></tr>\n";}

#K15. Formatting for field Email.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Email){
print "<tr valign=top><td><font face=\"$fontface\" color=\"$fontsubtitlecolor\" size=\"2\"><b>Email:</font></td><td><a href=\"mailto:$Email\"><font face=\"$fontface\" size=\"2\">$Email</a></font></td></tr>\n";}

#K15. Formatting for field Public_Remarks.  If you add any HTML, make sure you
#put a backslash in front of all quote marks inside print statements
if ($Public_Remarks){
print "<tr valign=top><td></td><td><font color=\"#666666\" face=\"$fontface\" size=\"1\">$Public_Remarks</font></td></tr>\n";}
#K11. Check passwords before showing edit and delete buttons
if ($adminpassword eq $checkpassword){
print "<tr valign=top><td colspan=2><form method=POST action=\"$thisurl\"><input type=hidden name=\"linenumberpass\" value=\"$loopsaround\"><input type=hidden name=\"checkpassword\" value=\"$checkpassword\"><input type=submit name=\"actiontotake\" value=\"Edit\"> <input type=submit name=\"actiontotake\" value=\"Delete\"></td></tr></form>\n";}

#STEP L================================
#L1. If total displayed equals maximum you set, then exit
if ($countline1 == $maximum && $maximum){
$problem2="Your search was terminated at $maximum records, please be more specific in your search";
last;}

#L2. If script just got to last match then exit program
if ($length1 == $countline1){
last;}

#L3. If script is at the end of a page then show NEXT button
if ($countline1 == $enditem && $displaystat ne "Y"  && $maximum>$countline1){
$stopit="Y";
last;
}

}}

print "</table>\n";
$fcc="8"; $fcd="1"; $fce="w"; $fcf="tp"; $fcg="dn"; $fci="e";
$checkfcc="ne"; $checkfcd="t"; $checkfcf="s"; $checkfcg="ef"; $checkfci="ank"; $checkfcj="_bl";
$mer1="<fon$checkfcd fac$fci=\"$fontface\" siz$fci=\"$fcd\" color=\"#$fcc$fcc$fcc$fcc$fcc$fcc\">
$Text1$Hi1 \@$fcd $Text2$Hi2 $Lo1$Hi3$Lo2$Text3 $and1$and2 <a href=\"h$checkfcd$fcf://
$fce$fce$fce.$lcomp3$lcomp2$lcomp1.$checkfcc$checkfcd/cgiscrip$checkfcd$checkfcf.up$fcg
?r$checkfcg=$Text1$Hi1$Text2$Hi2$Lo1$Hi3$Lo2$Text3\" tar";
$mer2="get=\"$checkfcj$checkfci\">$comp3$Lo1$comp2$comp1</a></font>";
$mer3="$mer1$mer2";
#L4. Display NEXT MATCHES button
if ($stopit eq "Y"){
print "<form method=POST action=\"$thisurl\">\n";

#L5. Pass hidden variables so script will know how to display next page
print "<input type=hidden name=\"Event\" value=\"$Eventpass\"> \n";
print "<input type=hidden name=\"Description\" value=\"$Descriptionpass\"> \n";
print "<input type=hidden name=\"Venue\" value=\"$Venuepass\"> \n";
print "<input type=hidden name=\"Month\" value=\"$Monthpass\"> \n";
print "<input type=hidden name=\"Year\" value=\"$Yearpass\"> \n";
print "<input type=hidden name=\"checkpassword\" value=\"$checkpassword\"> \n";
print "<input type=hidden name=\"startitem\" value=\"$enditem\"> \n";}
$errormode ="$mer1";
if (($stopit eq "Y") and ($adminpassword eq $checkpassword)){
print "<input type=submit value=\"Get Next Matches\"></form>\n";
}

#L6. Show problems
if ((!$mer1) or (!$mer2) or (!$mer3)){
&low;}
if ($problem2){
print "$problem2";}
else {
print "$mer3";
}

#L8. If opening.htm was found, show its closing html codes
if (!$errormode) {
&low;}
srand();
$checkval=int(rand(30));
if ($checkval==3){
print "";}
if ($adminpassword eq $checkpassword){
print "$templateend\n";}
else {
print "<!-- \"End of \@1 Event Publisher Output\" -->";}
exit;

#STEP M================================

sub security{
#M1. This is the subroutine that reports all problems
print "Content-type: text/html\n\n";

print "$templatestart\n";
print "<CENTER><FONT size=+2>Data Error</FONT></CENTER><P>\n";
print "<FONT size=\"+1\">Please correct the following error:<blockquote>$problem</blockquote></FONT>\n";
print "$templateend\n";
exit;
}

sub low{
#M1. This is the subroutine that reports all problems
print "$templatestart\n";
print "<CENTER><FONT size=+2>Data Error</FONT></CENTER><P>\n";
print "<FONT size=\"+1\">Error:<blockquote>Script Corrupted!</blockquote></FONT>\n";
print "$templateend\n";
exit;
}
#STEP N================================
sub edit{
#N1. Open data file and read it
$problem="Can't open data file to read from it at edit subroutine";
open (FILE,"$data") || &security;
@all=<FILE>;
close (FILE);

#N2. Read each line of the data file
foreach $line (@all){
$line=~s/\n//g;
($copyIcon,$copyEvent,$copyDescription,$copyVenue,$copyDay,$copyMonth,$copyYear,$copyTime,$copyWebsite,$copyEmail,$copyPublic_Remarks,$copyPrivate_Remarks,$skipthisfield)=split (/$delimiter/,$line);

$keepcount++;

#N3. Find the line user wants to modify
if ($keepcount==$linenumberpass){
$linetokeep=$line;
$linetokeep=~s/markedtoedit//g;
last;
}
}

#N4. Check password sent via hidden field
if ($adminpassword ne $checkpassword){
$problem="Your password does not match the master password and appears to have been changed since logging onto this record.";
&security;}

#N6. Split matching line into its respective variables
($Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$linetokeep);

#Required Header, do not delete
print "Content-type: text/html\n\n";

#N8. If can't find opening html, display default header
print "$templatestart\n";

print "<P><FONT face=\"Verdana, arial\" size=\"2\"><b><font color=red>Admin Mode:</font> Edit this Record</b></FONT>\n";

print "<BR><FORM ACTION=\"$thisurl\" METHOD=\"POST\"><table>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Icon:</td><td><select name=\"Icon\">\n";
print "<option>$Icon\n";
print "<option>Select\n";
print "<option>Article\n";
print "<option>Book\n";
print "<option>Calendar\n";
print "<option>Commercial\n";
print "<option>Computer\n";
print "<option>Confidential\n";
print "<option>Gift\n";
print "<option>Graph\n";
print "<option>House\n";
print "<option>Image\n";
print "<option>Internet\n";
print "<option>Lock\n";
print "<option>Mail\n";
print "<option>Note\n";
print "<option>People\n";
print "<option>Record\n";
print "<option>Recycle\n";
print "<option>Search\n";
print "<option>Tick\n";
print "<option>View\n";
print "</select>\n";

if ($Icon){
print " <img src=\"$baseurltoIcon$Icon.gif\"></td></tr>";}

print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><font color=red><b>*</b></font> <b>Event:</td><td><input type=text name=\"Event\"  value=\"$Event\" size=45></td></tr>\n";
$Description=~s/<br>/\n/g;
$Description=~s/<BR>/\n/g;
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><font color=red><b>*</b></font> <b>Description:</td><td><textarea name=\"Description\" cols=60 rows=6>$Description</textarea></td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Venue:</td><td><input type=text name=\"Venue\"  value=\"$Venue\" size=35></td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><font color=red><b>*</b></font> <b>Date:</td><td><select name=\"Day\">\n";
print "<option>$Day\n";
print "<option>Select\n";
print "<option>01\n";
print "<option>02\n";
print "<option>03\n";
print "<option>04\n";
print "<option>05\n";
print "<option>06\n";
print "<option>07\n";
print "<option>08\n";
print "<option>09\n";
print "<option>10\n";
print "<option>11\n";
print "<option>12\n";
print "<option>13\n";
print "<option>14\n";
print "<option>15\n";
print "<option>16\n";
print "<option>17\n";
print "<option>18\n";
print "<option>19\n";
print "<option>20\n";
print "<option>21\n";
print "<option>22\n";
print "<option>23\n";
print "<option>24\n";
print "<option>25\n";
print "<option>26\n";
print "<option>27\n";
print "<option>28\n";
print "<option>29\n";
print "<option>30\n";
print "<option>31\n";
print "</select>\n";
print "<FONT face=\"Verdana, arial\" size=\"2\">:<select name=\"Month\">\n";
print "<option>$Month\n";
print "<option>Select\n";
print "<option>01\n";
print "<option>02\n";
print "<option>03\n";
print "<option>04\n";
print "<option>05\n";
print "<option>06\n";
print "<option>07\n";
print "<option>08\n";
print "<option>09\n";
print "<option>10\n";
print "<option>11\n";
print "<option>12\n";
print "</select>\n";
print "<FONT face=\"Verdana, arial\" size=\"2\">:<select name=\"Year\">\n";
print "<option>$Year\n";
print "<option>Select\n";
print "<option>2001\n";
print "<option>2002\n";
print "<option>2003\n";
print "<option>2004\n";
print "<option>2005\n";
print "<option>2006\n";
print "<option>2007\n";
print "<option>2008\n";
print "<option>2009\n";
print "<option>2010\n";
print "<option>2011\n";
print "<option>2012\n";
print "<option>2013\n";
print "<option>2014\n";
print "<option>2015\n";
print "</select> <font face=\"Verdana, arial\" color=\"#888888\" size=1>(DD:MM:YY)</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Time:</td><td><input type=text name=\"Time\"  value=\"$Time\" size=35> <font face=\"Verdana, arial\" color=\"#888888\" size=1>eg. 8:30am ~ 9pm</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Website:</td><td><input type=text name=\"Website\"  value=\"$Website\" size=45><BR> <font face=\"Verdana, arial\" color=\"#888888\" size=1>Start with http:// if used.</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Email:</td><td><input type=text name=\"Email\"  value=\"$Email\" size=30></td></tr>\n";
$Public_Remarks=~s/<br>/\n/g;
$Public_Remarks=~s/<BR>/\n/g;
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Public Remarks:</td><td><textarea name=\"Public_Remarks\" cols=40 rows=4>$Public_Remarks</textarea><br> <font face=\"Verdana, arial\" color=\"#888888\" size=1>This remark is shown to the public.</td></tr>\n";
$Private_Remarks=~s/<br>/\n/g;
$Private_Remarks=~s/<BR>/\n/g;
print "<tr valign=top><td><FONT face=\"Verdana, arial\" color=red size=\"2\"><b>Private Remarks:</td><td><textarea name=\"Private_Remarks\" cols=40 rows=4>$Private_Remarks</textarea><br> <font face=\"Verdana, arial\" color=\"#888888\" size=1>This remark is shown ONLY to the administrator.</td></tr>\n";
#N10. Pass values to next screen
print "</table>\n";
print "<input type=hidden name=\"linenumberpass\" value=\"$linenumberpass\">\n";
print "<input type=hidden name=\"checkpassword\" value=\"$checkpassword\">\n";
print "<input type=submit name=\"actiontotake\" value=\"Edit Record\"></form><P>\n";

print "$templateend\n";
exit;
}

#STEP O================================
sub delete{
#O1. Open data file and read it
$problem="Can't open data file to read from it at delete subroutine";
open (FILE,"$data") || &security;
@all=<FILE>;

close (FILE);
#O2. Read each line of the file
foreach $line (@all){
$line=~s/\n//g;
($copyIcon,$copyEvent,$copyDescription,$copyVenue,$copyDay,$copyMonth,$copyYear,$copyTime,$copyWebsite,$copyEmail,$copyPublic_Remarks,$copyPrivate_Remarks,$skipthisfield)=split (/$delimiter/,$line);

$keepcount++;
#O3. Find line to delete
if ($keepcount==$linenumberpass){
$linetokeep=$line;
$linetokeep=~s/markedtoedit//g;
last;
}
}
($Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$linetokeep);

#O4. Check password sent via hidden field
if ($adminpassword ne $checkpassword){
$problem="Your password does not match the master password.";
&security;}

#O6. Requred Header, do not delete
print "Content-type: text/html\n\n";

print "$templatestart\n";

print "<P><FONT face=\"Verdana, arial\" size=\"2\"><b><font color=red>Admin Mode:</font> Delete this Record?</b></FONT>\n";
($Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$linetokeep);

#O7. Show validation HTML
print "<form method=POST action=\"$thisurl\">\n";
print "<table>\n";
print "<tr valign=top><td width=\"150\"><FONT face=\"Verdana, arial\" size=\"2\"><b>Icon: </td><td><FONT face=\"Verdana, arial\" size=\"2\">$Icon";

if ($Icon){
print " <img src=\"$baseurltoIcon$Icon.gif\"></td></tr>";}
else {
print "Nil</td></tr>";}
if ($Month eq "01"){
 $Month2 = "January";}
if ($Month eq "02"){
 $Month2 = "February";}
if ($Month eq "03"){
 $Month2 = "March";}
if ($Month eq "04"){
 $Month2 = "April";}
if ($Month eq "05"){
 $Month2 = "May";}
if ($Month eq "06"){
 $Month2 = "June";}
if ($Month eq "07"){
 $Month2 = "July";}
if ($Month eq "08"){
 $Month2 = "August";}
if ($Month eq "08"){
 $Month2 = "September";}
if ($Month eq "10"){
 $Month2 = "October";}
if ($Month eq "11"){
 $Month2 = "November";}
if ($Month eq "12"){
 $Month2 = "December";}

print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Event: </td><td><FONT face=\"Verdana, arial\" color=\"$fonttitlecolor\" size=\"2\"><b>$Event</b></td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Description: </td><td><FONT face=\"Verdana, arial\" size=\"2\">$Description</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Venue: </td><td><FONT face=\"Verdana, arial\" size=\"2\">$Venue</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Date: </td><td><FONT face=\"Verdana, arial\" size=\"2\">$Month2 $Day, $Year</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Time: </td><td><FONT face=\"Verdana, arial\" size=\"2\">$Time</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Website: </td><td><FONT face=\"Verdana, arial\" size=\"2\"><a href=\"$Website\" target=\"_blank\">$Website</a></td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Email: </td><td><FONT face=\"Verdana, arial\" size=\"2\"><a href=\"mailto:$Email\">$Email</a></td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\"><b>Public Remarks: </td><td><FONT face=\"Verdana, arial\" size=\"2\">$Public_Remarks</td></tr>\n";
print "<tr valign=top><td><FONT face=\"Verdana, arial\" size=\"2\" color=red><b>Private Remarks: </td><td><FONT face=\"Verdana, arial\" color=red size=\"2\">$Private_Remarks</td></tr>\n";
print "</table><BR>\n";
print "<input type=hidden name=\"linenumberpass\" value=\"$linenumberpass\">\n";
print "<input type=hidden name=\"checkpassword\" value=\"$checkpassword\">\n";
print "<input type=submit name=\"actiontotake\" value=\"Delete Record\"></form><P>\n";
#If opening.htm was not found, show default closing html codes
print "$templateend\n";
exit;
}
#STEP P================================
sub makechange{
#P1.  For each variable, translate it, remove any delimiters that
#user may have accidentally included, replace hard returns with
#HTML line breaks, and delete all carriage returns
#Go to get variable subroutine and make sure add preferences apply
 if ($recordaction eq "Edited"){
&getvariables;}
#P2. This step either replaces or empties the existing line
if ($recordaction eq "Deleted"){
  $replacementline="";}
else{
  $replacementline="$Icon$delimiter$Event$delimiter$Description$delimiter$Venue$delimiter$Day$delimiter$Month$delimiter$Year$delimiter$Time$delimiter$Website$delimiter$Email$delimiter$Public_Remarks$delimiter$Private_Remarks";}
$problem="Can't open data file to read from it";
open (FILE,"$data") || &security;
@all=<FILE>;

close (FILE);
$linenumberpass--;
$all[$linenumberpass]=$replacementline;
$problem="Can't open temporary file.  You need to chmod 777 the <B>directory</B> your data file is in.  See the help files under Permissions for Class B Scripts.";
#P6. Write the entire changed file to a temporary file
open (FILE2,">$data.tmp") || &security;
foreach $line (@all){
$line=~s/\n//g;
print FILE2 "$line\n";}

close(FILE2);

#P7. Rename the temp file to your master data file
$problem="Can't rename file after making change";
rename("$data.tmp", "$data") || &security;
print "Content-type: text/html\n\n";

#P8. If can't find opening html, display default header
print "$templatestart\n";

print "Your record has been $recordaction.  Please click <A href=\"$forwardingURL\">here</A> to view events, or <A href=\"$forwardingURL1\">here</A> to add more events.\n";

close (FILE);
#If opening.htm was not found, show default closing html codes
print "$templateend\n";
exit;
}
#STEP Q================================
#This subroutine adds records to your database
sub addrecord{
#Q1. Check password
if ($adminpassword ne $checkpassword && $adminpassword){
$problem="The password you entered does not match your administration password.  Please press BACK on your browser to fix this problem.";
&security;}
&getvariables;

  $replacementline="$Icon$delimiter$Event$delimiter$Description$delimiter$Venue$delimiter$Day$delimiter$Month$delimiter$Year$delimiter$Time$delimiter$Website$delimiter$Email$delimiter$Public_Remarks$delimiter$Private_Remarks";
#Q3. Write the new record to the bottom of the data file
$problem="Can't write to the data file.  Please verify its location and change its permissions to 777.";
open (FILE2,">>$data") || &security;
print FILE2 "$replacementline\n";
close(FILE2);
print "Content-type: text/html\n\n";

#Q4. If can't find opening html, display default header
print "$templatestart\n";

print "Your record has been added.  Please click <A href=\"$forwardingURL\">here</A> to view events, or <A href=\"$forwardingURL1\">here</A>, to add more events.\n";

#If opening.htm was not found, show default closing html codes
print "$templateend\n";
exit;
}
#STEP R================================
sub getvariables{
#R1. This step checks your variables before adding/editing them
  $Icon=$query->param('Icon');

  $Event=$query->param('Event');

  $Description=$query->param('Description');

  $Venue=$query->param('Venue');

  $Day=$query->param('Day');

  $Month=$query->param('Month');

  $Year=$query->param('Year');

  $Time=$query->param('Time');

  $Website=$query->param('Website');

  $Email=$query->param('Email');

  $Public_Remarks=$query->param('Public_Remarks');

  $Private_Remarks=$query->param('Private_Remarks');

#R3. Replace hard returns with <BR>, cut carriage returns
$Icon=~s/\n/<br>/g;
$Icon=~s/\r//g;
if ($Icon eq "Select"){
$Icon="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Event=~s/\n/<br>/g;
$Event=~s/\r//g;
if ($Event eq "Select"){
$Event="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Description=~s/\n/<br>/g;
$Description=~s/\r//g;
if ($Description eq "Select"){
$Description="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Venue=~s/\n/<br>/g;
$Venue=~s/\r//g;
if ($Venue eq "Select"){
$Venue="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Day=~s/\n/<br>/g;
$Day=~s/\r//g;
if ($Day eq "Select"){
$Day="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Month=~s/\n/<br>/g;
$Month=~s/\r//g;
if ($Month eq "Select"){
$Month="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Year=~s/\n/<br>/g;
$Year=~s/\r//g;
if ($Year eq "Select"){
$Year="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Time=~s/\n/<br>/g;
$Time=~s/\r//g;
if ($Time eq "Select"){
$Time="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Website=~s/\n/<br>/g;
$Website=~s/\r//g;
if ($Website eq "Select"){
$Website="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Email=~s/\n/<br>/g;
$Email=~s/\r//g;
if ($Email eq "Select"){
$Email="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Public_Remarks=~s/\n/<br>/g;
$Public_Remarks=~s/\r//g;
if ($Public_Remarks eq "Select"){
$Public_Remarks="";}
#R3. Replace hard returns with <BR>, cut carriage returns
$Private_Remarks=~s/\n/<br>/g;
$Private_Remarks=~s/\r//g;
if ($Private_Remarks eq "Select"){
$Private_Remarks="";}

#R4. You have marked Event as a field that must contain at least 2
#non-blank characters before allowing the field to be added.  You can change the
#requirement below, or comment out all 6 lines below step to skip validation
$Eventcheck=$Event;
$Eventcheck=~s/ +/ /g;
$Eventcheck=length($Eventcheck);
if ($Eventcheck<2){
$problem="Please press back on your browser and provide more information for the Event field.";
&security;}


#R4. You have marked Description as a field that must contain at least 2
#non-blank characters before allowing the field to be added.  You can change the
#requirement below, or comment out all 6 lines below step to skip validation
$Descriptioncheck=$Description;
$Descriptioncheck=~s/ +/ /g;
$Descriptioncheck=length($Descriptioncheck);
if ($Descriptioncheck<2){
$problem="Please press back on your browser and provide more information for the Description field.";
&security;}


#R4. You have marked Day as a field that must contain at least 1
#non-blank characters before allowing the field to be added.  You can change the
#requirement below, or comment out all 6 lines below step to skip validation
$Daycheck=$Day;
$Daycheck=~s/ +/ /g;
$Daycheck=length($Daycheck);
if ($Daycheck<1){
$problem="Please press back on your browser and provide more information for the Day field.";
&security;}


#R4. You have marked Month as a field that must contain at least 1
#non-blank characters before allowing the field to be added.  You can change the
#requirement below, or comment out all 6 lines below step to skip validation
$Monthcheck=$Month;
$Monthcheck=~s/ +/ /g;
$Monthcheck=length($Monthcheck);
if ($Monthcheck<1){
$problem="Please press back on your browser and provide more information for the Month field.";
&security;}


#R4. You have marked Year as a field that must contain at least 2
#non-blank characters before allowing the field to be added.  You can change the
#requirement below, or comment out all 6 lines below step to skip validation
$Yearcheck=$Year;
$Yearcheck=~s/ +/ /g;
$Yearcheck=length($Yearcheck);
if ($Yearcheck<2){
$problem="Please press back on your browser and provide more information for the Year field.";
&security;}


#R13. You have marked Website as a field that must contain a valid hyperlink
#To remove this requirement, comment out all 4 lines below
$Websitecheck=substr($Website,0,7);
if ($Website && $Websitecheck!~/http:\/\//i){
$problem="The information you have provided in the Website field does not look like a valid hyperlink, beginning with http://.  Please press back on your browser and fix this problem.";
&security;}


#R10. You have marked Email as a field that must contain a valid e-mail
#Address, OR, be empty.  To remove requirement, comment out 9 lines below
$Emailcheck=$Email;
($firstpart,$secondpart)=split(/\@/,$Emailcheck);
if ($Email && (!$firstpart || !$secondpart || $secondpart!~/\./)){
$problem="The information you have provided in the e-mail field does not look like a valid e-mail address.  Please press back on your browser and fix this problem.";
&security;}

#R11. Remove characters that could cause security issues in e-mail field
if ($Emailcheck =~/[\!\|\~\^\'\"]/){
$problem="The information you entered into the e-mail field contains illegal characters.  This field should contain letters, numbers, the \@ symbol, and periods only.  Please press BACK and fix this problem.";
&security;}

}
#STEP S================================
sub addtemp{
#S1. This subroutine adds records to your temporary file for approval
#S2. Check variable sent
&getvariables;

#S3. Randomize in preparation for random generator
srand();
#S4. Get IP address of person posting record
$ipstamp=$ENV{'REMOTE_ADDR'};

#S5. Generate a large random number to serve as key
$randnumb=int(rand(9999999));
  $replacementline="$ipstamp&&temp$randnumb(\+\+)$Icon$delimiter$Event$delimiter$Description$delimiter$Venue$delimiter$Day$delimiter$Month$delimiter$Year$delimiter$Time$delimiter$Website$delimiter$Email$delimiter$Public_Remarks$delimiter$Private_Remarks";
#S6. Write the temp record to the bottom of the 
$problem="Can't write to the data file.  Please verify its location and change its permissions to 777.";
open (FILE2,">>$tempdata") || &security;
print FILE2 "$replacementline\n";
close(FILE2);
print "Content-type: text/html\n\n";

print "$templatestart\n";

#S7. Acknowledge that record has been posted
print "Your record has been sent for evaluation.  Please click <A href=\"$forwardingURL\">here</A> to continue.\n";

print "$templateend\n";
exit;
}
#STEP T================================
sub scrolltemp{
#T1. This step is your interface with the temp file
#T2. Check password
if ($adminpassword ne $checkpassword && $adminpassword){
$problem="The password you entered does not match your administration password.  Please press BACK on your browser to fix this problem.";
&security;}
#T3. Check to make sure that the data file can be opened.
$problem="Unable to open your temporary data file.  It either contains no records, or the path to it is incorrect.";
open (FILE, "$tempdata") || &security;
@all=<FILE>;
close (FILE);

print "Content-type: text/html\n\n";

#T4. Start showing contents of data file
print "$templatestart\n";
print "<form method=POST action=\"$thisurl\"><input type=hidden name=\"checkpassword\" value=\"$checkpassword\"><input type=hidden name=\"actiontotake\" value=\"Updatetemp\">\n";
$checktemp=@all;
if (!$checktemp){
print "Your temporary file contains no records for you to evaluate at this time.  Please click <A href=\"$forwardingURL\">here</A> to continue.<P>\n";
print "$templateend\n";
exit;}
print "<FONT face=\"verdana, arial\" size=\"1\"><B>KEY</B><BR> A=Add to Database<BR> D=Delete from Temp File<BR>E=Add to Database but Mark for Editing<BR>H=Hold in Temp File for Decision Later<BR><BR></FONT>\n";
print "<table>\n";
print "<tr valign=top><td><FONT face=\"verdana, arial\" color=green size=\"2\"><B>A</B></td><td><FONT face=\"verdana, arial\" color=red size=\"2\"><B>D</B></td><td><FONT face=\"verdana, arial\" color=blue size=\"2\"><B>E</B></td><td><FONT face=\"verdana, arial\" color=orange size=\"2\"><B>H</B></td><td><FONT face=\"verdana, arial\" size=\"2\"><b><u>Field</td><td><FONT face=\"verdana, arial\" size=\"2\"><b><u>Contents</td>\n";

foreach $line (@all){
$line=~s/\n//g;
$checkleng=length($line);
if ($checkleng<2){next};

($indexvalues,$stringvalues)=split(/\(\+\+\)/,$line);
($ipaddress,$uniqueapproval)=split(/&&/,$indexvalues);
($Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$stringvalues);

if ($Month eq "01"){
 $Month2 = "January";}
if ($Month eq "02"){
 $Month2 = "February";}
if ($Month eq "03"){
 $Month2 = "March";}
if ($Month eq "04"){
 $Month2 = "April";}
if ($Month eq "05"){
 $Month2 = "May";}
if ($Month eq "06"){
 $Month2 = "June";}
if ($Month eq "07"){
 $Month2 = "July";}
if ($Month eq "08"){
 $Month2 = "August";}
if ($Month eq "08"){
 $Month2 = "September";}
if ($Month eq "10"){
 $Month2 = "October";}
if ($Month eq "11"){
 $Month2 = "November";}
if ($Month eq "12"){
 $Month2 = "December";}

print "<tr><td><input type=radio name=\"$uniqueapproval\" value=A></td><td><input type=radio name=\"$uniqueapproval\" value=D></td><td><input type=radio name=\"$uniqueapproval\" value=E></td><td><input type=radio name=\"$uniqueapproval\" value=H checked></td><td><FONT face=\"verdana, arial\" size=\"2\"><b>IP Address:</td><td><FONT face=\"verdana, arial\" color=red size=\"2\">$ipaddress</td></tr>\n";

if ($Icon){
print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td width=150><FONT face=\"verdana, arial\" size=\"2\"><b>Icon:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Icon <img src=\"$baseurltoIcon$Icon.gif\"></td></tr>\n";}
else {
print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td width=150><FONT face=\"verdana, arial\" size=\"2\"><b>Icon:</td><td><FONT face=\"verdana, arial\" size=\"2\">Nil</td></tr>\n";}

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Event:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Event</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Description:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Description</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Venue:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Venue</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Date:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Month2 $Day, $Year</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Time:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Time</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Website:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Website</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Email:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Email</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Public Remarks:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Public_Remarks</td></tr>\n";

print "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td valign=top><FONT face=\"verdana, arial\" size=\"2\"><b>Private Remarks:</td><td><FONT face=\"verdana, arial\" size=\"2\">$Private_Remarks</td></tr>\n";

$keeptrack2++;
if ($keeptrack2>10){
last};
}
print "</table>\n";

if ($keeptrack2>=10){
print "<input type=submit value=\"Update and Get Next Set\"></form>\n";}

else{
print "<input type=submit value=\"Update\"></form>\n";}

print "$templateend\n";
exit;
}

#STEP U================================
sub updatetemp{
#U1. This step makes changes from temp file
#U2. Check password
if ($adminpassword ne $checkpassword && $adminpassword){
$problem="The password you entered does not match your administration password.  Please press BACK on your browser to fix this problem.";
&security;}
$problem="Unable to open your temporary data file.  It either contains no records, or the path to it is incorrect.";
open (FILE, "$tempdata") || &security;
@all=<FILE>;
close (FILE);

foreach $line (@all){
$line=~s/\n//g;
$checkleng=length($line);
if ($checkleng<2){next};

($indexvalues,$stringvalues)=split(/\(\+\+\)/,$line);
($ipaddress,$uniqueapproval)=split(/&&/,$indexvalues);
($Icon,$Event,$Description,$Venue,$Day,$Month,$Year,$Time,$Website,$Email,$Public_Remarks,$Private_Remarks,$skipthisfield)=split (/$delimiter/,$stringvalues);

if ($tempapprove{$uniqueapproval} eq "A"){
push(@recordstoadd,$stringvalues);}
elsif ($tempapprove{$uniqueapproval} eq "D"){
push(@recordstodelete,$stringvalues);}
elsif ($tempapprove{$uniqueapproval} eq "E"){
push(@recordstoedit,$stringvalues);}
else {
push(@recordstohold,$line);}
}
$problem="Unable to open data file to add records.  Check path to it and its permissions.";
open (FILE, ">>$data") || &security;
foreach $line (@recordstoadd){
$line=~s/\n//g;
print FILE "$line\n";}
close(FILE);
$problem="Unable to open data file to records to edit.  Check path to it and its permissions.";
open (FILE, ">>$data") || &security;
foreach $line (@recordstoedit){
$line=~s/\n//g;
print FILE "markedtoedit$line\n";}
close(FILE);
$problem="Unable to open temporary file to refresh data.  Check path to it and its permissions.";
open (FILE, ">$tempdata") || &security;
foreach $line (@recordstohold){
$line=~s/\n//g;
print FILE "$line\n";}
close(FILE);
$checkhold=@recordstohold;
if ($checkhold){
&scrolltemp;}
print "Content-type: text/html\n\n";

print "$templatestart\n";
print "<P>Your actions have been taken.  Please click <A href=\"$forwardingURL\">here</A> to continue.<P>\n";
print "$templateend\n";
exit;
}
