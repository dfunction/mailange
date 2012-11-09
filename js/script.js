$(function() {
	// ANIMATION
	var users = "What users will see:";
	var crawlers = "What crawlers will see:";
	
	$("#hero").height($(window).height() - 140);
	$("#wrapper").css({top: $(window).height() - 140});
	
	//$("#wrapper").height($(window).height());
	$("#wrapper").waypoint(function(event, direction) {
		if (direction == "down")
			$("p").fadeIn();
		else $("p").fadeOut();
	}, {offset: "50%"});


	// GET HASH
	$("#send").click(function() {
		if ($("#email").val() != "") {
			$.ajax({
				type: 'POST',
				url: 'http://ec2-23-21-153-84.compute-1.amazonaws.com:5000/register',
				data: {
					email: $("#email").val()
				},
				success: receiver,
				error: output_ajax_error,
				dataType: 'json'
			});
		} else {
			output("Please enter a valid e-mail address.");
		}
	});
	
	function receiver(data) {
		if (data.result.indexOf("Success") != -1) {
			output(data.hash);
			use(data.hash);
		}
		else output(data.result);
	}
	
	function output(html) {
		$("#output").html(html);
	}
	
	function output_ajax_error(jqXHR, textStatus, errorThrown) {
		output("We could not service your request at this time. Please try again later.");
	}
	
	function use(hash) {
		$.ajax({
			type: 'GET',
			url: "http://ec2-23-21-153-84.compute-1.amazonaws.com:5000/retrieve/"+hash,
			success: display,
			error: output_ajax_error,
			dataType: 'json'
		});
	}
	
	function display(data) {
		var style = "<style>@font-face{font-family: 'myFont';src: url('data:font/opentype;base64," + data.font + "') format('svg');}</style>";
		$("head").append(style);
		
		$div = $("<div></div>");
		$div.css("font-family", "myFont");
		$div.append(data.email);
		$("body").append($div);
	}

});

//url("data:font/opentype;base64,[base-encoded font here]");