import { resetTextSelection } from "../dataBlock/resetTextSelection.js";
import { resetFileSelection } from "../file/readFile.js";
import { setProgressBarInDataBlock, setErrorInDataBlock } from "../dataBlock/setProgressAndErrorBlock.js";
import { setResultInputError, setInputTextError } from "../text/setTextError.js";
export function initDataModeSwitcher() {

    const typeInfoSelect = document.getElementById('data');
    const operationBlocks = document.querySelectorAll('.operation');
    const modeSelect = document.getElementById('mode');
    const dropZone = document.getElementById("drop-zone");
    function updateDataVisibility() {
        const selectedValue = typeInfoSelect.value;
        if (selectedValue === "text") {
            modeSelect.disabled = false;
            resetFileSelection(dropZone);
        }
        else if (selectedValue === "file") {
            modeSelect.disabled = true;
            resetTextSelection();
        }
         operationBlocks.forEach(block => {

            if (selectedValue === "text") {
                block.style.display =
                    block.id === "encrypt-text"
                        ? "block"
                        : "none";
            }

            else if (selectedValue === "file") {
                block.style.display =
                    block.id === "drop-zone"
                        ? "block"
                        : "none";
            }
        });
           
    }
     typeInfoSelect.addEventListener('change', updateDataVisibility);   

     updateDataVisibility()
}
