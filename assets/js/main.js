(function () {
	'use strict';

	var CADENCIAS = ['diario', 'semanal', 'mensual', 'anual'];
	var ETIQUETAS = { diario: 'Hoy', semanal: 'Esta semana', mensual: 'Este mes', anual: 'Este año' };
	var CHIP_CONFIANZA = {
		'confirmado oficial': 'chip--confirmado',
		'fiable': 'chip--fiable',
		'rumor de comunidad': 'chip--rumor'
	};

	var raiz = document.getElementById('lista-eventos');
	var pestanas = document.getElementById('pestanas');
	var estado = document.getElementById('estado');
	var actual = 'diario';
	var eventos = [];

	function escapar(texto) {
		var d = document.createElement('div');
		d.textContent = texto == null ? '' : String(texto);
		return d.innerHTML;
	}

	function tarjeta(ev) {
		var chips = '';
		if (ev.tramo === 'A') {
			chips += '<span class="chip chip--puntuacion">' + escapar(ev.puntuacion) + '/100</span>';
		} else {
			chips += '<span class="chip chip--tramo-b">Radar temprano</span>';
		}
		chips += '<span class="chip ' + (CHIP_CONFIANZA[ev.confianza] || '') + '">' + escapar(ev.confianza) + '</span>';
		(ev.notas || []).forEach(function (n) {
			chips += '<span class="chip chip--nota">' + escapar(n) + '</span>';
		});

		var fuentes = (ev.fuentes || []).map(function (f) {
			return '<a href="' + escapar(f.url) + '" target="_blank" rel="noopener">' + escapar(f.texto) + '</a>';
		}).join(' · ');

		return (
			'<li class="evento">' +
				'<div class="evento__cabecera">' +
					'<span class="evento__juego">' + escapar(ev.juego) + '</span>' +
					'<span class="evento__fecha">' + escapar(ev.fecha) + '</span>' +
				'</div>' +
				'<p class="evento__resumen">' + escapar(ev.resumen) + '</p>' +
				'<div class="evento__meta">' + chips + '</div>' +
				(fuentes ? '<div class="evento__fuentes">' + fuentes + '</div>' : '') +
			'</li>'
		);
	}

	function pintar() {
		var filtrados = eventos.filter(function (e) { return e.cadencia === actual; });

		if (!eventos.length) {
			estado.hidden = false;
			estado.textContent = 'Todavía no hay eventos guardados. El radar diario se ejecuta de lunes a viernes a las 8:05.';
			raiz.innerHTML = '';
			return;
		}
		if (!filtrados.length) {
			estado.hidden = false;
			estado.textContent = 'Sin eventos de este tipo por ahora.';
			raiz.innerHTML = '';
			return;
		}
		estado.hidden = true;
		raiz.innerHTML = filtrados.map(tarjeta).join('');
	}

	function cambiarPestana(cadencia) {
		actual = cadencia;
		Array.prototype.forEach.call(pestanas.children, function (b) {
			b.setAttribute('aria-selected', b.dataset.cadencia === cadencia ? 'true' : 'false');
		});
		pintar();
	}

	pestanas.innerHTML = CADENCIAS.map(function (c, i) {
		return '<button type="button" data-cadencia="' + c + '" aria-selected="' + (i === 0 ? 'true' : 'false') + '">' + ETIQUETAS[c] + '</button>';
	}).join('');
	Array.prototype.forEach.call(pestanas.children, function (b) {
		b.addEventListener('click', function () { cambiarPestana(b.dataset.cadencia); });
	});

	fetch('data/eventos.json', { cache: 'no-store' })
		.then(function (r) { return r.json(); })
		.then(function (datos) {
			eventos = Array.isArray(datos) ? datos : [];
			pintar();
		})
		.catch(function () {
			estado.hidden = false;
			estado.textContent = 'No se han podido cargar los eventos ahora mismo.';
		});
})();
