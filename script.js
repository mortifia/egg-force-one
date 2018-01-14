/*
    This file is part of egg-force-one.

    egg-force-one is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with egg-force-one.  If not, see <http://www.gnu.org/licenses/>. 2

    ############################################################################

    Created on Mon Sep 25 16:24:39 2017
    @author: CASAL Guillaume
*/

var lenTerm 			= 1000 				// nombre de ligne garder sur le terminal
var temp 				= "no temp data" 	// garde les derniere temperature recu
var print 				= "0"				// statut de l'impression
var oldPosLayer 		= 0 				// ancienne position du layer
var PosLayer 			= 0 				// position actiel du layer
var statutPrintData 	= 0					// donne le statu de l'impression
var timeUpdate 			= 1000 				// temps avant la mise a jour
var pathFolder 			= ""				//emplacement dans le dossier
var elementRightClic 	= false 			//element ayant recu un clic droit
var allParam 			= {} 				// tout les paramettre de l'application
var usbModify 			= 0					// element qui a recu le clic droit
var dragTimer 								//timeout on drag 
var listDirOld 			= []				//liste les dossier
////////////////////////////////////////////////////////////////////////////////
//// 								DEV 									////
function test_post() {
	$.ajax({
		type: 'POST',
		url: document.getElementById("test_post_url").value,
		data: document.getElementById("test_post_data").value,
		success: function (data) {
			alert("test_post : " + data);
		},
		error: function (data) {
			alert("test_post : return error");
		}
	});
}
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
////					fonction a chargé en priorité						////

//
function getAllParam() {
	$.ajax({
		type : 'POST',
		url : '/paramGetAll',
		data : '',
		success : function(data) {
			setTimeout(update,timeUpdate);
			//
			allParam = {};
			tableParam = data.split("&");
			for (var i = 0; i < tableParam.length; i++) {
				var pos = tableParam[i].indexOf(":");
				if (tableParam[i][pos+1] == "["){
					//console.log("tableau : " + tableParam[i].slice(0,pos));
					var tmp = [];
					var data = tableParam[i].slice(pos+2).split(",");
					//console.log(tableParam[i].slice(0,pos)+" : "+data);
					for (var j = 0; j < data.length; j++) {
						tmp.push(data[j]);
					}
					//alert(data[data.length -1].substring(0, data[data.length-1].length-2));
					var tmp2 = data[data.length -1].substring(0, data[data.length-1].length-1);
					tmp.pop();
					tmp.push(tmp2);
					allParam[tableParam[i].slice(0,pos)] = tmp;

				}
				else{
					allParam[tableParam[i].slice(0,pos)] = tableParam[i].slice(pos+1);					
				}
			}
			if (allParam.logDev == "True") {
				console.log(allParam);
			}
			updateAllInfo();
		},
		error : function() {
			setTimeout(update,timeUpdate);
			console.error("update param bug");
		}
	});
}
function update() {
	getAllParam();
	listDirUpdate(pathFolder);
}

function updateAllInfo(){
	updateUsb();
	updatePrint();
}

function updateUsb(){
	if (allParam.usbRun == "True"){
		$('#inprimanteRunUsb').text("utiliser");
	}
	else {
		$('#inprimanteRunUsb').text("non utiliser");
	}
	if (allParam.usbConnect == "True"){
		$('#inprimanteConnecterUsb').text("Connecté");
	}
	else {
		$('#inprimanteConnecterUsb').text("Non connecté");
	}
	if (usbModify == 0){
		$('#inprimantePortUsb').text(allParam.usbPort);
		$('#inprimanteBauderateUsb').text(allParam.usbBauderate);
	}
}

function updatePrint(){
	//statut impression
	switch (allParam.printStatut) {
		case "5":
			// initialisation de l'impression
			$('#statutImpression').text("analyse en cour");
			break;
		case "0":
			// aucune impression
			
			$('#statutImpression').text("Aucune impression");
			break;
		case "1":
			// impression en cour
			$('#statutImpression').text("Impression en cour");
			break;
		case "2":
			// impression terminer
			$('#statutImpression').text("Impression terminer");
			break;
		case "3":
			// impression en pause
			$('#statutImpression').text("Impression en pause");
			break;
		case "4":
			// impression areter
			$('#statutImpression').text("Impression arrêtée");
			break;
			default:
			$('#statutImpression').text("Bug");
	}
	//max total
	document.getElementById("progressPrint").max = allParam.printNbLine;
	//pos total
	document.getElementById("progressPrint").value = allParam.printPosLine;
	//max layer
	var tmp = allParam.printPosLayer[allParam.printLayer] - allParam.printOldLayer;
	document.getElementById("progressLayer").max = tmp;
	//pos layer
	document.getElementById("progressLayer").value = allParam.printPosLine - allParam.printOldLayer;
	//print src
	$('#emplacementFichier').text(allParam.printSrc);
	//print nb lines
	$('#nbLinesPrint').text(allParam.printNbLine);
	//print line
	$('#LinesPrint').text(allParam.printPosLine);
	//print nb layer
	$('#nbLayerPrint').text(allParam.printNbLayer);
	//print layer
	$('#layerPrint').text(allParam.printLayer);

}
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
////					fonction a lancer au démarrage						////
update();
window.onload=function(){
	addAtribute();
}
////////////////////////////////////////////////////////////////////////////////
function modifyUsb(send = 0) {
	if (usbModify == 0){
		usbModify = 1
	}
	else{
		usbModify = 0
	}
	var modifyUsb = document.getElementById("modifyUsb");
	var modifyCancelUsb = document.getElementById("modifyCancelUsb");
	var modifySendUsb = document.getElementById("modifySendUsb");

	if (modifyUsb.className == "none") {
		if(send == 1) {
			alert("send");
			modifyUsb.className = "";
			modifyCancelUsb.className = "none";
			modifySendUsb.className = "none";
		}
		else {
			modifyUsb.className = "";
			modifyCancelUsb.className = "none";
			modifySendUsb.className = "none";
		}
	}
	else {
		modifyUsb.className = "none";
		modifyCancelUsb.className = "";
		modifySendUsb.className = "";

	}
}

//
function openClose(test) {
	if (test.parentNode.parentNode.childNodes[3].className == "none") {
		test.parentNode.parentNode.childNodes[3].className = "infoBody";
	}
	else {
		test.parentNode.parentNode.childNodes[3].className = "none";
	}
}
function openCloseMenu(test) {
	if (test.parentNode.childNodes[1].className == "none") {
		test.parentNode.childNodes[1].className = "menuHome";
	}
	else {
		test.parentNode.childNodes[1].className = "none";
	}
}
//
function openCloseMenu2(test) {
	if (test.parentNode.childNodes[1].className == "none") {
		test.parentNode.childNodes[1].className = "menu2Home";
	}
	else {
		test.parentNode.childNodes[1].className = "none";
	}
}
//
function printStatut(data) {
	console.log("modify printStatut : " + data);
	$.ajax({
		type: 'POST',
		url: '/paramChange',
		data: 'printStatut=' + data,
		success: function(data) {
			console.log("printStatut update");
		},
		error: function() {
			console.error("error statutPrint");
		}
	});
}
function printFolder() {
	path = document.getElementById("dirPath").lastChild.lastChild.lastChild.innerHTML + this.lastChild.innerHTML; 
	//alert(path);
	$.ajax({
		type: 'POST',
		url: '/printSrc',
		data : 'path=' + path,
		success: function(data) {
			console.log("start Print : " + path);
			// body...
		},
		error: function() {
			alert('error');
		}
	});
}
function listDirPos(pos="/") {
	if (pathFolder != pos) {
		pathFolder = pos;
		document.getElementById('dirPath').innerHTML = "";
		var newLine = document.createElement('tr');
		newLine.className = "trPath";
		var firstElement = document.createElement('td');
		firstElement.innerHTML = "Position";
		firstElement.className = "td1";
		var secondElement = document.createElement('td');
		secondElement.className = "td2";
		var divSecondElement = document.createElement('div');
		divSecondElement.innerHTML = pos;
		divSecondElement.className = "tdDivDirPath";
		secondElement.appendChild(divSecondElement);
		newLine.appendChild(firstElement);
		newLine.appendChild(secondElement);
		document.getElementById('dirPath').appendChild(newLine);
	}
}
function posDirUpdate() {
	//alert(this.innerHTML);
	tmp = document.getElementById('dirPath').lastChild.lastChild.lastChild.innerHTML + this.lastChild.innerHTML + '/';
	listDirUpdate(tmp);
}

function posDirUpdate2(){
	tmp = document.getElementById('dirPath').lastChild.lastChild.lastChild.innerHTML + elementRightClic.lastChild.innerHTML + '/';
	listDirUpdate(tmp);
}

function dirReturn() {
	listDirUpdate(returnPath);
}

function getRightClic() {
	document.getElementById('rightClicNone').className = "none";
	document.getElementById('rightClicDir').className = "none";
	document.getElementById('rightClicFolder').className = "none";
}

function rightClickext(tmp = "", event) {
	getRightClic();
	console.log("right click ext");
	event.stopPropagation();
	event.preventDefault();
    var menu = document.getElementById('rightClicNone');

    menu.className 	= "rightClic";
    menu.style.left = event.pageX + "px";
    menu.style.top 	= event.pageY + "px";

	/*alert("ext right click");
	console.log(event.pageX);
    console.log(event.pageY);*/

}
function rightClickDir(event) {
	elementRightClic = this;
	getRightClic();
	console.log("right click Dir : " + this.lastChild.innerHTML);
	event.stopPropagation();
	event.preventDefault();

    var menu = document.getElementById('rightClicDir');

    menu.className 	= "rightClic";
    menu.style.left = event.pageX + "px";
    menu.style.top 	= event.pageY + "px";

	/*if (tmp != "") {
		alert("dossier : " + tmp.lastChild.innerHTML);
	}*/
}
function rightClickFolder(event) {
	elementRightClic = this;
	getRightClic();
	console.log("right click Folder : " + this.lastChild.innerHTML);
	event.stopPropagation();
	event.preventDefault();

    var menu = document.getElementById('rightClicFolder');

    menu.className 	= "rightClic";
    menu.style.left = event.pageX + "px";
    menu.style.top 	= event.pageY + "px";

	/*if (tmp != "") {
		alert("fichier : " +tmp.lastChild.innerHTML);
	}*/
}
function listDirUpdate(addPath="/") {
	if (addPath == ""){
		addPath = "/";
	}
	$.ajax({
		type: 'POST',
		url: '/dirPrint',
		data : 'path=' + addPath,
		success: function(data) {
			if (addPath != pathFolder){
				//si on change de dossier
				console.log("change dir");
				document.getElementById('listDirStartTable').innerHTML = "";
				listDirPos(addPath);
				listDirUpdateTestReturn(temp, addPath);
				var temp = data.split(";");
				var newList = [];
				for (var pos = 0; pos < temp.length && temp[pos] != ""; pos++) {
					//ajoute tout les dossier et fichier
					var temp2 = temp[pos].split('|');
					newList.push(temp2);
					listDirUpdateCreateLine(temp2);
				}
				listDirOld = newList;
			}
			else{
				//on est toujour dans le meme dossier
				var temp = data.split(";");
				var newList = [];
				for (var pos = 0; pos < temp.length && temp[pos] != ""; pos++) {
					//ajoute tout les dossier et fichier
					var temp2 = temp[pos].split('|');
					newList.push(temp2);
				}
				if (newList.length != listDirOld.length){
					// si on a pas le meme nombre d'elements
					console.log("change detected on dir");
					document.getElementById('listDirStartTable').innerHTML = "";
					listDirUpdateTestReturn(temp, addPath);
					for (var pos = 0; pos < newList.length && newList[pos] != ""; pos++) {
						//ajoute tout les dossier et fichier
						listDirUpdateCreateLine(newList[pos]);
					}
					listDirOld = newList;
				}
				else{
					//si on a le mem nombre d'elements
					for (var pos = 0; pos < newList.length && newList[pos] != ""; pos++) {
						//ajoute tout les dossier et fichier
						if (newList[pos][0] != listDirOld[pos][0] || newList[pos][1] != listDirOld[pos][1]){
							console.log("change detected on dir");
							listDirUpdateLine(newList[pos], pos);
						}
					}
					listDirOld = newList
				}
			}
		},
		error: function() {
			console.log('error update dir');
		}
	});
}
function listDirUpdateLine(temp2, pos){
	ret = 0;
	if(document.getElementById('listDirStartTable').firstChild.firstChild.innerHTML == "Retour"){
		ret = 1;
	}
	var tmp = document.getElementById('listDirStartTable').children[ret + pos];

	if(tmp.firstChild.innerHTML == "Dossier"){
		//Dossier
		tmp.removeEventListener("dblclick", posDirUpdate, false);
		tmp.removeEventListener("contextmenu", rightClickDir, false);
	}
	else{
		//Fichier
		tmp.removeEventListener("dblclick", printFolder, false);
		tmp.removeEventListener("contextmenu", rightClickFolder, false);
	}

	if (temp2[1] == "True") {
		// True
		tmp.firstChild.innerHTML = "Dossier";
		// double clic
		tmp.addEventListener("dblclick", posDirUpdate, false);
		//clic Droit
		tmp.addEventListener('contextmenu',rightClickDir, false);
	}
	else {
		// False
		tmp.firstChild.innerHTML = "Fichier";
		// double clic
		tmp.addEventListener("dblclick", printFolder, false);
		//clic Droit
		tmp.addEventListener('contextmenu',rightClickFolder, false);
	}
	tmp.lastChild.innerHTML = temp2[0];
}

function listDirUpdateTestReturn(temp, addPath) {
	if (addPath != "/"){
		var newLine = document.createElement('tr');
		var firstElement = document.createElement('td');
		firstElement.innerHTML = "Retour";
		firstElement.className = "td1";
		var secondElement = document.createElement('td');
		var temp = addPath.split("/");
		returnPath = "";
		for (var pos = 0; pos < temp.length - 2; pos++) {
			returnPath += temp[pos] + "/";
		}
		//alert("test : " + returnPath);
		secondElement.innerHTML = returnPath;
		secondElement.className = "td2";
		//newLine.onclick = listDirUpdate(returnPath);
		newLine.addEventListener("dblclick", dirReturn, false);
		newLine.appendChild(firstElement);
		newLine.appendChild(secondElement);
		document.getElementById('listDirStartTable').appendChild(newLine);
	}
}

function listDirUpdateCreateLine(temp2){
	var newLine = document.createElement('tr');
	var firstElement = document.createElement('td');
	if (temp2[1] == "True") {
		// True
		firstElement.innerHTML = "Dossier";
		// double clic
		newLine.addEventListener("dblclick", posDirUpdate, false);
		//clic Droit
		newLine.addEventListener('contextmenu',rightClickDir, false);
	}
	else {
		// False
		firstElement.innerHTML = "Fichier";
		// double clic
		newLine.addEventListener("dblclick", printFolder, false);
		//clic Droit
		newLine.addEventListener('contextmenu',rightClickFolder, false);
	}
	firstElement.className = "td1";
	var secondElement = document.createElement('td');
	secondElement.innerHTML = temp2[0];
	secondElement.className = "td2";
	newLine.tabIndex = "1";
	newLine.appendChild(firstElement);
	newLine.appendChild(secondElement);
	document.getElementById('listDirStartTable').appendChild(newLine);
}

function updateSoftware() {
	//met a jour le logiciel
	console.log("update run");
	$.ajax({
		type: 'POST',
		url: '/update',
		data: '',
		success: function(data) {
			console.log("updateSoftware : " + data);
		},
		error: function() {
			console.error('error updateSoftware');
		}
	});
}

function sendAlive(code) {
	//modifie le alive du programme
	console.log("modify alive : " + code);
	$.ajax({
		type: 'POST',
		url: '/paramChange',
		data: 'alive=' + code,
		success: function(data) {
			console.log("alive update");
			setTimeout(function() {
				document.location.reload(true);
			}, 2000);
		},
		error: function() {
			console.error("error sendAlive");
		}
	});
}
function createDir(){
	console.log("create dir");
	$.ajax({
		type	: 'POST',
		url 	: '/createDir',
		data 	: 'path=' + pathFolder 
				+ '&name=' + "nouveau dossier",
		success: function(data){
			console.log("createDir ok");
		},
		error: function() {
			console.error("error createDir");
		}
	});
}

function deleteThisDir() {
	pathDel = pathFolder + elementRightClic.lastChild.innerHTML;
	console.log("delete Dir : " + pathDel);
	$.ajax({
		type	: 'POST',
		url 	: '/deletePathDir',
		data 	: 'path=' + pathDel,
		success: function(data){
			console.log("createDir ok");
		},
		error: function() {
			console.error("error createDir");
		}
	});
}

function deleteThisFolder() {
	pathDel = pathFolder + elementRightClic.lastChild.innerHTML;
	console.log("delete folder : " + pathDel);
	$.ajax({
		type	: 'POST',
		url 	: '/deletePathFolder',
		data 	: 'path=' + pathDel,
		success: function(data){
			console.log("createDir ok");
		},
		error: function() {
			console.error("error createDir");
		}
	});
}

function renameThis() {
	console.log("rename : " + elementRightClic.lastChild.innerHTML + " by: " + "........");
	$.ajax({
		type	: 'POST',
		url 	: '/deletePathFolder',
		data 	: 'path=' + pathFolder
				+ '&pathRename=' + pathRename,
		success: function(data){
			console.log("createDir ok");
		},
		error: function() {
			console.error("error createDir");
		}
	});
}

function addAtribute(){
	document.getElementById('listDir').addEventListener('contextmenu',function(event){
		rightClickext(this, event);
	}, false);
	
	//
	document.getElementById('info').onscroll = function(event){
		document.getElementById('rightClicNone').className = "none";
		document.getElementById('rightClicDir').className = "none";
		document.getElementById('rightClicFolder').className = "none";
	}

	document.getElementById('listDirStart').onscroll = function(event){
		document.getElementById('rightClicNone').className = "none";
		document.getElementById('rightClicDir').className = "none";
		document.getElementById('rightClicFolder').className = "none";
	}

	document.addEventListener("click", function (event) {
		document.getElementById('rightClicNone').className = "none";
		document.getElementById('rightClicDir').className = "none";
		document.getElementById('rightClicFolder').className = "none";
	}, false);

	document.addEventListener("dragover", function(event) {
		document.getElementById('listDirStartTable').className = "none";
		document.getElementById('dragFileUpload').className = "dragFileUpload";
		window.clearTimeout(dragTimer);
	}, false);
	document.addEventListener("dragleave", function(event) {
		dragTimer = window.setTimeout(function() {
			document.getElementById('listDirStartTable').className = "";
			document.getElementById('dragFileUpload').className = "none";
		}, 120);
	}, false);
}