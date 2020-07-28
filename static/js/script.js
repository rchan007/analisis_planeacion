btn_wip = document.getElementById('calculate_wip');
btn_wip.addEventListener('click', function(){
    calcular();
})

window.addEventListener('load', function(){
    calcular();
})

function calcular(){
    //obtenemos todas las filas del tbody
    var filas = document.querySelectorAll("#analisis_planeacion tbody tr")
    var input_calc_days = document.querySelector("#calc_days")
    //recorremos cada una de las filas
    filas.forEach(function(e){
        //obtenemos cada columna
        var days_to_analysi = input_calc_days.value
        var columns = e.querySelectorAll("td")
        var pieces_goal = parseInt(columns[4].textContent)
        var pieces_wip_sts_20 = parseInt(columns[5].textContent)
        var pieces_wip_sts_60 = parseInt(columns[6].textContent)
        var pieces_wip_total = pieces_wip_sts_20 + pieces_wip_sts_60
        var days_wip = parseInt(pieces_wip_total / pieces_goal)
        var missing_days = days_to_analysi - days_wip
        
        //mostramos los calculos de las filas
        columns[8].textContent = days_wip
        columns[9].textContent = missing_days
        columns[10].textContent = parseInt( ( pieces_goal / 5 ) * missing_days )
    });
}