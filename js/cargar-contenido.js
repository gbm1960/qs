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

document.addEventListener('DOMContentLoaded', cargarContenido);