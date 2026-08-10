export function getVisibleBlock(){
        const operationBlocks = document.querySelectorAll('.operation');
        for (const block of operationBlocks){
            if(window.getComputedStyle(block).display==="flex"){return block}
        }
}