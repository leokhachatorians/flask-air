var button = document.getElementById('new_table_button');
var cancel = document.getElementById('cancel_new_table_button');

function hide_create_table_well() {
	var div = document.getElementById('create_table_well');
	if (div.style.display !== 'none') {
			div.style.display = 'none';
	}
	else {
			div.style.display = 'block';
	}
}

button.onclick = hide_create_table_well;
cancel.onclick = hide_create_table_well;
