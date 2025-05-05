class CodeAnalyzer {
    constructor() {
        this.editor = document.getElementById("editor");
        this.lineNumbers = document.getElementById("line-numbers");
        this.resultado = document.getElementById("resultado");
        this.executeBtn = document.getElementById("execute-btn");
        this.apiUrl = 'http://localhost:5000/api/analyze';
        
        this.initEventListeners();
        this.updateLineNumbers();
    }
    
    initEventListeners() {
        this.editor.addEventListener("input", () => this.updateLineNumbers());
        this.editor.addEventListener("scroll", () => this.syncScroll());
        this.editor.addEventListener("click", () => this.highlightCurrentLine());
        this.editor.addEventListener("keyup", () => this.highlightCurrentLine());
        this.executeBtn.addEventListener("click", () => this.analyzeCode());
    }
    
    updateLineNumbers() {
        const lines = this.editor.value.split("\n");
        this.lineNumbers.innerHTML = "";
        
        const totalLines = lines.length === 0 ? 1 : lines.length;
        
        for (let i = 1; i <= totalLines; i++) {
            const lineDiv = document.createElement("div");
            lineDiv.textContent = i;
            this.lineNumbers.appendChild(lineDiv);
        }
        
        this.highlightCurrentLine();
    }
    
    syncScroll() {
        this.lineNumbers.scrollTop = this.editor.scrollTop;
    }
    
    highlightCurrentLine() {
        const cursorPosition = this.editor.selectionStart;
        const currentLine = this.editor.value.substring(0, cursorPosition).split("\n").length;
        
        document.querySelectorAll(".line-numbers div").forEach((line, index) => {
            line.classList.toggle("highlight", index === currentLine - 1);
        });
    }
    
    async analyzeCode() {
        const code = this.editor.value;
        this.showLoading();
        
        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ code })
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            const data = await response.json();
            this.showResults(data);
            
        } catch (err) {
            this.showError(err);
            console.error("Error completo:", err);
        }
    }
    
    showLoading() {
        this.resultado.innerHTML = "<div class='loading'>Procesando código...</div>";
    }
    
    showResults(data) {
        if (data.error) {
            this.resultado.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        let html = `
            <div class="result-section">
                <h3>Tokens reconocidos:</h3>
                <pre class="pre-formatted">${JSON.stringify(data.tokens, null, 2)}</pre>
            </div>
            <div class="result-section">
                <h3>Estructura generada:</h3>
                <pre class="pre-formatted">${data.output}</pre>
            </div>
        `;
        
        this.resultado.innerHTML = html;
    }
    
    showError(err) {
        this.resultado.innerHTML = `
            <div class="error">
                <p>Error de conexión: ${err.message}</p>
                <p>Asegúrate que:</p>
                <ol>
                    <li>El servidor Flask está corriendo</li>
                    <li>La URL del backend es correcta</li>
                    <li>No hay errores en la consola (F12)</li>
                </ol>
            </div>
        `;
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new CodeAnalyzer();
});