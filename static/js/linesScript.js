var firstPoint
var secondPoint

function onKeyDown()
{
    firstPoint = checkCoordinates()
}

function onKeyUp()
{
    secondPoint = checkCoordinates()
    const request = new XMLHttpRequest()

    console.log(firstPoint, secondPoint)

    request.open('POST', '/lines/getJSON')
    request.setRequestHeader('content-type', 'application/json;charset=UTF-8')
    request.send(JSON.stringify({"firstPoint": firstPoint, "secondPoint":secondPoint}))

    request.addEventListener('load', requestListenerOnLoad)
}

function requestListenerOnLoad() {
    var resp = JSON.parse(this.responseText);
    document.getElementById("LineInfo").innerHTML = resp['line_length'];
    document.getElementById("LinesInfo").innerHTML = resp['lines_length'];
    console.log('this.resp: ', resp);
    console.log('this.status: ', this.status);
    const imgRequest = new XMLHttpRequest();
    imgRequest.open('GET', '/lines/getimg');
    imgRequest.responseType = 'blob';
    imgRequest.send();
    imgRequest.addEventListener('load', imgRequestListenerOnLoad)
}

function imgRequestListenerOnLoad() {
    document.getElementById("image").src = URL.createObjectURL(this.response)
}

function popThatButton() {
    document.getElementById("deleteLastResult").disabled = true
    document.getElementById("deleteAll").disabled = true
    const popRequest = new XMLHttpRequest()
    popRequest.open('POST', '/lines/popJSON')
    popRequest.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8')
    popRequest.send()
    popRequest.addEventListener('readystatechange', requestListenerOnReadyState)
}

function requestListenerOnReadyState() {
    if (this.readyState==4) {

        var resp = JSON.parse(this.responseText);
        document.getElementById("LineInfo").innerHTML = resp['line_length'];
        document.getElementById("LinesInfo").innerHTML = resp['lines_length'];
        console.log('this.resp: ', resp);
        console.log('this.status: ', this.status);
        const imgRequest = new XMLHttpRequest();
        imgRequest.open('GET', '/lines/getimg');
        imgRequest.responseType = 'blob';
        imgRequest.send();
        imgRequest.addEventListener('load', imgRequestListenerOnLoad)
        document.getElementById("deleteLastResult").disabled = false
        document.getElementById("deleteAll").disabled = false
    }
}

function deleteAllButton() {
    if (confirm('Вы действительно хотите очистить линии?')) {
		const deleteRequest = new XMLHttpRequest();
		deleteRequest.open('POST', '/lines/deleteAll');
		deleteRequest.responseType = 'blob';
        deleteRequest.send()
        deleteRequest.addEventListener('load', imgRequestListenerOnLoad)
        document.getElementById("LineInfo").innerHTML = '';
        document.getElementById("LinesInfo").innerHTML = '';
	}
}

function checkCoordinates()
{
    var body = document.body;
    var docEl = document.documentElement;
    var img = document.getElementById('image');
    var box = img.getBoundingClientRect();

    var scrollTop = window.pageYOffset || docEl.scrollTop || body.scrollTop;
    var scrollLeft = window.pageXOffset || docEl.scrollLeft || body.scrollLeft;

    var clientTop = docEl.clientTop || body.clientTop || 0;
    var clientLeft = docEl.clientLeft || body.clientLeft || 0;

	var offsetX = box.left + scrollLeft - clientLeft;
	var offsetY = box.top + scrollTop - clientTop;

	var posx = 0;
	var posy = 0;
	var mouseEvent = window.event;
	if (mouseEvent.pageX || mouseEvent.pageY)
	{
		posx = mouseEvent.pageX - offsetX;
		posy = mouseEvent.pageY - offsetY;
	}
	var coord = [posx/img.width, posy/img.height];
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