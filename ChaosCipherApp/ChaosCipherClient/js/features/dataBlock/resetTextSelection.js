import {setErrorInDataBlock, setProgressBarInDataBlock} from "../dataBlock/setProgressAndErrorBlock.js";
import { cancelUpload } from "./cancelUpload.js";
import {clearTextArea} from "../text/initText.js"
export function resetTextSelection(){    
      const textBlock = document.getElementById("encrypt-text");
      cancelUpload(textBlock); 
      setErrorInDataBlock(textBlock,"",false);
      setProgressBarInDataBlock(textBlock, 0, false);
      textBlock.style.display="none";      
      clearTextArea("original-text-content", "in-char-count");
      clearTextArea("processed-text-content", "out-char-count");
}
