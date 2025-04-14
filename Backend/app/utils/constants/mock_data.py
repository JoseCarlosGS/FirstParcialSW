MOCK_DATA = {
    "html": """ 
        <div class="registro-container">
            <h2 class="registro-titulo">Registro de Usuarios</h2>

            <div class="form-container">
                <input type="text" placeholder="Nombre" [(ngModel)]="usuario.nombre" />
                <input type="text" placeholder="Apellido" [(ngModel)]="usuario.apellido" />
                <input type="email" placeholder="Correo Electrónico" [(ngModel)]="usuario.email" />
                <input type="password" placeholder="Contraseña" [(ngModel)]="usuario.contrasena" />
                <input type="number" placeholder="Edad" [(ngModel)]="usuario.edad" />

                <button class="btn-registrar" (click)="registrarUsuario()">
                <i class="fa fa-user-plus"></i> Registrar
                </button>
            </div>
        </div>
    """,
    "css": """
        .registro-container {
    text-align: center;
    padding: 20px;
    }

    .registro-titulo {
    color: #333333;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    }

    .form-container {
    background: #f9f9f9;
    border: 1px solid #ddd;
    padding: 20px;
    margin: 10px auto;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    }

    .form-container input {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #cccccc;
    border-radius: 5px;
    color: #333333;
    box-shadow: none;
    }

    .form-container input[type="number"] {
    width: 100px;
    align-self: center;
    }

    .btn-registrar {
    background-color: #28a745;
    color: #ffffff;
    border: none;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
    }

    .btn-registrar:hover {
    background-color: #218838;
    }

    .btn-registrar i {
    margin-right: 5px;
    }
    
    
    """,
    "typescript": """
    import { Component } from '@angular/core';

    @Component({
    selector: 'app-registro-usuario',
    templateUrl: './registro-usuario.component.html',
    styleUrls: ['./registro-usuario.component.css']
    })
    export class RegistroUsuarioComponent {
    usuario = {
        nombre: '',
        apellido: '',
        email: '',
        contrasena: '',
        edad: null
    };

    registrarUsuario() {
        console.log('Datos del usuario:', this.usuario);
        // Aquí puedes integrar con una API o servicio
        alert('Usuario registrado con éxito');
    }
    }

    """
        
}