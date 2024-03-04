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

function validate() {
  pass1 = document.getElementById("password").value
  pass2 = document.getElementById("confirm_password").value
  bt = document.getElementById("submit-btn")
  if (pass1 != pass2) {
    bt.disabled = true;
    document.getElementById("validate-status").textContent = "passwords don't match!";
    document.getElementById("validate-status").style.color = 'red';
  } else {
    bt.disabled = false;
    document.getElementById("validate-status").textContent = "passwords match!";
    document.getElementById("validate-status").style.color = 'green';
  }
}

function showEdit() {
  var modal = document.getElementById("options-div");

  if (modal.style.display === "block") {
    modal.style.display = "none";
  } else {
    modal.style.display = "block";
  }
}

function showSave() {
  const save = document.getElementById('save_form');
  if (save.style.display === "block") {
    save.style.display = "none";
  } else {
    save.style.display = "block";
  }
}

function confirm() {
  const save = document.getElementById('confirm');
  if (save.style.display === "block") {
    save.style.display = "none";
  } else {
    save.style.display = "block";
  }
}

//new feature to be added: toggle between dark and light mode
function switchMode() {
  var el = document.body;
  el.classList.toggle('light-mode');
}

