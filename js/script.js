$(function() {
	$("#send").click(function() {
		if ($("#email").val() != "") {
			$.ajax({
				type: 'POST',
				url: 'http://ec2-23-21-153-84.compute-1.amazonaws.com:5000/register',
				data: {
					email: $("#email").val()
				},
				success: receiver,
				dataType: 'json'
			});
		}
	});
	
	function receiver(data) {
		console.log(data.result);
	}
});

//url("data:font/opentype;base64,[base-encoded font here]");