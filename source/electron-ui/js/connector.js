// +++ Global Variables +++

// +++ AJAX Requests +++

function getAllPresets(callback) {
  $.ajax({
      type: "GET",
      url: "http://localhost:5000/",
      success: callback
  });
}

function deletePreset(presetId, callback) {
  $.ajax({
      type: "DELETE",
      url: "http://localhost:5000/id/" + presetId,
      success: callback
  });
}

function addPreset(presetName, presetDescription, callback) {
  $.ajax({
      type: "POST",
      url: "http://localhost:5000/",
      headers: {
          "Content-Type": "application/json"
      },
      data: JSON.stringify({
          name: presetName,
          description: presetDescription
      }),
      success: callback
  });
}

// +++ Callback functions for the AJAX Requests +++

function fillListWithPresets(response) {
  // get the element with the id 'presetHolderTableBody' via jQuery and delete all its child elements
  $('#presetHolderTableBody').empty();

  console.log(response);
  // get the element with the id 'presetHolderTableBody' via jQuery and save it in a variable
  let tableBody = $('#presetHolderTableBody');

  // for each preset in the response variable
  for (var i = 0; i < response.length; i++) {
    // building a table row
    let tableRowStart = "<tr>";
    let td_checkbox ='<td><input class="form-check-input" type="checkbox" onclick="checkBoxClicked()"></td>';
    let td_presetname = "<td>" + response[i].name + "</td>";
    let td_presetdesc = "<td>" + response[i].description + "</td>";

    // actions
    let td_actions = '<td>'
        td_actions += '<a class="btn btn-sm btn-primary mx-1" href=""><i class="fa fa-check me-2 mx-2"></i></a>';
        td_actions += '<a class="btn btn-sm btn-primary mx-1" href=""><i class="fa fa-pen me-2 mx-2"></i></a>';
        td_actions += '</td>';
    let tableRowEnd = "</tr>";

    // appending the table row to the table body
    tableBody.append(tableRowStart + td_checkbox + td_presetname + td_presetdesc + td_actions + tableRowEnd);
  }
}

// +++ Other functions +++

var disableDeleteButton = true;

function checkBoxClicked() {
    disableDeleteButton = true;
    // iterate through all checkboxes in the table presetHolderTableBody and save each checkbox in a variable
    $('#presetHolderTableBody input[type="checkbox"]').each(function() {
        if (this.checked) {
            disableDeleteButton = false;
        }
    });

    if (disableDeleteButton == true) {
        $('#input_delete_button').addClass('btn-disabled');
    } else {
        $('#input_delete_button').removeClass('btn-disabled');
    }
}

function toggleAllCheckBoxes() {
    var newValue = $('#cb_checkAll')[0].checked;

    // iterate through all checkboxes in the table presetHolderTableBody and save each checkbox in a variable
    $('#presetHolderTableBody input[type="checkbox"]').each(function() {
        // toggle the checkbox
        this.checked = newValue;
    });

    checkBoxClicked();
}

function deletePresets(presets) {
  // iterate through all checkboxes in the table presetHolderTableBody and save each checkbox in a variable
  $('#presetHolderTableBody tr').each(function() {
      // check if the checkbox is checked
      if ($(this).find('input[type="checkbox"]').is(':checked')) {
          // get the second td element's value of the current row and send it to the delete function of the backend library
         
          for (var i = 0; i < presets.length; i++) {
            if (presets[i].name == $(this).find('td:nth-child(2)').text()) {
              console.log("delete preset with id: " + presets[i].id);
              deletePreset(presets[i].id, getAllPresets(fillListWithPresets));
            }
          }
      }
  });

  getAllPresets(fillListWithPresets);
}

function deleteSelectedPresets() {
    getAllPresets(deletePresets);
}

function createPreset() {
    let presetName = $('#input_preset_name').val();
    let presetDescription = $('#input_preset_description').val();
    addPreset(presetName, presetDescription, getAllPresets());
}