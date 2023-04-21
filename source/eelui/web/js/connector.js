/*
function createpreset_senddata() {
    let name = document.getElementById('prname').value;
    let desc = document.getElementById('prdesc').value;

    eel.createpreset(name, desc);

    document.getElementById('prdesc').value='';
    document.getElementById('prname').value='';

    delpreset_getdata();
}

// -- delete preset -- //

async function delpreset_getdata() {
    // clearing dropdown elements, in case its only refreshed
    const delpres_dropdown = document.getElementById("delpres_dropdown");

    while (delpres_dropdown.lastElementChild) {
        delpres_dropdown.removeChild(delpres_dropdown.lastElementChild);
    }

    // letting the python script call 'add_preset_to_dropdown()' fill the dropdown with options
    eel.refreshDropdown();
}

function delete_preset() {
    let presetToDel = document.getElementById("delpres_dropdown").value;
    eel.deletepreset(presetToDel);
    delpreset_getdata();
}

function load_preset() {
    let presetToDel = document.getElementById("delpres_dropdown").value;
    eel.loadpreset(presetToDel);
}

function save_preset() {
    let presetToDel = document.getElementById("delpres_dropdown").value;
    eel.savepreset(presetToDel);
}
*/


/*************************************/
/*             ON INIT               */
/*************************************/
//delpreset_getdata();

/*
async function delpreset_getdata() {
    // clearing dropdown elements, in case its only refreshed
    const delpres_dropdown = document.getElementById("presetHolderTableBody");

    while (delpres_dropdown.lastElementChild) {
        delpres_dropdown.removeChild(delpres_dropdown.lastElementChild);
    }

    // letting the python script call 'add_preset_to_dropdown()' fill the dropdown with options
    eel.refreshDropdown();
}
*/

function refreshTable() {
    // get the element with the id 'presetHolderTableBody' via jQuery and save it in a variable
    let tableBody = $('#presetHolderTableBody');

    while (tableBody.lastElementChild) {
        tableBody.removeChild(tableBody.lastElementChild);
    }

    eel.refresh_table();
}

function addPresetToTable(presetname, presetdesc) {
    // get the element with the id 'presetHolderTableBody' via jQuery and save it in a variable
    let tableBody = $('#presetHolderTableBody');

    // building a table row
    let tableRowStart = "<tr>";
    let td_checkbox ='<td><input class="form-check-input" type="checkbox" onclick="checkBoxClicked()"></td>';
    let td_presetname = "<td>" + presetname + "</td>";
    let td_presetdesc = "<td>" + presetdesc + "</td>";
    let td_details = '<td><a class="btn btn-sm btn-primary" href="">Details</a></td>';
    let tableRowEnd = "</tr>";

    // appending the table row to the table body
    tableBody.append(tableRowStart + td_checkbox + td_presetname + td_presetdesc + td_details + tableRowEnd);
}
eel.expose(addPresetToTable);

function createPreset() {
    // getting the values from the input fields
    let name = $('#inputName').val();
    let description = $('#inputDescription').val();

    // logging the variables to the console
    console.log(name);
    console.log(description);

    // calling the python function 'createPreset' and passing the values from the input fields
    eel.create_preset(name, description);
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

function deletePresets() {
    // iterate through all checkboxes in the table presetHolderTableBody and save each checkbox in a variable
    $('#presetHolderTableBody tr').each(function() {
        // check if the checkbox is checked
        if ($(this).find('input[type="checkbox"]').is(':checked')) {
            // get the second td element's value of the current row and send it to the delete function of the backend library
            eel.delete_preset($(this).find('td:eq(1)').text())
        }
    });

    refreshTable();
}

function fillPresetEditorDropdown() {
    eel.refresh_edit_dropdown(); 
}

function addPresetToEditDropdown(presetname, presetdesc) {
    // get the element with the id 'presetHolderTableBody' via jQuery and save it in a variable
    let dropdown = $('#presetEditorDropdown');

    // building a table row
    let option = "<option value='" + presetname + "'>" + presetname + "</option>";

    // appending the table row to the table body
    dropdown.append(option);
}
eel.expose(addPresetToEditDropdown);

function foundNoPresets() {
    // get the element with the id 'presetHolderTableBody' via jQuery and save it in a variable
    let dropdown = $('#presetEditorDropdown');

    // if the dropdown is empty, disable the update button
    if (dropdown.children().length == 0) {
        $('#input_update_button').addClass('btn-disabled');
        console.log('children is empty, added class')
    } else {
        console.log("children isnt empty:")
        console.log(dropdown.children().length)
    }
}
eel.expose(foundNoPresets);