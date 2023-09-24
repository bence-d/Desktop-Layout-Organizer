// +++ Global Variables +++
let sortedAscended = true;
let lastSortedIdx = 0;

let filesToAdd = [];
let filesAdded = [];
let presetData = [];
let lastFileAddedIdx = 0;
pause = false;

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

function updatePreset(presetId, presetName, presetDescription, presetFiles, callback) {
    $.ajax({
        type: "PATCH",
        url: "http://localhost:5000/id/" + presetId,
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            name: presetName,
            description: presetDescription,
            files: presetFiles
        }),
        success: callback
    });
}

function loadPreset(presetId) {
    $.ajax({
        type: "GET",
        url: "http://localhost:5000/load/" + presetId,
        success: (response) => {console.log(response)}
    });
  }

function savePreset(presetId) {
    $.ajax({
        type: "GET",
        url: "http://localhost:5000/save/" + presetId,
        success: (response) => {console.log(response)}
    });
}

function importPreset(sourceParam, nameParam) {
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/import",
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            source: sourceParam,
            name: nameParam
        }),
        success: (response) => {console.log("[connector.js] importPreset > response: " + response)}
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
        td_actions += '<a class="btn btn-sm btn-primary mx-1" onclick="loadPreset(' + response[i].id + ')"><i class="fa fa-check me-2 mx-2"></i></a>';
        td_actions += '<a class="btn btn-sm btn-primary mx-1" onclick="savePreset(' + response[i].id + ')"><i class="fa fa-save me-2 mx-2"></i></a>';
        td_actions += '<a class="btn btn-sm btn-primary mx-1" href=""><i class="fa fa-pen me-2 mx-2"></i></a>';
        td_actions += '</td>';
    let tableRowEnd = "</tr>";

    // appending the table row to the table body
    tableBody.append(tableRowStart + td_checkbox + td_presetname + td_presetdesc + td_actions + tableRowEnd);
  }
}

// param1: the new preset object
// param2: list of files
function addFilesToPreset(response) {

    /* For each file of the preset, pass a list with the files that have already been added to the preset,
        cause it's not gone move files anymore, only append them to the list in the backend.

        Because .lnk files just get skipped, won't be moved but only added to the list in the presetlist.json file
        See 'presetManager.py' for more information...
        
        example: 

        [1]: 
        updatepreset(6, "newPresetName", "newPresetDesc", "~/file1.txt")

        [2]: 
        updatepreset(6, "newPresetName", "newPresetDesc", "~/file1.txt", "~/file2.txt")

        [3]: 
        updatepreset(6, "newPresetName", "newPresetDesc", "~/file1.txt", "~/file2.txt", "~/file3.txt")
        */

    // finally call
    // getAllPresets()
    console.log("addFilesToPreset() response: " )
    console.log(response)

    console.log("starting to add files...")
    
    lastFileAddedIdx = 0
    presetData = response[0]
    filesToAdd = response[1]
    filesAdded.push(response[1][lastFileAddedIdx])
    updatePreset(response[0].id, response[0].name, response[0].description, filesAdded, null)
    $("#create-progressbar-progress").css("width",  ((filesAdded.length / filesToAdd.length) * 100) +  "%");
    $('#create-progressbar-progress').html(filesAdded.length + "/" + filesToAdd.length);
    $('#create-pause-progress').removeAttr("disabled");
    addNextFileToPreset()
}

// +++ Other functions +++

async function addNextFileToPreset() {

    do
    {
        lastFileAddedIdx++

        if (lastFileAddedIdx < filesToAdd.length) {
            console.log("adding file " + filesToAdd[lastFileAddedIdx] + " to preset")
            filesAdded.push(filesToAdd[lastFileAddedIdx])
            updatePreset(presetData.id, presetData.name, presetData.description, filesAdded, null)
            console.log("filesadded: " )
            console.log(filesAdded)
        }
        
        $("#create-progressbar-progress").css("width",  ((filesAdded.length / filesToAdd.length) * 100) +  "%");
        $('#create-progressbar-progress').html(filesAdded.length + "/" + filesToAdd.length);

        if (pause) {
            break;
        }

        await sleep(500);
    } while (lastFileAddedIdx+1 < filesToAdd.length);

    if (!pause) {
        await sleep(1500);
        window.location.href = 'create.html';
    }
}

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
    addPreset(presetName, presetDescription, addFilesToPreset);
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
    lastSortedIdx = columnIndex;


    /* Make a loop that will continue until no switching has been done: */
    while (switching) {

        // Start by saying: no switching is done:
        switching = false;
        rows = $('#presetHolderTableBody').children();

        console.log("got children of table -> ");
        console.log(rows.length)
        
        /* Loop through all table rows (except the first, which contains table headers): */
        for (i = 0; i < (rows.length - 1); i++) {
            console.log("chechking row by idx " + i);
            // Start by saying there should be no switching:
            shouldSwitch = false;
            
            /* Get the two elements you want to compare, one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[columnIndex];
            y = rows[i + 1].getElementsByTagName("TD")[columnIndex];

            if (sortedAscended) {
                console.log("sorting ascended");
                // Check if the two rows should switch place:
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else {
                console.log("sorting descended")
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

function sendImportRequest() {
    // to be implemented

    // Gather data from inputfields
    preset_source_path = $('#input_source_preset').val();
    preset_name = $('#input_preset_name').val();

    // Call function
    importPreset(preset_source_path, preset_name);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function togglePause() {
    pause = !pause;
    addNextFileToPreset();

    $('#create-pause-progress').html(pause ? "Resume" : "Pause");
}