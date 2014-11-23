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


