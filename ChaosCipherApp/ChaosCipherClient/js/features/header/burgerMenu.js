export function initBurgerMenu(){
const burgerBtn = document.getElementById('burgerBtn');
    const menuContainer = document.getElementById('menuContainer');

    burgerBtn.addEventListener('click', () => {
        menuContainer.classList.toggle('open');
        

        burgerBtn.classList.toggle('active');
    });
}
