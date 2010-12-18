var numforms = 0;
var wikEdAutoUpdateUrl;
var citeUserDateFormat;
function refbuttons() {
  if (mwCustomEditButtons && document.getElementById('toolbar') ) {
    button = document.createElement('a');
    button.href = "javascript:easyCiteMain()";
    button.title = "Insert Citation";
    buttonimage = document.createElement('img');
    buttonimage.src = "http://upload.wikimedia.org/wikipedia/commons/e/ea/Button_easy_cite.png";
    buttonimage.alt = "Insert Citation";
    button.appendChild(buttonimage);
    var toolbar = document.getElementById('toolbar');
    if (navigator.userAgent.indexOf('MSIE') == -1) {
      if (toolbar.style != null) {
        toolbar.style.height = 'auto';
      }
      else {
      	toolbar.setAttribute('style', 'margin-bottom: 6px; height: auto;');
      }
      toolbar.appendChild(button);
      citemain = document.createElement('div');
      citemain.style.display = 'none';
      citemain.style.margin = '0.2em 0 -0.2em 0';
      citemain.setAttribute('Id', 'citeselect');
      citemain.appendChild( addOption("citeWeb()", "Web") );
      citemain.appendChild( addOption("citeNews()", "News") );
      citemain.appendChild( addOption("citeBook()", "Book") );
      citemain.appendChild( addOption("citeJournal()", "Journal") );
      citemain.appendChild( addOption("citeNamedRef()", "Named references") );
      citemain.appendChild( addOption("dispErrors()", "Error check") );
      citemain.appendChild( addOption("showMore()", "More") );
      citemain.appendChild( addOption("hideInitial()", "Cancel") );
      
      citemore = document.createElement('div');
      citemore.style.display = 'none';
      citemore.setAttribute('Id', 'citemore');
      citemore.appendChild( addOption("citeEncyclopedia()", "Encyclopedia") );
      citemore.appendChild( addOption("citePressRelease()", "Press release") );
      citemore.appendChild( addOption("citeMap()", "Map") );
      citemore.appendChild( addOption("showRefSectionOptions()", "Ref Section") );
      citemain.appendChild(citemore);
      
      toolbar.appendChild(citemain);
    }
    else {
      toolbar.appendChild(button);
      selection = '<div id="citeselect" style="display:none"><input type="button" value="Web" onclick="citeWeb()" />'+
      '<input type="button" value="News" onclick="citeNews()" />'+
      '<input type="button" value="Book" onclick="citeBook()" />'+
      '<input type="button" value="Journal" onclick="citeJournal()" />'+
      '<input type="button" value="Named references" onclick="citeNamedRef()" />'+
      '<input type="button" value="Error check" onclick="dispErrors()" />'+
      '<input type="button" value="More" onclick="showMore()" />'+
      '<input type="button" value="Cancel" onclick="hideInitial()" />'+
      '<div id="citemore" style="display:none">\
      <input type="button" value="Encyclopedia" onclick="citeEncyclopedia()" />\
      <input type="button" value="Press release" onclick="citePressRelease()" />\
      <input type="button" value="Map" onclick="citeMap()" />\
      <input type="button" value="Ref Section" onclick="showRefSectionOptions()" />\
      </div>'+
      '</div>';
      document.getElementById('editform').innerHTML = selection + document.getElementById('editform').innerHTML;
    }
  }
}

function addOption(script, text) {
  option = document.createElement('input');
  option.setAttribute('type', 'button');
  option.setAttribute('onclick', script);
  option.setAttribute("value", text);
  return option;
}

function hideInitial() {
  document.getElementById('citeselect').style.display = 'none';
  oldFormHide();
}

function oldFormHide() {
  if (numforms != 0) {
    document.getElementById('citediv'+numforms).style.display = 'none';
  }
  if (document.getElementById('errorform') != null) {
    document.getElementById('citeselect').removeChild(document.getElementById('errorform'));
  }
}

function easyCiteMain() {
  document.getElementById('citeselect').style.display = '';
  document.getElementById('citemore').style.display = 'none';
}

function showMore() {
	document.getElementById('citemore').style.display = '';
}

var months = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'];
var citeGlobalDateFormat = "<date> <monthname> <year>";
function getTime() {
  var datestr = '';
  if (citeUserDateFormat) {
    datestr = citeUserDateFormat;
  } else {
    datestr = citeGlobalDateFormat;
  }
  var DT = new Date();
  var zmonth = '';
  var month = DT.getUTCMonth()+1;
  if (month < 10) {
    zmonth = "0"+month.toString();
  } else {
    zmonth = month.toString();
  }
  month = month.toString();
  var zdate = '';
  var date = DT.getUTCDate()
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
  datestr = datestr.replace('<monthname>', months[DT.getUTCMonth()]);
  datestr = datestr.replace('<year>', DT.getUTCFullYear().toString());
  return (datestr);
}

function citeWeb() {
  citeNewsWeb("cite web");
}
function citeNews() {
  citeNewsWeb("cite news");
}

function citeNewsWeb(templatename) {
  oldFormHide();
  template = templatename;
  var legend;
  if (template == "cite web") {
    legend = "Cite web source";
  } else {
    legend = "Cite news source";
  }
  newtime = getTime();
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>'+legend+'</legend>'+
    '<table cellspacing="5">'+
    '<input type="hidden" value="'+template+'" id="template">'+
    '<tr><td width="120"><label for="url">&nbsp;URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="url"></td>'+
    '<td width="120"><label for="title">&nbsp;Title: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="title"></td></tr>'+
    '<tr><td width="120"><label for="last">&nbsp;Last name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="last"></td>'+
    '<td width="120"><label for="first">&nbsp;First name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="first"></td></tr>'+
    '<tr><td width="120"><label for="coauthors">&nbsp;Coauthors: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="coauthors"></td>'+
    '<td width="120"><label for="date">&nbsp;Publication date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="date"></td></tr>'+
    '<tr><td width="120"><label for="work">&nbsp;' + ((template == 'cite news') ? 'Newspaper' : 'Work') + ': </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="work"></td>'+
    '<td width="120"><label for="publisher">&nbsp;Publisher: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="publisher"></td></tr>'+
    '<tr><td width="120"><label for="pages">&nbsp;Pages: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="pages"></td>'+
    '<td width="120"><label for="language">&nbsp;Language: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="language"></td></tr>'+
    '<tr><td width="120"><label for="accessdate">&nbsp;Access date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="accessdate" value="'+ newtime +'"></td>'+
    '<td width="120"><label for="location">&nbsp;Location: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="location"></td></tr>';
  if (template == 'cite web') {
	  form += '<tr><td width="120"><label for="archiveurl">&nbsp;Archive URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="archiveurl"></td>'+
    '<td width="120"><label for="archivedate">&nbsp;Archive date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="archivedate"></td></tr>';
  }
  form += '<tr><td width="120"><label for="refname">&nbsp;Reference name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="refname"></td></tr>'+
    '</table>'+
    '<input type="button" value="Add citation" onClick="addcites()">'+
    '<span style="float:right"><a href="http://en.wikipedia.org/wiki/Template:'+template.replace(/ /g, '_')+'" target="_blank">[Template documentation]</a></span>'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function citeBook() {
  oldFormHide();
  template = "cite book";
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>Cite book source</legend>'+
    '<table cellspacing="5">'+
    '<input type="hidden" value="'+template+'" id="template">'+
    '<tr><td width="120"><label for="last">&nbsp;Last name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="last"></td>'+
    '<td width="120"><label for="first">&nbsp;First name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="first"></td></tr>'+
    '<tr><td width="120"><label for="coauthors">&nbsp;Coauthors: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="coauthors"></td>'+
    '<td width="120"><label for="others">&nbsp;Others: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="others"></td></tr>'+
    '<tr><td width="120"><label for="title">&nbsp;Title: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="title"></td>'+
    '<td width="120"><label for="editor">&nbsp;Editor: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="editor"></td></tr>'+
    '<tr><td width="120"><label for="publisher">&nbsp;Publisher: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="publisher"></td>'+
    '<td width="120"><label for="location">&nbsp;Location: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="location"></td></tr>'+
    '<tr><td width="120"><label for="date">&nbsp;Publication date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="date"></td>'+
    '<td width="120"><label for="edition">&nbsp;Edition: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="edition"></td></tr>'+
    '<tr><td width="120"><label for="series">&nbsp;Series: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="series"></td>'+
    '<td width="120"><label for="volume">&nbsp;Volume: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="volume"></td></tr>'+
    '<tr><td width="120"><label for="pages">&nbsp;Pages: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="pages"></td>'+
    '<td width="120"><label for="chapter">&nbsp;Chapter: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="chapter"></td></tr>'+
    '<tr><td width="120"><label for="isbn">&nbsp;ISBN: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="isbn"></td>'+
    '<td width="120"><label for="oclc">&nbsp;OCLC: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="oclc"></td></tr>'+
    '<tr><td width="120"><label for="url">&nbsp;URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="url"></td>'+
    '<td width="120"><label for="accessdate">&nbsp;Access date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="accessdate"></td></tr>'+
    '<tr><td width="120"><label for="language">&nbsp;Language: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="language"></td>'+
    '<td width="120"><label for="refname">&nbsp;Reference name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="refname"></td></tr>'+
    '</table>'+
    '<input type="button" value="Add citation" onClick="addcites()">'+
    '<span style="float:right"><a href="http://en.wikipedia.org/wiki/Template:'+template.replace(/ /g, '_')+'" target="_blank">[Template documentation]</a></span>'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function citeJournal() {
  oldFormHide();
  template = "cite journal";
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>Cite journal article</legend>'+
    '<table cellspacing="5">'+
    '<input type="hidden" value="'+template+'" id="template">'+
    '<tr><td width="120"><label for="last">&nbsp;Last name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="last"></td>'+
    '<td width="120"><label for="first">&nbsp;First name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="first"></td></tr>'+
    '<tr><td width="120"><label for="coauthors">&nbsp;Coauthors: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="coauthors"></td>'+
    '<td width="120"><label for="date">&nbsp;Publication date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="date"></td></tr>'+
    '<tr><td width="120"><label for="title">&nbsp;Title: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="title"></td>'+
    '<td width="120"><label for="journal">&nbsp;Journal: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="journal"></td></tr>'+
    '<tr><td width="120"><label for="publisher">&nbsp;Publisher: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="publisher"></td>'+
    '<td width="120"><label for="location">&nbsp;Location: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="location"></td></tr>'+
    '<tr><td width="120"><label for="volume">&nbsp;Volume: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="volume"></td>'+
    '<td width="120"><label for="issue">&nbsp;Issue: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="issue"></td></tr>'+
    '<tr><td width="120"><label for="pages">&nbsp;Pages: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="pages"></td>'+
    '<td width="120"><label for="issn">&nbsp;ISSN: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="issn"></td></tr>'+
    '<tr><td width="120"><label for="oclc">&nbsp;OCLC: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="oclc"></td>'+
    '<td width="120"><label for="doi">&nbsp;DOI: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="doi"></td></tr>'+
    '<tr><td width="120"><label for="pmid">&nbsp;PMID: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="pmid"></td>'+
    '<td width="120"><label for="quote">&nbsp;Quote: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="quote"></td></tr>'+
    '<tr><td width="120"><label for="url">&nbsp;URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="url"></td>'+
    '<td width="120"><label for="accessdate">&nbsp;Access date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="accessdate"></td></tr>'+
    '<tr><td width="120"><label for="language">&nbsp;Language: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="language"></td>'+
    '<td width="120"><label for="refname">&nbsp;Reference name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="refname"></td></tr>'+
    '</table>'+
    '<input type="button" value="Add citation" onClick="addcites()">'+
    '<span style="float:right"><a href="http://en.wikipedia.org/wiki/Template:'+template.replace(/ /g, '_')+'" target="_blank">[Template documentation]</a></span>'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function citeEncyclopedia() {
  oldFormHide();
  template = "cite encyclopedia";
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>Cite encyclopedia source</legend>'+
    '<table cellspacing="5">'+
    '<input type="hidden" value="'+template+'" id="template">'+
    '<tr><td width="120"><label for="last">&nbsp;Last name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="last"></td>'+
    '<td width="120"><label for="first">&nbsp;First name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="first"></td></tr>'+
    '<tr><td width="120"><label for="coauthors">&nbsp;Coauthors: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="coauthors"></td>'+
    '<td width="120"><label for="editors">&nbsp;Editors: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="editors"></td></tr>'+
    '<tr><td width="120"><label for="title">&nbsp;Entry title: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="title"></td>'+
    '<td width="120"><label for="encyclopedia">&nbsp;Encyclopedia: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="encyclopedia"></td></tr>'+
    '<tr><td width="120"><label for="publisher">&nbsp;Publisher: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="publisher"></td>'+
    '<td width="120"><label for="location">&nbsp;Location: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="location"></td></tr>'+
    '<tr><td width="120"><label for="year">&nbsp;Year: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="year"></td>'+
    '<td width="120"><label for="volume">&nbsp;Volume: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="volume"></td></tr>'+
    '<tr><td width="120"><label for="pages">&nbsp;Pages: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="pages"></td>'+
    '<td width="120"><label for="isbn">&nbsp;ISBN: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="isbn"></td></tr>'+
    '<tr><td width="120"><label for="url">&nbsp;URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="url"></td>'+
    '<td width="120"><label for="accessdate">&nbsp;Access date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="accessdate"></td></tr>'+
    '<tr><td width="120"><label for="language">&nbsp;Language: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="language"></td>'+
    '<td width="120"><label for="refname">&nbsp;Reference name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="refname"></td></tr>'+
    '</table>'+
    '<input type="button" value="Add citation" onClick="addcites()">'+
    '<span style="float:right"><a href="http://en.wikipedia.org/wiki/Template:'+template.replace(/ /g, '_')+'" target="_blank">[Template documentation]</a></span>'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function citePressRelease() {
  oldFormHide();
  template = "cite press release";
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>Cite press release</legend>'+
    '<table cellspacing="5">'+
    '<input type="hidden" value="'+template+'" id="template">'+
    '<tr><td width="120"><label for="title">&nbsp;Title: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="title"></td>'+
    '<td width="120"><label for="publisher">&nbsp;Publisher: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="publisher"></td></tr>'+
    '<tr><td width="120"><label for="date">&nbsp;Date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="date"></td>'+
    '<td width="120"><label for="language">&nbsp;Language: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="language"></td></tr>'+
    '<tr><td width="120"><label for="url">&nbsp;URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="url"></td>'+
    '<td width="120"><label for="accessdate">&nbsp;Access date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="accessdate" value="'+ getTime() +'"></td></tr>'+
    '<tr><td width="120"><label for="refname">&nbsp;Reference name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="refname"></td></tr>'+
    '</table>'+
    '<input type="button" value="Add citation" onClick="addcites()">'+
    '<span style="float:right"><a href="http://en.wikipedia.org/wiki/Template:'+template.replace(/ /g, '_')+'" target="_blank">[Template documentation]</a></span>'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function citeMap() {
  oldFormHide();
  template = "cite map";
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>Cite map</legend>'+
    '<table cellspacing="5">'+
    '<input type="hidden" value="'+template+'" id="template">'+
    '<tr><td width="120"><label for="publisher">&nbsp;Publisher: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="publisher"></td>'+
    '<td width="120"><label for="title">&nbsp;Title: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="title"></td></tr>'+
    '<tr><td width="120"><label for="url">&nbsp;URL: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="url"></td>'+
    '<td width="120"><label for="accessdate">&nbsp;Access date: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="accessdate"></td></tr>'+
    '<tr><td width="120"><label for="edition">&nbsp;Edition: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="edition"></td>'+
    '<td width="120"><label for="date">&nbsp;Date or year: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="date"></td></tr>'+
    '<tr><td width="120"><label for="cartography">&nbsp;Cartography: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="cartography"></td>'+
    '<td width="120"><label for="scale">&nbsp;Scale: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="scale"></td></tr>'+
    '<tr><td width="120"><label for="series">&nbsp;Series: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="series"></td>'+
    '<td width="120"><label for="page">&nbsp;Page: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="page"></td></tr>'+
    '<tr><td width="120"><label for="section">&nbsp;Section: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="section"></td>'+
    '<td width="120"><label for="inset">&nbsp;Inset: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="inset"></td></tr>'+
    '<tr><td width="120"><label for="isbn">&nbsp;ISBN: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="isbn"></td>'+
    '<td width="120"><label for="refname">&nbsp;Reference name: </label></td>'+
      '<td width="400"><input type="text" tabindex=1 style="width:100%" id="refname"></td></tr>'+
    '</table>'+
    '<input type="button" value="Add citation" onClick="addcites()">'+
    '<span style="float:right"><a href="http://en.wikipedia.org/wiki/Template:'+template.replace(/ /g, '_')+'" target="_blank">[Template documentation]</a></span>'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function showRefSectionOptions() {
  oldFormHide();
  template = "cite encyclopedia";
  numforms++;
  form = '<div id="citediv'+numforms+'">'+
    '<fieldset><legend>Add references section</legend>\
	Headline:<br />\
	<input id="references" name="headline" type="radio" tabindex=1 checked="checked"><label for="references">== References ==</label><br /> \
	<input id="notes" name="headline" type="radio" tabindex=1><label for="notes">== Notes ==</label><br /> \
	Type:<br /> \
	<input id="type-references" name="type" type="radio" tabindex=1><label for="type-references">&lt;references/&gt;</label><br /> \
	<input id="type-reflist" name="type" type="radio" tabindex=1 checked="checked"><label for="type-reflist">{{Reflist}}</label><br /> \
	<input id="type-reflist2" name="type" type="radio" tabindex=1><label for="type-reflist2">{{Reflist|2}}</label><br /> \
	<input type="checkbox" tabindex=1 id="ldr"><label for="ldr">List-defined references</label> (<a href="http://en.wikipedia.org/wiki/Wikipedia:Footnotes#List-defined_references" target="_blank">Info 1</a>, <a href="http://en.wikipedia.org/wiki/Help:Footnotes#List-defined_references" target="_blank">Info 2</a>)<br />\
    <input type="button" value="Add references section" onClick="addRefSection()">'+
 '</fieldset></div>';
   document.getElementById('citeselect').innerHTML += form;
}

function addcites(template) {
  cites = document.getElementById('citediv'+numforms).getElementsByTagName('input');
  var template = '';
  var citebegin = '<ref';
  var citename = '';
  var citeinner = '';
  for (var i=0; i<cites.length-1; i++) {
    var citeid = cites[i].id;
    var citevalue = cites[i].value;
    citevalue = citevalue.replace(/^\s*(.*?)\s*$/, "$1");    //Trim leading and trailing whitespace
    if (citevalue != '') {
      if (citeid == "refname") {
        citebegin += ' name="' + citevalue + '"';
      }
      else if (citeid == "template") {
        citename = '>{{' + citevalue;
        template = citevalue;
      }
      else {
        if (citeid == "pages") {
          if (citevalue.match(/^\w+$/) && template != 'cite encyclopedia') {
            citeid = "page";    //Use page= instead of pages= if only one page. Makes p. 5 instead of pp. 5.
          }
          else {
            citevalue = citevalue.replace(/-/g, "–");    //Replace hyphens with en dashes [[WP:ENDASH]]
            citevalue = citevalue.replace(/,\s*/g, ", ");  //One space after each comma
          }
        }
        else if (citeid == "date" && citevalue.match(/^\d\d\d\d$/)) {
          citeid = "year";  // Use year= instead of date= if only the year is specified
        }
        citeinner += "|" + citeid + "=" + citevalue;
      }
    }
  }
  cite = citebegin + citename + citeinner + "}}</ref>";
  insertTags(cite, '', '');
  document.getElementById('citediv'+numforms).style.display = 'none';
}

function addRefSection() {
	var wikicode = "\n";
	if (document.getElementById('references').checked) {
		wikicode += "== References ==\n";
	}
	else if (document.getElementById('notes').checked) {
		wikicode += "== Notes ==\n";
	}
	else {alert('No headline selected!');}
	
	if (document.getElementById('type-references').checked) {
		if (document.getElementById('ldr').checked) {
			wikicode += "<references>\n\n</references>\n";
		}
		else {
			wikicode += "<references/>\n";
		}
	}
	else if (document.getElementById('type-reflist').checked || document.getElementById('type-reflist2').checked) {
		var col2 = document.getElementById('type-reflist2').checked ? '|2' : '' ;
		if (document.getElementById('ldr').checked) {
			wikicode += "{{Reflist" + col2 + "|refs=\n\n}}\n";
		}
		else {
			wikicode += "{{Reflist" + col2 + "}}\n";
		}
	}
	else {alert('No type selected!');}
	
	insertTags(wikicode, '', '');
	document.getElementById('citediv'+numforms).innerHTML = '';
}

function getNamedRefs(calls) {
  if (typeof(wikEdUseWikEd) != 'undefined') {
    if (wikEdUseWikEd == true) {
      WikEdUpdateTextarea();
    }
  }
  text = document.getElementById('wpTextbox1').value;
  var regex;
  if (calls) {
    regex = /< *?ref +?name *?= *?(('([^']*?)')|("([^"]*?)")|([^'"\s]*?[^\/]\b)) *?\/ *?>/gi //'
  } else {
    regex = /< *?ref +?name *?= *?(('([^']*?)')|("([^"]*?)")|([^'"\s]*?[^\/]\b)) *?>/gi //'
  }
  var namedrefs = new Array();
  var i=0;
  var nr=true;
  do {
    ref = regex.exec(text);
    if(ref != null){
      if (ref[5]) {
        namedrefs[i] = ref[5];
      } else if (ref[3]) {
        namedrefs[i] = ref[3];
      } else {
        namedrefs[i] = ref[6];
      }
      i++;
    } else {
      nr=false;
    }
  } while (nr==true);
  return namedrefs;
}

function citeNamedRef() {
  namedrefs = getNamedRefs(false);
  if (namedrefs == '') {
    oldFormHide();
    numforms++;
    out = '<div id="citediv'+numforms+'"><fieldset>'+
      '<legend>References in text</legend>There are no named refs (<tt>&lt;ref name="Name"&gt;</tt>) in the text</fieldset></div>';
    document.getElementById('citeselect').innerHTML += out;
  }
  else {
    oldFormHide();
    numforms++;
    form = '<div id="citediv'+numforms+'">'+
      '<fieldset><legend>References in article</legend>'+
      '<table cellspacing="5">'+
      '<tr><td><label for="namedrefs">&nbsp;Named references in text</label></td>'+
            '<td><select name="namedrefs" id="namedrefs">';
    for (var i=0;i<namedrefs.length;i++) {
      form+= '<option value="'+namedrefs[i]+'">'+namedrefs[i]+'</option>';
    }
    form+= '</select>'+
      '</td></tr></table>'+
      '<input type="button" value="Add citation" onClick="addnamedcite()">'+
      '</fieldset></div>';
     document.getElementById('citeselect').innerHTML += form;
  }
}

function addnamedcite() {
  name = document.getElementById('citediv'+numforms).getElementsByTagName('select')[0].value;
  ref = '<ref name="'+name+'" />';
  insertTags(ref, '', '');
  document.getElementById('citediv'+numforms).style.display = 'none';
}

function getAllRefs() {
  if (typeof(wikEdUseWikEd) != 'undefined') {
    if (wikEdUseWikEd == true) {
      WikEdUpdateTextarea();
    }
  }
  text = document.getElementById('wpTextbox1').value;
  regex = /< *?ref( +?name *?= *?(('([^']*?)')|("([^"]*?)")|([^'"\s]*?[^\/]\b)))? *?>((.|\n)*?)< *?\/? *?ref *?>/gim //"
  var allrefs = new Array();
  var i=0;
  var nr=true;
  do {
    ref = regex.exec(text);
    if(ref != null){
      if (ref[0].search(/[^\s]{150}/) != -1) {
        ref[0] = ref[0].replace(/\|([^\s])/g, "| $1");
      }
      ref[0] = ref[0].replace(/</g, "&lt;");
      ref[0] = ref[0].replace(/>/g, "&gt;");
      allrefs[i] = ref[0];
      i++;
    } else {
      nr=false;
    }
  } while (nr==true);
  return allrefs;
}

function NRcallError(namedrefs, refname) {
  for (var i=0; i<namedrefs.length; i++) {
    if (namedrefs[i] == refname) {
      return true;
    }
  }
  return false;
}

function errorCheck() {
  var allrefs = getAllRefs();
  var allrefscontent = new Array();
  var samecontentexclude = new Array();
  var sx=0;
  var templateexclude = new Array();
  var tx=0;
  var skipcheck = false;
  var namedrefcalls = getNamedRefs(true);
  for (var i=0; i<allrefs.length; i++) {
    allrefscontent[i] = allrefs[i].replace(/&lt; *?ref( +?name *?= *?(('([^']*?)')|("([^"]*?)")|([^'"\s]*?[^\/]\b)))? *?&gt;((.|\n)*?)&lt; *?\/? *?ref *?&gt;/gim, "$8");  //"
  }
  var namedrefs = getNamedRefs(false);
  var errorlist = new Array();
  var q=0;
  unclosed = document.getElementById('unclosed').checked;
  samecontent = document.getElementById('samecontent').checked;
  templates = document.getElementById('templates').checked;
  repeated = document.getElementById('repeated').checked;
  undef = document.getElementById('undef').checked;
  for (var i=0; i<allrefs.length; i++) {
    if (allrefs[i].search(/&lt; *?\/ *?ref *?&gt;/) == -1 && unclosed) {
      errorlist[q] = '<tr><td width="75%"><tt>'+allrefs[i]+'</tt></td>';
      errorlist[q] += '<td width="25%">Unclosed <tt>&lt;ref&gt;</tt> tag</td></tr>';
      q++;
    }
    if (samecontent) {
      for (var d=0; d<samecontentexclude.length; d++) {
        if (allrefscontent[i] == samecontentexclude[d]) {
          skipcheck = true;
        }
      }
      var p=0;
      while (p<allrefs.length && !skipcheck) {
        if (allrefscontent[i] == allrefscontent[p] && i != p) {
          errorlist[q] = '<tr><td width="75%"><tt>'+allrefscontent[i]+'</tt></td>';
          errorlist[q] += '<td width="25%">Multiple refs contain this content, a <a href="http://en.wikipedia.org/wiki/Wikipedia:Footnotes#Naming_a_ref_tag_so_it_can_be_used_more_than_once">named reference</a> should be used instead</td></tr>';
          q++;
          samecontentexclude[sx] = allrefscontent[i]
          sx++;
          break;
        }
        p++;
      }
     skipcheck=false;
    }
    if (templates) {
      if (allrefscontent[i].search(/\{\{cite/i) == -1 && allrefscontent[i].search(/\{\{citation/i) == -1 && allrefscontent[i].search(/\{\{Comic (book|strip) reference/i) == -1 && allrefscontent[i].search(/\{\{Editorial cartoon reference/i) == -1 && allrefscontent[i].search(/\{\{harv/i) == -1) {
        for (var x=0; x<templateexclude.length; x++) {
          if (allrefscontent[i] == templateexclude[x]) {
            skipcheck = true;
          }
        }
        if (!skipcheck) {
          errorlist[q] = '<tr><td width="75%"><tt>'+allrefs[i]+'</tt></td>';
          errorlist[q] += '<td width="25%">Does not use a <a href="http://en.wikipedia.org/wiki/Wikipedia:Citation_templates">citation template</a></td></tr>';
          q++;
          templateexclude[tx] = allrefscontent[i];
          tx++;
        }
        skipcheck = false;
      }
    }
  }
  if (repeated) {
    var repeatnameexclude = new Array();
    var rx=0;
    for (var k=0; k<namedrefs.length; k++) {
      for (var d=0; d<repeatnameexclude.length; d++) {
        if (namedrefs[k] == repeatnameexclude[d]) {
          skipcheck = true;
        }
      }
      var z=0;
      while (z<namedrefs.length && !skipcheck) {
        if (namedrefs[k] == namedrefs[z] && k != z) {
          errorlist[q] = '<tr><td width="75%"><tt>'+namedrefs[k]+'</tt></td>';
          errorlist[q] += '<td width="25%">Multiple references are given the same <a href="http://en.wikipedia.org/wiki/Wikipedia:Footnotes#Naming_a_ref_tag_so_it_can_be_used_more_than_once">name</a></td></tr>';
          q++;
          repeatnameexclude[rx] = namedrefs[z];
          rx++;
          break;
        }
        z++;
      }
     skipcheck = false;
    }
  }
  if (undef) {
    var undefexclude = new Array();
    var ux=0;
    for (var p=0; p<namedrefcalls.length; p++) {
      for (var d=0; d<undefexclude.length; d++) {
        if (allrefscontent[i] == undefexclude[d]) {
          skipcheck = true;
        }
      }
      if (!skipcheck) {
        if (!NRcallError(namedrefs, namedrefcalls[p])) {
          errorlist[q] = '<tr><td width="75%"><tt>'+namedrefcalls[p]+'</tt></td>';
          errorlist[q] += '<td width="25%">A <a href="http://en.wikipedia.org/wiki/Wikipedia:Footnotes#Naming_a_ref_tag_so_it_can_be_used_more_than_once">named reference</a> is used but not defined</td></tr>';
          q++;
          undefexclude[ux] = namedrefs[p];
          ux++;
        }
      }
      skipcheck = false;
    }
 }
  if (q > 0) {
    return errorlist;
  } else {
    return 0;
  }
}

function dispErrors() {
  oldFormHide();
  form = '<div id="errorform"><fieldset>'+
    '<legend>Error checking</legend>'+
    '<b>Check for:</b><br/>'+
    '<input type="checkbox" id="unclosed" /> Unclosed <tt>&lt;ref&gt;</tt> tags<br/>'+
    '<input type="checkbox" id="samecontent" /> References with the same content<br/>'+
    '<input type="checkbox" id="templates" /> References not using a <a href="http://en.wikipedia.org/wiki/Wikipedia:Citation_templates">citation template</a><br/>'+
    '<input type="checkbox" id="repeated" /> Multiple references with the same name<br/>'+
    '<input type="checkbox" id="undef" /> Usage of undefined named references<br/>'+
    '<input type="button" id="errorchecksubmit" value="Check for selected errors" onclick="doErrorCheck()"/>'+
    '</fieldset></div>';
  document.getElementById('citeselect').innerHTML += form;
}

function doErrorCheck() {
  var errors = errorCheck();
  document.getElementById('citeselect').removeChild(document.getElementById('errorform'));
  if (errors == 0) {
    if (numforms != 0) {
      document.getElementById('citediv'+numforms).style.display = 'none';
    }
    numforms++;
    out = '<div id="citediv'+numforms+'"><fieldset>'+
      '<legend>Error checking</legend>No errors found.</fieldset></div>';
    document.getElementById('citeselect').innerHTML += out;
  }
  else {
    if (numforms != 0) {
      document.getElementById('citediv'+numforms).style.display = 'none';
    }
    numforms++;
    form = '<div id="citediv'+numforms+'">'+
      '<fieldset><legend>Error checking</legend>'+
      '<table border="1px">';
    for (var i=0; i<errors.length; i++) {
      form+=errors[i];
    }
    form+= '</table>'+
      '</fieldset></div>';
     document.getElementById('citeselect').innerHTML += form;
  }
}

hookEvent("load", refbuttons);
