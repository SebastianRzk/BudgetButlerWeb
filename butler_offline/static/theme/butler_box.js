let boxs = document.getElementsByClassName('boxcontent');
for (let i = 0; i < boxs.length; ++i) {
    let box = boxs[i];
	let boxOpen = false;
	if (box.getBoundingClientRect().height > 0){
		boxOpen = true;
	}
	
	let id = box.id
	let parent = box.parentElement
	let closeButton = parent.getElementsByClassName('close_button')[0]
	let openButton = parent.getElementsByClassName('open_button')[0]
	
	
	
	closeButton.onclick = createClose(id, openButton, closeButton);
    openButton.onclick = createOpen(id, openButton, closeButton);	
	
	if(boxOpen){
		openButton.style.display = 'none'
	} else {
		closeButton.style.display = 'none'
	}		 
}

function createOpen(id, openButton, closeButton){
	return function() { openBox(id, openButton, closeButton) }
}

function createClose(id, openButton, closeButton){
	return function() { closeBox(id, openButton, closeButton) }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function closeBox(id, openButton, closeButton) {
	box = document.getElementById(id);
	
	let current_height = box.getBoundingClientRect().height;
	box.style.height = current_height;

	document.getElementById(id).style.height = 0;
	document.getElementById(id).style.opacity = 0;
	
	openButton.style.display = "block";
	closeButton.style.display = "none";

	document.getElementById(id).style.display = 'none';
}

function openBox(id, openButton, closeButton) {
	document.getElementById(id).style.display = 'block';
	document.getElementById(id).style.height = 'auto';
	document.getElementById(id).style.opacity = 1;
	

	let current_height = document.getElementById(id).getBoundingClientRect().height
	document.getElementById(id).style.height = current_height;
	
	
	openButton.style.display = "none";
	closeButton.style.display = "block";
}