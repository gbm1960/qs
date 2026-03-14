async function cargarContenido() {
    try {
        console.log("Cargando contenido...");
        
        // Cargar Quiénes Somos
        const quienesResponse = await fetch('data/quienes-somos.txt');
        if (!quienesResponse.ok) {
            throw new Error(`Error cargando quienes-somos: ${quienesResponse.status}`);
        }
        const quienesTexto = await quienesResponse.text();
        
        const quienesDiv = document.querySelector('.about-text');
        if (quienesDiv) {
            quienesDiv.innerHTML = '';
            const parrafos = quienesTexto.split('\n\n');
            parrafos.forEach(parrafo => {
                if (parrafo.trim() !== '') {
                    const p = document.createElement('p');
                    p.textContent = parrafo.trim();
                    quienesDiv.appendChild(p);
                }
            });
        }

        // Cargar Servicios
        const serviciosResponse = await fetch('data/servicios.txt');
        if (!serviciosResponse.ok) {
            throw new Error(`Error cargando servicios: ${serviciosResponse.status}`);
        }
        const serviciosTexto = await serviciosResponse.text();
        const servicios = JSON.parse(serviciosTexto);
        
        const serviciosGrid = document.querySelector('.services-grid');
        if (serviciosGrid) {
            serviciosGrid.innerHTML = '';
            servicios.forEach(servicio => {
                const card = document.createElement('div');
                card.className = 'service-card';
                card.innerHTML = `
                    <i class="fas ${servicio.icono}"></i>
                    <h3>${servicio.titulo}</h3>
                    <p>${servicio.descripcion}</p>
                `;
                serviciosGrid.appendChild(card);
            });
        }

    } catch (error) {
        console.error('Error:', error);
        const quienesDiv = document.querySelector('.about-text');
        if (quienesDiv) {
            quienesDiv.innerHTML = '<p style="color: #c0392b;">Error cargando contenido. Por favor, recarga la página.</p>';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    cargarContenido();

    // Lógica del Formulario de Contacto
    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');

    if (contactForm) {
        // Validación y formato del campo teléfono
        const phoneInput = document.getElementById('telefono');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => {
                let value = e.target.value;
                
                // Asegurar que siempre empiece con +57 
                if (!value.startsWith('+57 ')) {
                    value = '+57 ' + value.replace(/^\+?5?7?\s?/, '');
                }
                
                // Limitar a +57 seguido de máximo 10 dígitos
                const prefix = '+57 ';
                const digits = value.slice(prefix.length).replace(/\D/g, '').slice(0, 10);
                e.target.value = prefix + digits;
            });

            // Evitar que se borre el inicio
            phoneInput.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && e.target.selectionStart <= 4 && e.target.selectionEnd <= 4) {
                    e.preventDefault();
                }
            });
        }

        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Cambiar estado del botón
            const submitBtn = contactForm.querySelector('button');
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Enviando...';
            submitBtn.disabled = true;

            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData.entries());

            try {
                // NOTA: Esta URL será la de tu Cloudflare Worker una vez desplegada
                const WORKER_URL = 'https://contacto-quadratic.gilberto-borbon-1ec.workers.dev/'; 
                
                const response = await fetch(WORKER_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    formStatus.textContent = '¡Mensaje enviado con éxito! Nos contactaremos pronto.';
                    formStatus.className = 'status-success';
                    contactForm.reset();
                } else {
                    throw new Error('Error en el servidor');
                }
            } catch (error) {
                console.error('Error enviando formulario:', error);
                formStatus.textContent = 'Hubo un error al enviar el mensaje. Por favor intenta por WhatsApp.';
                formStatus.className = 'status-error';
            } finally {
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
});