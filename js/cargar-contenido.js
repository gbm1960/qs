// Función para cargar archivos de texto
async function cargarContenido() {
    try {
        // Cargar Quiénes Somos
        const quienesResponse = await fetch('data/quienes-somos.txt');
        const quienesTexto = await quienesResponse.text();
        
        // Reemplazar el contenido en el HTML
        const quienesParrafos = quienesTexto.split('\n\n'); // Separa por párrafos
        const quienesDiv = document.querySelector('.about-text');
        if (quienesDiv) {
            quienesDiv.innerHTML = ''; // Limpiar contenido existente
            quienesParrafos.forEach(parrafo => {
                if (parrafo.trim() !== '') {
                    const p = document.createElement('p');
                    p.textContent = parrafo.trim();
                    quienesDiv.appendChild(p);
                }
            });
        }

        // Cargar Servicios
        const serviciosResponse = await fetch('data/servicios.txt');
        const serviciosTexto = await serviciosResponse.text();
        const servicios = JSON.parse(serviciosTexto); // Convertir JSON a objeto
        
        // Reemplazar los servicios en el HTML
        const serviciosGrid = document.querySelector('.services-grid');
        if (serviciosGrid) {
            serviciosGrid.innerHTML = ''; // Limpiar servicios existentes
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
        console.error('Error cargando contenido:', error);
    }
}

// Ejecutar cuando la página esté lista
document.addEventListener('DOMContentLoaded', cargarContenido);