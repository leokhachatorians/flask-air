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

var edit_column_button = document.getElementById('edit_column_button');
var cancel_edit_button = document.getElementById('cancel_edit_column_button');
var edit_column_buttons = [].slice.call(document.querySelectorAll('[id^=edit_column_button_]'));

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

for (i = 0, len = edit_column_buttons.length; i < len; i++) {
	edit_column_buttons[i].onclick = function() {
		document.getElementById('edit_column_old_name').value = this.value;
		document.getElementById('col_to_alter').value = this.value;
		toggle_well('edit_column_well');
	}
}

if (typeof(cancel_edit_button) != 'undefined' && cancel_edit_button != null) {
	cancel_edit_button.onclick = function() {
		toggle_well('edit_column_well');
	};
}

