function load() {
    const loading = document.createElement("div");
    const mask = document.createElement("div");
    const animation = document.createElement("div");

    loading.setAttribute("id","loading");
    mask.setAttribute("id","mask");
    animation.setAttribute("id","animation");

    loading.appendChild(mask);
    loading.appendChild(animation);
    return loading;
}
function mask() {
    document.getElementById("loading").style.display = "flex";
};

function unmask() {
    document.getElementById("loading").style.display = "none";
}
init();
