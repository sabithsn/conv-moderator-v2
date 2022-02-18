$(document).ready(function() {

$('[data-bs-toggle="collapse"]').click(function() {
  $(this).toggleClass( "active" );
  if ($(this).hasClass("active")) {
    $(this).text("Hide Context");
  } else {
    $(this).text("See Context");
  }
});
});

function show_hateful_and_paraphrase_question(el){
	show_hateful_question(el);
	show_paraphrase_question(el);
}

function show_hateful_question(el){
	if(el.value == 'yes'){
						document.getElementById('isHatefulQuestion').style.display = 'block'; // Show el
				}else{
						document.getElementById('isHatefulQuestion').style.display = 'none';
						document.getElementById('hateTypeQuestion').style.display = 'none';
										// Hide el
				};

}

function show_hate_type_question(el){
	if(el.value == 'yes'){
						document.getElementById('hateTypeQuestion').style.display = 'block'; // Show el
				}else{
						document.getElementById('hateTypeQuestion').style.display = 'none';
										// Hide el
				};
				show_paraphrase_question(el);

}

function show_paraphrase_question(el){
	console.log(el.value);
	console.log($("#redditContentRules input:checkbox:checked").length);
	if ($("#redditContentRules input:checkbox:checked").length > 0 ||
			$("#subredditRules input:checkbox:checked").length > 0 ||
			document.getElementById('yesIsOffensive').checked)
{// at least one is checked}
						document.getElementById('paraphraseQuestion').style.display = 'block'; // Show el
				}else{
						document.getElementById('paraphraseQuestion').style.display = 'none';
										// Hide el
				};
}
