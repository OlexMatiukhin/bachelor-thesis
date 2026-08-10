import { updateCharCount } from "../text/initText.js";
export function setInputTextError(errorMessage,status) {
    const textArea = document.getElementById("original-text-content");
    if(status){      
        textArea.classList.add("textarea-error");
        textArea.value = errorMessage
    }
    else{
        textArea.classList.remove("textarea-error");
        textArea.value = "";
       

        const counterEl = textArea.parentElement.querySelector(".text-char-count");
        if (counterEl) {
            updateCharCount(textArea.id, counterEl.id);
        }
    }
   
}  
export function setResultInputError(errorMessage, status) {
    const textArea = document.getElementById("processed-text-content");
    if (status){
    textArea.classList.add("textarea-error");
    textArea.value = errorMessage
    }
    else{
      textArea.classList.remove("textarea-error");
      textArea.value = "";
       const counterEl = textArea.parentElement.querySelector(".text-char-count");
        if (counterEl) {
            updateCharCount(textArea.id, counterEl.id);
        }
    }
  
}  