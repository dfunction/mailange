$(function() {
	$("#send").click(function() {
		$.ajax({
			type: 'POST',
			url: '/register',
			data: {
				email: $("#email").val()
			},
			success: receiver,
			dataType: 'json'
		});
	});
	
	function receiver(data) {
		console.log(data.result);
	}
});