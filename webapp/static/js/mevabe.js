function ScaleWindow(){
	if($('.off-canvas-wrap').has('.move-right')){
		$('.off-canvas-wrap').removeClass('move-right');
	}
	if($('.off-canvas-wrap').has('.move-left')){
		$('.off-canvas-wrap').removeClass('move-left');
	}
}
$(window).bind('resize', ScaleWindow);

