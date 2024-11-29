let carritoModal = document.getElementById("carrito-modal")
  function carrito() {
    carritoModal.style.left = "55%"
  }
  function cerrarCarrito() {
    carritoModal.style.left = "150%"
  }
  window.addEventListener("scroll", function () {
    if (window.scrollX !== 0) {
      window.scrollTo(0, window.scrollY); // Forzar la posición horizontal a 0
    }
  });


  

  // Detectar eventos táctiles y bloquear el desplazamiento horizontal
  document.addEventListener("touchstart", function(e) {
    const startX = e.touches[0].clientX;
    const startY = e.touches[0].clientY;
  
    function onTouchMove(moveEvent) {
      const deltaX = moveEvent.touches[0].clientX - startX;
      const deltaY = moveEvent.touches[0].clientY - startY;
  
      // Permitir desplazamiento vertical pero bloquear el horizontal
      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        moveEvent.preventDefault();
      }
    }
  
    // Añadir el handler touchmove
    document.addEventListener("touchmove", onTouchMove, { passive: false });
  
    // Remover el handler touchmove cuando finaliza el touch
    document.addEventListener(
      "touchend",
      function() {
        document.removeEventListener("touchmove", onTouchMove);
      },
      { once: true }
    );
  });
  



  // Selecciona todos los botones dentro de la sidebar
const buttons = document.querySelectorAll('.sidebar-button');

// Agrega un event listener a cada botón
buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Elimina la clase 'active' de todos los botones
        buttons.forEach(btn => btn.classList.remove('active'));
        
        // Agrega la clase 'active' solo al botón que fue clicado
        button.classList.add('active');
    });
});


document.addEventListener('DOMContentLoaded', function () {
  if (document.documentElement.requestFullscreen) {
    document.documentElement.webkitRequestFullscreen();
  }
});
