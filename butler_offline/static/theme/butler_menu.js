let main_menus = document.getElementsByClassName('main_menu_item');
for (let i = 0; i < main_menus.length; ++i) {
    let main_menu = main_menus[i]
    let sub_menu = main_menu.parentElement.getElementsByClassName('sub_menu')[0];
	let menuOpen = false;
	if (sub_menu.getBoundingClientRect().height > 0){
		menuOpen = true;
	}
	
	let id = sub_menu.id
	
	if(menuOpen){
		sub_menu.style.display = 'block'
		main_menu.onclick = createCloseMenu(id, main_menu.id)
	} else {
		sub_menu.style.display = 'none'
		main_menu.onclick = createOpenMenu(id, main_menu.id)
	}		 
}

function createOpenMenu(id, mainMenuId){
	return function() { openMenu(id, mainMenuId) }
}

function createCloseMenu(id, mainMenuId){
	return function() { closeMenu(id, mainMenuId) }
}


function closeMenu(id, mainMenuId) {
	sub_menu = document.getElementById(id);

	let current_height = sub_menu.getBoundingClientRect().height;
	sub_menu.style.height = current_height;
	
	document.getElementById(id).style.height = 0;
	document.getElementById(id).style.opacity = 0;
	document.getElementById(mainMenuId).onclick = createOpenMenu(id, mainMenuId)
	document.getElementById(id).style.display = 'none';
}

function openMenu(id, mainMenuId) {
	document.getElementById(id).style.display = 'block';
	document.getElementById(id).style.height = 'auto';
	document.getElementById(id).style.opacity = 1;
	
	document.getElementById(mainMenuId).onclick = createCloseMenu(id, mainMenuId)
}