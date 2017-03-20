$(document).ready(function() {
	var logo = $("#logo");
	logo.wrap($("<a target='_self'/>").attr("href", logo.attr("href")));
});
