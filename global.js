$(document).ready(function(){ 
  $('.mobile_menu_button').click(function(){
    $('nav ul').slideToggle();
  })

  var numSlides = $('.slide').size();

  $('.slide').hide();
  $('.slide:eq(0)').show();

  //CHANGE INTERVAL TIMING HERE
  var timing = 7000;

  var slideIndex = 0;

  function sliderAnimate(){
    $('.slide:eq(' + slideIndex +')').fadeOut(1000);

    slideIndex++;

    //loop slide index back around to first one
    if (slideIndex == $('.slide').length) {
      slideIndex = 0;
    }

    $('.slide:eq(' + slideIndex +')').fadeIn(1000);
  }

  //Show/hide slides in slider
  var slideTimer = setInterval(sliderAnimate,timing);

  $('.slideshow .right-arrow').click(function(){
    clearInterval(slideTimer);
    $('.slide:eq(' + slideIndex +')').fadeOut(1000);
    slideIndex++;
    //loop slide index back around to first one
    if (slideIndex == $('.slide').length) {
      slideIndex = 0;
    }
    $('.slide:eq(' + slideIndex +')').fadeIn(1000);
    slideTimer = setInterval(sliderAnimate,timing);
  });

  $('.slideshow .left-arrow').click(function(){
    clearInterval(slideTimer);
    $('.slide:eq(' + slideIndex +')').fadeOut(1000);
    slideIndex--;
    //loop slide index back around to first one
    if (slideIndex == -1) {
      slideIndex = $('.slide').length-1;
    }
    $('.slide:eq(' + slideIndex +')').fadeIn(1000);
    slideTimer = setInterval(sliderAnimate,timing);
  });

});


// Copyright 2006-2007 javascript-array.com
var timeout	= 500;
var closetimer	= 0;
var ddmenuitem	= 0;
// open hidden layer

function mopen(id)
{	
	// cancel close timer
	mcancelclosetime();
	// close old layer
	if(ddmenuitem) ddmenuitem.style.visibility = 'hidden';

	// get new layer and show it
	ddmenuitem = document.getElementById(id);
	ddmenuitem.style.visibility = 'visible';

}

// close showed layer
function mclose()
{
	if(ddmenuitem) ddmenuitem.style.visibility = 'hidden';
}

// go close timer
function mclosetime()
{
	closetimer = window.setTimeout(mclose, timeout);
}

// cancel close timer
function mcancelclosetime()
{
	if(closetimer)
	{
		window.clearTimeout(closetimer);
		closetimer = null;
	}
}

// close layer when click-out
document.onclick = mclose; 

var popvid = null;                          // will store the window reference
function popWin(divId) {
   if (typeof(divId)=='string') { divId=document.getElementById(divId); }
   if (!popvid||popvid.closed) {
      popvid=window.open('','vidplayer','width=600,height=400,status=no');
   }
   popvid.document.body.style.backgroundColor='black';
   popvid.focus();
   popvid.document.body.innerHTML='<BR><center>'+divId.innerHTML+'</center>';
   return false;
}
window.onunload=function() {
   // if the user is navigating away from the page, check to see if we
   // opened a video window and if we did, make sure it's closed.
   if (popvid) {
      popvid.close();
   }
}


  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-21397698-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

<!--
/*
JavaScript Image slideshow:
By JavaScript Kit (www.javascriptkit.com)
Over 200+ free JavaScript here!
*/

var slideimages=new Array()
var slidelinks=new Array()
function slideshowimages(){
for (i=0;i<slideshowimages.arguments.length;i++){
slideimages[i]=new Image()
slideimages[i].src=slideshowimages.arguments[i]
}
}

function slideshowlinks(){
for (i=0;i<slideshowlinks.arguments.length;i++)
slidelinks[i]=slideshowlinks.arguments[i]
}

function gotoshow(){
if (!window.winslide||winslide.closed)
winslide=window.open(slidelinks[whichlink])
else
winslide.location=slidelinks[whichlink]
winslide.focus()
}
function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}
function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}
