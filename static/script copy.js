pressedcount=0;
function readmore(event) {
	var content=document.getElementById("content");
	content.style.height="auto";
	event.target.style.display="none";
}
function switchtab(event) {
	if (event.target.tagName="H2") {
		var matcher=document.getElementById(event.target.innerHTML);
		var alltabs=document.getElementsByClassName("tab");
		for (x=0; x<alltabs.length; x++) {
			if (alltabs[x].style.backgroundColor="lightgray") {
				alltabs[x].style.backgroundColor="transparent";
			}
		}
		pressedcount++;
		matcher.style.zIndex=pressedcount;
		event.target.parentNode.style.backgroundColor="lightgray";
	}
}
function setup() {
	var header=document.getElementById("header");
	var footer=document.getElementById("footer");
	var sidebar=document.getElementById("sidebar");
	var logo=document.createElement("IMG");
	var linklist=["Home", "Classes", "Activities", "PTO", "Support"];
	logo.setAttribute("src", "logo.png");
	logo.setAttribute("height", "100");
	var nav=document.createElement("NAV");
	var a=null;
	function href() {
		var url=window.location.pathname;
		a.setAttribute("href", a.innerHTML+".html");
		nav.appendChild(a);
		if (a.innerHTML+".html"==url.substr(url.lastIndexOf("/")+1)) {
			a.style.backgroundColor="white";
			a.style.color="black";
		}
	}
	for (ihtml=0; ihtml<linklist.length; ihtml++) {
		a=document.createElement("A");
		a.innerHTML=linklist[ihtml];
		href();
	}
	header.appendChild(nav);
	header.appendChild(logo);
	footer.innerHTML="&copy; 2014 Undefined, Inc. Blah blah blah have rights to blah blah blah of their respective owners blah blah.";
	sidebar.innerHTML="<h2>QuickLinks</h2> \
	<ul> \
	<li><a href='http://Ims.thinkthroughmath.com'>Think Through Math</a></li> \
	<li><a href='http://www.brainpop.com'>Brainpop</a></li> \
	<li><a href='http://hosted1.renlearn.com/230869'>Accellerated Reader</a></li> \
	<li><a href='http://www.renzullilearning.com'>Renzulli</a></li> \
	<li><a href='http://www.worldbook.com'>Worldbook Web</a></li> \
	</ul> \
	<h2>Event Calendar</h2> \
	Thursday, 2/27/14 - Cheerleading Practice<br> \
	Thursday, 3/6/14 - Cheerleading Practice<br> \
	Thursday, 3/13/14 - Cheerleading Practice<br>";
	window.addEventListener("click", switchtab);
}