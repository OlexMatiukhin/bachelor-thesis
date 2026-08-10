export function shouldDisableHeaderElements (block) {
    const systemSelect = document.getElementById("system");
    const dataSelect = document.getElementById("data");
    const modeSelect = document.getElementById("mode");
    if (systemSelect) systemSelect.disabled = block;
    if (dataSelect) dataSelect.disabled = block;
    if (modeSelect) {
        if (block || (dataSelect && dataSelect.value === "file")) {
            modeSelect.disabled = true;
        } else {
            modeSelect.disabled = false;
        }
    }
    

}



