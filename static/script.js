//code for image preview
var reader = new FileReader();
reader.onload = function(e) {
	$("#imager").attr("src", e.target.result);
};

function readURL(input) {
	if (input.files && input.files[0]) {
		reader.readAsDataURL(input.files[0]);
	}
}

$("#image-input").change(function() {
	readURL(this);
	$(".js-file-name")
		.html($("#image-input").val())
		.css("color", "green");
});

$(function() {
	$("#save-image").click(function() {
		html2canvas($(".design"), {
			width: 1500,
			onrendered: function(canvas) {
				theCanvas = canvas;
				Canvas2Image.saveAsPNG(canvas);
			}
		});
	});
});

$(".js-mirror").on("change keyup", function() {
	var valueToInput = $(this).val();
	var destination = ".js-" + $(this).data("destination");
	$(".design")
		.find(destination)
		.text(valueToInput);

	if ($(this).is("#word")) {
		var firstChar = $("input#word")
			.val()
			.charAt(0);
		$(".js-alphabet").html(firstChar + firstChar);
	}
});

$('input[name="word-type"]').on("change", function() {
	$(".js-type").html("(" + $(this).val() + ")");
});