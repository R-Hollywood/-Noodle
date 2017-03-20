$(document).ready(function() {
	var logo = $("#logo");
	logo.wrap($("<a target='_blank'/>").attr("href", logo.attr("href")));
});
