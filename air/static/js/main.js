function toggle_well(_id) {
	var div = document.getElementById(_id);
	if (div.style.display !== 'none') {
			div.style.display = 'none';
	}
	else {
			div.style.display = 'block';
	}
}

// Man I suck at Javascript.
try {
	var new_table_button = document.getElementById('new_table_button');
	var cancel_table_button = document.getElementById('cancel_new_table_button');

	new_table_button.onclick = function() {
		toggle_well('create_table_well');
	};

	cancel_table_button.onclick = function() {
		toggle_well('create_table_well');
	};
} catch (e) {
	var new_column_button = document.getElementById('new_column_button');
	var cancel_column_button = document.getElementById('cancel_new_column_button');

	new_column_button.onclick = function() {
		toggle_well('new_column_well');
	};

	cancel_column_button.onclick = function() {
		toggle_well('new_column_well');
	};
}
