function change_total_fees() {
    total_fees = document.querySelector("#total-fees")
    var fees = document.getElementsByClassName("fees");
    sum = 0
    for (var i = 0; i < fees.length; i++) {
        sum += parseFloat(fees[i].value);
    }
    total_fees.value = sum
}
