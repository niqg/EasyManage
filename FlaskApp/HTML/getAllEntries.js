var getAllEntries = function(){

	$.getJSON($SCRIPT_ROOT + '/entries',{
		
	},
	function(data){
		var data_array = data.result;
		document.write(data_array[0]);
	}
	
	);
}
