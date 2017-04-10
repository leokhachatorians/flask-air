function toggle_well(_id) {
	var div = document.getElementById(_id);
	if (div.style.display !== 'none') {
			div.style.display = 'none';
	}
	else {
			div.style.display = 'block';
	}
}

var new_table_button = document.getElementById('new_table_button');
var cancel_table_button = document.getElementById('cancel_new_table_button');
var new_column_button = document.getElementById('new_column_button');
var cancel_column_button = document.getElementById('cancel_new_column_button');

if (typeof(new_table_button) != 'undefined' && new_table_button != null) {
	new_table_button.onclick = function() {
		toggle_well('create_table_well');
	};

	cancel_table_button.onclick = function() {
		toggle_well('create_table_well');
	};
}

if (typeof(new_column_button) != 'undefined' && new_column_button != null) {
	new_column_button.onclick = function() {
		toggle_well('new_column_well');
	};

	cancel_column_button.onclick = function() {
		toggle_well('new_column_well');
	};
}
