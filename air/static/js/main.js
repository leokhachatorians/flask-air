function toggle_well(_id) {
	var div = document.getElementById(_id);
	if (div.style.display !== 'none') {
			div.style.display = 'none';
	}
	else {
			div.style.display = 'block';
	}
}

function toggle_editable(row_num) {
	for (var c = 0; c < num_columns; c++) {
		var save_button_span = document.getElementById('save_button_' + row_num);
	}
}

var new_table_button = document.getElementById('new_table_button');
var cancel_table_button = document.getElementById('cancel_new_table_button');

var new_column_button = document.getElementById('new_column_button');
var cancel_column_button = document.getElementById('cancel_new_column_button');

var edit_column_button = document.getElementById('edit_column_button');
var cancel_edit_button = document.getElementById('cancel_edit_column_button');
var edit_column_buttons = [].slice.call(document.querySelectorAll('[id^=edit_column_button_]'));

var sheet_rows = [].slice.call(document.querySelectorAll('[id^=row_]'));
var row_cells = [].slice.call(document.querySelectorAll('[id^=cell_]'));
var default_row_cells = []
var num_columns = [].slice.call(document.querySelectorAll('[id^=column_]')).length;
var num_rows = sheet_rows.length;

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

for (var i = 0; i < edit_column_buttons.length; i++) (function(i) {
	edit_column_buttons[i].onclick = function() {
		var id_tag = "edit_column_button_" + i;
		var old_type = id_tag.replace(id_tag, "clicked_column_type_" + i);
		document.getElementById('edit_column_old_name').value = this.value;
		document.getElementById('old_column_name').value = this.value;
		document.getElementById('edit_column_header').innerText = "Edit Column <" + this.value + ">";

		// set the ID associated with the button clicked. So we actually know what we're trying to edit.
		document.getElementById('column_id').value = document.getElementById("clicked_column_name_" + this.value).value;
		document.getElementById("edit_column_old_type").value = document.getElementById(old_type).value;
		toggle_well('edit_column_well');
	}
})(i);

for (var i = 0; i < sheet_rows.length; i++) (function(i) {
	sheet_rows[i].addEventListener("mouseover", function(e) {
		document.getElementById('row_' + i).classList.toggle('test');
		document.getElementById('expand_icon_'+i).classList.toggle('hide-icon');
	}, false);

	sheet_rows[i].addEventListener("mouseout", function(e) {
		document.getElementById('row_' + i).classList.toggle('test');
		document.getElementById('expand_icon_'+i).classList.toggle('hide-icon');
	}, false);
})(i);

if (typeof(cancel_edit_button) != 'undefined' && cancel_edit_button != null) {
	cancel_edit_button.onclick = function() {
		toggle_well('edit_column_well');
	};
}
