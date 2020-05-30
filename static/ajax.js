$(document).ready(function() {
	$('#form_register').on('submit', function(event) {
		$.ajax({
			data: {
				prenom: $('#prenom').val(),
				nom: $('#nom').val(),
				uid: $('#uid_register').val(),
				password: $('#password_register').val()
			},
			type: 'POST',
			url: '/register'
		}).done(function(data) {
			if (data.error) {
				Notiflix.Notify.Failure(data.error);
			}
			if (data.title) {
				Notiflix.Notify.Success(data.body);
			}
		});
		event.preventDefault();
	});
});
$(document).ready(function() {
	$('#form_login').on('submit', function(event) {
		$.ajax({
			data: {
				uid: $('#uid_login').val(),
				password: $('#password_login').val()
			},
			type: 'POST',
			url: '/login'
		}).done(function(data) {
			if (data.error) {
				Notiflix.Notify.Failure(data.error);
			}
			if (data.name) {
				document.querySelector("#tickets-form").style.display = "block";
				forms = document.querySelectorAll(".base-form")
				forms.forEach(form => form.style.display = "none");
				document.getElementById("nom_paiement").innerHTML = data.name;
				document.getElementById("tickets_paiement_info").innerHTML = data.tickets;
				document.getElementById("uid_paiement").value = data.uid;
				document.getElementById("password_paiement").value = data.pass;
			}
		});
		event.preventDefault();
	});
});
$(document).ready(function() {
	$('#form_paiement').on('submit', function(event) {
		$.ajax({
			data: {
				uid_paiement: $('#uid_paiement').val(),
				tickets_paiement: $('#tickets_paiement').val(),
				password_paiement: $('#password_paiement').val(),
			},
			type: 'POST',
			url: '/paiement'
		}).done(function(data) {
			if (data.error) {
				Notiflix.Notify.Failure(data.error);
			}
			if (data.title) {
				document.getElementById("tickets_paiement_info").innerHTML = data.tickets;
				Notiflix.Notify.Success(data.body);
			}
		});
		event.preventDefault();
	});
});