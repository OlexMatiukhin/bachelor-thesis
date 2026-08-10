import { MAX_FILE_SIZE, MAX_IMAGE_PIXELS } from "../../config.js";
import { revokeObjectUrl } from "../dropzone/revokeObjectUrl.js";
import { setError, setProgressBar } from "../dropzone/setProgAndErrDrZone.js";
import { shouldDisableHeaderElements } from "../header/headerBlock.js";
import { setProgressBarInDataBlock, setErrorInDataBlock } from "../dataBlock/setProgressAndErrorBlock.js";
import { populatePreview } from "../dataBlock/populatePreview.js";
import { cancelUpload } from "../dataBlock/cancelUpload.js";
import { detectKind } from "../dataBlock/detectKind.js";

function clearZoneState(zone) {
    setProgressBarInDataBlock(zone, "", false);
    setErrorInDataBlock(zone, "", false);
    setError(zone, "", false);
    const processedFileLink = zone.querySelector("#link-download-processed");
    processedFileLink?.removeAttribute("href");
    zone.querySelectorAll(".download-btn").forEach(btn => {
        btn.disabled = true;
    });
}


export function resetProcessedResultByZone(zone) {
    if (!zone) return;
    const zoneId = zone.id;
    clearZoneState(zone);

    if (zoneId === "encrypt-file") {
        const processedFileLink = zone.querySelector("#link-download-processed");
        processedFileLink?.removeAttribute("href");

        const resultName = zone.querySelector("#result-file-name");
        const resultMeta = zone.querySelector("#result-file-meta");
        const resultExt = zone.querySelector("#result-ext");

        if (resultName) resultName.textContent = "—";
        if (resultMeta) resultMeta.textContent = "—";
        if (resultExt) resultExt.textContent = "ENC";
        const pending = zone.querySelector("#result-pending");
        const ready = zone.querySelector("#result-ready");
        if (pending) pending.style.display = "";
        if (ready) ready.style.display = "none";
        const fileDlBtn = zone.querySelector("#file-dl-btn");
        if (fileDlBtn) fileDlBtn.disabled = true;
    }

  
    if (zoneId === "encrypt-image") {
        const processedImage = zone.querySelector("#processed-image-content");
        const resultImgEmpty = zone.querySelector("#result-img-empty");
        if (processedImage) {
            processedImage.removeAttribute("src");
            processedImage.style.display = "none";
        }
        if (resultImgEmpty) {
            resultImgEmpty.style.display = "";
        }
        const imageDlBtn = zone.querySelector("#image-dl-btn");
        if (imageDlBtn) imageDlBtn.disabled = true;

        const processedFileLink = zone.querySelector("#link-download-processed");
        processedFileLink?.removeAttribute("href");
    }

 
    if (zoneId === "encrypt-audio") {

        const audioPending = zone.querySelector("#audio-result-pending");
        const processedAudioPlayer = zone.querySelector("#processed-audio-content");
        const audioDlBtn = zone.querySelector("#audio-dl-btn");

        if (audioPending) {
            audioPending.style.display = "flex";
        }

        if (processedAudioPlayer) {
            processedAudioPlayer.removeAttribute("src");
            processedAudioPlayer.style.display = "none";
            processedAudioPlayer.load();
        }

        if (audioDlBtn) audioDlBtn.disabled = true;

        const processedFileLink = zone.querySelector("#link-download-processed");
        processedFileLink?.removeAttribute("href");
    }
}

export function resetFileSelection(zone) {
    revokeObjectUrl(zone);
    cancelUpload(zone);

    const originalFileLink = document.getElementById("link-download-original");
    const processedFileLink = document.getElementById("link-download-processed");
    originalFileLink?.removeAttribute("href");
    processedFileLink?.removeAttribute("href");

    const originalImage = document.getElementById("original-image-content");
    const processedImage = document.getElementById("processed-image-content");
    if (originalImage) {
        originalImage.src = "";
        originalImage.style.display = "none";
    }
    if (processedImage) {
        processedImage.src = "";
        processedImage.style.display = "none";
    }

    const audioPending = document.getElementById("audio-result-pending");
    const processedAudioPlayer = document.getElementById("processed-audio-content");
    const audioDlBtn = document.getElementById("audio-dl-btn"); 
    if (audioPending) audioPending.style.display = "flex";
    if (processedAudioPlayer) processedAudioPlayer.style.display = "none";
    if (audioDlBtn) audioDlBtn.disabled = true;


    document.querySelectorAll(".operation").forEach(el => {
        if (el.selectedFile) {
            el.selectedFile = null; 
        }
        if(el.id =="drop-zone"){
            setError(el, "", false)
        }
        setProgressBarInDataBlock(el, "", false);
        setErrorInDataBlock(el, "", false);
        el.style.display = "none";
    });

   
    document.querySelectorAll(".file-block-wrap").forEach(wrap => {
        wrap.querySelectorAll(".file-card-name").forEach(n => n.textContent = "—");
        wrap.querySelectorAll(".file-card-meta").forEach(m => m.textContent = "—");

        const origExt = wrap.querySelector("#orig-ext");
        if (origExt) origExt.textContent = "FILE";
        const resultExt = wrap.querySelector("#result-ext");
        if (resultExt) resultExt.textContent = "ENC";

    
        const pending = wrap.querySelector("#result-pending");
        const ready = wrap.querySelector("#result-ready");
        if (pending) pending.style.display = "";
        if (ready) ready.style.display = "none";
        const origImgEmpty = wrap.querySelector("#orig-img-empty");
        if (origImgEmpty) origImgEmpty.style.display = "";
        const resultImgEmpty = wrap.querySelector("#result-img-empty");
        if (resultImgEmpty) resultImgEmpty.style.display = "";


        const origAudio = wrap.querySelector("#original-audio-content");
        if (origAudio) { origAudio.src = ""; origAudio.load(); }

  
        wrap.querySelectorAll(".download-btn").forEach(btn => btn.disabled = true);
    });
}

export function bindProcessedFile(file, ext = null) {
    if (!file) return;

    const operationBlocks = document.querySelectorAll(".operation");
    operationBlocks.forEach(el => {
        if (window.getComputedStyle(el).display !== "flex") return;
        if (el.__objectUrl) {
            URL.revokeObjectURL(el.__objectUrl);
            el.__objectUrl = null;
        }

        el.__fileBuffer = file;
        el.__objectUrl = URL.createObjectURL(file);
        const url = el.__objectUrl;
        if (el.id === "encrypt-image") {
            const img = document.getElementById("processed-image-content");
            if (img) {
                img.src = url;
                img.style.display = "block";
                document.getElementById("result-img-empty")?.style.setProperty("display", "none");
                const dlBtn = document.getElementById("img-dl-btn");
                if (dlBtn) dlBtn.disabled = false;
            }
        }
        else if (el.id === "encrypt-audio") {
            const audioTrack = document.getElementById("processed-audio-content");
            if (audioTrack) {
                audioTrack.src = url;
                audioTrack.style.display = "block";
                document.getElementById("audio-result-pending")?.style.setProperty("display", "none");
                const dlBtn = document.getElementById("audio-dl-btn"); 
                if (dlBtn) dlBtn.disabled = false;
            }
        }
        else if (el.id === "encrypt-file") {
            const displayExt = (ext || 'BIN').toUpperCase();
            const downloadName = ext ? `processed.${ext}` : "processed";
            const a = document.getElementById("link-download-processed");
            if (a) { a.href = url; a.download = downloadName; }

            const nameEl = document.getElementById("processed-file-name");
            const metaEl = document.getElementById("processed-file-meta");
            const extEl  = document.getElementById("result-ext");
            const pending = document.getElementById("result-pending");
            const ready   = document.getElementById("result-ready");
            const dlBtn   = document.getElementById("file-dl-btn");

            if (nameEl) nameEl.textContent = downloadName;
            if (metaEl) metaEl.textContent = (file.size / (1024 * 1024)).toFixed(2) + " МБ";
            if (extEl)  extEl.textContent = displayExt;
            if (pending) pending.style.display = "none";
            if (ready)   ready.style.display = "flex";
            if (dlBtn)   dlBtn.disabled = false;
        }
    });
}


function getImageDimensions(file) {
    return new Promise((resolve, reject) => {
        const url = URL.createObjectURL(file);
        const img = new Image();
        img.onload = () => {
            resolve({ width: img.naturalWidth, height: img.naturalHeight });
            URL.revokeObjectURL(url);
        };
        img.onerror = () => {
            URL.revokeObjectURL(url);
            reject(new Error("Не вдалося прочитати зображення"));
        };
        img.src = url;
    });
}




async function  isFilesSizeCorrect(kind, file){
    if (kind=="image"){
        const { width, height } = await getImageDimensions(file);     
         return width * height < MAX_IMAGE_PIXELS;
    }
    if (kind=="audio"){return file.size < MAX_FILE_SIZE}
    else{
        return file.size < MAX_FILE_SIZE
    }

}
export async function readFile(zone, file) {
    let kind=detectKind(file);
    if (!await isFilesSizeCorrect(kind, file)) {
        if(kind=="image"){
            setError(zone, `Зображення завелике за кількістю пікселів. Максимум: ~2,07 Мпікс`, true);
            return
        }
        setError(zone, "Файл занадто великий за розміром!", true);
        return
    }
    shouldDisableHeaderElements(true);
    revokeObjectUrl(zone)
    zone.selectedFile = file

    setError(zone, "", false);
    const reader = new FileReader();
    zone.__reader = reader;
    reader.onload = () => {
        zone.__fileBuffer = reader.result;
        zone.__reader = null;
        zone.__objectUrl = URL.createObjectURL(file);
        console.log("File in Buffer");
        setProgressBar(zone, 100, true);
        setTimeout(() => { setProgressBar(zone, 0, false) }, 500);
        populatePreview(zone);
    }
    reader.onprogress = (e) => {
        if (e.lengthComputable) {
            const pct = Math.round((e.loaded / e.total) * 100);
            setProgressBar(zone, pct, true);
        }
    }
    reader.onabort = (e) => {
        setProgressBar(zone, 0, false)
        setError(zone, "Читання файлу скасовано", true);
        shouldDisableHeaderElements(false);

    }
    reader.onerror = (e) => {
        setProgressBar(zone, 0, false)
        setError(zone, "Помилка при читанні", true);
        shouldDisableHeaderElements(false);
    }
    reader.readAsArrayBuffer(file);
}