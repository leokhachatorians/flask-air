var table = new Vue({
	el: '#table',
	data: {
		my_list: [],
		columns: [],
		message: "blah",
	},
	methods: {
		populate_table: function() {
			var self = this;
			axios.get('/get_sheet')
				.then(response => {
							self.my_list = response.data;
							self.columns = response.data['columns'];
							delete self.my_list['columns'];
				});
		},
		add_data: function() {
			var self = this;
			var add_records = document.getElementsByName('add_records');
			var data = {}

			data['values'] = []
			for (var i = 0; i < add_records.length; i++) {
				data['values'].push(add_records[i]['value'])
			}
			data['sheet_id'] = document.getElementById('sheet_id').value;
			axios.post('/add_data', data)
				.then(function (res) {
					self.populate_table();
				})
				.catch(function (err) {
					console.log(err.message);
				});
		},
		delete_data: function(e) {
			var self = this;
			var form = e.target.form;
			var data = {}
			data['sheet_id'] = document.getElementById('sheet_id').value;
			data['row_id'] = form.elements.namedItem('row_id').value;
			axios.post('/delete_data', data)
				.then(function (res) {
					self.populate_table();
				})
				.catch(function (err) {
					console.log(err.message);
				});
		},
		edit_data: function(e) {
			var self = this;
			var form = e.target.form;
			var data = {}
			data['sheet_id'] = document.getElementById('sheet_id').value;
			data['row_id'] = form.elements.namedItem('row_id').value;
			data['values'] = []
			// A little hacky, but due to inability to have forms in tables,
			// have to access the input fields via their parent TD via ID (which is acutally the rowID)
			input_td_nodes = document.getElementsByName(data['row_id']);
			for (var i = 0; i < input_td_nodes.length; i++) {
				data['values'].push(input_td_nodes[i].childNodes[0].value);
			}
			axios.post('/modify_data', data)
				.then(function (res) {
					self.populate_table()
				})
			.catch(function (err) {
				console.log(err.message);
			});
		},
	},
	beforeMount() {
		this.populate_table()
	},
})

Vue.component('column-headers', {
	props: ['column'],
	template: '<th>{{ column }}</th>'
})

Vue.component('table-cell', {
	props: ['data'],
	template: `
		<td>
			<input v-bind:value="data" id="row_cell">
		</td>
		`,
})

Vue.component('row-id', {
	props: ['data'],
	template: `<input type="hidden" v-bind:value="data.id" id="row_id">`
})
