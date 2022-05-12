function burger_menu() {
    var param_container = document.getElementsByClassName("parameter-dashboard row")[0];
    var graph_container = document.getElementsByClassName("graph-dashboard row")[0];
    var burger_and_back = document.getElementsByClassName("burger-button-container-left")[0];

    param_container.classList.toggle("active");
    graph_container.classList.toggle("active");
    burger_and_back.classList.toggle("active");
}