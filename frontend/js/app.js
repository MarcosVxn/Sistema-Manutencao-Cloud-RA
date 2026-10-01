/*

fetch("./js/dados.json")
.then(response => response.json())
.then(dados => {
    console.log(dados[0].nome)
})
.catch( () => {
    console.error("Erro ao carregar o JSON:", error);
});

*/

document.getElementById("btnFuradeira").onclick = (e)=> {
    window.location.href = "./frontend/telas/furadeira.html"
};

document.getElementById("btnTorno").onclick = ()=> {
    window.location.href = "./frontend/telas/tornoCNC.html"
};