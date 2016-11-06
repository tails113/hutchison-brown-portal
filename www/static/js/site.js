// Initialize our editor
var editor = ContentTools.EditorApp.get();
editor.init('*[data-editable]', 'data-name');

// Listen for saved events
editor.addEventListener('saved', function (ev) {
    // Save the changes ...
    var regions = ev.detail().regions;
});

// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---  --- ---

// Add support for auto-save
editor.addEventListener('start', function (ev) {
    var _this = this;

    // Call save every 30 seconds
    function autoSave() {
	_this.save(true);
    };
    this.autoSaveTimer = setInterval(autoSave, 30 * 1000);
});

// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---  --- ---


editor.addEventListener('stop', function (ev) {
    // Stop the autosave
    clearInterval(this.autoSaveTimer);
});

// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---  --- ---

editor.addEventListener('saved', function (ev) {
    var name, onStateChange, passive, payload, regions, xhr;
    console.log('using first');

    // Check if this was a passive save
    passive = ev.detail().passive;

    // Check to see if there are any changes to save
    regions = ev.detail().regions;
    if (Object.keys(regions).length == 0) {
	return;
    }

    // Set the editors state to busy while we save our changes
    this.busy(true);

    // Collect the contents of each region into a FormData instance
    payload = new FormData();
    var editables = document.querySelectorAll('div[data-name]')

    for (var i=0; i<editables.length; i++){
	payload.append(
	    editables[i].getAttribute('data-name'),
	    editables[i].innerHTML
	);
    }

    // payload.append('regions', JSON.stringify(regions))

    onStateChange = function(ev) {
	// Check if the request is finished
	if (ev.target.readyState == 4) {
	    editor.busy(false);
	    if (ev.target.status == '200') {
		// Save was successful, notify the user with a flash
		if (!passive) {
		    new ContentTools.FlashUI('ok');
		}
	    } else {
		// Save failed, notify the user with a flash
		new ContentTools.FlashUI('no');
	    }
	}
    };

    xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', onStateChange);
    xhr.open('POST', '/save_page');
    xhr.send(payload);
});
