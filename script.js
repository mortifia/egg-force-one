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
var pathFolder 			= "/"				//emplacement dans le dossier
var elementRightClic 	= false 			//element ayant recu un clic droit
var allParam 			= {} 				// tout les paramettre de l'application
var usbModify 			= 0
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

			console.log(allParam);
			//console.log(test);
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
	if (document.getElementById("progressLayer").max != tmp){
		console.log(tmp);
		document.getElementById("progressLayer").max = tmp;
	}
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
function posDirUpdate() {
	//alert(this.innerHTML);
	tmp = document.getElementById('dirPath').lastChild.lastChild.lastChild.innerHTML + this.lastChild.innerHTML + '/';
	listDirUpdate(tmp);
	//document.getElementById('dirPath').lastChild.lastChild.lastChild.innerHTML += this.lastChild.innerHTML + '/';
}
function dirReturn() {
	listDirUpdate(returnPath);
}
function rightClickext(tmp = "") {
	alert("ext right click");
}
function rightClickDir(tmp = "") {
	event.stopPropagation();
	if (tmp != "") {
		alert("dossier : " + tmp.lastChild.innerHTML);
	}
}
function rightClickFolder(tmp = "") {
	event.stopPropagation();
	if (tmp != "") {
		alert("fichier : " +tmp.lastChild.innerHTML);
	}
}
function listDirUpdate(addPath="/") {
	pathFolder = addPath;
	$.ajax({
		type: 'POST',
		url: '/dirPrint',
		data : 'path=' + addPath,
		success: function(data) {
			document.getElementById('listDirStart').innerHTML = "";
			listDirPos(addPath);
			if (addPath != "/") {
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
				document.getElementById('listDirStart').appendChild(newLine);
			}
			var temp = data.split(";");
			for (var pos = 0; pos < temp.length && temp[pos] != ""; pos++) {
				//listDirStart
				//alert(temp[pos] + '|||' + pos);
				var temp2 = temp[pos].split('|');
				var newLine = document.createElement('tr');
				var firstElement = document.createElement('td');
				if (temp2[1] == "True") {
					// True
					firstElement.innerHTML = "Dossier";
					// double clic
					newLine.addEventListener("dblclick", posDirUpdate, false);
					//clic Droit
					newLine.addEventListener('contextmenu',function(e) {
						alert(e);
						rightClickDir(this);
					}, false);
				}
				else {
					// False
					firstElement.innerHTML = "Fichier";
					// double clic
					newLine.addEventListener("dblclick", printFolder, false);
					//clic Droit
					newLine.addEventListener('contextmenu',function(e) {
						rightClickFolder(this);
					}, false);
				}
				firstElement.className = "td1";
				var secondElement = document.createElement('td');
				secondElement.innerHTML = temp2[0];
				secondElement.className = "td2";
				newLine.tabIndex = "1";
				newLine.appendChild(firstElement);
				newLine.appendChild(secondElement);
				document.getElementById('listDirStart').appendChild(newLine);
			}
		},
		error: function() {
			console.log('error update dir');
		}
	});
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
			}, 1000);
		},
		error: function() {
			console.error("error sendAlive");
		}
	});
}

function addAtribute(){
	test = document.getElementById('listDir').addEventListener('contextmenu',function(){
		rightClickext();
	}, false);
}

/*
//socket io
var socket = io.connect('http://' + document.domain + ':' + location.port);
// envoi un message pour prevenir qu'on est connecté
socket.on('connect', function (data) {
	socket.emit('new user', "");
});
*/
// reception des message pour le terminal
/*socket.on('MsgTerm', function (data) {
	if (document.getElementById('outputTerm').childNodes.length >= (lenTerm * 2)) {
		document.getElementById('outputTerm').firstElementChild.remove();
		document.getElementById('outputTerm').firstElementChild.remove();
	}
	$('#outputTerm').append('<span>' + data + '</span><br>');
});*/

/*
//reception de la temperature
socket.on('temp', function (data) {
	temp = data
});
*/

/*
// previent si on est connecté a l'imprimante ou non
socket.on('inprimanteConnecterUsb', function (data) {
	if (data == "True") {
		$('#inprimanteConnecterUsb').text("Connecté");
	}
	else {
		$('#inprimanteConnecterUsb').text("Non connecté");
	}
})
//
socket.on('layerPrint', function(data) {
	if (data != 0) {
		$('#layerPrint').text(data);
	}
	else {
		$('#layerPrint').text("");
	}
});
//
socket.on('nbLinesPrint', function(data) {
	if (data != 0) {
		$('#nbLinesPrint').text(data);
	}
	else {
		$('#nbLinesPrint').text("");
	}
});
//
socket.on('nbLayerPrint', function(data) {
	if (data != 0) {
		$('#nbLayerPrint').text(data);
	}
	else {
		$('#nbLayerPrint').text("");
	}
});
// dit quel fichier il faut imprimé
$("#printSrc").keypress(function(e) {
	if (e.which == 13) {
		//alert($('#printSrc').val());
		var src = $('#printSrc').val();
		$('#printSrc').val("");
		socket.emit('printSrc', src);
	}
});
*/

/*
//met a jour l'interface avec la progression
socket.on('posPrint', function (data) {
	
	document.getElementById("progressLayer").value = data - oldPosLayer;
	document.getElementById("progressPrint").value = data;
});
socket.on('progressLayer', function (data) {
	allNb = data.split(" ");
	document.getElementById("progressLayer").value = allNb[2] - allNb[1];
	document.getElementById("progressLayer").max = allNb[0] - allNb[1];
	oldPosLayer = allNb[1];
});
socket.on('posEndPrint', function (data) {
	document.getElementById("progressPrint").max = data;
});
socket.on('srcImpression', function (data) {
	$('#emplacementFichier').text(data);
});
*/


/*
//
socket.on('statutImpression', function (data) {
	switch (data) {
		case 5:
			// initialisation de l'impression
			statutPrintData = data;
			$('#statutImpression').text("analyse en cour");
			break;
			case 0:
			// aucune impression
			statutPrintData = data;
			$('#statutImpression').text("Aucune impression");
			break;
			case 1:
			// impression en cour
			statutPrintData = data;
			$('#statutImpression').text("Impression en cour");
			break;
			case 2:
			// impression terminer
			statutPrintData = data;
			$('#statutImpression').text("Impression terminer");
			break;
			case 3:
			// impression en pause
			statutPrintData = data;
			$('#statutImpression').text("Impression en pause");
			break;
			case 4:
			// impression areter
			statutPrintData = data;
			$('#statutImpression').text("Impression arrêtée");
			break;
			default:
			$('#statutImpression').text("Bug");
		}
	});
*/

// analyse de la commande du terminal
/*
$('#inputTerm').keypress(function(e) {
	if (e.which == 13) {
		var commande = $('#inputTerm').val();
		$('#inputTerm').val("");
		var argCom = commande.split(" ");
		//alert(argCom)
		switch (argCom[0]) {
			//affiche les commande disponible
			case "help":
			$('#outputTerm').append("<span>" + "help :" + "<br>" + 
				"<dd>" + "temp : donne la temperature" + "<br>" + 
				"<dd>" + "msglvl : choisi le niveau de message afficher" + "</span><br>");
			break;
			//arret d'urgence distant du programme ATTENTION si une generation ou impression
			// est en cour ca sera coupé net 
			case "STOP":
			socket.emit('STOP', "");
			$('#outputTerm').append('<span>' + "stop execute" + '</span><br>');
			break;
			// affiche les derniere temperature recu 
			case "temp":
			$('#outputTerm').append('<span>' + temp + '</span><br>');
			break;
			// deprecié
			case "msglvl":
			if (argCom.length == 2) {
				socket.emit('msglvl', argCom[1]);
				$('#outputTerm').append("<span>" + "msglvl " + argCom[1] + " complete" + "</span><br>");
			}
			else {
				$('#outputTerm').append("<span>" + "usage> msglvl 'int:0,1,2' " + "</span><br>");
			}
			break;
			//permet d'envoyer une commande gcode
			case "gcode":
			if (argCom.length >= 2) {
				gcode = commande.substring(commande.indexOf(" "), commande.length);
					//alert(argCom[argCom.length - 1]);
					if (argCom[argCom.length - 1] != "\n") {
						gcode += "\n"
					}
					socket.emit('gcode', gcode);
				}
				break;
			// si aucune commande trouvé 
			default:
			$('#outputTerm').append('<span> commande inconnue </span><br>');
		}
	}
});
*/