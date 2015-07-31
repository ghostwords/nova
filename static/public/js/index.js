var GAL_IDS = [
	'workers-gallery',
	'restaurants-gallery'
];

var gals, cells;

function toArray(obj) {
	var array = [];
	// iterate backwards ensuring that length is an UInt32
	for (var i = obj.length >>> 0; i--;) {
		array[i] = obj[i];
	}
	return array;
}

function galOff(gal, i) {
	gal.element.className = 'pure-g l-box';

	cells[i].forEach(function (cell) {
		cell.className = cell.className.replace('cell', 'l-box');
	});

	gal.destroy();
}

function galOn(gal, i) {
	gal.element.className = 'gallery';

	cells[i].forEach(function (cell) {
		cell.className = cell.className.replace('l-box', 'cell');
	});

	gal.activate();
}

enquire.register("screen and (min-width: 48em)", {
	match: function () {
		gals.forEach(galOff);
	},

	unmatch: function () {
		gals.forEach(galOn);
	},

	setup: function () {
		cells = GAL_IDS.map(function (id) {
			return toArray(document.getElementById(id).children);
		});

		// page defaults to JS-less responsive layout
		// give the galleries appropriate classes before initializing below
		cells.forEach(function (cells) {
			cells.forEach(function (cell) {
				cell.className = cell.className.replace('l-box', 'cell');
			});
			cells[0].parentNode.className = 'gallery';
		});

		gals = GAL_IDS.map(function (id) {
			return new Flickity('#' + id)
		});
	}
});

smoothScroll.init();
