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
var allParam 			= {} 				// tout les paramettre de l'application
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
			allParam = {};
			tableParam = data.split("&");
			var test = "";
			for (var i = 0; i < tableParam.length; i++) {
				var pos = tableParam[i].indexOf(":");
				allParam[tableParam[i].slice(0,pos)] = tableParam[i].slice(pos+1);
				test += tableParam[i].slice(0,pos) + " : " + tableParam[i].slice(pos+1) + "\n";
			}
			//console.log(test);
			listDirUpdate(pathFolder);
			setTimeout(update,timeUpdate);
		},
		error : function() {
			setTimeout(update,timeUpdate);
			console.error("update param bug");
		}
	});
}
function update() {
	getAllParam();
}
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
////					fonction a lancer au démarrage						////
update();
////////////////////////////////////////////////////////////////////////////////
function modifyUsb(send = 0) {
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
function openCloseMenu2(test) {
	if (test.parentNode.childNodes[1].className == "none") {
		test.parentNode.childNodes[1].className = "menu2Home";
	}
	else {
		test.parentNode.childNodes[1].className = "none";
	}
}
//
function statutPrint(data) {
	socket.emit('statutPrint', data);
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
function rightClickDir(tmp = "") {
	if (tmp != "") {
		alert("dossier : " + tmp.lastChild.innerHTML);
	}
}
function rightClickFolder(tmp = "") {
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
			console.log('error updateSoftware');
		}
	});
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