function alertFoo() {
  alert("Foobaz!")
}

var months = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'];
var citeGlobalDateFormat = "<date> <monthname> <year>";
function getTime() {
  var datestr = '';
  datestr = citeGlobalDateFormat;
  var DT = new Date();
  var zmonth = '';
  var month = DT.getMonth()+1;
  if (month < 10) {
    zmonth = "0"+month.toString();
  } else {
    zmonth = month.toString();
  }
  month = month.toString();
  var zdate = '';
  var date = DT.getDate()
  if (date < 10) {
    zdate = "0"+date.toString();
  } else {
    zdate = date.toString();
  }
  date = date.toString()
  datestr = datestr.replace('<date>', date);
  datestr = datestr.replace('<month>', month);
  datestr = datestr.replace('<zdate>', zdate);
  datestr = datestr.replace('<zmonth>', zmonth);
  datestr = datestr.replace('<monthname>', months[DT.getMonth()]);
  datestr = datestr.replace('<year>', DT.getFullYear().toString());
  return (datestr);
}

function lastNameToRefname() {
  document.getElementById('refname').value = document.getElementById('last').value;
}

function getLastName(authornum) {
  if (/\S/.test(document.getElementById('last'+authornum).value)) {
    return document.getElementById('last'+authornum).value;
  }
  else {
    var author = document.getElementById('author'+authornum).value;
    var match = /(\S+)\s*$/.exec(author);
    if (match) {
      return match[1];
    }
    else {
      return '';
    }
  }
}

function makeRefname() {
  var refname = getLastName(1) + getLastName(2);
  if (/\S/.test(refname)) {
    var date = document.getElementById('date').value;
    var match = /[0-9]{4}/.exec(date);
    if (match) {
      refname += match[0];
    }
  }
  else {
    refname = "";
  }
  document.getElementById('refname').value = refname;
}

function splitName(i) {
  var author = document.getElementById('author' + i);
  var first = document.getElementById('first' + i);
  var last = document.getElementById('last' + i);
  
  var match = /(.+)\s+(.+)/.exec(author.value);
  if (match) {
    first.value = match[1];
    last.value = match[2];
    author.value = '';
  }
  else if (author.value == '' && 
           (first.value != '' || 
            last.value != '')) {
    // Reverse split
    author.value = 
        first.value + ' ' + 
        last.value;
    first.value = '';
    last.value = '';
  }
}

function makeCiteBook() {
  saveCookies();

  var cite = '<ref';
  var refname = document.getElementById('refname').value;
  if (/\S/.test(refname)) {
    cite += ' name="' + refname + '"';
  }
  cite += '>{{';
  
  if (document.getElementById('cite_book').checked) {
    cite += 'cite book';
    if (document.getElementById('harv').checked) {
        cite += '|ref=harv'
    }
  }
  else if (document.getElementById('citation').checked) {
    cite += 'citation';
  }
  else if (document.getElementById('plain').checked){
    cite += 'cite book';
  }
  else {alert('No template selected.');}
  
  var authorcite = '';
  var prevauthor = 0;
  for (var i=3;i>=1;i--) {
    var author = document.getElementById('author' + i).value;
    var last = document.getElementById('last' + i).value;
    var first = document.getElementById('first' + i).value;
    var authorlink = document.getElementById('authorlink' + i).value;
    if (i==1 && !prevauthor) { i = ''; }
    if (/\S/.test(authorlink)) {
      authorcite = '|authorlink' + i + '=' + authorlink + authorcite;
    }
    if (/\S/.test(last)) {
      authorcite = '|last' + i + '=' + last + '|first' + i + '=' + first + authorcite;
      prevauthor = 1;
    }
    else if (/\S/.test(author)) {
      authorcite = '|author' + i + '=' + author + authorcite;
      prevauthor = 1;
    }
  }
  cite += authorcite;

  var simplefields = ["coauthors", "editor", "others", "title", "url", "accessdate","edition","series","volume","date","publisher","location","language","isbn","pages","chapter"];
  for ( var i in simplefields ) {
    var fieldname = simplefields[i];
    var value = document.getElementById(fieldname).value;
    if (/\S/.test(value) || fieldname == "title") {
      if (fieldname == "pages") {
        if (/^\w+$/.test(value)) {
          fieldname = "page";    //Use page= instead of pages= if only one page. Makes p. 5 instead of pp. 5.
        }
        else {
          value = value.replace(/-/g, "–");      //Replace hyphens with en dashes [[WP:ENDASH]]
          value = value.replace(/,\s*/g, ", ");  //One space after each comma
        }
      }
      else if (fieldname == "date" && /^\d\d\d\d$/.test(value)) {
        fieldname = "year";  // Use year= instead of date= if only the year is specified
      }
      cite += '|' + fieldname + '=' + value;
    }
  }
  
  var otherfields = document.getElementById('otherfields').value;
  if (/\S/.test(otherfields)) {
    cite += '|' + otherfields;
  }
  
  if (document.getElementById('extraparams').checked) {
    cite += '|authormask=';
    if (!document.getElementById('citation').checked) {
      cite += '|trans_title=';
    }
    cite += '|format=';
    cite += '|origyear=';
    cite += '|oclc=';
    cite += '|doi=';
    cite += '|bibcode=';
    cite += '|id=';
    if (/\S/.test(document.getElementById('chapter').value)) {
      if (!document.getElementById('citation').checked) {
        cite += '|trans_chapter=';
      } 
      cite += '|chapterurl=';
    }
    cite += '|quote=';
    cite += '|laysummary=';
    cite += '|laydate=';
  }

  cite += "}}</ref>";

  if (document.getElementById('plain').checked) {
    var match = /^(.*?)({{.*}})(.*?)$/.exec(cite);
    if (match) {
      var citebeg = match[1];
      var citemid = match[2];
      var citeend = match[3];
      citemid = citemid.replace(/cite book/, "Vancite book");
      //alert(citebeg + ':::' + citemid + ':::' + citeend);
      document.getElementById('fullcite').value = 'Updating...';
      var url = 'expandtemplates.py?wikitext=' + urlencode(citemid,true);
      var xmlhttpExpand = new XMLHttpRequest();
      xmlhttpExpand.onreadystatechange=function() {
	if(xmlhttpExpand.readyState==4) {	  
	  var xmlDoc=xmlhttpExpand.responseXML.documentElement;
	  var expanded = xmlDoc.getElementsByTagName("expandtemplates")[0].textContent;
	  if (expanded == undefined) {
	    expanded = xmlDoc.getElementsByTagName("expandtemplates")[0].childNodes[0].nodeValue;
	  }
	  expanded = expanded.replace(/<span.*?>/ig, '');
	  expanded = expanded.replace(/<\/span>/ig, '');
	  expanded = expanded.replace(/<nowiki\/?>/ig, '');
	  expanded = expanded.replace(/\&\#32\;/ig, ' ');
	  expanded = expanded.replace(/\&\#59\;/ig, ';');
	  expanded = expanded.replace(/\&\#91\;/ig, '[');
	  expanded = expanded.replace(/\&\#93\;/ig, ']');
	  
	  document.getElementById('fullcite').rows = 5;
	  document.getElementById('fullcite').value = citebeg + expanded + citeend;
          makePreview();
	}
      }
      xmlhttpExpand.open("GET",url,true);
      xmlhttpExpand.send(null);
    }
    else {alert('Error A1');}
  }
  else {
    if (document.getElementById('verbose').checked) {
      cite = cite.replace(/\|/g, "\n|");
      document.getElementById('fullcite').rows = 15;
    }
    else {
      document.getElementById('fullcite').rows = 5;
    }
    document.getElementById('fullcite').value = cite;
    makePreview();
  }
}

function urlencode(str) {
  //return escape(str).replace('+', '%2B').replace('%20', '+').replace('*', '%2A').replace('/', '%2F').replace('@', '%40');
  //alert(str.length +':' + encodeURIComponent(str).length);
  return encodeURIComponent(str);
}

var xmlhttp=new XMLHttpRequest();
//var xmlDoc;
function RSchange() {
 if (xmlhttp.readyState==4) {
  document.getElementById('progress').style.visibility = "hidden";
  var xmlDoc=xmlhttp.responseXML.documentElement;
  //alert(xmlDoc.getElementsByTagName("text").length);
  //document.getElementById('preview').value = xmlDoc.getElementsByTagName("text")[0].childNodes[0].nodeValue;
  var previewHTML = xmlDoc.getElementsByTagName("text")[0].textContent;
  if (previewHTML == undefined) {
    previewHTML = xmlDoc.getElementsByTagName("text")[0].childNodes[0].nodeValue;
  }
  //alert(previewHTML);
  previewHTML = previewHTML.replace(/href="\//gi, 'href="http://en.wikipedia.org/');

  document.getElementById('previewSpan').innerHTML = previewHTML;
  //alert(xmlhttp.responseText.length);
  //parser=new DOMParser();
  //var xmlDoc=parser.parseFromString(xmlhttp.responseXML,"text/xml");
  //alert("A" + xmlDoc.getElementsByTagName("updated")[0].childNodes[0].nodeValue + "B");
  //document.getElementById('preview').value = xmlDoc.getElementsByTagName("*")[0].value;
  //document.getElementById('preview').value = xmlhttp.responseText;
 }
}
function makePreview() {
  document.getElementById('progress').style.visibility = "visible";
  var wikitext = document.getElementById('fullcite').value;
  wikitext += '<references />';
  //wikitext = '{{reflist|refs=' + wikitext + '}}';  //List-defined method
  //wikitext = '<ref name="refname1"/><references>' + wikitext + '</references>';  //List-defined method
  xmlhttp.open("GET", "getwprender.py?wikitext=" + urlencode(wikitext),true);
  xmlhttp.onreadystatechange=RSchange;
  xmlhttp.send(null);
}


function formatDate(datein, dateformat) {
  if (dateformat == '') {return (datein);}
  datein = datein.replace(/^\s*(.*?)\s*$/, "$1");  //Trim whitespace
  var year = -1;
  var month = -1;
  var date = -1;
  var match = /^(\d\d\d\d)-(\d\d?)(-(\d\d?))?$/.exec(datein);
  if(match) {
    //alert(' match[1]=' + match[1] + ' match[2]=#' + match[2] + '# match[3]=' + match[3] + ' match[4]=' + match[4]  );
    year = parseInt(match[1], 10);	//10 forces decimal conversion
    month = parseInt(match[2], 10);
    if (match[4]) {
      date = parseInt(match[4], 10);
    }
  }
  else if (/^\d\d? \w+ \d\d\d\d$/.test(datein) || /^\w+ \d\d?, \d\d\d\d$/.test(datein)) {
    var DT = new Date(datein);
    year = DT.getFullYear();
    month = DT.getMonth()+1;
    date = DT.getDate();
  }
  else if (datein == 'today') {
    var DT = new Date();
    year = DT.getFullYear();
    month = DT.getMonth()+1;
    date = DT.getDate();
  }
  else {return (datein);}
  //alert('datein=' + datein + ', y=' + year + ', m=' + month + ', d=' + date);

  var zmonth = '';
  if (month < 10) {
    zmonth = "0"+month.toString();
  } else {
    zmonth = month.toString();
  }
  month = month.toString();
  var zdate = '';
  if (date > -1) {
    if (date < 10) {
      zdate = "0"+date.toString();
    } else {
      zdate = date.toString();
    }
    date = date.toString()
  }
  else { date = ''; }
  
  var datestr = dateformat;
  datestr = datestr.replace('<date>', date);
  datestr = datestr.replace('<month>', month);
  datestr = datestr.replace('<zdate>', zdate);
  datestr = datestr.replace('<zmonth>', zmonth);
  datestr = datestr.replace('<monthname>', months[month-1]);
  datestr = datestr.replace('<year>', year.toString());
  datestr = datestr.replace(/\s+/, ' ').replace(/^\s+/, '').replace(/(\D),/, '$1').replace(/-$/, '');
  return (datestr);
}
function getDateFormat() {
  var dateformat = '';
  if (document.getElementById('dmy').checked) {dateformat = '<date> <monthname> <year>'}
  else if (document.getElementById('mdy').checked) {dateformat = '<monthname> <date>, <year>'}
  else if (document.getElementById('ymd').checked) {dateformat = '<year>-<zmonth>-<zdate>'}
  return (dateformat);
}
function getDateFormatShort() {
  var dateformat = '';
  if (document.getElementById('dmy').checked) {dateformat = 'dmy'}
  else if (document.getElementById('mdy').checked) {dateformat = 'mdy'}
  else if (document.getElementById('ymd').checked) {dateformat = 'ymd'}
  return (dateformat);
}
function reformatDates() {
  var dateformat = getDateFormat();
  //alert(':' + dateformat + ':');
  document.getElementById('accessdate').value = formatDate(document.getElementById('accessdate').value, dateformat);
  document.getElementById('date').value = formatDate(document.getElementById('date').value, dateformat);
  
  saveCookies();
}

function setAccessDateToday() {
  var dateformat = getDateFormat();
  if (dateformat == '') {dateformat = citeGlobalDateFormat;}
  document.getElementById('accessdate').value = formatDate('today', dateformat);
}

//var xmlhttpAuthorLinks = [new XMLHttpRequest(), new XMLHttpRequest(), new XMLHttpRequest()];
function checkAuthorLinks() {
  for (var i=1;i<=3;i++) {
    var authorName = document.getElementById('author' + i).value;
    if (/\S/.test(authorName)) {
      checkOneAuthorLink(authorName, i);
    }
  }
}

function checkOneAuthorLink(authorName, i) {
  document.getElementById('authorLinkButton'+i).style.visibility = "visible";
  var url = 'wparticleexists.py?title=' + urlencode(authorName);
  var xmlhttpAuthorLinks = new XMLHttpRequest();
  xmlhttpAuthorLinks.onreadystatechange=function() {
    if(xmlhttpAuthorLinks.readyState==4) {
      //document.getElementById('location').value += '(' + i + ', ' + xmlhttpAuthorLinks.responseText + ')';
      //document.getElementById('progressAuthor'+i).style.visibility = "hidden";
      if (/^1/.test(xmlhttpAuthorLinks.responseText)) {
        document.getElementById('authorLinkButton'+i).src = "static/makelink.gif";
	document.getElementById('authorLinkAnchor'+i).href='javascript:makeAuthorLink('+i+');'
	document.getElementById('authorTryLink'+i).style.visibility = "visible";
      }
      else {
        document.getElementById('authorLinkButton'+i).style.visibility = "hidden";
      }
    }
  }
  xmlhttpAuthorLinks.open("GET",url,true);
  xmlhttpAuthorLinks.send(null);  
}
function makeAuthorLink(i) {
  document.getElementById('authorlink'+i).value = document.getElementById('authorOrig'+i).value;
}

function formClear() {
  document.getElementById('book_url').value='';
  if (document.getElementById('citespan')){ document.getElementById('citespan').innerHTML=''; }
  document.getElementById('book_url').focus();
}

// IE only
function sendToClipboard(s)
{
   if( window.clipboardData && clipboardData.setData )
   {
      clipboardData.setData("Text", s);
   }
   else
   {
     alert("Internet Explorer required");
   }
}

function makeCopyButton() {
  if( window.clipboardData && clipboardData.setData ) {
    document.getElementById('clipboardspan').innerHTML='<input type="button" value="Copy" tabindex=1 onClick=\'clipboardData.setData("Text", document.getElementById("fullcite").value)\'>';
  }
}

function loadRun() {
  if (document.getElementById('accessdate')) {
    readCookies();
    reformatDates();
    makeRefname();
    setAccessDateToday();
    checkAuthorLinks();
    makeCiteBook();
    makeCopyButton()
  }
  else {
    document.getElementById('book_url').focus();
  }
}

function setCookie(c_name,value) {
  var exdays = 30;
  var exdate=new Date();
  exdate.setDate(exdate.getDate() + exdays);
  var c_value=escape(value) + 
    ((exdays==null) ? "" : ("; expires="+exdate.toUTCString()));
  document.cookie=c_name + "=" + c_value;
}

function getCookie(c_name) {
  var i,x,y,ARRcookies=document.cookie.split(";");
  for (i=0;i<ARRcookies.length;i++)
  {
    x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
    y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
    x=x.replace(/^\s+|\s+$/g,"");
    if (x==c_name)
    {
      return unescape(y);
    }
  }
}


function checkboxToCookie(name) {
  var c = document.getElementById(name).checked;
  setCookie(name, c);
  //if (name === 'harv') {alert("Saved: " + name + " " + c);}
}

function cookieToCheckbox(name) {
  var c = getCookie(name) === "true";
  document.getElementById(name).checked = c;
  //if (name === 'harv') {alert("Read: " + name + " " + c + "-" + getCookie(name));}
}

function calleach(func, list) {
  var length = list.length;
  for (var i = 0; i < length; i++) {
    func(list[i]);
  }  
}

function getCiteTemplate() {
  if (document.getElementById('cite_book').checked) {
    return 'cite_book';
  }
  else if (document.getElementById('citation').checked) {
    return 'citation';
  }
  else if (document.getElementById('plain').checked){
    return 'plain';
  }
  return 'cite_book';  
}

var cookienames = ["harv", "extraparams", "verbose"];

function saveCookies() {
  calleach(checkboxToCookie, cookienames);
  setCookie("template", getCiteTemplate());
  setCookie("dateformat", getDateFormatShort());
}

function readCookies() {
  calleach(cookieToCheckbox, cookienames);
  
  var template = getCookie("template");
  if (template === 'citation') {
      document.getElementById('citation').checked = true;
  }
  else if (template === 'plain') {
      document.getElementById('plain').checked = true;
  }
  else {
    document.getElementById('cite_book').checked = true;
  }

  var dateformat = getCookie("dateformat");
  if (dateformat === 'mdy') {
      document.getElementById('mdy').checked = true;
  }
  else if (dateformat === 'ymd') {
      document.getElementById('ymd').checked = true;
  }
  else {
    document.getElementById('dmy').checked = true;
  }
}
