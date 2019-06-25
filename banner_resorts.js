
$(document).ready(function(){

	var ban1 = 0;
	var ban2 = 0;

	var cnt = 0;
	$('.bottom-banner-resort').each(function(){
		var num_banners = $(this).find('img').length - 1;
		rand =  Math.floor((Math.random() * num_banners));
		while (rand == ban1 || rand == ban2) {
			//generate a random number until it hasn't been used yet
			rand =  Math.floor((Math.random() * num_banners));
		}

		$(this).find('img').hide();
		$(this).find('img').eq(rand).show();

		if (cnt == 0) {
			ban1 = rand;
		}
		else if (cnt == 1) {
			ban2 = rand;
		}

		cnt++;
	});
});
