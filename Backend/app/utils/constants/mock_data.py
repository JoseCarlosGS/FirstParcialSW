MOCK_DATA = [
    {
        "name":"register",
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
<router-outlet />
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
        "typescript": 
        """
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
        """     
    },
    {
        "name":"login",
        "html":
        """
<div class="login-container">
  <form (ngSubmit)="onLogin()" #loginForm="ngForm">
    <h2>Login</h2>
    <div class="form-group">
      <input
        type="text"
        name="username"
        [(ngModel)]="username"
        required
        placeholder="Username"
      />
    </div>
    <div class="form-group">
      <input
        type="password"
        name="password"
        [(ngModel)]="password"
        required
        placeholder="Password"
      />
    </div>
    <button type="submit" [disabled]="!loginForm.valid">Login</button>
  </form>
</div>
        """
        ,
        "css":"""
.login-container {
  width: 300px;
  margin: 100px auto;
  padding: 30px;
  background-color: #f7f7f7;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  border-radius: 8px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  border: none;
  color: white;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #a0c4ff;
  cursor: not-allowed;
}

        """
        ,
        "typescript":"""
  username: string = '';
  password: string = '';

  onLogin() {
    if (this.username && this.password) {
      alert('Login exitoso');
    }
  }
        """
    },
]