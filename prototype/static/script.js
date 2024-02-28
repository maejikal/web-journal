function classToggle() {
  const navs = document.querySelectorAll('.Navbar__Items')
  
  navs.forEach(nav => nav.classList.toggle('Navbar__ToggleShow'));
}


function goBack() {
        window.history.back();
    }

function showVerses() {
  const extra = document.getElementsByClassName('.extra');
  extra.classList.toggle('extra-show');
}