document.addEventListener('DOMContentLoaded', () => {
  const title = document.getElementById('title');
  const menu   = document.getElementById('side_menu');
  const open   = document.getElementById('menu');
  const close  = document.querySelector('#side_menu .close_button');

  open.addEventListener('click', () => {
    menu.classList.add('visible');

  });

  close.addEventListener('click', () => {
    menu.classList.remove('visible');
  });

  requestAnimationFrame(() => {
    
  });
});