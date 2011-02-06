function highlightFile(elem, highl)
{
  elem.style.backgroundColor = highl ? "#fff0d9": "";
  elem.style.border          = highl ? "1px solid #ffd699" : "1px solid #fff";
}

function fold(root, collapse, recursive)
{
  var elem = root.firstElementChild;
  while (elem)
  {
    if ((elem.className == "file") ||
        (elem.className == "directory"))
    {
      elem.style.display = collapse ? "none" : "";
    }
    if ((recursive) &&
        (elem.className == "directory"))
    {
      fold(elem, collapse, recursive);
    }
    elem = elem.nextElementSibling;
  }
}

function foldAll(collapse)
{
  var elem = document.getElementById("dirlisting").firstElementChild;
  while (elem)
  {
    if ((elem.className == "file") ||
        (elem.className == "directory"))
    {
      fold(elem, collapse, true);
    }
    elem = elem.nextElementSibling;
  }
}

function getFolding(root)
{
  var elem = root.firstElementChild;
  while (elem)
  {
    if ((elem.className == "file") ||
        (elem.className == "directory"))
    {
      return elem.style.display == "none"
    }
    elem = elem.nextElementSibling;
  }
  return false;
}

function toggleFolding(elem)
{
  fold(elem, !getFolding(elem), false);
}

function attachEventHandler(root)
{
  var elem = root.firstElementChild;
  while (elem)
  {
    if (elem.className == "file")
    {
      elem.onmouseover = function(){highlightFile(this, true);};
      elem.onmouseout = function(){highlightFile(this, false);};
    }
    if (elem.className == "directory-label")
    {
      var html = elem.innerHTML;
      elem.innerHTML = '<a href="#">' + html + '</a>';
      elem.firstElementChild.onclick = function(){
          toggleFolding(this.parentNode.parentNode);
          return false;
        };
    }
    if (elem.className == "directory")
    {
      attachEventHandler(elem);
    }
    elem = elem.nextElementSibling;
  }
}

function init()
{
  attachEventHandler(document.getElementById("dirlisting"))
  foldAll(true);

  var elem = document.createElement("p");
  elem.innerHTML =
    'Directory Tree Control: ' +
    '<a class="js" onclick="foldAll(false);return false;" href="#">' +
      'Expand All' +
    '</a> | ' +
    '<a class="js" onclick="foldAll(true);return false;" href="#">' +
      'Collapse All' +
    '</a>';
  document.getElementById("document").insertBefore(
    elem,
    document.getElementById("dirlisting"));
}

window.onload = init;
