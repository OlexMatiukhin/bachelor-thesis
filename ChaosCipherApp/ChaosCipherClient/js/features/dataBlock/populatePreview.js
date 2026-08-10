import { detectKind } from "./detectKind.js";
import { shouldDisableHeaderElements } from "../header/headerBlock.js";
import { checkFileMarker } from "../file/checkFileMarker.js";
function setButtonMaker(block, marker) {
    const decryptbtn = block.querySelector(".decrypt-btn")
    const encryptbtn = block.querySelector(".encrypt-btn")
    if (decryptbtn) decryptbtn.disabled = !marker;
    if (encryptbtn) encryptbtn.disabled = !!marker;
}

function setupImageBlock(activeBlock, url, marker) {
    const img = document.getElementById("original-image-content");
    if (img) {
        img.src = url;
        setButtonMaker(activeBlock, marker);
        img.style.display = "block";
        const empty = document.getElementById("orig-img-empty");
        if (empty) empty.style.display = "none";
    }
}

function setupAudioBlock(activeBlock, url, marker) {
    const audioTrack = document.getElementById("original-audio-content");
    if (audioTrack) {
        audioTrack.src = url;
        setButtonMaker(activeBlock, marker);
    }
}

function setupFileBlock(activeBlock, file, url, marker) {
    const a = document.getElementById("link-download-original")
    if (a) {
        a.href = url;
        setButtonMaker(activeBlock, marker);
        a.download = file.name;
        const nameEl = document.getElementById("original-file-name");
        const metaEl = document.getElementById("original-file-meta");
        const extEl = document.getElementById("orig-ext");
        if (nameEl) nameEl.textContent = file.name;
        if (metaEl) metaEl.textContent = (file.size / (1024 * 1024)).toFixed(2) + " МБ";
        if (extEl) extEl.textContent = file.name.split('.').pop().toUpperCase();
    }
    activeBlock.dataset.originalFilename = file.name;
}

function setupBlockPreview(activeBlock, kind, file, url, marker) {
    switch (kind) {
        case "image":
            setupImageBlock(activeBlock, url, marker);

            break;
        case "audio":
            setupAudioBlock(activeBlock, url, marker);
            break;
        case "other":
            setupFileBlock(activeBlock, file, url, marker);
            break;
        default:
            break;
    }
}
export async function populatePreview(zone) {
    const file = zone.selectedFile;
    const url = zone.__objectUrl;
    if (!file) return;
    const kind = detectKind(file);
    const kindToBlockId = { image: "encrypt-image", audio: "encrypt-audio", other: "encrypt-file" };
    const operationBlocks = document.querySelectorAll('.operation');
   try {
        shouldDisableHeaderElements(false);
        let marker = null;    
        marker = await checkFileMarker(file);
        operationBlocks.forEach(block => {
            block.style.display = block.id === kindToBlockId[kind] ? "flex" : "none";
        });
        const activeBlock = document.getElementById(kindToBlockId[kind]);
        if (activeBlock) setupBlockPreview(activeBlock, kind, file, url, marker);
    } 
    catch (error){
        shouldDisableHeaderElements(false);
    }
} 