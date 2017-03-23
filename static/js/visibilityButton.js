//sets a button to toggle the visibility of some other object
function visibilityButton(url, buttonID, visibilityObject) {
	$.get(url, {}, function(){
		$("#" +visibilityObject).hide();
		$('#' + buttonID).click(function(){
			if($("#" + visibilityObject).is(':visible')){
				$("#" + visibilityObject).hide();
			}else{
				$("#" + visibilityObject).show();
			}
		})
	})
}
