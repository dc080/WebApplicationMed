var firstPoint
var secondPoint

function onKeyDown()
{
    firstPoint = checkCoordinates()
}


function onKeyUp()
{
    secondPoint = checkCoordinates()
    alert(firstPoint + " -> " + secondPoint)
}


function checkCoordinates()
{
	var posx = 0;
	var posy = 0;
	var mouseEvent = window.event;
	if (mouseEvent.pageX || mouseEvent.pageY)
	{
		posx = mouseEvent.pageX;
		posy = mouseEvent.pageY;
	}
	else if (mouseEvent.clientX || mouseEvent.clientY)
	{
		posx = mouseEvent.clientX + document.body.scrollLeft;
		posy = mouseEvent.clientY + document.body.scrollTop;
	}
	var sourceX = findPosX(document.getElementById("image"))
	var sourceY = findPosY(document.getElementById("image"))

	var coord = [posx-sourceX, posy-sourceY];
	return coord;
}

function findPosX(obj)
{
	var curleft = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curleft += obj.offsetLeft
			obj = obj.offsetParent;
		}
	}
	else if (obj.x)
		curleft += obj.x;
	return curleft;
}

function findPosY(obj)
{
	var curtop = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curtop += obj.offsetTop
			obj = obj.offsetParent;
		}
	}
	else if (obj.y)
		curtop += obj.y;
	return curtop;
}