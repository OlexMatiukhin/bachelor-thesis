import { initBurgerMenu } from "./features/header/burgerMenu.js";

import { initSystemSwitcher } from "./features/haosSelect/switchingSystemHaos.js";
import { initDataModeSwitcher } from "./features/dataMode/switchingFile.js";

import { readFile, resetFileSelection } from "./features/file/readFile.js";
import { abortDownload } from "./features/dropzone/abortDownload.js";
import { uploadStoredFile } from "./features/file/uploadFile.js";
import { uploadText } from "./features/text/uploadText.js";
import { setupDownloadButtons } from "./features/dataBlock/setupDownloadButtons.js";
import { setInputTextError, setResultInputError } from "./features/text/setTextError.js";
import { initText } from "./features/text/initText.js";
document.addEventListener('DOMContentLoaded', () => {
    window.addEventListener("dragover", (e) => { e.preventDefault() }, { passive: false });
    window.addEventListener("drop", (e) => {
        const insideZone = e.target && (e.target.closest ? e.target.closest('[data-dropzone]') : null)
        if (!insideZone) e.preventDefault()
    }, { passive: false })

  
    initBurgerMenu();
    initSystemSwitcher();
    initDataModeSwitcher();
    
    const input = document.querySelector(".file-input");
    const dropzone = document.querySelector(".dropzone-inner");
    const removeButtons = document.querySelectorAll(".remove-btn");
    const encryptButtons = document.querySelectorAll(".encrypt-btn");
    const decryptButtons = document.querySelectorAll(".decrypt-btn");
    dropzone.addEventListener("click", (e) => {
        input.click();

    });
    input.addEventListener('change', () => {
        const f = input.files && input.files.length ? input.files[0] : null;
        if (f) {
            readFile(dropzone, f);
            input.value = '';
        }
    });
    dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        const files = e.dataTransfer && e.dataTransfer.files ? e.dataTransfer.files : null;
        if (!files || files.length == 0) return
        const f = files[0]
        console.log(f.name);
        readFile(dropzone, f);


    });

    removeButtons.forEach(button => {
        button.addEventListener("click", () => {
            resetFileSelection(dropzone);
            const dropZone = document.getElementById("drop-zone");
            dropZone.style.display = "flex";
        })
    })
    encryptButtons.forEach(btn => btn.addEventListener("click", () => uploadStoredFile(dropzone, "Encrypt", btn)));

    decryptButtons.forEach(btn => btn.addEventListener("click", () => uploadStoredFile(dropzone, "Decrypt", btn)));
    setupDownloadButtons();
    initText();
});
