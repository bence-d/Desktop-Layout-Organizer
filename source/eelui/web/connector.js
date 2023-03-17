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

function add_preset_to_dropdown(presetname) {
    console.log("adding " + presetname + " to dropdown");

    let presetToAdd = new Option(presetname, presetname);
    const select = document.getElementById('delpres_dropdown'); 
    select.add(presetToAdd,undefined);
}
eel.expose(add_preset_to_dropdown);

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


/*************************************/
/*             ON INIT               */
/*************************************/
delpreset_getdata();