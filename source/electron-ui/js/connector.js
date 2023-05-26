// +++ Global Variables +++
sortedAscended = true;
lastSortedIdx = 0;

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

function sortTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch;

    table = document.getElementById("presetHolderTableBody");
    switching = true;

    
    if (lastSortedIdx != columnIndex) {
        sortedAscended = true;
    } else {
        sortedAscended = !sortedAscended;
    }


    /* Make a loop that will continue until no switching has been done: */

    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = $('#fileHolderTableBody').children();
        
        /* Loop through all table rows (except the first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            
            /* Get the two elements you want to compare, one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[columnIndex];
            y = rows[i + 1].getElementsByTagName("TD")[columnIndex];

            if (sortedAscended) {
                // Check if the two rows should switch place:
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else {
                // Check if the two rows should switch place:
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}