var upload = function(input) {
  var formData = new FormData();
  var file = input.files[0];
	var xhr = new XMLHttpRequest();
  var data = input.dataset;

  formData.append('file', file);

	if (xhr.upload) {
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        response = JSON.parse(xhr.responseText);
        if (data.fieldName) {
          document.getElementsByName(data.fieldName)[0].value = response.data.object_id;
        }

        if (data.previewElement) {
          document.getElementById(data.previewElement).src = response.data.thumbnail;
        }
      }
    };
    xhr.open("POST", '/api/v1/upload/', true);
		xhr.setRequestHeader("X_FILENAME", file.name);
    xhr.send(formData);
  }
}

var upload_file = function(file, callback) {
	var xhr = new XMLHttpRequest();
  var data = input.dataset;

  formData.append('file', file);

	if (xhr.upload) {
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        response = JSON.parse(xhr.responseText);
        callback(response);
      }
    };
    xhr.open("POST", '/api/v1/upload/', true);
		xhr.setRequestHeader("X_FILENAME", file.name);
    xhr.send(formData);
  }
}

var multiple_upload = function(input) {
  var files = input.files;
  var data = input.dataset;
  var container = $(data.fieldContainer);

  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    var formData = new FormData();
    var xhr = new XMLHttpRequest();

    formData.append('file', file);
   
    if (xhr.upload) {
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
          response = JSON.parse(xhr.responseText);

          if (data.fieldName) {
            var hidden_field = $('<input>', {
              type: 'hidden',
              name: data.fieldName + '[]',
              value: response.data.object_id,
              multiple: true
            }).appendTo(container);

            container.append("<img src='" + response.data.thumbnail + "'/>"); 
          }
        }
      };
      xhr.open("POST", '/api/v1/upload/', false);
      xhr.setRequestHeader("X_FILENAME", file.name);
      xhr.send(formData);
    } 
  }
}

