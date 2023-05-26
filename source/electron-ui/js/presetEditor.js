// Global Variables

presets = []

// +++ AJAX Requests +++

function updatePreset(presetId) {
  $.ajax({
    type: "PATCH",
    url: "http://localhost:5000/id/" + presetId,
    headers: {
        "Content-Type": "application/json"
    },
    data: JSON.stringify({
        name: presets[presetId].name,
        description: presets[presetId].description,
        files: presets[presetId].files
    }),
    success: reloadPresetListAfterChange
});
}

// +++ Callback functions for the AJAX Requests +++

// +++ Other functions +++

function fillPresetEditorDropdown(response) {
    presets = response;

    // get the element with the id 'presetHolderTableBody' via jQuery and delete all its child elements
    
    let presetEditorDropdown = $('#preset-editor-dropdown');
    presetEditorDropdown.empty();

    // for each preset in the response variable
    for (var i = 0; i < response.length; i++) {
        // building a table row
        let option = '<option value="' + response[i].id + '">' + response[i].name + '</option>';

        presetEditorDropdown.append(option);
    }

    if (response) {
      fillPresetEditorForm(response[0].id);
    }
}

function fillPresetEditorForm(presetId) {
  // search for the preset with the given id in the variable 'presets'
  for (var i = 0; i < presets.length; i++) {
    if (presets[i].id == presetId) {
      $('#inputName').val(presets[i].name);
      $('#inputDescription').val(presets[i].description);
      
      // get the element with the id 'fileHolderTableBody' via jQuery and delete all its child elements
      $('#fileHolderTableBody').empty();

      // add a row to each file in the table 'fileHolderTableBody' that's found in the preset with the id 'presetId'
      for (var j = 0; j < presets[i].files.length; j++) {
        var checkBoxTD = '<td><input class="form-check-input" type="checkbox" checked></td>';
        var fileNameTD = '<td>' + presets[i].files[j].name + '</td>';
        var filePathTD = '<td class="filePathTD">' + presets[i].files[j].path + '</td>';

        var fileRow = '<tr>' + checkBoxTD + fileNameTD + filePathTD + '</tr>';

        $('#fileHolderTableBody').append(fileRow);
      }
    }
  }
}

function reloadPresetListAfterChange() {
  // get the element with the id 'presetHolderTableBody' via jQuery and delete all its child elements
  let presetEditorDropdown = $('#preset-editor-dropdown');
  presetEditorDropdown.empty();

  // for each preset in the presets variable
  for (var i = 0; i < presets.length; i++) {
      // building a table row
      let option = '<option value="' + presets[i].id + '">' + presets[i].name + '</option>';

      presetEditorDropdown.append(option);
  }

  if (presets) {
    fillPresetEditorForm(presets[0].id);
  }
}

// +++ Event Listeners +++

// Form Handler
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          } else {

            // Prevent page from auto reload after submit 
            event.preventDefault()
            event.stopPropagation()


            // update the values of the selected presets in the global variable named 'presets'

            // #1 iterate through all presets in the global variable 'presets'
            for (var i = 0; i < presets.length; i++) {

                // #2 save the selected preset's id in a variable (to avoid constantly calling the jQuery function)
                var selectedPresetId = $('#preset-editor-dropdown').val();

                // #3 check if the current preset is the one that's selected in the dropdown
                if (presets[i].id == selectedPresetId) {

                    // #4 update the preset's name and description
                    presets[i].name = $('#inputName').val();
                    presets[i].description = $('#inputDescription').val();

                    // #5 check if there will be any files left in the preset after the deleting the unchecked ones
                    var presetsUnchecked = 0;

                    $('#fileHolderTableBody').children().each(function () {
                      if (!$(this).find('input').prop('checked')) {
                        presetsUnchecked++;
                      }
                    });

                    // todo: make an input that counts the remaning children, and make a bootstrap validator that shows the
                    // was-validated div beneath if the number of remaining children is 0

                    // #6 remove the unchecked files from the selected preset and save it in the global variable 'presets'

                    $('#fileHolderTableBody').children().each(function () {
                      if (!$(this).find('input').prop('checked')) {
                        
                        // remove the file from the preset
                        presets[i].files.splice($(this).index(), 1);
                      }
                    });

                    // Since we found the preset we were searching for, we should stop searching 
                    break;
                  }
                }

            updatePreset($('#preset-editor-dropdown').val());
          }
  
          form.classList.add('was-validated')
        }, false)
      })
})()