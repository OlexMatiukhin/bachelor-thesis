export function initSystemSwitcher() {
 const systemSelect = document.getElementById('system');
    const paramBlocks = document.querySelectorAll('.parameters');
  if (!systemSelect) return;

    function updateVisibility() {
        const selectedValue = systemSelect.value; 
        paramBlocks.forEach(block => {
            if (block.id === `${selectedValue}-params`) {
                block.style.display="block";
            } else {
                block.style.display="none";
            }
        });
    }
    
    updateVisibility();
    systemSelect.addEventListener('change', updateVisibility);
}